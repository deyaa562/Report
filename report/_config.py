import configparser
import os

config = configparser.ConfigParser()

# Get the absolute path of the current file
current_file_path = os.path.abspath(__file__)

# Get the directory containing the current file
current_dir = os.path.dirname(current_file_path)

# Traverse up the directory hierarchy until we find a directory containing a file named 'requirements.txt'
while not os.path.exists(os.path.join(current_dir, 'report.ini')):
    current_dir = os.path.dirname(current_dir)
    config.read('report.ini')

UUID = config.get('Launch', 'UUID')