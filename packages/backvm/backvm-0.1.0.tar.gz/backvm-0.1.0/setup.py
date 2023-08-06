
# Author: Pietro Marini <backvm@fastmail.com>
# License: BSD 3 clause

from setuptools import setup, find_packages

README = open("./Readme.md","r").read()

setup(
    name='backvm',

    version='0.1.0',
    
    description="This program performs the backup of one or several KVM domains",
    
    long_description=README,
    
    long_description_content_type="text/markdown",
    
    packages=find_packages(),
    
    include_package_data=True,
    
    license="new BSD",
    
    author="Pietro Marini",
    
    author_email="backvm@fastmail.com",
    
    install_requires=[
        'click',
        'libvirt-python',
        'pandas',
        'paramiko',
        'scp'
        
    ],
    
    entry_points='''
        [console_scripts]
        backvm=backvm.scripts.backvm:perform_action
    ''',
)
