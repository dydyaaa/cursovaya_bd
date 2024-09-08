from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
import requests
import os
import json


app = Flask(__name__)


@app.route('/')
def home():
    token = True if request.cookies.get('token') else False
    try:
        response = requests.get('http://localhost:5001/api/home')
        data = response.json()
        return render_template('index.html', data=data['result'], token=token)
    except:
        return render_template('connection_error.html', token=token)
    
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            response = requests.post('http://localhost:5001/api/register', json={
                'user_login': request.form['user_login'],
                'password': request.form['password']
            })
            
            data = response.json()
            
            if response.status_code == 200:
                token = data.get('token')
                resp = make_response(redirect(url_for('home')))
                resp.set_cookie('token', token, httponly=True, max_age=3600)
                return resp
            else:
                error = data.get('result')
                return render_template('register.html', error=error)
        except Exception:
            return render_template('connection_error.html')
    return render_template('register.html')

        
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            response = requests.post('http://localhost:5001/api/login', json={
                'user_login': request.form['user_login'],
                'password': request.form['password']
            })
            
            data = response.json()
            
            if response.status_code == 200:
                token = data.get('token')
                resp = make_response(redirect(url_for('home')))
                resp.set_cookie('token', token, httponly=True, max_age=3600)
                return resp
            else:
                error = data.get('result')
                return render_template('login.html', error=error)
        except Exception:
            return render_template('connection_error.html', token=token)
    return render_template('login.html')


@app.route('/logout')
def logout():

    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('token', '', expires=0)
    
    return resp


@app.route('/become_client', methods=['GET', 'POST'])
def become_client():
    token = request.cookies.get('token') if request.cookies.get('token') else False
    if not token:
        return redirect('register.html')
    if request.method == 'POST':
        response = requests.post('http://localhost:5001/api/become_client', json={
                'client_name': request.form['name'],
                'birth_day': request.form['birth_day'],
                'passport_series': request.form['passport_series'],
                'passport_number': request.form['passport_number'],
                'contact_number': request.form['contact_number'],
                'address': request.form['adress']
            },
            headers={
                'Authorization': token
            })
        
        data = response.json()
        
        if response.status_code == 200:
            return redirect('/profile')
        else:
            error = data['result']
            return render_template('become_client.html', token=token, error=error)
    return render_template('become_client.html', token=token)


@app.route('/profile')
def profile():
    token = request.cookies.get('token') if request.cookies.get('token') else False
    if not token:
        return redirect('/register')
    try:
        response = requests.get('http://localhost:5001/api/profile', headers={
            'Authorization': token
        })
        
        data = response.json()
        if response.status_code == 200:
            return render_template('profile.html', 
                                   data=data['result'][0], 
                                   client=data.get('client')[0], 
                                   token=token)
        else:
            return render_template('connection_error.html', token=token, data=data['result'])
    except:
        return render_template('connection_error.html', token=token)

@app.errorhandler(404)
def not_found(e):
    token = True if request.cookies.get('token') else False
    return render_template('not_found.html', token=token)


if __name__ == "__main__":
    app.run(debug=True, port=3000)
    