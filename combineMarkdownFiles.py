"""
This script searches for Markdown files in all subfolders, sorts them by date, and combines them into a single Markdown file. The date is extracted from the filename, which is in the format YYYY-MM-DD. The filename is written as a header at the beginning of each file, and the content of each file is written to the combined file. Square brackets surrounding words, such as [[example word]], are removed from the content.
"""

import os
import re

# Regex to extract the date from the filename
date_regex = re.compile(r'(\d{4})-(\d{2})-(\d{2})')

# List of Markdown files, sorted by date
markdown_files = []

# Search all subfolders
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.md'):
            # Add the file to the list
            full_path = os.path.join(root, file)
            date_match = date_regex.search(file)
            if date_match:
                year, month, day = map(int, date_match.groups())
                date = (year, month, day)
            else:
                date = None
            markdown_files.append((date, full_path))

# Sort the list by date
markdown_files.sort(key=lambda x: x[0])

# Open the target file in write mode ('w')
with open('combined.md', 'w') as outfile:
    # Write all files to the target file
    for date, file in markdown_files:
        with open(file, 'r') as infile:
            # Read the content of the file
            content = infile.read()
            # Remove the square brackets from words surrounded by them
            content = re.sub(r'\[\[(.+?)\]\]', r'\1', content)
            # Write the filename as a header
            filename = os.path.splitext(os.path.basename(file))[0]
            outfile.write(f'# {filename}\n')
            # Write the content of the file
            outfile.write(content)
            outfile.write('\n')
