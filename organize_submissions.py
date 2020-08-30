from pathlib import Path
import shutil
import re

import config as cfg

zybooks_submission_regex = "^(?P<first_name>[^_]+)_((?P<middle_name>[^_]+)?\_){0,2}(?P<last_name>[^_]+)_(?P<email>[^_]+)_(?P<date>[^_]+)_(?P<time>[^_.]+)\.?(?P<extension>[\w\d]+)?$"
canvas_submission_regex = "^(?P<student_name>[^_]+)\_((?P<late>LATE)\_)?(?P<user_id>[^_]+)_(?P<submission_item_id>[^_]+)_(?P<file_name>[^.]+)\.?(?P<extension>[\w\d]+)?$"

def extract_submissions(config):
    shutil.unpack_archive(config.submission_archive, config.submission_folder)

def organize_submissions_zybooks(config):
    submission_folder = Path(config.submission_folder)
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

def organize_submissions_canvas(config):
    """
    Organizes the downloaded submissions from Canvas. 
    """
    submission_folder = Path(config.submission_folder)
    regex = re.compile(canvas_submission_regex)
    files = []
    files.extend(submission_folder.iterdir())

    for filepath in files:
        # canvas files are usually zips or the files themselves .pdf etc
        if filepath.is_dir():
            continue

        result = regex.match(filepath.name)
        if result is None:
            continue

        student_name = result.group('student_name')
        is_late = result.group('late')
        file_name = result.group('file_name')
        extension = result.group('extension')

        student_folder = submission_folder.joinpath(student_name)
        student_folder.mkdir(exist_ok=True)

        print('file: {}, student_name: {}, file_name: {}, ext: {}'.format(filepath, student_name, file_name, extension))

        # Three possible extension we want to conside zip, java, other
        # zip: we want to unarchive the folder and take the java files into the student's folder
        # java: place into the student's folder
        # other: discard
        if extension.lower() == 'zip':
            organize_canvas_zip(filepath, student_folder)
        elif extension.lower() == 'java':
            dest = student_folder.joinpath(file_name + '.java')
            print('dest: ' + str(dest))
            shutil.move(filepath, dest)

        if filepath.exists():
            filepath.unlink()


def organize_canvas_zip(filepath, student_folder):
    search_queue = []
    delete_stack = []
    

    shutil.unpack_archive(filepath, student_folder, 'zip')
    search_queue.extend(student_folder.iterdir())

    for item in search_queue:
        # if the item is a directory, then we add it to the search queue to see if it has any java files
        if item.is_dir():
            search_queue.extend(item.iterdir())
            delete_stack.insert(0,item)
        elif item.suffix == '.java': # if it is a java file, then we move it to the student folder
            shutil.move(item, student_folder.joinpath(item.name))
        else: # not source code, so we remove it
            item.unlink()
    
    for item in delete_stack:
        if item.is_dir():
            item.rmdir()
        else:
            item.unlink()


if __name__ == "__main__":
    config = cfg.Config()
    extract_submissions(config)
    if config.site_type == cfg.SiteType.CANVAS:
        organize_submissions_canvas(config)
    elif config.site_type == cfg.SiteType.ZYBOOKS:
        organize_submissions_zybooks(config)
    