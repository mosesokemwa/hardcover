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
        cart = Cart(userid=userId, productid=productId,
                    quantity=number_of_items)
    else:
        cart = Cart(userid=userId, productid=productId,
                    quantity=(qry[0][0] + number_of_items))

    db.session.merge(cart)
    db.session.flush()
    db.session.commit()


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


def calculate_based_on_category(category, days):
    """
    Regular books:
    - First 2 days = Rs 1 per day and 1.5 Rs there after. Minimum changes will be considered as Rs 2 if days rented is less than 2 days. 
    Novel minimum charges are introduced as 4.5 Rs if days rented is less than 3 days.
    """
    if category == regular:
        if days >= 2:
            inital = 2 * 1
            after = days - 2 * 1.5
            pricing = inital + after
            return pricing
    elif category == novels:
        if days <= 3:
            return 4.5 * days
        else:
            return days * 1.5
    elif category == fiction:
        return days * 3


def getusercartdetails():
    productsincart = Product.query.join(Cart, Product.productid == Cart.productid) \
        .add_columns(Product.productid, Product.product_name, Product.regular_price, Cart.quantity, Product.category) \
        .filter(Cart.productid == Product.productid)
    
    product_pricing = []
    totalsum = 0
    for row in productsincart:
        # returns category item prices
        product_pricing.append(calculate_based_on_category(row[5], row[4]))

        # returns cart items prices
        totalsum +=calculate_based_on_category(row[5], row[4])
    return (productsincart, totalsum, product_pricing)

