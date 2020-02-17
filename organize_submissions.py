from pathlib import Path
import shutil
import re

zybooks_submission_regex = "^(?P<first_name>[^_]+)_((?P<middle_name>[^_]+)?\_){0,2}(?P<last_name>[^_]+)_(?P<email>[^_]+)_(?P<date>[^_]+)_(?P<time>[^_.]+)\.?(?P<extension>[\w\d]+)?$"

def extract_submissions(config):
    shutil.unpack_archive(config['submissions_archive'], config['submissions_folder'])

def organize_submissions(config):
    submission_folder = Path(config['submissions_folder'])
    regex = re.compile(zybooks_submission_regex)

    # iterate over each submitted file
    for filepath in submission_folder.iterdir():
        # ignore any directories, in case they exist
        if filepath.is_dir():
            continue

        result = regex.match(filepath.name)
        if result is None:
            continue

        first_name = result.group('first_name')
        last_name = result.group('last_name')
        
        extension = result.group('extension')

        if extension is None:
            extension = ""

        # make the student's directory if it doesn't exist
        destination = submission_folder.joinpath(first_name + "_" + last_name)
        destination.mkdir(exist_ok=True)

        if extension.lower() == 'zip':
            shutil.unpack_archive(filepath, destination, 'zip')
            filepath.unlink()

if __name__ == "__main__":
    config = {}
    config['submissions_archive'] =  "resources/archive2.zip"
    config['submissions_folder'] = "resources/submissions"
    extract_submissions(config)
    organize_submissions(config)