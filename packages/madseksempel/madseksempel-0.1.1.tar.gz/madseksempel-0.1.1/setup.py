from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='madseksempel',
  version='0.1.1',
  description='A statistical calculator for the course \'Probability Theory and Statistics at the University of Copenhagen',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Mads Klynderud',
  author_email='madsanton31@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='statcalc', 
  packages=find_packages(),
  install_requires=[''] 
)