try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


VERSION = "0.1.1"

setup(name="cloverpy",
      version=VERSION,
      description=("Utility to convert coverage.py's"
                   " coverage.xml to clover.xml"
                   " without any 3rd party dependencies."),
      author="Digicat",
      packages=["cloverpy"],
      entry_points="""\
      [console_scripts]
      cloverpy = cloverpy.clover:main
      """)
