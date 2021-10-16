from flask import Flask, render_template, request, redirect, make_response, flash, abort
import json

app = Flask(__name__)

app.secret_key = "dev"
memos: dict = {}

def parse_cookie(data: str = None) -> dict:
    if not data:
        return {}
    pairs = data.split(":")
    kvpairs = [p.split("=") for p in pairs]
    return dict(kvpairs)

@app.route('/')
def read_index():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def do_login():
    form_data = request.form

    if form_data.get('username') == 'steve' and form_data.get('password') == 'P@$$word':
        resp = make_response(redirect('/admin'))
        resp.set_cookie('login', "username=steve:admin=0")
        return resp
    
    flash('Incorrect username or password.')
    return redirect('/')

@app.route('/admin')
def read_admin_panel():
    cookie = parse_cookie(request.cookies.get("login"))
    
    username = cookie.get('username')
    is_admin = cookie.get('admin') == '1'

    flag: str
    with open("flag.txt") as fd:
        flag = fd.read()

    return render_template("admin.html", username=username, admin=is_admin, flag=flag)

@app.route('/memo/<id>')
def read_memo(id: str):
    if memo := memos.get(id):
        return render_template("memo.html", memo=memo)
    
    abort(404)

def create_app():
    global memos

    with open("memos.json") as fd:
        memos = json.loads(fd.read())
    
    return app

if __name__ == "__main__":
    create_app().run()
