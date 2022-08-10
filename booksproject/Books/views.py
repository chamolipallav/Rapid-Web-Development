from flask import Blueprint, render_template, url_for, session, request, flash, redirect
from .models import Genre, Book, Order
from datetime import datetime
from .forms import CheckoutForm
from . import db



bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    genres = Genre.query.order_by(Genre.name).all()
    return render_template('index.html', genres = genres)


@bp.route('/books/<int:genreid>/')
def genre_books(genreid):
    books = Book.query.filter(Book.genre_id == genreid)
    return render_template('genre_books.html', books = books)

@bp.route('/books')
def search():
    search = request.args.get('search')
    search = '%{}%'.format(search)
    books = Book.query.filter(Book.description.like(search)).all()
    return render_template('genre_books.html', books = books)


#for order
@bp.route('/order/', methods=['POST', 'GET'])
def order():
    
    book_id = request.values.get('book_id')

    # retrive order if there is one
    if 'order_id' in session.keys():
        order = Order.query.get(session['order_id'])

    else:
        # there is no order
        order = None

    # create new order if needed
    if order is None:
        order = Order(status = False, firstname='', surname='', email='',phone='', totalcost=0, date=datetime.now())
        try:
            db.session.add(order)
            db.session.commit()
            session['order_id'] = order.id
        except:
            print("failed at creating new order")
            order = None

    #calculate total price
    totalprice =0 
    if order is not None:
        for book in order.books:
            totalprice = totalprice + book.price
    # adding any more items 
    if book_id is not None and order is not None:
        book = Book.query.get(book_id)
        if book not in order.books:
            try:
                order.books.append(book)
                db.session.commit()
            except:
                return "there was issue adding th item to basket"
            return redirect(url_for('main.order'))
        else:
            flash('itme already in basket')
            return redirect(url_for('main.order'))
    
    return render_template('order.html', order = order, totalprice = totalprice)

#for delete order
@bp.route('/deleteorder/')
def deleteorder():
    if 'order_id' in session:
        del session['order_id']
        flash('All items deleted')
    return redirect(url_for('main.index'))
    
#for delete single item
@bp.route('/deleteorderitem/', methods=['POST'])
def deleteorderitem():
    id = request.form['id']
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])
        book_to_delete = Book.query.get(id)
        try:
            order.books.remove(book_to_delete)
            db.session.commit()
            return redirect(url_for('main.order'))
        except:
            return 'Problem deleting item from order'
    return redirect(url_for('main.order'))

#for checkout
@bp.route('/checkout/', methods=['POST', 'GET'])
def checkout():
    form = CheckoutForm()
    if 'order_id' in session:
        order = Order.query.get_or_404(session['order_id'])

        if form.validate_on_submit():
            order.status = True
            order.firstname = form.firstname.data
            order.surname = form.surname.data
            order.email = form.email.data
            order.phone = form.phone.data
            totalcost = 0
            for book in order.books:
                totalcost = totalcost + book.price
            order.totalcost = totalcost
            order.date = datetime.now()
            try:
                db.session.commit()
                del session['order_id']
                flash('thank you for providing details ! we will contact you shortly')
                return redirect(url_for('main.index'))
            except:
                return ' there was an issue completing your order'
    return render_template('checkout.html', form = form)

