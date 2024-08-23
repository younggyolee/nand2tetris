import sys
import os
from processor import Processor

def main():
    # Check if the correct number of arguments are passed
    if len(sys.argv) != 2:
        print("Usage: python vm_translator.py <filename.vm>")
        sys.exit(1)

    # Get the filename from the command-line arguments
    filename = sys.argv[1]

    # Split the filename into the directory and the base name
    directory, basename = os.path.split(filename)

    # Split the base name into the name and the extension
    name, _ = os.path.splitext(basename)

    # Create a new file path with a different extension (e.g., '.txt')
    new_extension = '.asm'
    new_filepath = os.path.join(directory, name + new_extension)

    try:
        # Open the file for reading
        with open(filename, 'r') as file:
            content = file.read()
            Processor.process_file(content, new_filepath)

    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
