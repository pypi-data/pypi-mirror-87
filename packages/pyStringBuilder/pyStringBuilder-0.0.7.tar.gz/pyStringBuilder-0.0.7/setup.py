from distutils.core import setup

setup(
    name = 'pyStringBuilder',
    packages = ['pyStringBuilder'],
    version = '0.0.7',
    license = 'GNU General Public License v3 (GPLv3)',
    description = 'A python implementation of StringBuilder class found on Java and C-Sharp.',
    author = 'LMongoose',
    author_email = 'lukaspellezario@hotmail.com',
    url = 'https://github.com/LMongoose/py-stringbuilder',
    download_url = 'https://github.com/LMongoose/py-stringbuilder/0.0.1.tar.gz',
    keywords = [
        'string',
        'building',
        'append',
        'concatenation'
    ],
    python_requires='>=3.6',
    install_requires = [],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
    ]
)