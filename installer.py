import os, subprocess, webbrowser
# Check if Python is installed

try:
    subprocess.check_output('python --version', shell=True)
except subprocess.CalledProcessError:
    print("""Critical error: Python not found""")
    webbrowser.open('https://www.google.com/search?q=how+to+install+python')

# Check if pip is installed
try:
    subprocess.check_output('pip --version', shell=True)
except subprocess.CalledProcessError:
    print("""Critical error: pip not found.""")
    webbrowser.open('https://www.google.com/search?q=how+to+install+pip')

# Install the required packages with pip
os.system('pip install scipy.io.wavfile')
os.system('pip install sounddevice')
os.system('pip install pycaw.pycaw')
os.system('pip install elevenlabs')
os.system('pip install colourama')
os.system('pip install comtypes')
os.system('pip install sqlite3')
os.system('pip install openai')
os.system('pip install ctypes')
os.system('pip install pydub')
os.system('pip install time')

import requests

r = requests.get('https://raw.githubusercontent.com/OneTrueTreeTree/JPT/main/ICR.py')
with open(os.path.join(os.getcwd(), 'ICR.py'), 'wb') as file:
    file.write(r.content)

r = requests.get('https://raw.githubusercontent.com/OneTrueTreeTree/JPT/main/JPT.py')
with open(os.path.join(os.getcwd(), 'JPT.py'), 'wb') as file:
    file.write(r.content)

r = requests.get('https://raw.githubusercontent.com/OneTrueTreeTree/JPT/main/IGR.py')   
with open(os.path.join(os.getcwd(), 'IGR.py'), 'wb') as file:
    file.write(r.content)


import sqlite3

connection = sqlite3.connect('Users.db')
connection.close()

con = sqlite3.connect("Users.db")
cur = con.cursor()
sqlite_execute_string = """
    CREATE TABLE "user" (
        "user_id"	INTEGER NOT NULL UNIQUE,
        "first_name"	TEXT NOT NULL,
        "last_name"	TEXT,
        "user_info"	TEXT,
        PRIMARY KEY("user_id" AUTOINCREMENT)
    );"""
cur.execute(sqlite_execute_string)
con.commit()
con.close()

exit()
