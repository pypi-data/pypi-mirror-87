from setuptools import setup, find_packages
from pybase_db.version import __version__

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='pybase_db',
    version=__version__,
    description=
    'PyBase is a database manager for multiple filetypes including SQLite3. Very poweful, simple and effective.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://ntbbloodbath.gitlab.io/PyBase/',
    author='NTBBloodbath, Danny2105',
    author_email='bloodbathalchemist@protonmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'psutil>=5.7.3',
        'pyyaml>=5.3.1',
        'rich>=9.2.0',
        'toml>=0.10.2'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Database',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: Software Development :: Libraries'
    ],
    zip_safe=False)
