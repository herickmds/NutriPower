./sudo.bat net start MySQL56
FLASK_APP=app.py FLASK_DEBUG=1 flask run --port 80 --host 0.0.0.0

./sudo.bat net stop MySQL56