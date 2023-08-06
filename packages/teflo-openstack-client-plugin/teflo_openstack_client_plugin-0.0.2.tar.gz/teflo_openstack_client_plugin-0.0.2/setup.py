import os
import re
from setuptools import setup, find_packages


ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([a-zA-Z0-9.]+)['"]''')


def get_version():
    init = open(os.path.join(ROOT, 'teflo_openstack_client_plugin', '__init__.py')).read()
    return VERSION_RE.search(init).group(1)

setup(
    name='teflo_openstack_client_plugin',
    version=get_version(),
    description="openstack client provisioner plugin for Teflo",
    long_description="""# teflo_openstack_client_plugin\n\n* A provisioner plugin for Teflo to provision resources using openstack client\n""",
    long_description_content_type='text/markdown',
    author="Red Hat Inc",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'ospclientsdk'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
    entry_points={
        'provisioner_plugins': 'openstack_client_plugin = teflo_openstack_client_plugin:OpenstackClientProvisionerPlugin',
    }
)
