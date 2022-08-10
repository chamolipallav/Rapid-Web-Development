from . import db

class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False, default = 'defaultgenre.jpg')
    books = db.relationship('Book', backref='Genre', cascade="all, delete-orphan")

    def __repr__(self):
        str = "Id: {}, Name: {}, Description: {}, Image: {} \n"
        str = str.format(self.id, self.name, self.description, self.image)
        return str

orderdetails = db.Table('orderdetails',
db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), nullable=False),
db.Column('book_id', db.Integer, db.ForeignKey('books.id'), nullable=False),
db.PrimaryKeyConstraint('order_id', 'book_id'))


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False)
    price = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    ISBN = db.Column(db.Integer, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))

    def __repr__(self):
        str = "Id: {}, Name: {}, Description: {}, Image: {}, Price: {}, genres: {}, ISBN: {} \n"
        str = str.format(self.id, self.name, self.description,
                         self.image, self.price, self.genre_id, self.ISBN)
        return str


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    firstname = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    totalcost = db.Column(db.Float)
    date = db.Column(db.DateTime)
    books = db.relationship("Book", secondary = orderdetails, backref="orders") 
    

    def __repr__(self):
        str = "id: {}, status: {}, Firstname: {}, Surname: {}, Email: {}, Phone: {}, Date: {}, Books: {}, Total Cost: {}\n"
        str = str.format(self.id, self.status, self.firstname, self.surname,
                         self.email, self.phone, self.date, self.books, self.totalcost)
        return str
