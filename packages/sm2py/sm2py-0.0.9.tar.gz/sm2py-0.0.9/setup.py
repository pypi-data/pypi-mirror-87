from setuptools import setup, find_packages
from distutils.extension import Extension
try:
    from Cython.Build import cythonize, build_ext
except:
    build_ext = None

version = '0.0.9'


setup(name='sm2py',
      version=version,
      description="Python version SM2 keypair generator signature and verify, ecdh secret sharing, for human mind",
      long_description="""\
Python version SM2 keypair generator signature and verify, ecdh secret sharing, for human mind""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='ecc,ecdh,secp256k1,signature,verification',
      author='Alexander.Li',
      author_email='superpowerlee@gmail.com',
      url='https://github.com/ipconfiger/sm2py',
      license='GPLv2+',
      packages=find_packages(exclude=['ez_setup', 'sm2py.egg-info']),
      include_package_data = True,
      zip_safe=True,
      install_requires=[
          "point",
          "salsa20>=0.3.0"
      ],
      cmdclass={'build_ext': build_ext} if build_ext else {},
      ext_modules=[Extension('sm2py.curv', ['sm2py/curv.c'])],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
