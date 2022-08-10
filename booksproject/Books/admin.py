from flask import Blueprint
from . import db
from . models import Genre, Book, Order
import datetime

bp = Blueprint('admin', __name__, url_prefix='/admin/')

#seed data into database
@bp.route('/dbseed/')
def dbseed():
    g1 = Genre(name='Fiction', image='fiction.jpg', description='Fiction')
    g2 = Genre(name='Scifi', image='scifi.jpg', description='Scifi')
    g3 = Genre(name='Comedy', image='comedy.jpg', description='Comedy')

    try:
        db.session.add(g1)
        db.session.add(g2)
        db.session.add(g3)
        db.session.commit()
    except:
        return 'There is an issue adding Genres in DATABASE'

    
    b1 = Book(genre_id=g1.id, image='fiction1.jpg', price=45.56, date=datetime.datetime(2020,6,1), ISBN = 112311, name='1984 by GEORGE ORWELL', description='Fiction')

    b2 = Book(genre_id=g1.id, image='fiction2.jpg', price=145.56, date=datetime.datetime(2020,6,12), ISBN = 11212, name='ALL THE LIGHT WE CANNOT SEE by ANTHONY DOERR', description='Fiction')

    b3 = Book(genre_id=g2.id, image='scifi1.jpg', price=100.56, date=datetime.datetime(2020,6,14), ISBN = 544343, name='THE MARTIANS by ANDY WEIR', description='Scifi')

    b4 = Book(genre_id=g2.id, image='scifi2.jpg', price=105.56, date=datetime.datetime(2020,6,16), ISBN = 54533, name='THE WAR OF THE WORLDS by H. G WELLs', description='Scifi')
    
    b5 = Book(genre_id=g3.id, image='comedy1.jpg', price=120.56, date=datetime.datetime(2020,6,17), ISBN = 23423, name='BORN A CRIME by TREVOR NOAH', description='Comedy')

    b6 = Book(genre_id=g3.id, image='comedy2.jpg', price=173.56, date=datetime.datetime(2020,6,19), ISBN = 43435, name='I FEEL BAD ABOUT MY NECK by NORA EPHRON', description='Comedy')


    try:
        db.session.add(b1)
        db.session.add(b2)
        db.session.add(b3)
        db.session.add(b4)
        db.session.add(b5)
        db.session.add(b6)
        db.session.commit()
    except:
        return 'There is an issue adding Books in DATABASE'

    return 'DATA LOADED'
