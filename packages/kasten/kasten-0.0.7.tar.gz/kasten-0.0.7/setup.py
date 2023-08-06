from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='kasten',
      version='0.0.7',
      description='Efficient, secure data serialization format with extensibility.',
      author='Kevin Froman',
      author_email='beardog@mailbox.org',
      url='https://chaoswebs.net',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      python_requires='>3.6.0',
      install_requires=['msgpack', 'mimcvdf>=1.1.0'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers"
      ],
     )
