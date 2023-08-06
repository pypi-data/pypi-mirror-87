import subprocess
from setuptools import setup, find_packages
from setuptools.command.install import install


EVALUATION_REQUIREMENTS = [
    'flask==1.1.2',
    'flask_restful',
    'pillow',
    'PIL',
    'wordcloud',
    'matplotlib'
]

TRAINING_REQUIREMENTS = []

setup(name='lightai',
      packages=find_packages(include=['lightai.*']),
      author='Marouen Azzouz, Youssef Azzouz',
      author_email='azzouz.marouen@gmail.com, youssef.azzouz1512@gmail.com',
      version='0.0.1',
      install_requires=EVALUATION_REQUIREMENTS,
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'train': TRAINING_REQUIREMENTS,
      })
