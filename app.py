from flask import Flask, render_template, request, redirect, session
import os
import bcrypt
import psycopg2
from models import users
from datetime import datetime
from flask_socketio import SocketIO,send, emit 
# import webbrowser

app = Flask(__name__)
app.config["SECRET_KEY"] = "My secret key"
socketio = SocketIO(app)

@app.route('/')
def index():
    user_id= session.get('user_id','')
    if user_id=='':
        return render_template('homepage.html')
    elif user_id==None:
        return render_template('homepage.html')

    else:
        name =users.id_to_name(user_id)
        return render_template('homepage.html',name=name)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/api/signup', methods=['POST'])
def api_signup():
    email = request.form.get('email')
    if '@' and '.' not in email:
        return render_template('signup.html', invalid=True) 
    elif users.email_in_db(email):
        return render_template('signup.html', invalid=True) 
    else:
        name = request.form.get('firstname')
        password =request.form.get('password')
        hashedpassword =bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
        users.new_user(name,email,hashedpassword)
        # app.config["SECRET_KEY"] = "My secret key"
        return redirect('http://127.0.0.1:5000/')

@app.route('/login')
def login():
    chat=False
    return render_template('login.html')

@app.route('/api/login', methods=['post'])
def api_login():
    # return render_template('login.html')
    email= request.form.get('email')
    password = request.form.get('password')
    #user = hashpasssword
    user_info = users.check_user(email)
    isValidPassword = bcrypt.checkpw(password.encode(), user_info[1].encode())
    if isValidPassword:
        session['user_id']= user_info[0]
        return redirect('/')
    else:
        return redirect('/login')
    # return f"{user_id}"
    
@app.route('/logout')
def logout():
    session['user_id'] = None
    return redirect('/')

@app.route('/search')
def search():
    user_id= session.get('user_id','')
    # get previous chats here
    friends =users.userid_to_friends(user_id)
    # return f'{friends}'
    if user_id:
        return render_template('usersearch.html',friends=friends)
    else:
        return redirect('/login')    

@app.route('/api/search',methods=['POST'])
def user_search():
    user_id= session.get('user_id','')
    other_email=request.form.get('email')
    users.is_valid_email(other_email)[0]
    if users.is_valid_email(other_email)[0]:
        #redirect('/')
        receiver =users.is_valid_email(other_email)[1]
        session['receiver']=receiver
        return redirect('/chatroom')
    else:
        return redirect('/search')

@app.route('/chatroom')
def chatroom():
    sender = session.get('user_id')
    receiver = session.get('receiver')
    messages =users.receive_messages(sender,receiver)
    # return f'{messages}'
    sender_name= users.id_to_name(sender)
    receiver_name= users.id_to_name(receiver)
    return render_template('chatroom.html', messages=messages,sender=sender,receiver=receiver,sender_name=sender_name,receiver_name=receiver_name)

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data["message"])
    emit('new-message', data, broadcast=True)


@app.route('/api/chatroom',methods=['POST'])
def chatroom_api():
    sender = session.get('user_id')
    receiver = session.get('receiver')
    message = request.form.get('textmessage')
    users.send_message(message,sender,receiver)
    return redirect('/chatroom')

if __name__ == '__main__':
    socketio.run(app, debug=True, port=os.getenv("PORT", default=5000))
    # app.run())


