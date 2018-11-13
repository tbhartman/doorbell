from setuptools import find_packages
from setuptools import setup

import versioneer

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

setup(
    name="doorbell",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Tim Hartman",
    author_email="tbhartman@gmail.com",
    description=("A visitor pattern implementation for Python"),
    license="MIT",
    keywords="visitor",
    url="https://github.com/tbhartman/doorbell",
    packages=find_packages('src', exclude=['test*']),
    package_dir={'': 'src'},
    install_requires=[],
    tests_require=test_deps,
    extras_require=extras,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
