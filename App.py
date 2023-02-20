from flask import Flask, render_template, request, redirect, session
import sqlite3 as sql
import bcrypt


app = Flask(__name__)
db_file = 'delivery.db'

app.secret_key = 'any random string'

def create_schema_users():
    with sql.connect(db_file) as con:
        cur = con.cursor()
        try:
            cur.execute( """
                        CREATE TABLE users(user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, lastname1 TEXT NOT NULL, 
                        lastname2 TEXT NOT NULL, email TEXT NOT NULL UNIQUE, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)
                        """)
            con.commit()
        except sql.OperationalError:
            pass

def create_schema_packages():
    with sql.connect(db_file) as con:
        cur = con.cursor()
        try:
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE packages(package_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, lat INTEGER, lon INTEGER, price FLOAT, user_id TEXT NOT NULL, FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE )")
            con.commit()
        except sql.OperationalError:
            pass


@app.route('/enterpackage')
def new_package():
   return render_template('package.html')

@app.route('/addpackage', methods = ['POST', 'GET'])
def add_package():
    if session.get("user"):
        if request.method == 'POST':
            try:
                lat = request.form['lat']
                lon = request.form['lon']
                price = request.form['price']
                user_id = session["user"][1]
            
                # connection to the on-disk database
                with sql.connect(db_file) as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO packages(lat,lon,price,user_id) VALUES (?,?,?,?)", (lat, lon, price, user_id,))
                    con.commit()
                    print("Package successfully added")
                    return redirect("/home")

            except BaseException as e:
                print(e)
                con.rollback()
                msg = "error in insert operation"
                return render_template('result.html', msg = msg)
           
               

@app.route('/packages')
def get_packages():
    with sql.connect(db_file) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM packages")
        result = cur.fetchall()
        con.commit()
    return render_template('result.html', msg = str(result))

@app.route("/")
def get_index():
    return render_template('index.html')


@app.route("/login", methods = ['POST', 'GET'])
def login_user():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            # encoding user password
            userBytes = password.encode('utf-8')
            # connection to the on-disk database
            with sql.connect(db_file) as con:
                cur = con.cursor()
                cur.execute("SELECT password, user_id, name FROM users where email=?",(email,))
                user = cur.fetchone()
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



@app.route("/home")
def get_home():
    if session.get("user"):
        with sql.connect(db_file) as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM packages where user_id=? ", (session["user"][1],))
            packages = cur.fetchall()
            con.commit()

        return render_template('home.html', user = session["user"], packages = packages)
    return redirect("/")
    

@app.route("/register")
def get_register():
    return render_template('register.html')

@app.route('/adduser', methods = ['POST', 'GET'])
def add_user():
    if request.method == 'POST':
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
            with sql.connect(db_file) as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users(name, lastname1, lastname2, email, username, password) VALUES (?,?,?,?,?,?)", 
                (name, lastname1, lastname2, email, username, hash))
                con.commit()
                print("User successfully added")
                cur = con.cursor()
                cur.execute("SELECT password, user_id, name FROM users where email=?",(email,))
                user = cur.fetchone()
                session["user"] = user
                
            return redirect('/home')
        except BaseException as e:
            print(e)
            con.rollback()
            msg = "error in add user"
            return render_template('result.html', msg = msg)


@app.route('/users')
def get_users():
    with sql.connect(db_file) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users")
        result = cur.fetchall()
        con.commit()
    return render_template('result.html', msg = str(result))

@app.route("/logout")
def logout():
    session["user"] = None
    return redirect("/")

@app.route("/deletepackage",methods = ['POST', 'GET'] )
def delete_package():
    if request.method == 'POST':
        try:
            package_id = request.form["id-delete"]
            
            # connection to the on-disk database
            with sql.connect(db_file) as con:
                cur = con.cursor()
                cur.execute("DELETE FROM packages WHERE package_id=?",(package_id,))
                con.commit()
                print("Package successfully deleted")
                return redirect('/home') 
        except BaseException as e:
            print(e)
            con.rollback()
            msg = "Error while deleting package"
            return render_template('result.html', msg = msg)


        
@app.route("/updatepackage", methods = ['POST', 'GET'])
def update_package():
    if request.method == 'POST':
        package = request.form
    return render_template('updatepackage.html', package = package)

 
@app.route("/packageupdated", methods = ['POST', 'GET'])
def package_updated():
    if request.method == 'POST':
        try:
                id_package = request.form['id-update']
                lat = request.form['lat']
                lon = request.form['lon']
                price = request.form['price']

                # connection to the on-disk database
                with sql.connect(db_file) as con:
                    cur = con.cursor()
                    cur.execute("UPDATE packages SET lat=?, lon=?, price=? WHERE package_id=?",(lat, lon, price,id_package))
                    con.commit()
                    print("Package successfully updated")
                return redirect('/home') 
        except BaseException as e:
            print(e)
            con.rollback()
            msg = "Error while updating package"
            return render_template('result.html', msg = msg)

@app.route("/profile")
def get_profile():
    if session.get('user'):
        try:
            user_id = session["user"][1]
            # connection to the on-disk database
            with sql.connect(db_file) as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM users where user_id=?",(user_id,))
                user_data = cur.fetchone()
                user = {}
                user['user_id'] = user_data[0]
                user['name'] = user_data[1]
                user['lastname1'] = user_data[2]
                user['lastname2'] = user_data[3]
                user['email'] = user_data[4]
                user['username'] = user_data[5]
                user['password']= user_data[6]
                

                return render_template('profile.html', user = user)        
        except BaseException as e:
            print(e)
            con.rollback()
            msg = "Error while getting user"
            return render_template('result.html', msg = msg) 
    return redirect("/")

@app.route("/updateuser", methods = ['POST', 'GET'])
def update_user():
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
            with sql.connect(db_file) as con:
                cur = con.cursor()
                cur.execute("UPDATE users SET name=?, lastname1=?, lastname2=?, username=?, password=? WHERE user_id=?",(name, lastname1, lastname2,username, hash, user_id,))
                con.commit()
                print("User successfully updated")
                return redirect('/home') 
        except BaseException as e:
            print(e)
            con.rollback()
            msg = "Error while getting user"
            return render_template('result.html', msg = msg) 





if __name__ == '__main__':
    create_schema_users()
    create_schema_packages()
    app.run(port=8000, debug = True)
