from setuptools import setup, find_packages

setup(
    name='nvalid',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.7',
    package_dir={'nvalid': 'nvalid'},
    install_requires=[
        'requests',
        'aiohttp',
        'configparser',
    ],
    description="Nginx configuration file check util",
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ]
)
