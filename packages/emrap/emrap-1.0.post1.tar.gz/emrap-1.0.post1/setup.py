from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    desc_lines = fh.readlines()

long_description = ''.join(
    filter(lambda line: '<img' not in line, desc_lines))

setup(
    name='emrap',
    version='1.0.post1',
    url='https://github.com/aayla-secura/eMRaP',
    author='AaylaSecura1138',
    author_email='aayla.secura.1138@gmail.com',
    description='eMail Requestor and Processor',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    install_requires=[
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'http-parser',
        'requests',
        'colorlog',
    ],
    zip_safe=False)
