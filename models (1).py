from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from config import db, bcrypt
from datetime import datetime
from helpers import calculate_age

class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.Date)
    country = db.Column(db.String)
    state = db.Column(db.String)
    city = db.Column(db.String)
    street_address = db.Column(db.String)
    postal_code = db.Column(db.String)
    job_title = db.Column(db.String)
    bio = db.Column(db.String)
    phone_number = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    profile_image = db.Column(db.String)
    _password_hash = db.Column(db.String, nullable=False)

    rental_agreements = db.relationship('Agreement', back_populates="account", cascade="all, delete")
    messages = db.relationship("Message", back_populates="account", cascade="all, delete")
    favorites = db.relationship('Favorite', back_populates='account', cascade="all, delete")
    orders = db.relationship('Order', back_populates='account', cascade="all, delete")

    @property
    def age(self):
        return calculate_age(self.birth_date)
    
    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    def __repr__(self):
        return f"Account({self.first_name} {self.last_name})"


class ServiceProvider(db.Model):
    __tablename__ = "service_providers"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    date_of_birth = db.Column(db.Date)
    country = db.Column(db.String)
    state = db.Column(db.String)
    city = db.Column(db.String)
    street_address = db.Column(db.String)
    postal_code = db.Column(db.String)
    profession = db.Column(db.String)
    profile_image = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)

    equipment_list = db.relationship('Equipment', back_populates='provider', cascade="all, delete")
    service_agreements = db.relationship('Agreement', back_populates='provider', cascade="all, delete")
    service_reviews = db.relationship('Review', back_populates='provider', cascade="all, delete")

    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    def __repr__(self):
        return f"ServiceProvider({self.first_name} {self.last_name})"


class Equipment(db.Model):
    __tablename__ = "equipment"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category = db.Column(db.String)
    make = db.Column(db.String)
    model = db.Column(db.String)
    description = db.Column(db.String)
    availability = db.Column(db.String)
    rental_price = db.Column(db.Integer)

    provider_id = db.Column(db.Integer, db.ForeignKey('service_providers.id'))
    provider = db.relationship('ServiceProvider', back_populates='equipment_list')

    def __repr__(self):
        return f"Equipment({self.name} {self.make} {self.model})"


class Agreement(db.Model):
    __tablename__ = "agreements"

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String)
    delivery_address = db.Column(db.String, nullable=True)

    provider_id = db.Column(db.Integer, db.ForeignKey('service_providers.id'))
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))

    provider = db.relationship('ServiceProvider', back_populates='service_agreements')
    account = db.relationship('Account', back_populates='rental_agreements')

    def __repr__(self):
        return f"Agreement({self.start_date} - {self.end_date})"


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    comment = db.Column(db.String)

    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    provider_id = db.Column(db.Integer, db.ForeignKey('service_providers.id'))

    account = db.relationship('Account', back_populates='reviews')
    provider = db.relationship('ServiceProvider', back_populates='service_reviews')

    def __repr__(self):
        return f"Review({self.rating} stars)"


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    provider_id = db.Column(db.Integer, db.ForeignKey('service_providers.id'))

    account = db.relationship('Account', back_populates='messages')
    provider = db.relationship('ServiceProvider', back_populates='messages')

    def __repr__(self):
        return f"Message({self.content[:20]}...)"

class Favorite(db.Model):
    __tablename__ = "favorites"

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))

    account = db.relationship('Account', back_populates='favorites')
    equipment = db.relationship('Equipment', back_populates='favorites')

    def __repr__(self):
        return f"Favorite({self.account_id} - {self.equipment_id})"


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.Integer)
    status = db.Column(db.String)

    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'))
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))

    account = db.relationship('Account', back_populates='orders')
    equipment = db.relationship('Equipment', back_populates='orders')

    def __repr__(self):
        return f"Order({self.total_amount} {self.status})"
