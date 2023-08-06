from distutils.core import setup
setup(
  name = 'Py2SQL',
  packages = ['Py2SQL'],
  version = '0.1',
  license='mit',
  description = 'Package to work with firebirdSQL',
  author = 'Alexander Podvazhuk',
  author_email = 'sapod7@gmail.com',
  url = 'https://github.com/inmistlosted',
  download_url = 'https://github.com/inmistlosted/metaprogramming/archive/0.1.tar.gz',
  keywords = ['Firebird', 'Py2SQL', 'SQL'],
  install_requires=[
          'fdb'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)