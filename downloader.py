import logging          # for logging purposes
import zipfile          # for zipping/unzipping files
import os               # for os related stuff, like walking through direcory structures
from pathlib import Path     # object-oriented paths

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

def unzip_recursive(zipped_file,to_folder,set_remove=True):
    """
    Function that recursively goes through folders and unpacks zip them.
    """
    print(to_folder)
    with zipfile.ZipFile(zipped_file, 'r') as zfile:
        #TODO catch exceptions
        zfile.extractall(path=Path(to_folder))
    # remove the zip file
    if (set_remove):
        os.remove(zipped_file)
    # walk through the selected folder
    for dir_name, subdir_list, file_list in os.walk(to_folder):
        absolute_path = Path(to_folder).parent / Path(dir_name)
        logger.info('inside folder: {}'.format(absolute_path))
        for specific_file in file_list:
            # look for zip-files
            if (Path(specific_file).suffix == '.zip'):
                # if it is a zip file, extract its contents and enter the folder, then unzip and look for files again.
                unzip_recursive(specific_file,absolute_path)

logger.info("Start extraction")
unzip_recursive("/home/osoc19/best/foldertje.zip","/home/osoc19/best/foldertje",False)
logger.info("Done")
