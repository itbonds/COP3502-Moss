import mosspy
import os

moss_user_id = os.environ['moss_user_id']
m = mosspy.Moss(moss_user_id, "java")

m.setDirectoryMode(1)
m.setIgnoreLimit(1000)
m.setNumberOfMatchingFiles(600)

m.addFilesByWildcard("resources/submissions/*/*.java")

url = m.send()

print("Report URL:" + url) 

m.saveWebPage(url, "out/report.html")

mosspy.download_report(url, "out/report/", connections=8, log_level=20)

# TODO Clean up the mossum call
args = {
    'filter': [], # string list; Include only matches between these names.
    'filteri': [],  # string list; Include only matches involving these names.
    'filterx': [],  # string list; Exclude matches between these names.
    'filterxi': [],  # string list; Exclude matches involving any of these names.
    'min-matches': 1, # Show only files with N or more matces between each other. This is only applicable to merged results.
    'show-loops': False, # Include loops in the output graph.
    'output': '', # Name of the output file.
    'hide-labels': False, # Hide edge labels, which otherwise show the percentage and lines of code matches have in common'
    'report': False, # Generates a report showing how many submissions each pair has in common.
    'merge': False, # Merge all reports into one image
    'anonymize': False, # Substitute names of matched files for random names
    'transformer': '', # A regular expression that is used to transform the name of them matched files.
    'format': 'png', # Format of output files. See Graphviz documentation.
    'min-lines': 1, # All matches where fewer than L lines are matched are ignored.
    'min-percent': 90, # All matches where less than P%% of both files are matched are ignored.
    'urls': [] , # string list; URLs to Moss result pages.
}

cmd = []
cmd.append('mossum {}'.format(url))
cmd.append('--output out/mossum/report')
cmd.append('--t ".*/(.+)/.*"')
cmd.append('--min-percent 75')
final = ' '.join(cmd)
print('exec: {}'.format(final))
os.system(final)
