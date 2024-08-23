import sys
from processor import Processor

def main():
    # Check if the correct number of arguments are passed
    if len(sys.argv) != 2:
        print("Usage: python vm_translator.py <filename.vm>")
        sys.exit(1)

    # Get the filename from the command-line arguments
    filename = sys.argv[1]

    try:
        # Open the file for reading
        with open(filename, 'r') as file:
            content = file.read()
            file_path_without_ext = filename.split('.')[0]
            Processor.process_file(content, file_path_without_ext)

    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
