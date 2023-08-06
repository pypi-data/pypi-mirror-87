from setuptools import setup, find_packages
 
classifiers = []
 
setup(
  name='fastapi_auth',
  version='0.1.0',
  description='Standard authorization method from fastapi documentation',
  long_description="Standard authorization method from fastapi documentation",
  url='',  
  author='Alex Demure',
  author_email='alexanderdemure@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='fastapi',
  packages=find_packages(),
  install_requires=[
    'python-multipart>=0.0.5',
    'pydantic>=1.4',
    'python-jose>=3.1.0',
    'passlib>=1.7.2',
    'bcrypt>=3.1.7'
  ],
  dependency_links=['https://github.com/AlexDemure/fastapi_auth']
)
