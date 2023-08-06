from setuptools import setup

with open('./readme.md') as f:
    readme = f.read()

setup(
    name='leboncoin-api-wrapper',
    url="https://github.com/Shinyhero36/Leboncoin-API-Wrapper",
    version='0.2',
    license='MIT',
    install_requires=[
        'requests >= 2.25.0',
        'cloudscraper >= 1.2.48',
        'dataclasses'  # not included in Python <= 3.7
    ],
    author="Shinyhero36",
    setup_requires=['setuptools_scm'],  # Automatically include Ressources files
    include_package_data=True,
    packages=['leboncoin_api_wrapper'],
    long_description=readme,
    long_description_content_type='text/markdown'
)
