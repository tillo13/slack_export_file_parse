# Slack Export File Extractor

This script provides a way to categorize and download all files of a certain type from a Slack workspace export. It's an efficient tool for large-scale downloads, extracting code snippets, or retrieving valuable information spread across a variety of Slack channels.

## How It Works

The script traverses all subdirectories of a given directory, inspecting all '.json' files (which represent Slack channels) in these folders. 

For every 'filetype' found in these files, the script provides a count of how many instances of this filetype are present in the Slack exports.

Two main functionalities are then provided:

1. `count_filetypes_in_json(path)`: This function traverses all .json files in the given directory and counts the instances of each filetype, while excluding the ones specified in the `exclude_filetypes` list. 

2. `extract_code_files(path, code_filetypes)`: This function downloads the specified code files from the Slack workspace, renames them with an epoch timestamp and their originating channel name, and saves them in a directory named after the filetype.

This structure makes it easy for users to quickly locate files of a certain type, particularly useful for code snippets or other commonly used resources.

## How To Use It

To use this, follow these steps:

1. Export your data from Slack. This should download as a zip file.
2. Unzip the file. This should produce a folder filled with subfolders representing your channels and containing .json files.
3. Place the .py script into the parent folder of the Slack export.
4. Set the `folder_path` in the script to match the parent folder of your Slack export.
5. Optionally, specify filetypes to exclude in the `exclude_filetypes` list.
6. Execute the script.

The scripts output will be directories organized by file type, each populated with the corresponding retrieved files.

## Requirements

You will need Python 3.x and the 'requests' and 'json' libraries installed to use this script.
You also need an exported Slack workspace data.

## Caveats

The scripts default timezone is PST. Change this if you are in a different locale.

Some files may not be downloadable if they were shared via external links or if the links are expired.


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.