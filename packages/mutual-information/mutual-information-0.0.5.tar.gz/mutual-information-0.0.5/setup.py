#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'mutual-information',
        version = '0.0.5',
        description = '',
        long_description = 'mutual information-based synergy between variables for one response',
        long_description_content_type = None,
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        keywords = '',

        author = 'Xingmin Aaron Zhang',
        author_email = 'kingmanzhang@gmail.com',
        maintainer = '',
        maintainer_email = '',

        license = 'MIT',

        url = 'https://github.com/kingmanzhang/mutual-information',
        project_urls = {},

        scripts = [],
        packages = ['mutual_information'],
        namespace_packages = [],
        py_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [
            'networkx',
            'numpy',
            'pandas',
            'treelib'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
