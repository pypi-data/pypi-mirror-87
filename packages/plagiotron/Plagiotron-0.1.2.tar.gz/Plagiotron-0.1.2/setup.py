from distutils.core import setup


setup(
    name = 'Plagiotron',
    packages = ['src'], 
    version = '0.1.2',
    description = 'Plagiotron proyecto',
    install_requires = ['Click', 'nltk', 'termcolor'],
    author= 'Wladmir Domingos',
    author_email='wladmir_d@hotmail.com',
    url= 'https://github.com/WladmirD/Plagiotron',
    keywords = ['NLP', 'text', 'text reuse'],
    entry_points='''
    [console_scripts]
    plagiotron = src.src:cli''',
)
