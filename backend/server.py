import os
from flask import Flask, request

# working directory
UPLOAD_FOLDER = 'backend/file_uploads'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# function that checks if file is allowed to be stored
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# configurations
app.config.update(
    TESTING=True,
    SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
)

# function that checks the number of the file
def check_file_number(path):
    # get the name of the file
    filename = os.path.splitext(os.path.basename(path))[0]

    # if it ends with '(x)' where x is a digit, return x. else return 0
    if filename[-3] == '(' and filename[-2].isdigit() and filename[-1] == ')':
        return(int(filename[-2]))
    else:
        return(0)
    

# function that creates new filenime e.g. text.txt -> text(1).txt, and text(1).txt -> text(2).txt etc.
def create_new_filename(filename, old_number):
    # get base name and extension of the file
    base_name, file_extension = os.path.splitext(filename)

    # if base name ends with '(x)' where x is a digit, replace x with x+1 and store into new string. else, add '(x)' to old base name
    if base_name[-3] == '(' and base_name[-2].isdigit() and base_name[-1] == ')':
        new_base_name = f'{base_name[:-3]}({old_number+1})'
    else:
        new_base_name = f'{base_name}({old_number+1})'

    # add file extension to new base name
    new_filename = f'{new_base_name}{file_extension}'

    return new_filename


# function to write new file or rename an existing one
def write_or_rename(file, dir_name, filename):
    # create path for posted file
    path = os.path.join(dir_name, filename)

    # if file already stored, create new filename and apply it. else, save file
    if os.path.exists(path):
        number = check_file_number(path)
        new_filename = create_new_filename(filename, number)
        new_path = os.path.join(dir_name, new_filename)
        os.rename(path, new_path)

        return 'File Renamed'
    else:
        file.save(os.path.join(path))
        return 'File Uploaded'


# function that runs when file is posted
@app.route('/', methods=['POST'])
def upload_file():
    # get file from request
    file = request.files['file']
    
    # if file is allowed to be stored, write it or rename an dold one
    if file and allowed_file(file.filename):
        message = write_or_rename(file, app.config['UPLOAD_FOLDER'], file.filename)

        return message


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)