import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(__file__, os.pardir, 'src')))

import doorbell  # noqa

info = {
    'author': 'Timothy B. Hartman',
    'author_email': 'tbhartman@gmail.com',
    'classifiers': [
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    'copyright': '2018, Timothy B. Hartman',
    'description': 'A visitor pattern implementation for Python',
    'keywords': 'visitor-pattern, python',
    'license': 'MIT',
    'long_description_content_type': 'text/x-rst',
    'name': 'doorbell',
    'url': 'https://github.com/tbhartman/doorbell',
    'version': doorbell.__version__,
    }
with open(os.path.join(os.path.split(__file__)[0], 'README.rst'), 'r') as fh:
    info['long_description'] = fh.read()


test_deps = [
    'coverage',
    'flake8',
    'pytest',
    'pytest-cov',
    'sphinx_rtd_theme',
    'tox',
    'versioneer',
    ],
extras = {
    'test': test_deps,
}

if __name__ == '__main__':
    from setuptools import find_packages
    from setuptools import setup
    import versioneer
    args = {
        'cmdclass': versioneer.get_cmdclass(),
        'extras_require': extras,
        'install_requires': [],
        'package_dir': {'': 'src'},
        'packages': find_packages('src', exclude=['test*']),
        'tests_require': test_deps,
        }
    args.update(info)
    setup(**args)
