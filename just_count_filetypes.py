import os
import json
import requests
from collections import defaultdict

def download_and_save_code_file(url, path):
    response = requests.get(url)
    with open(path, 'wb') as f:
        f.write(response.content)

def extract_code_files(path):
    code_filetypes = ['python', 'cpp', 'javascript']  # Add more code filetypes if needed
    
    # Traverse directory/subdirectory
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.json'):
                json_file_path = os.path.join(root, file)
                
                # Open json file
                with open(json_file_path, 'r') as json_file:
                    try:
                        data = json.load(json_file)  # Load json content
                    except json.JSONDecodeError:
                        continue  # Skip file if it's not valid JSON
                    
                    if isinstance(data, list):  # If the json content is a list
                        for item in data:
                            # Traverse the dictionary for "files" key which has a list of dictionaries as it's value
                            if "files" in item:  
                                for entry in item["files"]:
                                    if 'filetype' in entry and entry['filetype'] in code_filetypes:  # Check if 'filetype' key exists in the dictionary and is a code filetype
                                        # Download code file and save it in "code_extracted" directory
                                        file_url = entry['url_private']
                                        file_path = os.path.join("./code_extracted", entry['name'])
                                        download_and_save_code_file(file_url, file_path)

folder_path = './'  # Change this to your specific folder nested within the current directory
extract_code_files(folder_path)