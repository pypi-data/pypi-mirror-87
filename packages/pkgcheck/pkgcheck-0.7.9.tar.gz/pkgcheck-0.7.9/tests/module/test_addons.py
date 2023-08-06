import os
from unittest.mock import patch

import pytest
from pkgcheck import addons
from pkgcore.ebuild import repo_objs, repository
from pkgcore.restrictions import packages
from pkgcore.util import commandline
from snakeoil.cli import arghparse
from snakeoil.cli.exceptions import UserException
from snakeoil.fileutils import write_file
from snakeoil.osutils import ensure_dirs, pjoin

from .misc import FakePkg, FakeProfile, Tmpdir


class ArgparseCheck:

    def process_check(self, args, preset_values={},
                      namespace=None, addon_kls=None, **settings):
        addon_kls = addon_kls if addon_kls is not None else self.addon_kls
        p = commandline.ArgumentParser(domain=False, color=False)
        p.plugin = p.add_argument_group('plugin options')
        addon_kls.mangle_argparser(p)
        args, unknown_args = p.parse_known_args(args, namespace)
        assert unknown_args == []
        for attr, val in preset_values.items():
            setattr(args, attr, val)
        addon_kls.check_args(p, args)
        for attr, val in settings.items():
            assert getattr(args, attr) == val, (
                f"for args {args!r}, {attr} must be {val!r}, got {getattr(args, attr)!r}")
        return args


class TestArchesAddon:

    @pytest.fixture(autouse=True)
    def _setup(self, tool, repo):
        self.tool = tool
        self.repo = repo
        self.args = ['scan', '--repo', repo.location]

    def test_empty_default(self):
        options, _ = self.tool.parse_args(self.args)
        assert options.arches == ()

    def test_repo_default(self):
        with open(pjoin(self.repo.location, 'profiles', 'arch.list'), 'w') as f:
            f.write("arm64\namd64\n")
        options, _ = self.tool.parse_args(self.args)
        assert options.arches == ('amd64', 'arm64')

    def test_enabled(self):
        data = (
            ('x86', ('x86',)),
            ('ppc', ('ppc',)),
            ('x86,ppc', ('ppc', 'x86')),
        )
        for arg, expected in data:
            for opt in ('-a', '--arches'):
                options, _ = self.tool.parse_args(self.args + [f'{opt}={arg}'])
                assert options.arches == expected

    def test_disabled(self):
        # set repo defaults
        with open(pjoin(self.repo.location, 'profiles', 'arch.list'), 'w') as f:
            f.write("arm64\namd64\narm64-linux\n")

        data = (
            ('-x86', ('amd64', 'arm64',)),
            ('-x86,-amd64', ('arm64',)),
        )
        for arg, expected in data:
            for opt in ('-a', '--arches'):
                options, _ = self.tool.parse_args(self.args + [f'{opt}={arg}'])
                assert options.arches == expected

    def test_unknown(self, capsys):
        # unknown arch checking requires repo defaults
        with open(pjoin(self.repo.location, 'profiles', 'arch.list'), 'w') as f:
            f.write("arm64\namd64\narm64-linux\n")

        for arg in ('foo', 'bar'):
            for opt in ('-a', '--arches'):
                with pytest.raises(SystemExit) as excinfo:
                    self.tool.parse_args(self.args + [f'{opt}={arg}'])
                assert excinfo.value.code == 2
                out, err = capsys.readouterr()
                assert not out
                assert f'unknown arch: {arg}' in err


class TestStableArchesAddon:

    @pytest.fixture(autouse=True)
    def _setup(self, tool, repo):
        self.tool = tool
        self.repo = repo
        self.args = ['scan', '--repo', repo.location]

    def test_empty_default(self):
        options, _ = self.tool.parse_args(self.args)
        assert options.stable_arches == set()

    def test_repo_arches_default(self):
        """Use GLEP 72 arches.desc file if it exists."""
        with open(pjoin(self.repo.location, 'profiles', 'arch.list'), 'w') as f:
            f.write("arm64\namd64\nriscv\n")
        with open(pjoin(self.repo.location, 'profiles', 'arches.desc'), 'w') as f:
            f.write("arm64 stable\namd64 stable\nriscv testing")
        options, _ = self.tool.parse_args(self.args)
        assert options.stable_arches == {'amd64', 'arm64'}

    def test_repo_profiles_default(self):
        """Otherwise arch stability is determined from the profiles.desc file."""
        with open(pjoin(self.repo.location, 'profiles', 'arch.list'), 'w') as f:
            f.write("arm64\namd64\nriscv\n")
        os.mkdir(pjoin(self.repo.location, 'profiles', 'default'))
        with open(pjoin(self.repo.location, 'profiles', 'profiles.desc'), 'w') as f:
            f.write("arm64 default dev\namd64 default stable\nriscv default exp")
        options, _ = self.tool.parse_args(self.args)
        assert options.stable_arches == {'amd64'}

    def test_selected_arches(self):
        for opt in ('-a', '--arches'):
            options, _ = self.tool.parse_args(self.args + [f'{opt}=amd64'])
            assert options.stable_arches == {'amd64'}


class Test_profile_data:

    def assertResults(self, profile, known_flags, required_immutable,
                      required_forced, cpv="dev-util/diffball-0.1",
                      key_override=None, data_override=None):
        profile_data = addons.ProfileData(
            "test-profile", key_override,
            profile.provides_repo,
            packages.AlwaysFalse, profile.iuse_effective,
            profile.use, profile.pkg_use, profile.masked_use, profile.forced_use, {}, set(),
            'stable', False)
        pkg = FakePkg(cpv, data=data_override)
        immutable, enabled = profile_data.identify_use(pkg, set(known_flags))
        assert immutable == set(required_immutable)
        assert enabled == set(required_forced)

    def test_identify_use(self):
        profile = FakeProfile()
        self.assertResults(profile, [], [], [])

        profile = FakeProfile(masked_use={"dev-util/diffball": ["lib"]})
        self.assertResults(profile, [], [], [])
        self.assertResults(profile, ["lib"], ["lib"], [])

        profile = FakeProfile(masked_use={"=dev-util/diffball-0.2": ["lib"]})
        self.assertResults(profile, ["lib"], [], [])

        profile = FakeProfile(masked_use={"dev-util/foon": ["lib"]})
        self.assertResults(profile, ["lib"], [], [])

        profile = FakeProfile(forced_use={"dev-util/diffball": ["lib"]})
        self.assertResults(profile, [], [], [])
        self.assertResults(profile, ["lib", "bar"], ["lib"], ["lib"])

        profile = FakeProfile(
            forced_use={"dev-util/diffball": ["lib"]},
            masked_use={"dev-util/diffball": ["lib"]})
        self.assertResults(profile, [], [], [])
        # check that masked use wins out over forced.
        self.assertResults(profile, ["lib", "bar"], ["lib"], [])

        profile = FakeProfile(
            forced_use={"dev-util/diffball": ["lib"]},
            masked_use={"dev-util/diffball": ["lib"]})
        self.assertResults(profile, [], [], [])
        # check that masked use wins out over forced.
        self.assertResults(profile, ["lib", "bar"], ["lib"], [])


class ProfilesMixin(ArgparseCheck, Tmpdir):

    addon_kls = addons.ProfileAddon

    def mk_profiles(self, profiles, arches=None, make_defaults=None):
        os.mkdir(pjoin(self.dir, 'metadata'))
        # write empty masters to suppress warnings
        write_file(pjoin(self.dir, 'metadata', 'layout.conf'), 'w', 'masters=')

        loc = pjoin(self.dir, 'profiles')
        os.mkdir(loc)
        for profile in profiles:
            assert ensure_dirs(pjoin(loc, profile)), f"failed creating profile {profile!r}"
        if arches is None:
            arches = {val[0] for val in profiles.values()}
        write_file(pjoin(loc, 'arch.list'), 'w', "\n".join(arches))
        write_file(pjoin(loc, 'repo_name'), 'w', 'testing')
        write_file(pjoin(loc, 'eapi'), 'w', '5')
        with open(pjoin(loc, 'profiles.desc'), 'w') as fd:
            for profile, vals in profiles.items():
                l = len(vals)
                if l == 1 or not vals[1]:
                    fd.write(f"{vals[0]}\t{profile}\tstable\n")
                else:
                    fd.write(f"{vals[0]}\t{profile}\t{vals[1]}\n")
                if l == 3 and vals[2]:
                    with open(pjoin(loc, profile, 'deprecated'), 'w') as f:
                        f.write("foon\n#dar\n")
                with open(pjoin(loc, profile, 'make.defaults'), 'w') as f:
                    if make_defaults is not None:
                        f.write('\n'.join(make_defaults))
                    else:
                        f.write(f'ARCH={vals[0]}\n')
                with open(pjoin(loc, profile, 'eapi'), 'w') as f:
                    f.write('5')

    def process_check(self, *args, **kwds):
        namespace = arghparse.Namespace()
        repo_config = repo_objs.RepoConfig(location=self.dir)
        namespace.target_repo = repository.UnconfiguredTree(
            repo_config.location, repo_config=repo_config)
        namespace.search_repo = arghparse.Namespace()
        namespace.cache = {'profiles': False}
        options = ArgparseCheck.process_check(self, namespace=namespace, *args, **kwds)
        return options


class TestProfileAddon(ProfilesMixin):

    def assertProfiles(self, check, key, *profile_names):
        assert (
            sorted(x.name for y in check.profile_evaluate_dict[key] for x in y) ==
            sorted(profile_names))

    def test_defaults(self):
        self.mk_profiles({
            "profile1": ["x86"],
            "profile1/2": ["x86"],
        })
        options = self.process_check([], selected_profiles=None)
        # override the default
        addon = addons.init_addon(self.addon_kls, options)
        assert sorted(addon.profile_evaluate_dict) == ['x86', '~x86']
        self.assertProfiles(addon, 'x86', 'profile1', 'profile1/2')

    def test_profiles_base(self):
        self.mk_profiles({
            "default-linux/dep": ["x86", False, True],
            "default-linux": ["x86", "dev"],
            "default-linux/x86": ["x86"],
        })
        options = self.process_check([])
        addon = addons.init_addon(self.addon_kls, options)
        self.assertProfiles(addon, 'x86', 'default-linux', 'default-linux/x86')

    def test_nonexistent(self, capsys):
        self.mk_profiles({"x86": ["x86"]})
        for profiles in ('bar', '-bar', 'x86,bar', 'bar,x86', 'x86,-bar'):
            with pytest.raises(SystemExit) as excinfo:
                self.process_check([f'--profiles={profiles}'])
            assert excinfo.value.code == 2
            out, err = capsys.readouterr()
            assert not out
            assert "nonexistent profile: 'bar'" in err

    def test_make_defaults(self):
        self.mk_profiles({
            "amd64": ["amd64"],
            "prefix/amd64": ["amd64-linux"]},
            make_defaults=['ARCH="amd64"'])
        options = self.process_check(['--profiles=prefix/amd64'])
        addon = addons.init_addon(self.addon_kls, options)
        self.assertProfiles(addon, 'amd64', 'prefix/amd64')

    def test_make_defaults_missing_arch(self, capsys):
        self.mk_profiles({
            "arch/amd64": ["amd64"]},
            make_defaults=[])
        with pytest.raises(SystemExit) as excinfo:
            self.process_check(['--profiles=arch/amd64'])
        assert excinfo.value.code == 2
        out, err = capsys.readouterr()
        assert not out
        assert "profile make.defaults lacks ARCH setting: 'arch/amd64'" in err

    def test_enable_stable(self):
        self.mk_profiles({
            "default-linux/dep": ["x86", False, True],
            "default-linux/dev": ["x86", "dev"],
            "default-linux/exp": ["x86", "exp"],
            "default-linux": ["x86"],
        })
        options = self.process_check(['--profiles=stable'])
        addon = addons.init_addon(self.addon_kls, options)
        self.assertProfiles(addon, 'x86', 'default-linux')

    def test_disable_stable(self):
        self.mk_profiles({
            "default-linux/dep": ["x86", False, True],
            "default-linux/dev": ["x86", "dev"],
            "default-linux/exp": ["x86", "exp"],
            "default-linux": ["x86"],
        })
        options = self.process_check(['--profiles=-stable'])
        addon = addons.init_addon(self.addon_kls, options)
        self.assertProfiles(addon, 'x86', 'default-linux/dev', 'default-linux/exp')

    def test_enable_dev(self):
        self.mk_profiles({
            "default-linux/dep": ["x86", False, True],
            "default-linux/dev": ["x86", "dev"],
            "default-linux/x86": ["x86"],
        })
        options = self.process_check(['--profiles=dev'])
        addon = addons.init_addon(self.addon_kls, options)
        self.assertProfiles(addon, 'x86', 'default-linux/dev')

    def test_disable_dev(self):
        self.mk_profiles({
            "default-linux/dep": ["x86", False, True],
            "default-linux/dev": ["x86", "dev"],
            "default-linux/x86": ["x86"],
        })
        options = self.process_check(['--profiles=-dev'])
        addon = addons.init_addon(self.addon_kls, options)
        self.assertProfiles(addon, 'x86', 'default-linux/x86')

    def test_enable_exp(self):
        self.mk_profiles({
            "default-linux/dep": ["x86", False, True],
            "default-linux/exp": ["x86", "exp"],
            "default-linux/x86": ["x86"],
        })
        options = self.process_check(['--profiles=exp'])
        addon = addons.init_addon(self.addon_kls, options)
        self.assertProfiles(addon, 'x86', 'default-linux/exp')

    def test_disable_exp(self):
        self.mk_profiles({
            "default-linux/dep": ["x86", False, True],
            "default-linux/exp": ["x86", "exp"],
            "default-linux/x86": ["x86"],
        })
        options = self.process_check(['--profiles=-exp'])
        addon = addons.init_addon(self.addon_kls, options)
        self.assertProfiles(addon, 'x86', 'default-linux/x86')

    def test_enable_deprecated(self):
        self.mk_profiles({
            "default-linux/dep": ["x86", False, True],
            "default-linux/x86": ["x86"],
        })
        options = self.process_check(['--profiles=deprecated'])
        addon = addons.init_addon(self.addon_kls, options)
        self.assertProfiles(addon, 'x86', 'default-linux/dep')

    def test_disable_deprecated(self):
        self.mk_profiles({
            "default-linux/dep": ["x86", False, True],
            "default-linux/x86": ["x86"],
        })
        options = self.process_check(['--profiles=-deprecated'])
        addon = addons.init_addon(self.addon_kls, options)
        self.assertProfiles(addon, 'x86', 'default-linux/x86')

    def test_profile_enable(self):
        self.mk_profiles({
            "default-linux/dep": ["x86", False, True],
            "default-linux": ["x86"],
            "default-linux/x86": ["x86"],
        })
        options = self.process_check(['--profiles', 'default-linux/x86'])
        addon = addons.init_addon(self.addon_kls, options)
        self.assertProfiles(addon, 'x86', 'default-linux/x86')

    def test_profile_disable(self):
        self.mk_profiles({
            "default-linux/dep": ["x86", False, True],
            "default-linux": ["x86"],
            "default-linux/x86": ["x86"],
        })
        options = self.process_check(['--profiles=-default-linux/x86'])
        addon = addons.init_addon(self.addon_kls, options)
        self.assertProfiles(addon, 'x86', 'default-linux')

    def test_profile_collapsing(self):
        self.mk_profiles({
            'default-linux': ['x86'],
            'default-linux/x86': ["x86"],
            'default-linux/ppc': ['ppc'],
        })
        options = self.process_check([])
        addon = addons.init_addon(self.addon_kls, options)

        # assert they're collapsed properly.
        self.assertProfiles(addon, 'x86', 'default-linux', 'default-linux/x86')
        assert len(addon.profile_evaluate_dict['x86']) == 1
        assert len(addon.profile_evaluate_dict['x86'][0]) == 2
        self.assertProfiles(addon, 'ppc', 'default-linux/ppc')

        l = addon.identify_profiles(FakePkg("d-b/ab-1", data={'KEYWORDS': 'x86'}))
        assert len(l) == 2, f"checking for profile collapsing: {l!r}"
        assert len(l[0]) == 2, f"checking for proper # of profiles: {l[0]!r}"
        assert sorted(x.name for x in l[0]) == sorted(['default-linux', 'default-linux/x86'])

        # check arch vs ~arch runs (i.e. arch KEYWORDS should also trigger ~arch runs)
        l = addon.identify_profiles(FakePkg("d-b/ab-1", data={'KEYWORDS': '~x86'}))
        assert len(l) == 1, f"checking for profile collapsing: {l!r}"
        assert len(l[0]) == 2, f"checking for proper # of profiles: {l[0]!r}"
        assert sorted(x.name for x in l[0]) == sorted(['default-linux', 'default-linux/x86'])

        # check keyword collapsing
        l = addon.identify_profiles(FakePkg("d-b/ab-2", data={'KEYWORDS': 'ppc'}))
        assert len(l) == 2, f"checking for profile collapsing: {l!r}"
        assert len(l[0]) == 1, f"checking for proper # of profiles: {l[0]!r}"
        assert l[0][0].name == 'default-linux/ppc'

        l = addon.identify_profiles(FakePkg("d-b/ab-2", data={'KEYWORDS': 'foon'}))
        assert len(l) == 0, f"checking for profile collapsing: {l!r}"


class TestUseAddon(ArgparseCheck, Tmpdir):

    addon_kls = addons.UseAddon

    def test_it(self):
        pass
    test_it.skip = "todo"


try:
    import requests
    net_skip = False
except ImportError:
    net_skip = True


@pytest.mark.skipif(net_skip, reason="requests isn't installed")
class TestNetAddon:

    def test_failed_import(self, tool):
        options, _ = tool.parse_args(['scan'])
        addon = addons.NetAddon(options)
        with patch('pkgcheck.net.Session') as net:
            net.side_effect = ImportError('import failed', name='foo')
            with pytest.raises(ImportError):
                addon.session
            # failing to import requests specifically returns a nicer user exception
            net.side_effect = ImportError('import failed', name='requests')
            with pytest.raises(UserException, match='network checks require requests'):
                addon.session

    def test_custom_timeout(self, tool):
        options, _ = tool.parse_args(['scan', '--timeout', '10'])
        addon = addons.NetAddon(options)
        assert isinstance(addon.session, requests.Session)
        assert addon.session.timeout == 10
        # a timeout of zero disables timeouts entirely
        options, _ = tool.parse_args(['scan', '--timeout', '0'])
        addon = addons.NetAddon(options)
        assert addon.session.timeout is None

    def test_args(self, tool):
        options, _ = tool.parse_args(
            ['scan', '--timeout', '10', '--tasks', '50', '--user-agent', 'firefox'])
        addon = addons.NetAddon(options)
        with patch('pkgcheck.net.Session') as net:
            addon.session
        net.assert_called_once_with(concurrent=50, timeout=10, user_agent='firefox')
