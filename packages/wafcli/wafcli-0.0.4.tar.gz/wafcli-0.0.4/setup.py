#!/usr/bin/env python
import codecs
import os.path
import re
import sys

from setuptools import setup, find_packages
here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r', encoding='gbk', errors='ignore').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


install_requires = [
    'tencentcloud-sdk-python',
    'fire',
]


setup_options = dict(
    name='wafcli',
    version=find_version("wafcli", "__init__.py"),
    description='腾讯T-Sec Web应用防火墙命令行工具',
    long_description="https://github.com/huangjacky/waf-cli",
    long_description_content_type="text/markdown",
    author='HuangJacky',
    maintainer_email="HuangJacky@163.com",
    url='https://cloud.tencent.com/product/waf',
    scripts=['bin/waf', 'bin/waf.cmd'],
    packages=find_packages(exclude=['tests*']),
    package_data={'wafcli': ['data/*.json', 'examples/*/*.rst',
                             'examples/*/*.txt', 'examples/*/*/*.txt',
                             'examples/*/*/*.rst', 'topics/*.rst',
                             'topics/*.json']},
    install_requires=install_requires,
    extras_require={},
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)


if 'py2exe' in sys.argv:
    setup_options['options'] = {
        'py2exe': {
            'optimize': 0,
            'skip_archive': True,
            'dll_excludes': ['crypt32.dll'],
            'packages': ['docutils', 'urllib', 'httplib', 'HTMLParser',
                         'wafcli', 'ConfigParser', 'xml.etree', 'pipes'],
        }
    }
    setup_options['console'] = ['bin/waf']


setup(**setup_options)
