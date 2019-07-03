import logging                  # for logging purposes
import zipfile                  # for zipping/unzipping files
import os                       # for os related stuff, like walking through direcory structures
from pathlib  import Path       # object-oriented paths
import argparse                 # for command-line argument parsing
import requests

# Setup logger - (Python logger breaks PEP8 by default)
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')
# file_handler logs to file, stream_handler to console
file_handler = logging.FileHandler('downloader.log')
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(name)s : %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

def unzip_recursive(zipped_file, to_folder, set_remove=True):
    """
    Function that recursively goes through folders and unpacks zips inside them.
    All unzipped files are stored in the same folder (output_folder)
    """
    print(to_folder)
    with zipfile.ZipFile(zipped_file, 'r') as zfile:
        #TODO catch exceptions
        zfile.extractall(path=to_folder)
    # if set_remove is True, remove the original zip file after extraction
    if (set_remove):
        os.remove(zipped_file)
    # walk through the selected folder
    for dir_name, subdir_list, file_list in os.walk(to_folder):
        logger.info('inside folder: {}'.format(to_folder))
        for specific_file in file_list:
            print(specific_file)
            specific_file_path = Path(specific_file)
            # look for zip-files
            if (specific_file_path.suffix =='.zip'):
                new_file_path = (Path(dir_name) / specific_file_path)
                # if it is a zip file, extract its contents and enter the folder, then unzip and look for files again.
                unzip_recursive(new_file_path,to_folder)

logger.info("Start download")

logger.info("Download done")

logger.info("Start extraction")
# create the output directory
output_directory = Path("/home/osoc19/best/unzip_output")
try:
    os.mkdir(output_directory)
except FileExistsError:
    logger.error("Output directory already exists")
unzip_recursive(Path("/home/osoc19/best/foldertje.zip"),Path("/home/osoc19/best/foldertje"),False)
logger.info("Done")
