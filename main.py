import ast
import getpass
import os
import zipfile

import pandas as pd
from dotenv import load_dotenv
from kaggle.api.kaggle_api_extended import KaggleApi
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from sqlalchemy import create_engine

load_dotenv()


class Kaggle:
    def __init__(self):
        self.kaggle = KaggleApi()
        self.kaggle.authenticate()
        self.path = os.getcwd()
        self.conn = None
        self.openai = (
            os.getenv("OPEN_AI_KEY")
            if os.getenv("OPEN_AI_KEY")
            else getpass.getpass("Enter your OpenAI Key:")
        )

    def search(self, query):
        return self.kaggle.dataset_list(search=query)

    def download(self, dataset, folder_name=None) -> str:
        try:
            # dataset, folder_name, *_ = line.split() + [None]
            if folder_name is None:
                folder_name = dataset.split("/")[1]

            path = os.path.join(self.path, folder_name)
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
        data_frames = []
        for file_path in os.listdir(path):
            file_name, ext = file_path.split("/")[-1].split(".")
            if ext == "csv":
                csv_file = os.path.join(path, file_path)
                globals()["_".join([file_name.lower(), "df"])] = pd.read_csv(csv_file)
                data_frames.append("_".join([file_name.lower(), "df"]))
        return f"Here are the dataframes created: {data_frames}"

    def establish(self, url):
        try:
            self.conn = create_engine(url)
            print("Database connected successfully!")
            return self.conn
        except:
            print("Unable to connect to the database.")

    def load(self, datasets):
        try:
            datasets = ast.literal_eval(datasets)
        except ValueError:
            pass
        for df in datasets:
            table_name = df
            globals()[df].to_sql(
                table_name, self.conn, if_exists="replace", index=False
            )


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
        description="useful for when you need to extract or unzip downloaded files",
    ),
    Tool(
        name="Create",
        func=kaggle.create,
        description="useful for when you need to create dataframes from extracted files",
    ),
    Tool(
        name="Establish",
        func=kaggle.establish,
        description="useful for when you need to establish a database connection",
    ),
    Tool(
        name="Load",
        func=kaggle.load,
        description="useful for when you need to load a dataset to database",
    ),
]

llm = OpenAI(temperature=0, openai_api_key=kaggle.openai)

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
