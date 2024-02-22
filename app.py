from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import sqlite3
import os
import json

UPLOAD_FOLDER = 'mysite/static/uploads'
ALLOWED_EXTENSIONS =set(['png','jpg','jpeg'])

app = Flask(__name__)
app.config['DATABASE'] = 'QRBase.db'
app.secret_key = 'TH15_1S_@_S3CR3T_K3Y'

if not os.path.exists(app.config['DATABASE']):
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                mail TEXT PRIMARY KEY,
                passwd TEXT NOT NULL 
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS access_log (
                id INTEGER  PRIMARY KEY,
                mail TEXT NOT NULL,
                key INTEGER NOT NULL,
                counter INTEGER NOT NULL DEFAULT 1
            )
        ''')

        conn.commit()
        conn.close()

@app.route('/',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        mail = request.form['mail']
        passwd = request.form['passwd']

        signup_conn = sqlite3.connect(app.config['DATABASE'])
        cur=signup_conn.cursor()
        cur.execute('SELECT * FROM users WHERE mail=?', (mail,))
        result = cur.fetchone()
        
        if result:
            signup_conn.close()
            return render_template('index.html',message="User already exists")
        else:
            cur.execute('INSERT INTO users (mail,passwd) VALUES (?,?)', (mail,passwd))
            signup_conn.commit()
            signup_conn.close()
            session['mail'] = mail
            return redirect(url_for('dashboard'))
    
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    session.clear()
    if request.method == 'POST':
        mail = request.form['mail']
        passwd = request.form['passwd']
        if mail == 'admin@inwaster.com' and passwd == 'admin':
            session['mail'] = mail
            return redirect(url_for('admin'))
        
        login_conn = sqlite3.connect(app.config['DATABASE'])
        cur=login_conn.cursor()
        cur.execute('SELECT * FROM users WHERE mail=? AND passwd=?', (mail,passwd))
        result = cur.fetchone()
        
        if result:
            session['mail'] = mail
            login_conn.close()
            return redirect(url_for('dashboard'))
        else:
            login_conn.close()
            return render_template('login.html',message="Invalid credentials")
    
    return render_template('login.html')

@app.route('/dashboard',methods=['GET'])
def dashboard():
    if 'mail' in session:
        dashboard_conn = sqlite3.connect(app.config['DATABASE'])
        cur = dashboard_conn.cursor()
        cur.execute("SELECT key,counter from access_log where mail=?",(session['mail'],))
        rec=cur.fetchall()
        score=0
        for i in rec:
            score+=i[0]*i[1]
        return render_template('homepage.html', mail=session['mail'], score = score)
    else:
        return redirect(url_for('login'))
    
@app.route('/processQR',methods=['POST'])
def processQR():   
    qrdata = request.json
    print("Recievied: ", qrdata)
    key = qrdata['data']
    mail = qrdata['email']
    new_key=''
    for i in key:
        if i.isdigit():
            new_key+=i

    new_key = int(new_key)
    access_conn = sqlite3.connect(app.config['DATABASE'])
    cur=access_conn.cursor()
    cur.execute('SELECT * FROM access_log WHERE mail=? AND key=?', (mail,new_key))
    result = cur.fetchone()
    if result:
        cur.execute('UPDATE access_log SET counter=counter+1 WHERE mail=? AND key=?', (mail,new_key))
    else:
        cur.execute('INSERT INTO access_log (mail,key) VALUES (?,?)', (mail,new_key))
    access_conn.commit()
    access_conn.close()

    return jsonify({"status":"success"})

@app.route('/adminlogs',methods=['GET'])
def admin():
    if 'mail' not in session or session['mail'] != 'admin@inwaster.com':
        return redirect(url_for('login'))
    
    with open('messages.json', 'r') as file:
        data = json.load(file)
    return render_template('admin.html', data=data, d_keys = data[0].keys())

@app.route('/recievemsg',methods=['POST'])
def recievemsg():
    data = request.json
    print("Recievied: ", data)

    filename = 'messages.json'

    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            json.dump([], file)

    # Load existing data from the file
    with open(filename, 'r') as file:
        existing_data = json.load(file)
        
    # Append the new data to the existing data
    existing_data.append(data)

    # Write the updated data back to the file
    with open(filename, 'w') as file:
        json.dump(existing_data, file)
    
    return jsonify({"status":"success"})

if __name__ == '__main__':
    app.run(debug=True)

