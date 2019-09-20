from app.models import User, Cart, Product
from flask import flash, redirect, url_for, session
import hashlib
from app import db

fiction = "fiction"
novels = "novels"
regular = "regular"


def getAllProducts():
    itemData = Product.query.all()
    return itemData


def massageItemData(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(6):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans

def extractAndPersistKartDetailsUsingSubquery(productId, quantity):
    number_of_items = quantity
    userId = session['user_id']

    subqury = Cart.query.filter(Cart.productid == productId).subquery()
    qry = db.session.query(Cart.quantity).select_entity_from(subqury).all()

    if len(qry) == 0:
        cart = Cart(userid=userId, productid=productId, quantity=number_of_items)
    else:
        cart = Cart(userid=userId, productid=productId, quantity=(qry[0][0] + number_of_items))

    db.session.merge(cart)
    db.session.flush()
    db.session.commit()


def getusercartdetails():
    # userId = User.query.with_entities(User.userid).filter(User.email == session['email']).first()

    productsincart = Product.query.join(Cart, Product.productid == Cart.productid) \
        .add_columns(Product.productid, Product.product_name, Product.regular_price, Cart.quantity) \
        .filter(Cart.productid == Product.productid)
    
    totalsum = 0
    for row in productsincart:
        totalsum += (row[3] * row[4])
    return (productsincart, totalsum)


# There are three kinds of books: 
# regular, fiction, and novels. 
# Regular Rs. 1.5.
# Fiction Rs. 3.
# Novels Rs. 1.5.

# Removes products from cart when user clicks remove
def removeProductFromCart(productId):
    kwargs = {'productid': productId}
    cart = Cart.query.filter_by(**kwargs).first_or_404()
    if productId is not None:
        db.session.delete(cart)
        db.session.commit()
        flash("Product has been removed from cart !!")
    else:
        flash("failed to remove Product cart please try again !!")
    return redirect(url_for('cart'))


def extractAndPersistUserDataFromForm(request):
    password = request.form['password']
    email = request.form['email']
    firstName = request.form['firstName']
    lastName = request.form['lastName']

    user = User(fname=firstName, lname=lastName, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.flush()
    db.session.commit()
    return "Registered Successfully"


