# Here we will create structure of thefiles of our project 
import os
from pathlib import Path
import logging

project_path = Path(os.getcwd())
print(project_path)

logging.basicConfig(level=logging.INFO,format='[%(asctime)s]: %(message)s:')
# List all the required files:

list_files=[
   
    f"Backend/__init__.py",
    f"Backend/main.py",
    f'Backend/preprocess.py'
    
    f"Fetch_Files/_init__.py",
    f'Fetch_Files/fetch_files.py'
  
    "app.py",
    "requirements.txt",
    "setup.py",

    ]

for filepath in list_files:
    filepath=Path(filepath)
    filedir,filename=os.path.split(filepath)
    
    if filedir!="":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"Created directory: {filedir} for the file {filename}")

    # we will only create file when file do not exits and there is no code in the file
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        
        with open(filepath,'w') as f:
            pass
            logging.info(f"Creating file: {filepath}")
    
    else:
        logging.info(f"File {filepath} already exists")

# Branch created