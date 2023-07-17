#first export your data from Slack.  It's a zip file.  WHen unzipped it'll show JSON files in a directory.  Put this script in that directory.
import os
import json
import requests
from collections import defaultdict
from datetime import datetime, timezone, timedelta

exclude_filetypes = ['dog', 'cat']  # file types to exclude

def count_filetypes_in_json(path):
    filetypes = defaultdict(int)

    # Traverse directory/subdirectory
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.json'):
                json_file_path = os.path.join(root, file)

                # Open json file here
                with open(json_file_path, 'r') as json_file:
                    try:
                        data = json.load(json_file)  # Load json content
                    except json.JSONDecodeError:
                        continue  # Skip file if it's not valid json
                    
                    if isinstance(data, list):  # If the json content is a list
                        for item in data:
                            # Traverses the dictionary for "files" key which has a list of dictionaries as its value
                            if "files" in item:  
                                for entry in item["files"]:
                                    # Check if 'filetype' key exists in the dictionary, and is not in the exclusion list
                                    if 'filetype' in entry and entry['filetype'] not in exclude_filetypes: 
                                        filetypes[entry['filetype']] += 1  # Increment filetype count
                                              
    # List out the details of each file type and its count.
    for filetype, count in filetypes.items():
        print(f'Filetype: {filetype} - Count: {count}')
    return filetypes.keys()

def download_and_save_code_file(url, path):
    print(f'\r\033[K{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - Downloading file: {path.split("/")[-1]}', end='')
    response = requests.get(url)
    with open(path, 'wb') as f:
        f.write(response.content)

def extract_code_files(path, code_filetypes):
    
    # Traverse directory/subdirectory
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.json'):
                json_file_path = os.path.join(root, file)

                # Get the channel name from the parent directory
                channel_name = os.path.basename(os.path.dirname(json_file_path))
                
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
                                    # Check if 'filetype' key exists in the dictionary, is a code filetype, and is not in the exclusion list
                                    if 'filetype' in entry and entry['filetype'] in code_filetypes and entry['filetype'] not in exclude_filetypes:  
                                       # Create directory name by filetype
                                        directory_path = os.path.join("./code_extracted", entry['filetype'])
                                        os.makedirs(directory_path, exist_ok=True)
                                        # Add epoch timestamp to filename
                                        dt = datetime.fromtimestamp(entry['created'], tz=timezone(-timedelta(hours=8)))  # Convert epoch time to local time (PST)
                                        filename = f"{dt.strftime('%Y%m%d%H%M')}_{channel_name}_{entry['name'].rpartition('.')[0]}.{entry['name'].rpartition('.')[2]}" 
                                        # Download code file and save it in "<filetype>" directory within "code_extracted"
                                        file_url = entry['url_private']
                                        file_path = os.path.join(directory_path, filename)
                                        download_and_save_code_file(file_url, file_path)

start_time = datetime.now()

folder_path = './'  # Change this to your specific folder nested within the current directory
filetypes = count_filetypes_in_json(folder_path)
print("\nDownloading files:")
extract_code_files(folder_path, filetypes)

end_time = datetime.now()
print(f'\nTime taken: {end_time - start_time}')