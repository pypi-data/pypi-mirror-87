from setuptools import setup, find_packages

setup(
    name='cisu_python',
    version='0.1',
    packages=find_packages('src/'),
    package_dir={'cisu': 'src/cisu'},
    include_package_data=True,
    package_data={'cisu': [
        'constants/*.json',
        'templates/*.xml',
    ]},
)