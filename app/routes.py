from app.models import User
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.service import getAllProducts, massageItemData, extractAndPersistKartDetailsUsingSubquery, getusercartdetails


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user)
        # if user is None or not user.check_password(form.password.data):
        #     flash('Invalid username or password')
        #     return redirect(url_for('login'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    fname=form.fname.data, lname=form.lname.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/store")
@login_required
def store():
    # loggedIn, firstName, productCountinKartForGivenUser = getLoginUserDetails()
    allProductDetails = getAllProducts()
    allProductsMassagedDetails = massageItemData(allProductDetails)

    return render_template('home.html', itemData=allProductsMassagedDetails)


@app.route("/productDescription")
@login_required
def productDescription():
    productid = request.args.get('productId')
    productDetailsByProductId = getProductDetails(productid)
    return render_template("productDescription.html", data=productDetailsByProductId)


@app.route("/addToCart")
def addToCart():
    productId = int(request.args.get('productId'))
    quantity = int(request.args.get('quantity'))

    # Using Flask-SQLAlchmy SubQuery
    extractAndPersistKartDetailsUsingSubquery(productId, quantity)

    # Using Flask-SQLAlchmy normal query
    # extractAndPersistKartDetailsUsingkwargs(productId)
    flash('Item successfully added to cart !!', 'success')
    return redirect(url_for('store'))


@app.route("/cart")
@login_required
def cart():
    cartdetails, totalsum, tax = getusercartdetails()
    return render_template("cart.html", cartData=cartdetails,
                           totalsum=totalsum, tax=tax)


@app.route("/removeFromCart")
def deletecItemFromCart():
    productId = int(request.args.get('productId'))
    removeProductFromCart(productId)
    return redirect(url_for('cart'))
