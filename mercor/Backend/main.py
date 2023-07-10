
import openai
from Fetch_Files.fetch_files import fetch_user_repositories

from Fetch_Files.fetch_files import fetch_files_from_github
from Backend.preprocess import final_processing
import re
import pandas as pd
from dotenv import dotenv_values
import os
from dotenv import dotenv_values
import os
import openai

# Load variables from the .env file
env_variables = dotenv_values(".env")

# Access the OpenAI API key
secret_key = env_variables.get("OPENAI_SECRET_KEY")

# Set the OpenAI API key
openai.api_key = secret_key

def analyze_file(file):
    """
    Analyzes a file to determine its technical complexity of the particular file.

    Args:
        file (str): The content of the file to be analyzed.

    Returns:
        str: The analysis response for the file.
    """
    prompt = f"Analyzing file:\nTechnical complexity of file: {file}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        temperature=0.7,
        n=1,
        stop=None,
    )
    return response.choices[0].text.strip()

def chunk_and_analyze(process):
    """
    Chunks and analyzes the given list of files.
    If the file is too long, it will be split into chunks of like 1000 tokens and analyzed.

    Args:
        process (list): The list of files to be processed.

    Returns:
        list: The analysis responses for the files.
    """
    responses = []
    for file in process:
        file=''.join(file)
        file_str = str(file)
        prompt_tokens = len(file_str.split())
        if prompt_tokens <= 1000:
            response = analyze_file(file_str)
            responses.append(response)
        else:
            chunks = []
            for i in range(0, prompt_tokens, 1000):
                chunks.append(file_str[i : i + 1000])
            for chunk in chunks:
                response = analyze_file(chunk)
                responses.append(response)
    return responses

def GPT_call(repo):
    """
    Generates the final output for the given repository.

    Args:
        repo (dict): The dictionary of repository names and URLs.

    Returns:
        pandas.DataFrame: The sorted DataFrame containing repo_name, overall_complexity, and reason.
        And DataFrame is sorted by the descending order of the overall_complexity. values.
    """
    result = []

    for name, url in repo.items():
        file_url = fetch_files_from_github(url)
        process = final_processing(file_url)
        responses = chunk_and_analyze(process)
        
        prompt = prompt = f"""
Analyze the responses obtained from all the files of the GitHub repository: {responses}.
Assign a score between 1-10 based on the technical complexity of the repository, where (0-5) indicates low complexity and (6-10) indicates high complexity.
Consider factors such as code organization, usage of advanced algorithms, integration of external libraries, and adherence to best practices.
Provide the overall score, including a decimal, to sort the repository complexity.
Additionally, list the content or topics present in this repository and briefly explain the reason for the overall score (30 words only).
"""


        response1 = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0.7,
            n=1,
            stop=None,
        )
        
        overall_complexity_prompt = f"Extract the numeric value for the overall score from the reason: {response1.choices[0].text.strip()}"
        overall_complexity_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=overall_complexity_prompt,
            max_tokens=50,
            temperature=0.7,
            n=1,
            stop=None,
        )
        
        extracted_complexity = overall_complexity_response.choices[0].text.strip() 
        numeric_value = re.findall(r"\d+\.\d+", extracted_complexity)
        extracted_value = None
        if numeric_value:
            extracted_value = float(numeric_value[0])

        dict2 = {
            'repo_name': name,
            'overall_complexity': extracted_value,
            'reason': response1.choices[0].text.strip()
        }
        result.append(dict2)

        if len(result) > 7:
            break
    
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(result, columns=['repo_name', 'overall_complexity', 'reason'])

    # Sort the DataFrame by 'overall_complexity' in descending order
    df_sorted = df.sort_values('overall_complexity', ascending=False)

    return df_sorted

