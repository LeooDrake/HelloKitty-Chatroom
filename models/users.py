dbpassword ='fred1234'
from flask import Flask, render_template, request, redirect, session
import bcrypt
import os
import psycopg2
# import dotenv
from datetime import datetime
from flask_socketio import SocketIO,send, emit


def new_user(name,email,password):
    connection = psycopg2.connect(host=os.getenv("PGHOST"), user=os.getenv("PGUSER"), password=os.getenv("PGPASSWORD"), port=os.getenv("PGPORT"), dbname=os.getenv("PGDATABASE"))
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))    
    # connection=psycopg2.connect(user='postgres', port='5433', password=dbpassword, dbname='chat_room')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users(email,firstname,hashedpassword) VALUES(%s,%s,%s);',[email,name,password])
    connection.commit()
    connection.close()

def check_user(email): # returns id if email and password r correct
    # connection=psycopg2.connect(user='postgres', port='5433', password=dbpassword, dbname='chat_room')
    connection = psycopg2.connect(host=os.getenv("PGHOST"), user=os.getenv("PGUSER"), password=os.getenv("PGPASSWORD"), port=os.getenv("PGPORT"), dbname=os.getenv("PGDATABASE"))
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))        
    cursor = connection.cursor()

    cursor.execute("SELECT id,hashedpassword FROM users WHERE email=%s;",[email])
    results =cursor.fetchall()
    id_and_hashedpassword= results[0]
    connection.commit()
    connection.close()
    return id_and_hashedpassword

def id_to_email(id):
    # connection=psycopg2.connect(user='postgres', port='5433', password=dbpassword, dbname='chat_room')
    connection = psycopg2.connect(host=os.getenv("PGHOST"), user=os.getenv("PGUSER"), password=os.getenv("PGPASSWORD"), port=os.getenv("PGPORT"), dbname=os.getenv("PGDATABASE"))
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))        
    cursor = connection.cursor()
    cursor.execute("SELECT email FROM users WHERE id=%s;",[id]) 
    user=cursor.fetchone()   
    connection.close()
    return user[0]

def email_in_db(email):
    # connection=psycopg2.connect(user='postgres', port='5433', password=dbpassword, dbname='chat_room')
    connection = psycopg2.connect(host=os.getenv("PGHOST"), user=os.getenv("PGUSER"), password=os.getenv("PGPASSWORD"), port=os.getenv("PGPORT"), dbname=os.getenv("PGDATABASE"))
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))        
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s;",[email]) 
    user=cursor.fetchone()   
    connection.close()
    if user==None:    
        return False
    else:
        return True

def is_valid_email(email):
    # connection=psycopg2.connect(user='postgres', port='5433', password=dbpassword, dbname='chat_room')
    connection = psycopg2.connect(host=os.getenv("PGHOST"), user=os.getenv("PGUSER"), password=os.getenv("PGPASSWORD"), port=os.getenv("PGPORT"), dbname=os.getenv("PGDATABASE"))
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))        
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM users WHERE email=%s;",[email])
    results =cursor.fetchone()
    user_id= results[0]
    connection.commit()
    connection.close()
    if user_id:
        return True,user_id
    else:
        return False, None 

def send_message(message,sender,receiver):
    # connection=psycopg2.connect(user='postgres', port='5433', password=dbpassword, dbname='chat_room')
    connection = psycopg2.connect(host=os.getenv("PGHOST"), user=os.getenv("PGUSER"), password=os.getenv("PGPASSWORD"), port=os.getenv("PGPORT"), dbname=os.getenv("PGDATABASE"))
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))        
    cursor = connection.cursor()
    cursor.execute("INSERT INTO messages(content,attime,fromuser,touser) VALUES (%s,%s,%s,%s)",[message,datetime.now(),sender,receiver])

    connection.commit()
    connection.close()

def receive_messages(sender, receiver):
    # connection=psycopg2.connect(user='postgres', port='5433', password=dbpassword, dbname='chat_room')
    connection = psycopg2.connect(host=os.getenv("PGHOST"), user=os.getenv("PGUSER"), password=os.getenv("PGPASSWORD"), port=os.getenv("PGPORT"), dbname=os.getenv("PGDATABASE"))
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))        
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM messages WHERE (fromuser=%s OR fromuser=%s) AND (touser=%s OR touser=%s) ORDER BY attime ASC;",[sender,receiver,sender,receiver])
    messages =cursor.fetchall()
    message_list=[]
    for message in messages:
        message_list.append({'id':message[0],'content':message[1],'attime':message[2],'fromuser':message[3],'touser':message[4]})
    connection.commit()
    connection.close()
    return message_list

def id_to_name(id):
    # connection=psycopg2.connect(user='postgres', port='5433', password=dbpassword, dbname='chat_room')
    connection = psycopg2.connect(host=os.getenv("PGHOST"), user=os.getenv("PGUSER"), password=os.getenv("PGPASSWORD"), port=os.getenv("PGPORT"), dbname=os.getenv("PGDATABASE"))
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))        
    cursor = connection.cursor()
    cursor.execute('SELECT firstname FROM users WHERE id=%s',[id])
    name= cursor.fetchone()
    connection.commit()
    connection.close()
    return name[0]     

def deleteaccount_with_id(id):
    # connection=psycopg2.connect(user='postgres', port='5433', password=dbpassword, dbname='chat_room')
    connection = psycopg2.connect(host=os.getenv("PGHOST"), user=os.getenv("PGUSER"), password=os.getenv("PGPASSWORD"), port=os.getenv("PGPORT"), dbname=os.getenv("PGDATABASE"))
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))        
    cursor = connection.cursor()
    cursor.execute('DELETE FROM users WHERE id=%s;',[id])
    connection.commit()
    connection.close()

def updatepassword_with_id(password,id):
    # connection=psycopg2.connect(user='postgres', port='5433', password=dbpassword, dbname='chat_room')
    connection = psycopg2.connect(host=os.getenv("PGHOST"), user=os.getenv("PGUSER"), password=os.getenv("PGPASSWORD"), port=os.getenv("PGPORT"), dbname=os.getenv("PGDATABASE"))
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))        
    cursor = connection.cursor()
    cursor.execute('UPDATE users SET hashedpassword=%s WHERE id=%s;',[password,id])
    connection.commit()
    connection.close() 


def userid_to_friends(userid):
    # connection=psycopg2.connect(user='postgres', port='5433', password=dbpassword, dbname='chat_room')
    connection = psycopg2.connect(host=os.getenv("PGHOST"), user=os.getenv("PGUSER"), password=os.getenv("PGPASSWORD"), port=os.getenv("PGPORT"), dbname=os.getenv("PGDATABASE"))
    connection = psycopg2.connect(os.getenv("DATABASE_URL"))        
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT fromuser,touser FROM messages WHERE (fromuser=%s OR touser=%s);',[userid,userid])
    friends =cursor.fetchall()
    connection.commit()
    connection.close()
    friend_list=[]
    [friend_list.extend(list(i)) for i in friends]
    previous_friends=[]
    for j in friend_list:
        if j==userid:
            pass
        elif j in [i['id'] for i in previous_friends]: # idk why but proud of myself for this
            pass
        else:
            previous_friends.append({'name':id_to_name(j),'id':j, 'email':id_to_email(j)})
    return previous_friends