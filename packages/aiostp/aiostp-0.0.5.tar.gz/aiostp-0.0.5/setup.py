from importlib.machinery import SourceFileLoader

from setuptools import find_packages, setup

version = SourceFileLoader('version', 'aiostp/version.py').load_module()

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='aiostp',
    version=version.__version__,
    author='Cuenca',
    author_email='dev@cuenca.com',
    description='asyncio client library for stpmex.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cuenca-mx/aiostp',
    packages=find_packages(),
    include_package_data=True,
    package_data=dict(stpmex=['py.typed']),
    python_requires='>=3.7',
    install_requires=[
        'aiohttp>=3.7.3,<3.8.0',
        'cryptography>=3.0,<4.1',
        'cuenca-validations>=0.5.0,<0.7.0',
        'aiofile>=3.3.0,<3.4.0',
        'pydantic>=1.7.0,<1.8.0',
        'pandas>=1.1.0,<1.2.0',
        'stpmex>=3.6.0,<3.7.0',
    ],
    setup_requires=['pytest-runner'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
