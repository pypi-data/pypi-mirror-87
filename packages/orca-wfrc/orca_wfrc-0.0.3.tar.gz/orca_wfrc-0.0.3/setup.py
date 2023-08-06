import setuptools
from setuptools.command.sdist import sdist


# these make sure the js distribution bundle is created and
# up-to-date when creating distribution packages.
cmdclass = {}

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name='orca_wfrc',
    version='0.0.3',
    description='A pipeline orchestration tool with Pandas support, modified by WFRC',
    long_description=long_description,
    author='WFRC_Analytics.',
    author_email='jreynolds@wfrc.org',
    url='https://github.com/WFRCAnalytics/orca_wfrc',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: BSD License'
    ],
    packages=setuptools.find_packages(exclude=['*.tests']),
    package_data={
        'orca': [
            'server/static/css/*',
            'server/static/js/dist/*',
            'server/templates/*']
    },
    # New versions of PyTables ("tables" on pypi) often fail to install correctly, so we
    # are being conservative here and disallowing them until tested
    install_requires=[
        'pandas >= 0.15.0',
        'tables >=3.1, <3.6; python_version <"3.6"',
        'tables >=3.1, <3.7; python_version >="3.6"',
        'toolz >= 0.8.1'
    ],
    extras_require={
        'server': ['flask >= 0.10', 'pygments >= 2.0', 'six >= 1.9.0']
    },
    entry_points={
        'console_scripts': [
            'orca-server = orca.server.server:main [server]'
        ]
    },
    cmdclass=cmdclass
)