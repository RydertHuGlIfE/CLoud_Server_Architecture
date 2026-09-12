from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session
from functools import wraps
import os
import shutil
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']

UPLOAD_FOLDER = '/home/ryder2001/Documents'


os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#users FAAH
U1 = os.environ['USER1']
uploadu1 = os.environ['UPLOAD_FOLDER_USER1']
PU1 = os.environ['LOGIN_PASSWORD_USER1']

U2 = os.environ['USER2']
uploadu2 = os.environ['UPLOAD_FOLDER_USER2']
PU2 = os.environ['LOGIN_PASSWORD_USER2']

U3 = os.environ['USER3']
uploadu3 = os.environ['UPLOAD_FOLDER_USER3']
PU3 = os.environ['LOGIN_PASSWORD_USER3']

U4 = os.environ['USER4']
uploadu4 = os.environ['UPLOAD_FOLDER_USER4']
PU4 = os.environ['LOGIN_PASSWORD_USER4']

U5 = os.environ['USER5']
uploadu5 = os.environ['UPLOAD_FOLDER_USER5']
PU5 = os.environ['LOGIN_PASSWORD_USER5']
os.makedirs(uploadu1, exist_ok=True)
os.makedirs(uploadu2, exist_ok=True)
os.makedirs(uploadu3, exist_ok=True)
os.makedirs(uploadu4, exist_ok=True)
os.makedirs(uploadu5, exist_ok=True)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        if user == U1 and pwd == PU1:
            session['user'] = user
            return redirect(url_for('index'))
        elif user == U2 and pwd == PU2:
            session['user'] = user
            return redirect(url_for('index'))
        elif user == U3 and pwd == PU3:
            session['user'] = user
            return redirect(url_for('index'))
        elif user == U4 and pwd == PU4:
            session['user'] = user
            return redirect(url_for('index'))
        elif user == U5 and pwd == PU5:
            session['user'] = user
            return redirect(url_for('index'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    tree = {}
    for root, _, files in os.walk(UPLOAD_FOLDER):
        rel_root = os.path.relpath(root, UPLOAD_FOLDER)
        if rel_root == ".":
            rel_root = ""
        folder = tree.setdefault(rel_root, [])
        folder.extend(files)
    return render_template('index.html', tree=tree)

@app.route('/upload_file', methods=['POST'])
@login_required
def upload_file_only():
    files = request.files.getlist('file')
    for file in files:
        if file.filename:
            filename = os.path.basename(file.filename)
            full_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(full_path)
    return redirect(url_for('index'))

@app.route('/upload_folder', methods=['POST'])
@login_required
def upload_folder_only():
    files = request.files.getlist('file')
    for file in files:
        if file.filename:
            safe_path = os.path.normpath(file.filename).lstrip(os.sep)
            full_path = os.path.join(UPLOAD_FOLDER, safe_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            file.save(full_path)
    return redirect(url_for('index'))


@app.route('/download/<path:filename>')
@login_required
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route('/delete/<path:filename>')
@login_required
def delete_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.isfile(file_path):
        os.remove(file_path)
    return redirect(url_for('index'))

@app.route('/delete_folder/<path:foldername>')
@login_required
def delete_folder(foldername):
    folder_path = os.path.join(UPLOAD_FOLDER, foldername)
    if os.path.isdir(folder_path):
        shutil.rmtree(folder_path)
    return redirect(url_for('index'))

@app.route('/delete_files_in_folder/<path:foldername>')
@login_required
def delete_files_in_folder(foldername):
    folder_path = os.path.join(UPLOAD_FOLDER, foldername)
    if os.path.exists(folder_path):
        for f in os.listdir(folder_path):
            fp = os.path.join(folder_path, f)
            if os.path.isfile(fp):
                os.remove(fp)
    return redirect(url_for('index'))

@app.route('/delete_all')
@login_required
def delete_all():
    for root, dirs, files in os.walk(UPLOAD_FOLDER):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            shutil.rmtree(os.path.join(root, dir))
    return redirect(url_for('index'))

@app.route('/view/<path:filename>')
def view_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_from_directory(UPLOAD_FOLDER, filename)
    return "File not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

