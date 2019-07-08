import logging                  # for logging purposes import zipfile                  
import zipfile                  # for zipping/unzipping files
import os                       # for os related stuff, like walking through direcory structures
import argparse                 # for command-line argument parsing
import requests

def get_best_logger(log_file, verbose):
    # Setup logger - (Python logger breaks PEP8 by default)
    logger = logging.getLogger(__name__)
    if verbose:
        logger.setLevel('DEBUG')
    # file_handler logs to file, stream_handler to console
    file_handler = logging.FileHandler(log_file)
    stream_handler = logging.StreamHandler()
    # formatter sets log format
    formatter = logging.Formatter('%(asctime)s - %(name)s : %(levelname)s - %(message)s')
    # add formatter to both handlers
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    # add both handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger

def unzip_recursive(zipped_file, to_folder, set_remove=True):
    """
    Function that recursively goes through folders and unpacks zips inside them.
    All unzipped files are stored in the same folder (output_folder)
    """
    logger.debug("Unzipping {} to {}".format(zipped_file, to_folder))
    with zipfile.ZipFile(zipped_file, 'r') as zfile:
        try:
            zfile.extractall(path=to_folder)
        except (zipfile.BadZipFile, IOError) as ziperror:
            logger.fatal("Tried unzipping {} but got stuck: {}".format(zipped_file, ziperror))
            exit(0)
    # if set_remove is True, remove the original zip file after extraction
    if (set_remove):
        os.remove(zipped_file)
        return
    # walk through the selected folder
    for dir_name, subdir_list, file_list in os.walk(to_folder):
        for specific_file in file_list:
            # look for zip-file
            if (specific_file.endswith('.zip')):
                new_file_path = os.path.join(dir_name, specific_file)
                # if it is a zip file, extract its contents and enter the folder, then unzip and look for files again.
                logger.debug("Zip file: {}".format(new_file_path))
                unzip_recursive(new_file_path, os.path.dirname(new_file_path))

def downloadfile(url, file_name):
    # This way the file is downloaded and completely saved in memory before writing to external storage. Should this be avoided?
    try:
        r = requests.get(url, allow_redirects=True)
    # Stop when there are connection issues
    except requests.exceptions.RequestException as re:
        logger.fatal(re)
        exit(1)
    try:
        with open(file_name,'wb') as f:
            f.write(r.content)
    # Stop when the file cannot be opened or written.
    except IOError as ioe:
        logger.fatal(ioe)
        exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and unzip the BeST-dataset")
    parser.add_argument('output_dir', type=str, help="location to store the xml-files")
    parser.add_argument('--url', type=str, help="url to download location of dataset", default="https://opendata.bosa.be/download/best/best-full-latest.zip")
    parser.add_argument('--file_name', type=str, help="use this option to change the file name", default="dataset.zip")
    parser.add_argument('--log_name', type=str, help="use this option to change the log file name", default="download.log")
    parser.add_argument('--verbose', action="store_true", help="toggle verbose output",  default=False)
    parser.add_argument('--no_download', action="store_true", help="Don't download file, only extract", default=False)
    args = parser.parse_args()
    # Make the logger
    logger = get_best_logger(args.log_name, args.verbose)
    # Download the file
    if not args.no_download:
        logger.info("Start download")
        downloadfile(args.url,args.file_name)
        logger.info("Download done")
    logger.info("Start extraction")
    unzip_recursive(args.file_name,args.output_dir,False)
    logger.info("Done")
