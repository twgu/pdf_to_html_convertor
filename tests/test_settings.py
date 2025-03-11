import os
from dotenv import load_dotenv

load_dotenv()

# File
FILE_FULL_NAME = os.path.normpath(
    'C:/Users/a2023200/Documents/file_name.pdf'
)
FILE_PATH = os.path.dirname(FILE_FULL_NAME)
FILE_NAME, FILE_EXTENSION = os.path.splitext(os.path.basename(FILE_FULL_NAME))
FILE_EXTENSION = FILE_EXTENSION.lower()

# Working Folder
WORKING_FOLDER = os.path.normpath(os.path.join(FILE_PATH, FILE_NAME))
CONVERSION_SAVE_FOLDER = os.path.normpath(os.path.join(WORKING_FOLDER, 'conversion'))

# Azure Document Intelligence
AZURE_DI_ENDPOINT_URL = os.getenv('ENDPOINT')
AZURE_DI_API_KEY = os.getenv('API_KEY')

# Image min size
IMAGE_MIN_WIDTH = 15
IMAGE_MIN_HEIGHT = 15


def page_start_line(page_number: int) -> str:
    return f'↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓ {page_number} page ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓'


def page_end_line(page_number: int) -> str:
    return f'↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑ {page_number} page ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑'
