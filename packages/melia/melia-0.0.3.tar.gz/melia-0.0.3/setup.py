import pathlib
from setuptools import setup, find_packages

HERE    = pathlib.Path(__file__).parent
README  = (HERE/'README.md').read_text()

setup(
    name='melia',
    version='0.0.3',
    description='Meta-linguistic abstractions',
    long_description=README,
    long_description_content_type='text/markdown',
    author='dindefi',
    author_email='dindefi@gmail.com',
    license='Apache 2.0',
    include_package_data=True,
    # Dict[Package Name, Dir Name]
    package_dir={'melia': 'src'},
    packages=find_packages(), # use the logical name ( after the pacakge_dir mapping)
)


#NOTE: when used as the installed  package, will the existing call 'import base.x' 
# in dev environment ( /src is in path, so base is within package), will this still work?