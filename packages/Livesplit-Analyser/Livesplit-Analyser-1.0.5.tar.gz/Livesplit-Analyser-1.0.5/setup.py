from setuptools import setup, find_packages
import re
import io

with open('README.md', 'r') as f:
    long_description = f.read()

with io.open('livesplit_analyser/__version__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)


setup(
    name='Livesplit-Analyser',
    version=version,
    author='IguanasInPyjamas',
    author_email='liquidmikerrs@gmail.com',
    description='Get statistical analysis from livesplit files',
    packages=find_packages(),
    url='https://https://github.com/IguanasInPyjamas/Livesplit-Analyser',
    keywords=['livesplit','statistics','graphs','playtime'],
    install_requires=[
        'PyQt5>=5.15.1',
        'matplotlib>=3.3.3',
        'DateTime>=4.3',
    ],

    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points='''
        [console_scripts]
        livesplit-analyse=livesplit_analyser.gui:main
    '''
)
