import os

def list_files_and_directories(directory):
    # Get the list of files and directories in the specified directory
    contents = os.listdir(directory)

    # Separate files and directories
    files = [item for item in contents if os.path.isfile(os.path.join(directory, item))]
    directories = [item for item in contents if os.path.isdir(os.path.join(directory, item))]

    return files, directories

files, directories = list_files_and_directories(r'C:\Program Files\Dev ECO\Projects\test\dump\removing')

print(files)
print(directories)
