import os
import zipfile

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ["KAGGLE_CONFIG_DIR"] = os.path.join(project_root, ".kaggle")

from kaggle.api.kaggle_api_extended import KaggleApi

class DataIngestion:

    def __init__(self):

        # dataset name from kaggle
        self.dataset_name = "salonijaroli/airbnb-price"

        # where zip will be stored
        self.download_dir = "artifacts"

        # zip file path
        self.zip_file_path = os.path.join(self.download_dir, "airbnb-price.zip")

        # extracted data path
        self.extract_dir = os.path.join(self.download_dir, "raw_data")

    def download_dataset(self):

        print("Starting dataset download...")

        os.makedirs(self.download_dir, exist_ok=True)

        api = KaggleApi()
        api.authenticate()

        api.dataset_download_files(
            self.dataset_name,
            path=self.download_dir,
            unzip=False
        )

        print("Dataset downloaded successfully!")

    def extract_zip_file(self):

        print("Extracting dataset...")

        os.makedirs(self.extract_dir, exist_ok=True)

        with zipfile.ZipFile(self.zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(self.extract_dir)

        print("Dataset extracted successfully!")


if __name__ == "__main__":

    obj = DataIngestion()

    obj.download_dataset()

    obj.extract_zip_file()