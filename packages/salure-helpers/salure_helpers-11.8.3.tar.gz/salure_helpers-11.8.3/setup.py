from setuptools import setup

setup(
    name='salure_helpers',
    version='11.8.3',
    description='Files with helpful code, developed by Salure',
    url='https://bitbucket.org/salurebi/salure_helpers/',
    author='Salure',
    author_email='bi@salure.nl',
    license='Salure License',
    packages=['salure_helpers'],
    package_data={'salure_helpers': ['templates/*', 'datasets/*', 'helpers/*']},
    install_requires=[
        'aiohttp',
        'pandas',
        'mandrill-really-maintained',
        'pymysql',
        'requests',
        'pysftp',
        'pyarrow',
        'twine',
        'clickhouse-driver',
        'fs',
        'python-gnupg',
        'xmltodict',
        'zeep'
    ],
    zip_safe=False
)
