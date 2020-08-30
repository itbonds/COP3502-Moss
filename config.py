from enum import Enum

class SiteType(Enum):
  CANVAS = 1
  ZYBOOKS = 2

class Config():
  def __init__(self):
    self.site_type = SiteType.CANVAS # 

    self.submission_archive = "resources/submissions_pro4.zip" # path to the downloaded submission archive is
    self.submission_folder = 'resources/submissions_canvas' # where files be extracted to 

    self.moss_ignore_limit = 1000 # -m: the maximum number of times a given passage may appear before it is ignored
    self.moss_directory_mode = True # If each folder represents a student
    self.moss_file_type = 'java' # file type / program language
    self.moss_number_of_matching_files = 600 # -n: the number of similarity matches to show
    self.moss_file_wildcard = self.submission_folder + '/*/*.java' if self.moss_directory_mode else '/*.java' # wildcard to get all of the relevant files
