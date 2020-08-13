from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import session
from paho_mqtt.src.paho.mqtt import publish
from paho_mqtt.src.paho.mqtt import client
from config import CFG
import json
from threading import Timer


app = Flask(__name__, static_folder='static')
app.secret_key = CFG['secret_key']


@app.route('/auth', methods = ['GET', 'POST'])
def authPage():
    if 'login' in session:
        return redirect('/page2')
    
    login = request.values.get('login')
    password = request.values.get('password')
    
    d = {}
    
    if login != None and password != None:
        if login in CFG['users']:
            if CFG['users'][login]['password'] == password:
                session['login'] = login
                print('User {} logged in'.format(login))
                return redirect('/page2')
            else:
                d['errorMessage'] = 'Incorrect login or/and password 1';
        else:
            d['errorMessage'] = 'Incorrect login or/and password 2';
    return render_template('auth.html', **d)


@app.route('/logout')
def logoutPage():
    if 'login' in session:
        print('User {} logged out'.format(session['login']))
        session.pop('login')
        
    return redirect('/auth')


@app.route('/')
def func():
    return render_template('mainPage.html')


@app.route('/page1')
def func2():
    return render_template('developersInfo.html')


@app.route('/page2', methods=['GET', 'POST'])
def page2():
    if 'login' not in session:
        return redirect('/auth')
    
    d = {}
    current_key = request.values.get('current_password')
    
    with open("static/data.json", "r") as file:
        buff = file.read() 
    
    obj = json.loads(buff)
    pwd = obj['password']
    
    enter_message = False
    
    if pwd == current_key:
        enter_message = True
    
    
    if pwd != current_key and current_key != None:
        d['errorMessage'] = 'Incorrect password';
        msgs = [{'topic': "mqtt/paho/enter", 'payload': enter_message}
                ]
        publish.multiple(msgs, hostname="localhost")
        return render_template('appPage.html', **d)
    
    if enter_message == True:
        d['errorMessage'] = 'Available';
    
    new_key = request.values.get('new_password')
    if new_key != None and new_key != current_key and enter_message == True:
        with open("static/data.json", "w") as file:
            obj_ = {"password" : str(new_key)}
            file.write(json.dumps(obj_, indent=2))
            enter_message = False
            
    else: new_key = False

    if current_key == None:
        return render_template('appPage.html')

    msgs = [{'topic': "mqtt/paho/enter", 'payload': enter_message},
           {'topic': "mqtt/paho/change", 'payload': new_key}
        ]
    publish.multiple(msgs, hostname="localhost")


    return render_template('appPage.html', **d)


@app.route('/api/getData')
def apiGetData():
    if 'login' not in session:
        return redirect('/auth')

    global mess
    data = {'message': mess}
    return {'data': data}


@app.route('/page3')
def index():
    if 'login' not in session:
        return redirect('/auth')
        
    return render_template('statusPage.html')


def on_connect(client, userdata, flags, rc):  
    print("Connected with result code: %s" % rc)
    client.subscribe("mqtt/paho/enter")

def on_message(client, userdata, msg):  
    print("%s: %s" % (msg.topic, msg.payload))
    global mess 
    mess = msg.payload.decode()


def main2():  
    subscriber = client.Client()
    subscriber.on_connect = on_connect
    subscriber.on_message = on_message


    print(subscriber.connect("localhost", 1883))
    Timer(1, subscriber.loop_forever).start()


    
main2()
global mess
mess = 'False'
if __name__ == '__main__':

    app.run(host='0.0.0.0', port = CFG['port'],debug = CFG['debug'])
