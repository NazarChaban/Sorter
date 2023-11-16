# Sorter
File Organizer Script

This Python script is designed to organize files within a specified directory by categorizing them based on their file extensions. It also handles file name normalization using transliteration for non-English characters (specifically designed for Cyrillic characters).

Features:
-Supports a predefined set of file categories: images, videos, documents, audio, and archives.
-Allows for easy addition of new file categories and associated extensions.
-Normalizes file names by replacing non-alphanumeric characters with underscores and transliterating Cyrillic to Latin characters.
-Unpacks archives to dedicated folders while removing the original archive files.
-Moves sorted files into their respective category folders.
-Deletes empty directories that remain after sorting files.
-Outputs the list of sorted files along with known and unknown file extensions encountered during the sorting process.

Usage:
To use this script, run it with a single argument specifying the path to the directory you want to organize:
python sorter.py <path_to_directory>

Ensure that you have the necessary permissions to modify the contents of the directory.

Requirements:
Python 3.x
-os module
-sys module
-shutil module

How It Works:
1. The script checks if the correct number of command-line arguments is provided and whether the specified path is a directory.
2. It creates categories' directories within the specified directory.
3. The script walks through the directory, normalizing file names and sorting them into their respective categories based on file extensions.
4. Archives are unpacked into their own directories, and the original archive files are deleted.
5. The script removes any empty directories it finds.
6. Finally, it outputs the results of the sorting operation, listing the sorted files by category and the known and unknown file extensions.

Notes
-The script expects Cyrillic characters and will transliterate them to their Latin alphabet equivalents.
-It treats unrecognized file extensions as unknown and reports them at the end of the operation.
-The script is designed to be run from the command line and does not have a graphical user interface.

Contribution
Feel free to contribute to this project by adding new features or improving the existing code. You can add support for more file types, improve error handling, or create a more interactive user experience.