from IPython.core.magic import (register_line_magic)
from langchain.agents import create_csv_agent

from main import llm, kaggle, agent


@register_line_magic
def search(line):
    return kaggle.search(line)


@register_line_magic
def download(line):
    agent.run("Download {dataset} and extract it".format(dataset=line))


@register_line_magic
def eda(line):
    csv_agent = create_csv_agent(llm, line, verbose=True)
    csv_agent.run("Write a detailed exploratory data analysis for this dataset")