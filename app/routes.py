from app.models import User
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import application, db
from app.forms import LoginForm, RegistrationForm
from app.service import getAllProducts, massageItemData, extractAndPersistKartDetailsUsingSubquery, getusercartdetails, removeProductFromCart
# from flask_weasyprint import HTML, render_pdf


@application.route('/')
@application.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'moses'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Me '},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


@application.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('store'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None and user.check_password(form.password.data):
                user.authenticated = True
                login_user(user)
                flash('Thanks for logging in, {}'.format(current_user.email))
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('store')
                return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@application.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@application.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                user = User(email=form.email.data,
                            fname=form.fname.data, lname=form.lname.data)
                user.set_password(form.password.data)
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user)
                flash('Congratulations, you are now a registered user!')
                return redirect(url_for('store'))
            except IntegrityError:
                flash('Please use a different email address.')
                db.session.rollback()
    return render_template('register.html',  title='Register', form=form)


@application.route("/store")
@login_required
def store():
    # loggedIn, firstName, productCountinKartForGivenUser = getLoginUserDetails()
    allProductDetails = getAllProducts()
    allProductsMassagedDetails = massageItemData(allProductDetails)

    return render_template('home.html', itemData=allProductsMassagedDetails)


@application.route("/addToCart", methods=['GET', 'POST'])
@login_required
def addToCart():
    productId = int(request.args.get('productId'))
    quantity = int(request.args.get('quantity'))

    # Using Flask-SQLAlchmy SubQuery
    msg = extractAndPersistKartDetailsUsingSubquery(productId, quantity)

    # Using Flask-SQLAlchmy normal query
    # extractAndPersistKartDetailsUsingkwargs(productId)
    flash('Item successfully added to cart !!', 'success')
    flash(msg)
    return redirect(url_for('store'))


@application.route("/removeFromCart", methods=['GET', 'POST'])
@login_required
def deletecItemFromCart():
    productId = int(request.args.get('productId'))
    removeProductFromCart(productId)
    return redirect(url_for('cart'))


@application.route("/cart")
@login_required
def cart():
    cartdetails, totalsum, tax = getusercartdetails()
    return render_template("cart.html", cartData=cartdetails,
                           totalsum=totalsum, tax=tax)


@application.route("/pdf")
@login_required
def pdf():
    cartdetails, totalsum, tax = getusercartdetails()
    html = render_template("pdf.html", cartData=cartdetails, totalsum=totalsum, tax=tax)
    return render_pdf(HTML(string=html))

