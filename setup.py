# encoding: utf-8
from distutils.core import setup
import codecs
from swatch import __version__ as VERSION


README = codecs.open('README.rst', encoding='utf-8').read()
LICENSE = codecs.open('LICENSE', encoding='utf-8').read()

setup(
    name='swatch',
    version=VERSION,
    author='Marcos A Ojeda',
    author_email='marcos@generic.cx',
    url='http://github.com/nsfmc/swatch',
    packages=['swatch'],
    license=LICENSE,
    description='a parser for adobe swatch exchange files',
    long_description=README,
    platforms=['any'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Artistic Software',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
