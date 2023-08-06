from setuptools import setup, Extension, find_packages

import os.path
import distutils.extension

setup(name='funnyjoke',
      version='0.5',
      description='The funniest joke in the world',
      author='Flying Circus',
      license='MIT',
      #packages=['funnyjoke'],
	  packages=find_packages(),
	  scripts=['tell.py'],
	  ext_modules = [Extension('funnyjoke.fastjoke', ['src/fastjoke.c'])],
      zip_safe=False)
