import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'backend/file_uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app.config.update(
    TESTING=True,
    SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
)


def check_file_number(path):
    filename = os.path.splitext(os.path.basename(path))[0]
    if filename[-1] == ')':
        return(int(filename[-2]))
    else:
        return(0)
    

def create_new_filename(filename, old_number):
    base_name, file_extension = os.path.splitext(filename)

    if base_name[-1] == ')':
        new_base_name = f'{base_name[:-3]}({old_number+1})'
    else:
        new_base_name = f'{base_name}({old_number+1})'

    new_filename = f'{new_base_name}{file_extension}'

    return new_filename


def write_or_rename(file, dir_name, filename):
    path = os.path.join(dir_name, filename)

    if os.path.exists(path):
        number = check_file_number(path)
        new_filename = create_new_filename(filename, number)
        new_path = os.path.join(dir_name, new_filename)
        os.rename(path, new_path)

        return 'File Renamed'
    else:
        file.save(os.path.join(path))
        return 'File Uploaded'


@app.route('/', methods=['POST'])
def upload_file():
    file = request.files['file']
    
    if file and allowed_file(file.filename):
        # filename = secure_filename(file.filename)
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        message = write_or_rename(file, app.config['UPLOAD_FOLDER'], file.filename)

        return message


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)