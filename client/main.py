from flask import Flask, render_template, request, redirect, url_for, make_response
import requests


app = Flask(__name__)
BACKEND_URL = 'http://localhost:5001/api/'

@app.route('/')
def home():
    token = True if request.cookies.get('token') else False
    try:
        response = requests.get(f'{BACKEND_URL}home')
        data = response.json()
        return render_template('index.html', data=data['result'], token=token)
    except:
        return render_template('connection_error.html', token=token)
    
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            response = requests.post(f'{BACKEND_URL}register', json={
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
    token = True if request.cookies.get('token') else False
    if request.method == 'POST':
        try:
            response = requests.post(f'{BACKEND_URL}login', json={
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


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    token = request.cookies.get('token') if request.cookies.get('token') else False
    if request.method == 'POST':
        response = requests.post(f'{BACKEND_URL}change_password', headers={
                'Authorization': token
            }, json={
            "user_password_first": request.form['password_1'],
            "user_password_second": request.form['password_2']
        })
        data = response.json
        if response.status_code == 200:
            resp = make_response(redirect(url_for('home')))
            resp.set_cookie('token', '', expires=0)
            return resp
        else:
            return render_template('change_password.html', token=token, error=data)
    return render_template('change_password.html', token=token)


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
        response = requests.post(f'{BACKEND_URL}become_client', json={
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


@app.route('/change_client_data', methods=['GET', 'POST'])
def change_client_data():
    token = request.cookies.get('token') if request.cookies.get('token') else False
    if not token:
        return redirect('register.html')
    if request.method == 'POST':
        response = requests.post(f'{BACKEND_URL}change_client_data', json={
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
            return render_template('change_client_data.html', token=token, error=error)
    return render_template('change_client_data.html', token=token)


@app.route('/profile')
def profile():
    token = request.cookies.get('token') if request.cookies.get('token') else False
    if not token:
        return redirect('/register')
    try:
        response = requests.get(f'{BACKEND_URL}profile', headers={
            'Authorization': token
        })
        
        data = response.json()
        if response.status_code == 200:
            client = data.get('client')[0] if data.get('client') else None
            return render_template('profile.html', 
                                   data=data['result'][0], 
                                   client=client, 
                                   token=token)
        else:
            return render_template('connection_error.html', token=token, data=data['result'])
    except:
        return render_template('connection_error.html', token=token)


@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    token = True if request.cookies.get('token') else False
    
    response = requests.get(f'{BACKEND_URL}calculator')
    
    data = response.json
    
    return render_template('calculator.html', data=data, token=token)
    

@app.route('/agent/clients_to_approve', methods=['GET'])
def clients_to_approve():
    token = True if request.cookies.get('token') else False
    
    response = requests.get(f'{BACKEND_URL}clients_to_approve', headers={
        "Authorization": request.cookies.get('token')
    })
    
    if response.status_code == 200:
        data = response.json()
        
        return render_template('clients_to_approve.html', token=token, clients=data['result'])
    else:
        return redirect('/')


@app.route('/approve_client', methods=['POST'])
def approve_client():
    client_id = request.form.get('client_id')
    response = requests.post(f'{BACKEND_URL}/approve_client', headers={
        "Authorization": request.cookies.get('token')
    }, json={
        "client_id": client_id
    })
    return redirect('/agent/clients_to_approve')


@app.route('/reject_client', methods=['POST'])
def reject_client():
    client_id = request.form.get('client_id')
    response = requests.post(f'{BACKEND_URL}/reject_client', headers={
        "Authorization": request.cookies.get('token')
    }, json={
        "client_id": client_id
    })
    return redirect('/agent/clients_to_approve')


@app.route('/get_my_polis', methods=['GET'])
def get_my_polis():
    token = True if request.cookies.get('token') else False
    
    response = requests.get(f'{BACKEND_URL}get_my_polis', headers={
        "Authorization": request.cookies.get('token')
    })
    
    data = response.json()
    
    if response.status_code == 200:
        return render_template('get_my_polis.html', policies=data['result'], token=token)
    else:
        return render_template('connection_error.html', token=token)


@app.route('/make_new_policy', methods=['GET', 'POST'])
def make_new_policy():
    token = True if request.cookies.get('token') else False
    
    if request.method == 'POST':
        response = requests.post(f'{BACKEND_URL}make_new_polis', headers={
            "Authorization": request.cookies.get('token')
        }, json={
            "policy_type": request.form['policy_type'],
            "date_start": request.form['date_start'],
            "date_stop": request.form['date_stop'],
            "car_brand": request.form['car_brand'],
            'year_of_manufacture': request.form['year_of_manufacture'],
            "sum_insurance": request.form['sum_insurance']
        })
        
        data = response.json()
        
        if response.status_code == 200:
            return redirect('/profile')
        else:
            error = data['result']
            return render_template('make_new_policy.html', token=token, error=error)
        
    return render_template('make_new_policy.html', token=token)


@app.route('/make_new_inshurance', methods=['GET', 'POST'])
def make_new_inshurance():
    token = True if request.cookies.get('token') else False
    
    if request.method == 'POST':
        
        response = requests.post(f'{BACKEND_URL}make_new_inshurance', headers={
            "Authorization": request.cookies.get('token')
        }, json={
            "policy_id": request.form['policy_id'],
            "date": request.form['date'],
            "description": request.form['description']
        })
        
        dataa = response.json()
        
        if response.status_code == 200:
            return redirect('/profile')
        
        else:
            response = requests.get(f'{BACKEND_URL}get_my_polis', headers={
                "Authorization": request.cookies.get('token')
            })
        
            data = response.json()
            
            return render_template('make_new_inshurance.html', token=token, policies=data['result'], error=dataa['result']) 
    
    else:
        
        response = requests.get(f'{BACKEND_URL}get_my_polis', headers={
            "Authorization": request.cookies.get('token')
        })
        
        data = response.json()
        
        return render_template('make_new_inshurance.html', token=token, policies=data['result'])

@app.route('/get_my_inshurance', methods=['GET'])
def get_my_inshurance():
    token = True if request.cookies.get('token') else False
    
    response = requests.get(f'{BACKEND_URL}get_my_insurance', headers={
        "Authorization": request.cookies.get('token')
    })
    
    data = response.json()
    
    if response.status_code == 200:
        return render_template('get_my_inshurance.html', token=token, inshurance=data["result"])
    else:
        error = data['result']
        return render_template('connection_error.html', token=token, error=error)
    

@app.route('/agent/all_policy', methods=['GET'])
def all_policy():
    token = True if request.cookies.get('token') else False
    
    response = requests.get(f'{BACKEND_URL}all_policy', headers={
        "Authorization": request.cookies.get('token')
    })
    
    data = response.json()
    
    return data


@app.route('/agent/policy_to_approve', methods=['GET'])
def policy_to_approve():
    token = True if request.cookies.get('token') else False
    
    response = requests.get(f'{BACKEND_URL}policy_to_approve', headers={
        "Authorization": request.cookies.get('token')
    })
    
    data = response.json()
    
    return data


@app.route('/approve_polis', methods=['POST'])
def approve_polis():
    policy_id = request.form.get('policy_id')
    response = requests.post(f'{BACKEND_URL}/approve_polis', headers={
        "Authorization": request.cookies.get('token')
    }, json={
        "policy_id": policy_id
    })
    return redirect('/policy_to_approve')


@app.errorhandler(404)
def not_found(e):
    token = True if request.cookies.get('token') else False
    return render_template('not_found.html', token=token)


if __name__ == "__main__":
    app.run(debug=True, port=3000)
    