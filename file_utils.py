import shutil
import os

def write_file(data, download_path):

    with open(download_path, 'x') as file:
        file.write(data)

    print(f"File downloaded to {download_path}")


def create_zip(file_path):
    shutil.make_archive(file_path, format='zip', root_dir=file_path)
