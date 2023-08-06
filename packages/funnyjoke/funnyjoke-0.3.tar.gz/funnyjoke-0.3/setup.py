from setuptools import setup, Extension, find_packages

setup(name='funnyjoke',
      version='0.3',
      description='The funniest joke in the world',
      author='Flying Circus',
      license='MIT',
      #packages=['funnyjoke'],
	  packages=find_packages(),
	  scripts=['tell.py'],
	  ext_modules = [Extension('fastjoke', ['src/fastjoke.c'])],
      zip_safe=False)
