# instal package
pip install -r requirements.txt

# run backend server
gunicorn --bind 0.0.0.0:8000 "app:app" --timeout 15
