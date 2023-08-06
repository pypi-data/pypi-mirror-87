import setuptools

USERNAME = 'beasteers'
NAME = 'ixconfig'

setuptools.setup(
    name=NAME,
    version='0.1.1',
    description='',
    long_description=open('README.md').read().strip(),
    long_description_content_type='text/markdown',
    author='Bea Steers',
    author_email='bea.steers@gmail.com',
    url='https://github.com/{}/{}'.format(USERNAME, NAME),
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': ['ixcfg=ixconfig:main']},
    install_requires=['fire'],
    license='MIT License',
    keywords='')
