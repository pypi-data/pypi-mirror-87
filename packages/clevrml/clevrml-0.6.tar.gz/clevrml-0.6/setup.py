from setuptools import setup

with open('README.md') as f:
    long_description = f.read() 

setup(
    name='clevrml',
    version='0.6',
    description='The Official Package for clevrML.',
    py_modules=['clevrml'],
    install_requires=['Pillow>=7.2.0'],
    license='Apache 2.0',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={'': 'src'}
)