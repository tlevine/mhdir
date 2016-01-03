from setuptools import setup

setup(
    name = 'mhdir',
    version = '0.0.1',
    description = 'Like MH but smaller and based on Maildir',
    author = 'Thomas Levine',
    author_email = '_@thomaslevine.com',
    url = 'http://dada.pink/mhdir/',
    entry_points = {'console_scripts': ['m = mhdir:m']},
    license = 'AGPL',
    packages = ['mhdir'],
    install_requires = [
        'horetu',
    #   'lxml',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.4',
    ],
)
