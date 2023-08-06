from setuptools import setup, find_packages
import sys

# Python 3.0 or later needed
if sys.version_info < (3, 0, 0, 'final', 0):
    raise SystemExit('Python 3.0 or later is required!')

setup(
    name= 'pydevmgr',
    version= '0.1.5', # https://www.python.org/dev/peps/pep-0440/
    author='Sylvain Guieu',
    author_email='sylvain.guieu@univ-grenoble-alpes.fr',
    packages=find_packages(exclude=['pydevmgrtest']), #['pydevmgr', 'pydevmgr_qt', 'pydevmgr.scripts', 'pydevmgr_qt.scripts'],
    #scripts=scripts,
    #data_files=data_files,
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    install_requires=['opcua', 'pyyaml', 'jinja2', 'argparse', 'cryptography'],
    dependency_links=[],
    long_description_content_type='text/markdown',
    
    include_package_data=True, 
    package_data={
        'pydevmgr':    ["resources/*.yml"], 
        'pydevmgr_qt': ["uis/*.ui"]
    }, 
    entry_points = {
        'console_scripts': [
                            'pydevmgr_dump=pydevmgr.scripts.dump:main', 
                            'pydevmgr_gui=pydevmgr_qt.scripts.manager_gui:main', 
                            ],
    }
)
