import os
from setuptools import find_packages, setup

os.chdir(os.path.dirname(os.path.abspath(__file__)))

NAME = 'lightning-crm'
VERSION = '0.1.0'

def get_install_require_packages():
    """获取依赖的安装包"""
    with open('requirements.in', 'r') as file:
        return [line
            for line in file.readlines() if not line.startswith('http')]

# with open('README.md', 'r') as file:
#     long_description = file.read()


def get_packages(app):
    """获取包"""
    return [app] + [
        "{}.{}".format(app, item) for item in find_packages(app)
    ]

all_packages = []
[all_packages.extend(item) for item in map(get_packages, [
    'lightning_crm'
])]

import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

setup(
    name=NAME,
    version=VERSION,
    url='https://github.com/git-men/lightning-crm',
    author='gitmen.com',
    author_email='jeff@gitmen.com',
    description='CRM for lightning',
    long_description='CRM for lightning',
    license='MIT',
    packages=all_packages,
    include_package_data=True,
    data_files={},
    install_requires=get_install_require_packages(),
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
