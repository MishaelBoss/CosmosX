from flask import Flask, render_template, request, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
HOST = '0.0.0.0'
PORT = 5000
server_address = '127.0.0.1:5000'
db = SQLAlchemy(app)

class Tickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    intro = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return '<Tickets %r>' % self.id
    
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    intro = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id
    
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    dateR = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Users %r>' % self.id
    

@app.route('/')
@app.route('/home')
def index():
    return render_template("Index.html")

@app.route('/About')
def about():
    return render_template("About.html")

@app.route('/register', methods=['POST', 'GET'])
def register():
    name = request.cookies.get('user')
    if request.method == "POST":
        login = request.form['login']
        email = request.form['email']
        passw1 = request.form['password']
        password = hashlib.md5(passw1.encode("utf-8")).hexdigest()
        exists = db.session.query(Users.id).filter_by(login=login).first() is not None or db.session.query(Users.id).filter_by(email=email).first() is not None
        if not exists:
            user = Users(login=login, password=password, email=email)
            try:
                db.session.add(user)
                db.session.commit()
                resp = make_response(redirect("/"))
                resp.set_cookie('user', user.login)
                return resp
            except Exception as ex:
                print(ex)
                return redirect("/register")
        else:
            return redirect("/register")
    else:
        return render_template("register.html")

@app.route('/login', methods=['POST', "GET"])
def login():
    name = request.cookies.get('user')
    if request.method == "POST":
        login = request.form['login']
        passw1 = request.form['password']
        password = hashlib.md5(passw1.encode("utf-8")).hexdigest()
        exists = db.session.query(Users.id).filter_by(login=login, password=password).first() is not None
        user = db.session.query(Users.login).filter_by(login=login, password=password).first()
        if exists:
            resp = make_response(redirect("/"))
            resp.set_cookie('user', user[0])
            return resp
        else:
            return redirect("/login")
    else:
        return render_template("login.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route('/Buy')
def Buy():
    return render_template("Buy.html")

@app.route('/video')
def Video():
    return render_template("video.html")

@app.route('/Admin')
def admin():
    return render_template("Admin-Index.html")

@app.route('/One_rocet')
def One_rocet():
    return render_template("The_first.html")

@app.route('/Russian_astronomers')
def Russian_astronomers():
    return render_template("Russian_astronomers.html")

@app.route('/The_most_famous_Soviet_cosmonauts')
def The_most_famous_Soviet_cosmonauts():
    return render_template("The_most_famous_Soviet_cosmonauts.html")


@app.route('/Statistics')
def Statistics():
    return render_template("Statistics.html")

@app.route('/tickets')
def tickets():
    ticket = Tickets.query.order_by(Tickets.date.desc()).all()
    return render_template("tickets.html", ticket=ticket)

@app.route('/tickets/<int:id>')
def products_detail_tickets(id):
    ticket = Tickets.query.get(id)
    return render_template("products_detail_tickets.html", ticket=ticket)

@app.route('/tickets/<int:id>/del')
def ticket_delete(id):
    ticket = Tickets.query.get_or_404(id)

    try:
        db.session.delete(ticket)
        db.session.commit()
        return redirect('/tickets')
    except:
        return "При удаление произошла ошибка"

@app.route('/Create-ticets', methods=['POST', 'GET'])
def Create_ticets():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        ticet = Tickets(title=title, intro=intro, text=text)

        try:
            db.session.add(ticet)
            db.session.commit()
            return redirect("/tickets")
        except:
            return "Ошибка"
    else:
        return render_template("Create-ticets.html")


@app.route('/products')
def products():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("products.html", articles=articles)

@app.route('/products/<int:id>')
def products_detail(id):
    article = Article.query.get(id)
    return render_template("products_detail.html", article=article)


@app.route('/products/<int:id>/del')
def products_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/products')
    except:
        return "При удаление ароизошла ошибка"
    
@app.route('/products/<int:id>/update', methods=['POST', 'GET'])
def products_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/products')
        except:
            return "Опа"
    else:
            return render_template("products_update.html", article=article)


@app.route('/Create-product', methods=['POST', 'GET'])
def Create_product():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/products')
        except:
            return "Опа"
    else:
            return render_template("Create-product.html")
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=True, host=HOST, port=PORT)