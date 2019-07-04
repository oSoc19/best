import logging                  # for logging purposes import zipfile                  # for zipping/unzipping files
import os                       # for os related stuff, like walking through direcory structures
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
    logger.debug("Unzipping {} to {}".format(zipped_file, to_folder))
    with zipfile.ZipFile(zipped_file, 'r') as zfile:
        #TODO catch exceptions
        zfile.extractall(path=to_folder)
    # if set_remove is True, remove the original zip file after extraction
    if (set_remove):
        os.remove(zipped_file)
    # walk through the selected folder
    for dir_name, subdir_list, file_list in os.walk(to_folder):
        for specific_file in file_list:
            # look for zip-files
            if (specific_file.endswith('.zip')):
                new_file_path = os.path.join(dir_name, specific_file)
                # if it is a zip file, extract its contents and enter the folder, then unzip and look for files again.
                logger.debug("Zip file: {}".format(new_file_path))
                unzip_recursive(new_file_path, os.path.dirname(specific_file))

def downloadfile(url, file_name):
    # This way the file is downloaded and completely saved in memory before writing to external storgae. Should this be avoided?
    r = requests.get(url, allow_redirects=True)
    open(,'wb').write(r.content)

def main():
    # Download the file
    logger.info("Start download")
    file_name = 'dataset.zip'
    url = 'https://opendata.bosa.be/download/best/best-full-latest.zip'
    downloadfile(url,file_name):
    """
    logger.info("Download done")
    input_zip = "/home/osoc19/best/dataset.zip"
    output_dir = "/home/osoc19/best/out"
    logger.info("Start extraction")
    unzip_recursive(input_zip,output_dir,False)
    """
    logger.info("Done")

# call main
main()
