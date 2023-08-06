#! /usr/bin/env python

from setuptools import setup, find_packages
from setuptools.command.install import install

with open("README.rst", "r") as readme:
    long_desc = readme.read()

setup(
    name='mqtttasky_groupme',
    version='0.1.4',
    license='MIT',
    author='Ryan Haas',
    author_email='haasrr@etsu.edu',
    description='GroupMe bot to schedule tasks, display and speak notifications, and publish them over MQTT.',
    long_description=long_desc,
    long_description_content_type='text/x-rst',
    url='https://github.com/haasr/mqtttttttasky_groupme',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only'
    ],
    entry_points={
        'console_scripts': [
            'mqtttasky_groupme=mqtttasky_groupme.app:main',
            'mqtttasky_groupme_config=mqtttasky_groupme.reconfig_util:main'
        ],
    },
    package_data={
        'mqtttasky_groupme': ['config/groupme_bot_config.py',
                                'config/mqtt_config.py', 'images/clock-32x32.png']
    },
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.7',
    install_requires=[
        'certifi==2020.11.8',
        'cffi==1.14.4',
        'chardet==3.0.4',
        'cryptography==3.2.1',
        'idna==2.10',
        'paho-mqtt==1.5.1',
        'Pillow==7.2.0',
        'pkg-resources==0.0.0',
        'pycparser==2.20',
        'requests==2.25.0',
        'RPi.GPIO==0.7.0',
        'six==1.15.0',
        'urllib3==1.26.2'
    ]
)