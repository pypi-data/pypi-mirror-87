import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='fhnw_ds_weatherstation_client',
    version='0.0.13',
    author='Jelle Schutter',
    author_email='jelle@schutter.xyz',
    description='Provides access to the Wasserschutzpolizei Zurich live and historic weather data.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jelleschutter/fhnw-ds-weatherstation-client',
    packages=setuptools.find_packages(),
    install_requires=[
        'pandas>=1',
        'influxdb',
        'requests',
        'numpy',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
