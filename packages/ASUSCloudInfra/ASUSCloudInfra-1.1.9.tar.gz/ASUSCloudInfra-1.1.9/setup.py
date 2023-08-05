# coding:utf-8

from setuptools import setup

version_file = open("ASUSCloudInfra/VERSION", "r")
VERSION = version_file.readline()
version_file.close()

setup(
    name='ASUSCloudInfra',
    version=VERSION,
    description='the library for ASUS Cloud Infra',
    author='scott_su',
    author_email='scott_su@asus.com',
    packages=['ASUSCloudInfra','ASUSCloudInfra.Base','ASUSCloudInfra.Docker','ASUSCloudInfra.SFTP','ASUSCloudInfra.AIMaker','ASUSCloudInfra.AIMakerMonitor'],
    package_data={'ASUSCloudInfra': ['VERSION']},
    install_requires=[
        'requests',
        'pyjwt',
        'paramiko'
    ],
    license='MIT',
    zip_safe=False
)
