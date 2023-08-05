from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools import setup, find_packages
import pathlib


here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

def post_install_script():
    import nltk
    nltk.download('stopwords')
    import stanza
    stanza.download('en', package='mimic', processors={'ner': 'i2b2'})

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        post_install_script()
        install.run(self)

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        post_install_script()
        develop.run(self)

setup(
	name='phenobert',
	version='1.0.5',
	description='A novel tool for human clinical disease phenotype recognizing with deep learning.', 
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/EclipseCN/PhenoBERT',
    author='NeoFengyh',
	author_email='18210700100@fudan.edu.cn',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
		],
	keywords='deep-learning, nlp, bert', 
	packages=find_packages(),
	include_package_data=True,
	python_requires='>=3.6, <4',
	install_requires=['nltk>=3.5', 'prettytable>=1.0.1', 'fasttext>=0.9.2', 'torch>=1.3.1', 'scipy>=1.5.2', 'stanza>=1.1.1'],
	scripts=['phenobert/utils/annotate'],
	cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
)