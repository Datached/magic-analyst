import os
import zipfile

from dotenv import load_dotenv
from kaggle.api.kaggle_api_extended import KaggleApi
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI

load_dotenv()


class Kaggle:
    def __init__(self):
        self.kaggle = KaggleApi()
        self.kaggle.authenticate()
        self.path = os.getcwd()
        self.folder = None

    def search(self, query):
        return self.kaggle.dataset_list(search=query)

    def download(self, dataset, folder_name=None) -> str:
        try:
            # dataset, folder_name, *_ = line.split() + [None]
            if folder_name is None:
                folder_name = dataset.split("/")[1]

            path = os.path.join(self.path, folder_name)
            self.folder = folder_name
            self.kaggle.dataset_download_files(dataset, path)
            return path
        except (ValueError, IndexError) as e:
            raise ValueError("Not a valid dataset name")

    @staticmethod
    def extract(path):
        try:
            for file_name in os.listdir(path):
                if file_name.split(".")[-1] == "zip":
                    file_name = os.path.join(path, file_name)
                    with zipfile.ZipFile(file_name, "r") as zipref:
                        zipref.extractall(path)
            return path
        except Exception as e:
            return str(e)


"""
This method is unused. But the idea is to dynamically create dataframes for extracted .csv files.

    @staticmethod
    def filter(path):
        try:
            output = []
            for file_path in os.listdir(path):
                file_name = file_path.split('/')[-1]
                split_file_name = file_name.split(".")
                if split_file_name[-1] == "csv":
                    _ = os.path.join(path, file_path)
                    locals()["_".join([split_file_name[0], "df"])] = pd.read_csv(_)
                    return f'pd.read_csv({locals()["_".join([split_file_name[0], "df"])]})'
            return str(output)
        except Exception as e:
            return str(e)
"""

# Load the tool configs that are needed.
kaggle = Kaggle()

tools = [
    Tool(
        name="Download",
        func=kaggle.download,
        description="useful for when you need to find and download dataset about current events",
    ),
    Tool(
        name="Extract",
        func=kaggle.extract,
        description="useful for when you need to extract downloaded files",
    ),
]

llm = OpenAI(temperature=0, openai_api_key=os.getenv("OPEN_AI_KEY"))

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)


if __name__ == "__main__":
    agent.run("Download the 'heptapod/titanic' dataset and extract it")
