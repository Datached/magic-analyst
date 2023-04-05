from setuptools import setup, find_packages

setup(
    name="magic-analyst",
    version="0.1.0",
    author="David Okpare",
    description="IPython extension for data analysis on datasets from Kaggle",
    long_description="IPython extension that allows searching, downloading, extracting and performing EDA on datasets "
    "from Kaggle",
    url="https://github.com/DaveOkpare/magic-analyst",
    keywords="ipython, jupyter",
    packages=find_packages(),
    install_requires=[
        "ipython>=8.12.0",
        "kaggle==1.5.13",
        "langchain==0.0.131",
        "openai==0.27.4",
        "jupyter",
        "python-dotenv==1.0.0",
    ],
)
