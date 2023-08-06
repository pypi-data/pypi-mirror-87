from setuptools import setup
import os 
import myprojet

setup(name = 'projetpyfadsey',
      version = myprojet.__version__,
      author = 'fadoun_seydou',
      author_email = 'aliamagnefique123@gmail.com',
      package = 'myprojet',
      url='https://github.com/fadoun-seydou/projet',
      description = 'creation d’un package python',
      long_description = open(os.path.join(os.path.dirname(__file__), 'README.txt ')).read(),
      long_description_content_type='text/markdown',
      install_requires=[
       'requests'
         ],
      python_requires='>=3.7',
      classifiers = ['Programming Language :: Python :: 3.7 ',
        ' License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'],
     )
