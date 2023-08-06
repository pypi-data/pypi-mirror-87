from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Construct_Code_py',
  version='2.2.4',
  description='Generador de ID de Usuarios',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Wilbert Sanchez',
  author_email='wilbertenriquechable522@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='IDs', 
  packages=find_packages(),
  install_requires=['']
)
