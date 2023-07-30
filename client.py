import requests
from tqdm import tqdm

# def send_file_to_server():
#     url = 'http://localhost:5000/'  # Replace with the actual URL of your Flask server

#     with open('input.txt', 'rb') as file:
#         files = {'file': ('input.txt', file)}  # The key 'file' should match the key used in the server's request.files

#         response = requests.post(url, files=files)

#         # if response.status_code == 200:
#         #     print("File upload successful.")
#         # else:
#         #     print("File upload failed.")
#         print(response.text)

def read_input_file(path):
    with open(path, 'r') as file:
        lines = file.readlines()
    
    files_to_upload = [line.strip() for line in lines]
    
    return files_to_upload

def send_files_to_server():
    url = 'http://localhost:5000/'
    file_storage = 'file_storage/'

    files_to_upload = read_input_file('input.txt')

    for filename in tqdm(files_to_upload, desc='Uploading files', unit='file'):
        with open(file_storage+filename, 'rb') as file:
            files = {'file': (filename, file)}

            response = requests.post(url, files=files)

if __name__ == '__main__':
    send_files_to_server()