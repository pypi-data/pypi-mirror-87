import subprocess
import setuptools
from setuptools.command.install import install

# -* dependencies *-
__install_requires__ = ['pandas', 'sklearn', 'matplotlib', 'numpy', 'spacy', 'nltk', 'tqdm',
                        'unicodedata2', 'gensim', 'configparser', 'vaderSentiment', 'unidecode',
                        'wordcloud']


# -* nltk.punkt, nltk.stopwords *-
class Install(install):
    def run(self):
        install.run(self)

        # install nltk punkt, stopwords
        for sub_module in ('punkt', 'stopwords'):
            cmd = ["python", "-m", "nltk.downloader", sub_module]
            with subprocess.Popen(cmd, stdout=subprocess.PIPE) as proc:
                print(proc.stdout.read())


# -* sample corpus: vatican publication *-
def doc_iterator(path: str) -> str:
    """Yields json documents."""
    import os

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.json'):
                yield os.path.join(root, file)

import pkg_resources
__sample_docs__ = list(doc_iterator(pkg_resources.resource_filename('compling', 'example-corpus/vatican-publications')))
__senti_lexicons__ = [pkg_resources.resource_filename('compling', 'senti-lexicons/sentix.csv'),
                      pkg_resources.resource_filename('compling', 'senti-lexicons/fannix.csv')]

# -* long description *-
with open("README.md", "r") as fh:
    __long_description__ = fh.read()

setuptools.setup(
    name="compling",
    version="0.0.30",
    author="Francesco Periti",
    author_email="peritifrancesco@gmail.com",
    description="Computational Linguistic",
    long_description=__long_description__,
    long_description_content_type="text/markdown",
    url="https://github.com/FrancescoPeriti/compling",
    packages=setuptools.find_packages(),
    package_data={'compling': ['config.ini', 'default_config.ini'] + __sample_docs__ + __senti_lexicons__},
    cmdclass={'install': Install},
    install_requires=__install_requires__,
    setup_requires=['nltk', 'spacy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

# python setup.py sdist bdist_wheel
# python -m twine upload --repository pypi dist/* --skip-existing

# dependency_links=[
# 'https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz',
# 'https://github.com/explosion/spacy-models/releases/download/it_core_news_sm-2.3.0/it_core_news_sm-2.3.0.tar.gz',
# 'https://github.com/explosion/spacy-models/releases/download/es_core_news_sm-2.3.1/es_core_news_sm-2.3.1.tar.gz',
# 'https://github.com/explosion/spacy-models/releases/download/pt_core_news_sm-2.3.0/pt_core_news_sm-2.3.0.tar.gz',
# 'https://github.com/explosion/spacy-models/releases/download/fr_core_news_sm-2.3.0/fr_core_news_sm-2.3.0.tar.gz'
# 'https://github.com/explosion/spacy-models/releases/download/zh_core_web_sm-2.3.1/zh_core_web_sm-2.3.1.tar.gz',
# 'https://github.com/explosion/spacy-models/releases/download/da_core_news_sm-2.3.0/da_core_news_sm-2.3.0.tar.gz',
# 'https://github.com/explosion/spacy-models/releases/download/nl_core_news_sm-2.3.0/nl_core_news_sm-2.3.0.tar.gz',
# 'https://github.com/explosion/spacy-models/releases/download/de_core_news_sm-2.3.0/de_core_news_sm-2.3.0.tar.gz',
# 'https://github.com/explosion/spacy-models/releases/download/el_core_news_sm-2.3.0/el_core_news_sm-2.3.0.tar.gz',
# 'https://github.com/explosion/spacy-models/releases/download/ja_core_news_sm-2.3.2/ja_core_news_sm-2.3.2.tar.gz',
# 'https://github.com/explosion/spacy-models/releases/download/lt_core_news_sm-2.3.0/lt_core_news_sm-2.3.0.tar.gz',
# 'https://github.com/explosion/spacy-models/releases/download/nb_core_news_sm-2.3.0/nb_core_news_sm-2.3.0.tar.gz',
# 'https://github.com/explosion/spacy-models/releases/download/pl_core_news_sm-2.3.0/pl_core_news_sm-2.3.0.tar.gz',
# 'https://github.com/explosion/spacy-models/releases/download/ro_core_news_sm-2.3.1/ro_core_news_sm-2.3.1.tar.gz'
# ],
