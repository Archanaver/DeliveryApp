from flask import Flask, render_template, request, redirect, session
import sqlite3 as sql
from db import *


def create():
    if session.get("user"):
        if request.method == 'POST':
            try:
                lat = request.form['lat']
                lon = request.form['lon']
                price = request.form['price']
                user_id = session["user"][1]
            
                # connection to the on-disk database
                con = get_db_connection()
                cur = con.cursor()
                cur.execute("INSERT INTO packages(lat,lon,price,user_id) VALUES (?,?,?,?)", (lat, lon, price, user_id,))
                con.commit()
                print("Package successfully added")
                con.close()
                return redirect("/home")

            except BaseException as e:
                print(e)
                con.rollback()
                msg = "error in insert operation"
                return render_template('result.html', msg = msg)
        else:
            return render_template('package/create.html')



def delete():
    if request.method == 'POST':
        try:
            package_id = request.form["id-delete"]
            # connection to the on-disk database
            con = get_db_connection()
            cur = con.cursor()
            cur.execute("DELETE FROM packages WHERE package_id=?",(package_id,))
            con.commit()
            print("Package successfully deleted")
            con.close()
            return redirect('/home') 
        except BaseException as e:
            print(e)
            con.rollback()
            msg = "Error while deleting package"
            return render_template('result.html', msg = msg)

def get_update_form():
    if request.method == 'POST':
        package = request.form
    return render_template('/package/updateform.html', package = package)


def update():
    if request.method == 'POST':
        try:
                id_package = request.form['id-update']
                lat = request.form['lat']
                lon = request.form['lon']
                price = request.form['price']

                # connection to the on-disk database
                con = get_db_connection()
                cur = con.cursor()
                cur.execute("UPDATE packages SET lat=?, lon=?, price=? WHERE package_id=?",(lat, lon, price,id_package))
                con.commit()
                print("Package successfully updated")
                con.close()
                return redirect('/home') 
        except BaseException as e:
            print(e)
            con.rollback()
            msg = "Error while updating package"
            return render_template('result.html', msg = msg)