# Kaggle Datasets Extension

This is an ipython extension that allows you to search and download datasets from Kaggle.

## Installation

To install the extension, you first need to clone the repo:

```commandline
git clone https://github.com/DaveOkpare/magic-analyst.git
```
Then run the command below
```python 
pip install .
```

You must authenticate using Kaggle’s public API. To obtain your Kaggle configuration file, visit [Kaggle](https://www.kaggle.com/me/account) and select the “Create New API Token” option to download the file.

Next, create a directory in your root folder called `.kaggle`. 
```shell
mkdir ~/.kaggle
```

Move the downloaded configuration file to the new directory, and change the permission using the command below.
```shell
mv kaggle.json ~/.kaggle
chmod 600 ~/.kaggle/kaggle.json
```


## Usage

To use the extension, simply import it in your notebook:


```python
%load_ext magic
```


You can then use the `%search` command to search for datasets:

```python
%search <query>
```


And the `%download` command to download and extract datasets:

```python
%download <dataset>
```


## Example

Here&apos;s an example of how to use the extension:

```python
%load_ext magic

%search "fifa"


# [
# abecklas/fifa-world-cup,
# ...
# ...
# ]


%download "abecklas/fifa-world-cup"

# The dataset abecklas/fifa-world-cup has been downloaded and extracted to /content/fifa-world-cup.
```



This will search for all datasets related to Titanic and download the Titanic dataset.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
