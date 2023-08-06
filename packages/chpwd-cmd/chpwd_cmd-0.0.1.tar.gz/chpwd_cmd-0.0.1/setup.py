from setuptools import setup, find_packages

with open('requirements.txt') as requirements_file:
    install_requirements = requirements_file.read().splitlines()

with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='chpwd_cmd',
    version='0.0.1',
    description='Execute the commands in the configuration file according to the current working directory.',
    author_email='teddy@sfc.wide.ad.jp',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='KIMOTO Mizuki',
    url='https://github.com/teddyyy/chpwd_cmd',
    license='MIT',
    packages=find_packages(),
    install_requires=install_requirements,
    entry_points={
        'console_scripts': [
            'chpwd_cmd=chpwd_cmd.chpwd_cmd:main',
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]
)
