# Kaggle Datasets Extension

This is an ipython extension that allows you to search and download datasets from Kaggle.

## Installation

To install the extension, run:


```python 
pip install 
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

"""
[
abecklas/fifa-world-cup,
...
...
]
"""

%download "abecklas/fifa-world-cup"

"""
The dataset abecklas/fifa-world-cup has been downloaded and extracted to /content/fifa-world-cup.
"""
```



This will search for all datasets related to Titanic and download the Titanic dataset.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
