from setuptools import setup

setup(
    name= 'pydevmgr',
    version= '0.1.4', # https://www.python.org/dev/peps/pep-0440/
    author='Sylvain Guieu',
    author_email='sylvain.guieu@univ-grenoble-alpes.fr',
    packages=['pydevmgr', 'pydevmgr_qt'],
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
        'console_scripts': ['pydevmgr_hello=pydevmgr.scripts.hello:main', 
                            'pydevmgr_dump=pydevmgr.scripts.dump:main', 
                            'pydevmgr_gui=pydevmgr_qt.scripts.manager_gui:main', 
                            ],
    }
)
