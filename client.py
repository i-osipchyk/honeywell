import requests
from tqdm import tqdm

# function to read file with the list of files. returns the list of files that should be uploaded
def read_input_file(path):
    with open(path, 'r') as file:
        lines = file.readlines()
    
    # remove \n from filenames
    files_to_upload = [line.strip() for line in lines]
    
    return files_to_upload


# function to send files
def send_files_to_server():
    # server address and port, directory with files to be sent
    url = 'http://localhost:5000/'
    file_storage = 'file_storage/'

    # filenames from input.txt
    files_to_upload = read_input_file('input.txt')

    # tqdm is used to print a progress bar
    for filename in tqdm(files_to_upload, desc='Uploading files', unit='file'):
        try:
            with open(file_storage + filename, 'rb') as file:
                # saves file and sends it to the server
                files = {'file': (filename, file)}
                response = requests.post(url, files=files)
                print(response.text)

        # in case wrong path is provided
        except FileNotFoundError:
            print(f"File {filename} not found. Skipping...")

if __name__ == '__main__':
    send_files_to_server()