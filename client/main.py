from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
import requests
import os
import json


app = Flask(__name__)


@app.route('/')
def home():
    try:
        response = requests.get('http://localhost:5001/api/home')
        data = response.json()
        token = True if request.cookies.get('token') else False
        return render_template('index.html', data=data['result'], token=token)
    except:
        return render_template('connection_error.html')
    
    
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
        except Exception as e:
            print(e)
            return render_template('connection_error.html')
    return render_template('register.html')


@app.route('/logout')
def logout():

    resp = make_response(redirect(url_for('home')))
    resp.set_cookie('token', '', expires=0)
    
    return resp

        
@app.route('/login')
def login():
    pass


@app.route('/become_client')
def become_client():
    pass


@app.errorhandler(404)
def not_found(e):
    return render_template('not_found.html')


if __name__ == "__main__":
    app.run(debug=True, port=3000)
    