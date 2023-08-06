from setuptools import setup

with open('README.md') as readme_file:
    README = readme_file.read()

setup(
    name='wic',
    packages=['wic'],
    version='0.1',
    license='apache-2.0',
    description='WinIDEA command line interface',
    author='Juergen Schmid',
    author_email='jur.schmid@gmail.com',
    url='https://github.com/hacki11/wic',
    keywords=['isystem', 'winidea', 'cli'],
    install_requires=[
        'click'
        #, 'isystem.connect' not available for windows yet - needs to be installed manually
    ],
    entry_points={
        'console_scripts': ['wic=wic.cli:cli'],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)