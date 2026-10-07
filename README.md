# TechZone Store — Full-Stack Demo (with Owner Login)

## What's inside
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python + Flask (with login sessions)
- **Database:** SQLite

## Two roles
- **Visitors** (public): see live stock and buy items only
- **Owner/Admin** (login required): restock items AND add new products

## Admin login
- Username: `admin`
- Password: `techzone123`
- Login at: http://127.0.0.1:5000/login

## How to run
1. pip install -r requirements.txt
2. python app.py
3. Open http://127.0.0.1:5000

## Security note
This is a learning demo — the admin password is stored in plain text in app.py.
Real websites hash passwords (e.g. with bcrypt) and use HTTPS.
