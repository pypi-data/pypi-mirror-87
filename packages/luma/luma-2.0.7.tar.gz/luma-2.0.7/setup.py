from setuptools.command.install import install
from setuptools import setup, find_packages
from os.path import abspath, dirname, join
import sys, os, stat, json, getpass
from pathlib import Path
import platform
import mmap

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
This version of Lumavate CLI requires Python {}.{}, but you're trying to
install it on Python {}.{}.
This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
are installing with pip3, then try again:
    $ pip3 install .
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)

home = str(Path.home())

luma_dir = f'{home}/.luma/'
cli_path = f'{home}/.luma/luma_cli_config.json'
old_config_path = f'{home}/.luma_cli_config'

if not os.path.exists(luma_dir):
  os.mkdir(f'{Path.home()}/.luma/', mode=0o700)

if os.path.exists(cli_path):
  print("Already updated to new .luma config", flush=True)
elif os.path.exists(old_config_path):
  with open(old_config_path, 'r') as f:
    old_config = json.load(f)
  with open(cli_path, 'w+') as config:
    json.dump(old_config, config)
else:
  with open(cli_path, 'w+') as config:
    json.dump({ "envs": {}, "profiles": {} }, config)

os.chmod(cli_path, 0o777)
os.chmod(f'{home}/.luma/', 0o777)

# Read the version number from version.py
with open(abspath(join(dirname(__file__), 'cli', 'version.py'))) as versionFile:
  __version__ = versionFile.read().strip().replace('__version__ = ', '').replace("'", '')

with open('README.md') as f:
  long_description = f.read()

packages = find_packages()

if platform.system() == 'Windows':
  icon_path = "images"
else:
  icon_path = "/images"

setup(
    name="luma",
    version=__version__,
    description='A CLI to interact with the Lumavate platform',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Gunnar Norred',
    author_email='g.norred@lumavate.com',
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    packages=packages,
    data_files=[(icon_path, ['images/default-icon.svg'])],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    install_requires=[
        'click>=7.0',
        'pycparser==2.18',
        'pyparsing==2.2.0',
        'python-dateutil>=2.8',
        'requests>=2.22.0',
        'docker>=4.0.1',
        'PyQRCode==1.2.1'
    ],
    entry_points='''
        [console_scripts]
        luma=cli:cli
    '''
)

zshrc = str(Path.home()) + '/.zshrc'
bashrc = str(Path.home()) + '/.bash_profile'

tab_comp = False

if os.path.exists(zshrc):
    with open(zshrc, 'rb', 0) as zsh_config, mmap.mmap(zsh_config.fileno(), 0, access=mmap.ACCESS_READ) as s:
        if s.find(b'_LUMA_COMPLETE=source_zsh luma') != -1:
            tab_comp = True
            print("Completion already activated for ZSH")

    if tab_comp is False:
        with open(zshrc, 'a') as zsh:
            zsh.write('eval "$(_LUMA_COMPLETE=source_zsh luma)"')

if os.path.exists(bashrc):
    with open(bashrc, 'rb', 0) as bash_config, mmap.mmap(bash_config.fileno(), 0, access=mmap.ACCESS_READ) as s:
        if s.find(b'_LUMA_COMPLETE=source luma') != -1:
            tab_comp = True
            print("Completion already activated for Bash")

    if tab_comp is False:
        with open(bashrc, 'a+') as bash:
            bash.write('eval "$(_LUMA_COMPLETE=source luma)"')
else:
    with open(bashrc, 'a+') as bash:
        bash.write('eval "$(_LUMA_COMPLETE=source luma)"')
