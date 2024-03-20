import unicodedata
from . import db

class Property(db.Model):
    
    __tablename__ = 'property'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(200))
    rooms = db.Column(db.String(100))
    bathrooms = db.Column(db.String(100))
    price = db.Column(db.Numeric(10))
    type = db.Column(db.String(100))
    location = db.Column(db.String(100))
    photo = db.Column(db.String(100))

    def __init__(self, title, description, rooms, bathrooms, price, type, location, photo):
       self.title = title
       self.description = description
       self.rooms = rooms
       self.bathrooms = bathrooms
       self.price = price
       self.type = type
       self.location = location
       self.photo = photo

    def get_id(self):
        try:
            return unicodedata(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<Property %r>' % (self.title)
