from flask import Flask, render_template, request, redirect, session
import sqlite3 as sql
import bcrypt
from db import *


def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            # encoding user password
            userBytes = password.encode('utf-8')
            # connection to the on-disk database
            con = get_db_connection()
            cur = con.cursor()
            user = cur.execute("SELECT password, user_id, name FROM users where email=?",(email,)).fetchone()
            con.close()
            print("usuario",user)
            if user is None:
                msg = "Email not registered"
                return render_template('result.html', msg = msg)
            else:
                user_password = user[0]
                correct_password = bcrypt.checkpw(userBytes, user_password)
                if correct_password:
                    session["user"] = user
                    return redirect("/home")
                else:
                    msg = "Wrong password"
                    return render_template('result.html', msg = msg) 
        except BaseException as e:
            print(e)
            con.rollback()
            msg = "error in Login opertation"
            return render_template('result.html', msg = msg)


def register():
    if request.method == 'GET':
        return render_template('/user/register.html')
    else:
        try:
            name = request.form['name']
            lastname1 = request.form['last-name-1']
            lastname2 = request.form['last-name-2']
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']
        
            # converting password to array of bytes
            bytes = password.encode('utf-8')
            # generating the salt
            salt = bcrypt.gensalt()
            # Hashing the password
            hash = bcrypt.hashpw(bytes, salt)
           
            # connection to the on-disk database
            con = get_db_connection()
            cur = con.cursor()
            cur.execute("INSERT INTO users(name, lastname1, lastname2, email, username, password) VALUES (?,?,?,?,?,?)", 
                (name, lastname1, lastname2, email, username, hash))
            con.commit()
            print("User successfully added")
            user = cur.execute("SELECT password, user_id, name FROM users where email=?",(email,)).fetchone()
            session["user"] = user
            con.close()
            return redirect('/home')
        except BaseException as e:
            print(e)
            con.rollback()
            msg = "error in add user"
            return render_template('result.html', msg = msg)


def get_profile():
    print(session.get('user'))
    if session.get('user'):
        try:
            user_id = session["user"][1]
            # connection to the on-disk database
            con = get_db_connection()
            cur = con.cursor()
            user_data = cur.execute("SELECT * FROM users where user_id=?",(user_id,)).fetchone()
            user = {}
            user['user_id'] = user_data[0]
            user['name'] = user_data[1]
            user['lastname1'] = user_data[2]
            user['lastname2'] = user_data[3]
            user['email'] = user_data[4]
            user['username'] = user_data[5]
            user['password']= user_data[6]
            return render_template('/user/profile.html', user = user)        
        except BaseException as e:
            print(e)
            con.rollback()
            msg = "Error while getting user"
            return render_template('result.html', msg = msg) 
    return redirect("/")


def delete():
    if request.method == 'POST':
        try:
            user_id = request.form['id-delete']
            # connection to the on-disk database
            con = get_db_connection()
            cur = con.cursor()
            cur.execute("DELETE FROM users WHERE user_id=?",(user_id,))
            con.commit()
            print("User successfully deleted")
            con.close()
            session['user'] = None
            return redirect('/home')
        except BaseException as e:
            print(e)
            con.rollback()
            msg = "Error while deleting user"
            return render_template('result.html', msg = msg)


def update():
    if request.method == 'POST':
        try:
            user_id = request.form['userid']
            name = request.form['name']
            lastname1 = request.form['lastname1']
            lastname2 = request.form['lastname2']
            username = request.form['username']
            password = request.form['password']

            # converting password to array of bytes
            bytes = password.encode('utf-8')
            # generating the salt
            salt = bcrypt.gensalt()
            # Hashing the password
            hash = bcrypt.hashpw(bytes, salt)
            

            # connection to the on-disk database
            con = get_db_connection()
            cur = con.cursor()
            cur.execute("UPDATE users SET name=?, lastname1=?, lastname2=?, username=?, password=? WHERE user_id=?",(name, lastname1, lastname2,username, hash, user_id,))
            con.commit()
            print("User successfully updated")
            con.close()
            session['user'] = (password,user_id,name)
            return redirect('/home') 
        except BaseException as e:
            print(e)
            con.rollback()
            msg = "Error while getting user"
            return render_template('result.html', msg = msg) 



