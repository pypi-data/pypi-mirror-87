from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='N2PC_Library',
  version='0.0.1',
  description='Calculates N2PC component of attention',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Lora Fanda',
  author_email='lorafanda7@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='N2PC', 
  packages=find_packages(),
  install_requires=[''] #libraries that the module depends on 
)