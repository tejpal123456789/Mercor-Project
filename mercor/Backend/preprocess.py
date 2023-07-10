import re 
import os
import requests
import nbformat
from Fetch_Files.fetch_files import fetch_files_from_github,fetch_user_repositories






import re
import requests
import nbformat

def preprocess_code(code):
    """
    Preprocesses the code by removing comments and extra whitespaces.
    
    Args:
        code (str): The code to be preprocessed.
    
    Returns:
        str: The preprocessed code.
    """
    # Remove single-line comments starting with #
    code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)

    # Remove multi-line comments enclosed in /* */
    code = re.sub(r'/\*(.*?)\*/', '', code, flags=re.DOTALL)

    # Remove extra whitespaces
    code = re.sub(r'\s+', ' ', code)

    # Trim leading and trailing whitespaces
    code = code.strip()

    return code

def final_processing(file_urls):
    """
    Performs the final processing of files from the given URLs by fetching their contents and extracting code.
    In this  code, utf-8 refers to the UTF-8 encoding scheme. 
    UTF-8 is a character encoding that can represent virtually all characters in the Unicode standard, 
    which includes a vast range of characters from different languages and scripts.
    It means here, we are ignoring the other files like files with .pkl or .pt or .model etc extensions
    
    Args:
        file_urls (list): A list of tuples containing the URL and file name of the files to be processed.
    
    Returns:
        list: A list of lists, where each inner list contains the extracted code from a file.
    """
    preprocessed_code = []

    for file_url, file_name in file_urls:
        response = requests.get(file_url)
        print(file_name)
        files_text = []

        if response.status_code == 200:
            try:
                file_content = response.content.decode('utf-8')  # Decode the response content using UTF-8

                if file_name.endswith('.ipynb'):  # Check if the file is a Jupyter Notebook
                    notebook = nbformat.reads(file_content, as_version=4)  # Parse the notebook

                    for cell in notebook['cells']:
                        if cell['cell_type'] == 'code':
                            source = cell['source']
                            code = ''.join(source)
                            files_text.append(code)

                else:  # Assume it's a text file
                    files_text.append(file_content)

                preprocessed_code.append(files_text)

            except UnicodeDecodeError:
                print(f"Error decoding {file_name} using 'utf-8' codec. Skipping file.")

    return preprocessed_code
