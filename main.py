import os
import zipfile

import pandas as pd
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
        # self.openai = os.getenv("OPEN_AI_KEY") if os.getenv("OPEN_AI_KEY") else input("Enter your OpenAI Keys")
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

    @staticmethod
    def create(path):
        for file_path in os.listdir(path):
            file_name, ext = file_path.split("/")[-1].split(".")
            if ext == "csv":
                csv_file = os.path.join(path, file_path)
                globals()["_".join([file_name.lower(), "df"])] = pd.read_csv(csv_file)
        data_frames = [i for i in globals().keys() if i.endswith("df")]
        return f"Here are the dataframes created: {data_frames}"


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
    Tool(
        name="Create",
        func=kaggle.create,
        description="useful for when you need to create dataframes from extracted files",
    ),
]

llm = OpenAI(temperature=0, openai_api_key=os.getenv("OPEN_AI_KEY"))

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

if __name__ == "__main__":
    agent.run(
        "Download abecklas/fifa-world-cup and extract and create dataframes from it"
    )
