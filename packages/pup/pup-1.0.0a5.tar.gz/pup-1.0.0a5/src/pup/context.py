"""
Packaging Context.
"""

from urllib import parse


class Context:

    def __init__(self, *, src, launch_module, ignore_plugins, platform, python_version):

        self.src = src
        self.launch_module = launch_module

        self.src_metadata = None

        self.ignore_plugins = ignore_plugins
        self.pkg_platform = platform
        self.tgt_platform = platform
        self.tgt_python_version = python_version[:3]
        self.tgt_python_version_suffix = '.'.join(map(str, python_version[:2]))

        self.relocatable_root = None

        self.python_runtime_dir = None
        self.python_rel_exe = None
        self.python_rel_scripts = None
        self.python_rel_stdlib = None
        self.python_rel_site_packages = None

        self.python_test_packages = None
        self.stdlib_platform_config = None


    @property
    def application_id(self):

        """
        Returns the application identifier built from the package's home_page
        URL, consisting of two-sets of '.'-separated strings: the reverse DNS
        host/domain part, followed by the in-order path components.

        Example:
        - home_page='https://example.com/a/path'
        - bundle_id='com.example.a.path'
        """

        url_parts = parse.urlsplit(self.src_metadata.home_page)
        return '.'.join((
            '.'.join(reversed(url_parts.netloc.split('.'))),
            '.'.join(filter(None, url_parts.path.split('/')))
        ))
