# Cloud Server

A small Flask-based private cloud server for managing files through a web browser. Users sign in with credentials configured in environment variables and can upload, view, download, and delete files in their own storage directory.

## Features

- Session-based login and logout
- Separate storage folders for up to five users
- Individual file uploads
- Folder uploads with nested paths
- File preview and download
- File, folder, and all-file deletion
- Basic path validation to keep users inside their assigned folders

## Requirements

- Python 3.9 or newer
- A writable directory for each user's files

Install the Python dependency with:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project directory. The application requires the following values:

```dotenv
FLASK_SECRET_KEY=replace-with-a-long-random-secret

USER1=user1
UPLOAD_FOLDER_USER1=/path/to/user1/files
LOGIN_PASSWORD_USER1=change-this-password

USER2=user2
UPLOAD_FOLDER_USER2=/path/to/user2/files
LOGIN_PASSWORD_USER2=change-this-password

USER3=user3
UPLOAD_FOLDER_USER3=/path/to/user3/files
LOGIN_PASSWORD_USER3=change-this-password

USER4=user4
UPLOAD_FOLDER_USER4=/path/to/user4/files
LOGIN_PASSWORD_USER4=change-this-password

USER5=admin
UPLOAD_FOLDER_USER5=/path/to/admin/files
LOGIN_PASSWORD_USER5=change-this-password
```

`USER5` is treated as the administrator account by the application. The current implementation uses the configured usernames as dictionary keys, so each `USER` value should be unique.

Keep `.env` private and do not commit real passwords or secret keys.

## Running the server

From the project directory, with the virtual environment activated:

```bash
python3 app.py
```

Open <http://localhost:5000> in a browser and sign in with one of the configured users. The server listens on all interfaces, so it can also be reached from another device using the host machine's local IP address.

## Project structure

```text
.
├── app.py                 # Flask application and file operations
├── requirements.txt       # Python dependencies
├── templates/
│   ├── index.html         # File browser
│   └── login.html         # Login page
└── static/                # Static assets, including fonts
```

## Security notes

- Use a strong, randomly generated `FLASK_SECRET_KEY`.
- Use strong, unique passwords for every account.
- Run behind HTTPS before exposing the server outside a trusted local network.
- Restrict permissions on the configured upload directories.
- The application currently stores passwords in environment variables and compares them directly; use a proper password-hashing system before deploying it publicly.
