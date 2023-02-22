from flask import Flask, render_template, request, redirect, session
from db import *
from routes.user_bp import user_bp
from routes.package_bp import package_bp


app = Flask(__name__)

app.secret_key = 'any random string'

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(package_bp, url_prefix='/package')


@app.route("/")
def get_index():
    return render_template('index.html')

@app.route("/home")
def get_home():
    if session.get("user"):
        con = get_db_connection()
        cur = con.cursor()
        packages = cur.execute("SELECT * FROM packages where user_id=? ", (session["user"][1],)).fetchall()
        return render_template('user/home.html', user = session["user"], packages = packages)
    return redirect("/")

@app.route("/logout")
def logout():
    session["user"] = None
    return redirect("/")

######## se tienen que borrar
@app.route('/users')
def get_users():
    with sql.connect(db_file) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users")
        result = cur.fetchall()
        con.commit()
    return render_template('result.html', msg = str(result))

@app.route('/packages')
def get_packages():
    with sql.connect(db_file) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM packages")
        result = cur.fetchall()
        con.commit()
    return render_template('result.html', msg = str(result))


if __name__ == '__main__':
    create_schema()
    app.run(port=8000, debug = True)