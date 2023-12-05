import os 

def write_file(file_path, content):
    """Write file to path"""    
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        with open(file_path, 'w+') as file:
            file.write(content)
        print(f'File written successfully to {file_path}')
    except Exception as e:
        print(f'Error writing to file: {e}')

def load_file(file_path):
    try:
        with open(file_path, 'r+') as file:
            content = file.read()
            return content
    except Exception as e:
        print(f'Error loading file: {e}')
        return None
