from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from config import db, bcrypt
from datetime import datetime, date
from helpers import calculate_age

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    firstName = db.Column(db.String)
    lastName = db.Column(db.String)

    date_of_birth = db.Column(db.Date)


    country = db.Column(db.String)
    state = db.Column(db.String)
    city = db.Column(db.String)
    address = db.Column(db.String)
    address_line_2 = db.Column(db.String, nullable=True)
    postal_code = db.Column(db.String)

    profession = db.Column(db.String)
    bio = db.Column(db.String, nullable=True)
    phone = db.Column(db.String)
    email = db.Column(db.String)
    profileImage = db.Column(db.String)
    _password_hash = db.Column(db.String, nullable=False)
    

    agreements = db.relationship('RentalAgreement', back_populates="user", cascade="all, delete")

    user_inboxes = db.relationship("UserInbox", back_populates="user", cascade="all, delete")

    cart = db.relationship('Cart', back_populates='user', cascade="all, delete")

    review = db.relationship ('Review', back_populates='user', cascade="all, delete")

    orders = db.relationship('OrderHistory', back_populates='user', cascade="all, delete")

    user_favorite = db.relationship('UserFavorite', back_populates='user', cascade="all, delete")
    owner_favorite = db.relationship('OwnerFavorite', back_populates='user', cascade="all, delete")

    payment_record = db.relationship('PaymentRecord', back_populates='user')


    serialize_rules = ('-review.user.cart','-review.user.user_inboxes', '-review.user.user_favorite','-review.user.owner_favorite','-review.owner.owner_favorite','-review.owner.owner_inboxes','-review.owner.equipment','-review.owner.agreements','-review.cart_item','-cart.cart_item.agreements.cart_item','-cart.cart_item.agreements.review.user', '-cart.cart_item.agreements.review.owner','-cart.cart_item.equipment.featured_equipment','-cart.cart_item.equipment', '-cart.cart_item.equipment.owner.owner_inboxes','-cart.cart_item.equipment.owner.review','-cart.user.user_inboxes', '-cart.user.user_favorite', '-agreements', '-user_inboxes.user', '-user_favorite.owner_favorite', '-cart.cart_item.equipment.user_favorite', '-owner_favorite', '-cart.cart_item.equipment.owner.owner_favorite','-cart.cart_item.equipment.owner.user_favorite', '-review.owner.user_favorite', '-user_favorite.owner.equipment', '-user_favorite.owner.agreements', '-user_favorite.owner.review', '-user_favorite.owner.owner_favorite','-user_favorite.owner.user_favorite', '-user_favorite.owner.owner_favorite', '-user_favorite.owner.owner_inboxes','-user_favorite.equipment.cart_item', '-user_favorite.equipment.equipment_price', '-user_favorite.equipment.featured_equipment', '-user_favorite.equipment.owner', '-user_favorite.user','-orders.user', '-orders.owner', '-payment_record.user')


    @property
    def age(self):
        return calculate_age(self.date_of_birth)
    
    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))



class EquipmentOwner(db.Model, SerializerMixin):
    __tablename__ = "owners"

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String)
    lastName = db.Column(db.String)

    date_of_birth = db.Column(db.Date)


    country = db.Column(db.String)
    state = db.Column(db.String)
    city = db.Column(db.String)
    address = db.Column(db.String)
    address_line_2 = db.Column(db.String, nullable=True)
    postal_code = db.Column(db.String)

    stripe_id = db.Column(db.String, unique=True, nullable=True)
    # stripe_onboard_link = db.Column(db.String, nullable=True)
    profession = db.Column(db.String)
    bio = db.Column(db.String, nullable=True)
    phone = db.Column(db.String)
    email = db.Column(db.String)
    _password_hash = db.Column(db.String, nullable=False)
    profileImage = db.Column(db.String)
    website = db.Column(db.String)
    
    equipment = db.relationship('Equipment', back_populates='owner', cascade="all, delete")

    agreements = db.relationship('RentalAgreement', back_populates ='owner', cascade="all, delete")

    owner_inboxes = db.relationship('OwnerInbox', back_populates='owner', cascade="all, delete")

    review = db.relationship ('Review', back_populates='owner', cascade="all, delete")

    owner_favorite = db.relationship('OwnerFavorite', back_populates='owner', cascade="all, delete")
    user_favorite = db.relationship('UserFavorite', back_populates='owner', cascade="all, delete")

    orders = db.relationship('OrderHistory', back_populates='owner', cascade="all, delete")


    serialize_rules = ('-orders.owner', '-orders.user','-equipment.owner', '-agreements.owner', '-owner_inboxes.owner','-owner_inboxes.user','-review.owner', '-review.user.user_favorite','-review.user.cart', '-review.user.user_inboxes','-review.cart_item', '-equipment.cart_item.cart.cart_item', '-owner_favorite.owner', '-owner_favorite.equipment', '-owner_favorite.user.user_inboxes','-owner_favorite.user.cart','-owner_favorite.user.review','-owner_favorite.user.user_favorite','-user_favorite.owner', '-user_favorite.user','-agreements.cart_item.equipment.user_favorite', '-agreements.cart_item.review', '-equipment.cart_item.cart.user','-equipment.user_favorite.user', '-agreements.cart_item.equipment.featured_equipment', '-agreements.review.owner', '-agreements.review.user', '-review.agreements', '-orders.equipment',)


    @property
    def age(self):
        return calculate_age(self.date_of_birth)
    
    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))

    #VALIDATIONS HERE
    @validates("email")
    def validates_email(self, key, email):
        if len(email) > 0 and "@"  in email:
            return email
        else:
            raise ValueError("Please check that you entered your email correctly")
        
    @validates("name")
    def validates_name(self, key, firstName):
        if len(firstName) > 0:
            return firstName
        else:
            raise ValueError("Please input a first name")

    def __repr__(self):
        return f"My name is {self.firstName}"

class Equipment(db.Model, SerializerMixin):
    __tablename__= "equipments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    type = db.Column(db.String)
    make = db.Column(db.String)
    model = db.Column(db.String)
    description = db.Column(db.String, nullable= True)
    equipment_image = db.Column(db.String)

    country = db.Column(db.String)
    state = db.Column(db.String)
    city = db.Column(db.String)
    address = db.Column(db.String)
    address_line_2 = db.Column(db.String, nullable= True)
    postal_code = db.Column(db.String)

    availability = db.Column(db.String)
    delivery = db.Column(db.String)
 
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))

    owner = db.relationship("EquipmentOwner", back_populates="equipment")


    cart_item = db.relationship('CartItem', back_populates='equipment', cascade="all, delete")

    equipment_price = db.relationship('EquipmentPrice', back_populates='equipment', cascade="all, delete")

    images = db.relationship('EquipmentImage', back_populates='equipment', cascade="all, delete")

    featured_equipment = db.relationship('FeaturedEquipment', back_populates='equipment', cascade="all, delete")

    user_favorite = db.relationship('UserFavorite', back_populates='equipment', cascade="all, delete")
    
    state_history = db.relationship('EquipmentStateHistory', back_populates='equipment', cascade="all, delete")

    status = db.relationship('EquipmentStatus', back_populates='equipment', cascade="all, delete")

    equipment_state_summary = db.relationship('EquipmentStateSummary', back_populates='equipment', cascade="all, delete")

    orders = db.relationship('OrderHistory', back_populates='equipment')

    serialize_rules = ('-owner.equipment','-owner.owner_inboxes','-owner.agreements', '-owner.owner_favorite','-owner.review','-owner.user_favorite','-images.equipment', '-cart_item.equipment','-equipment_price.equipment', '-featured_equipment.equipment','-cart_item.review','-cart_item.agreements', '-cart_item.cart', '-user_favorite.equipment', '-user_favorite.owner', '-user_favorite.user.user_inboxes', '-user_favorite.user.agreement','-user_favorite.user.cart','-user_favorite.user.review', '-state_history.equipment', '-status.equipment', '-equipment_state_summary.equipment', '-state_history.equipment_state_summary', '-equipment_state_summary.state_history', '-orders.equipment', '-orders.user', '-orders.owner', '-owner.orders',)
    
class EquipmentPrice(db.Model, SerializerMixin):
    __tablename__= "equipment_prices"
    id = db.Column(db.Integer, primary_key = True)

    hourly_rate = db.Column(db.Integer, nullable= True)
    daily_rate = db.Column(db.Integer, nullable= True)
    weekly_rate = db.Column(db.Integer, nullable= True)
    promo_rate = db.Column(db.Integer, nullable= True) # I need to incorporate maybe multiple promo rates

    equipment_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))
    equipment = db.Relationship('Equipment', back_populates ='equipment_price')

    serialize_rules = ('-equipment.equipment_price',)


class EquipmentImage(db.Model, SerializerMixin):
    __tablename__= "equipment_images"

    id = db.Column(db.Integer, primary_key = True)
    imageURL = db.Column(db.String)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))
    

    equipment = db.relationship('Equipment', back_populates='images')

    serialize_rules = ('-equipment.images', )

class EquipmentStateHistory(db.Model, SerializerMixin):
    __tablename__ = "equipment_state_history"

    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))
    total_quantity = db.Column(db.Integer)
    available_quantity = db.Column(db.Integer)
    reserved_quantity = db.Column(db.Integer, default=0)
    rented_quantity = db.Column(db.Integer, default=0)
    maintenance_quantity = db.Column(db.Integer, default=0)
    transit_quantity = db.Column(db.Integer, default=0)
    damaged_quantity = db.Column(db.Integer, default=0)
    previous_state = db.Column(db.String)
    new_state = db.Column(db.String)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    equipment = db.relationship('Equipment', back_populates='state_history')
    equipment_state_summary = db.relationship('EquipmentStateSummary', back_populates='state_history')

    serialize_rules = ('-equipment.state_history', '-equipment_state_summary.state_history')


class EquipmentStateSummary(db.Model, SerializerMixin):
    __tablename__ = "equipment_state_summaries"
    
    id = db.Column(db.Integer, primary_key=True)
    equipment_history_id = db.Column(db.Integer, db.ForeignKey('equipment_state_history.id'))
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))
    date = db.Column(db.Date)
    state = db.Column(db.String)
    total_quantity = db.Column(db.Integer, default=0)
    total_available = db.Column(db.Integer, default=0)
    total_reserved = db.Column(db.Integer, default=0)
    total_rented_out = db.Column(db.Integer, default=0)
    total_cancelled = db.Column(db.Integer, default=0)
    total_maintenance_quantity = db.Column(db.Integer, default=0)
    total_transit_quantity = db.Column(db.Integer, default=0)

    equipment = db.relationship('Equipment', back_populates='equipment_state_summary')

    state_history = db.relationship('EquipmentStateHistory', back_populates='equipment_state_summary', cascade="all, delete")

    serialize_rules = ('-state_history.equipment_state_summary','-equipment.equipment_state_summary', '-equipment.state_history')

class EquipmentStatus(db.Model, SerializerMixin):
    __tablename__ = "equipment_status"
    
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))
    total_quantity = db.Column(db.Integer)
    available_quantity = db.Column(db.Integer)
    reserved_quantity = db.Column(db.Integer, default=0)
    rented_quantity = db.Column(db.Integer, default=0)
    maintenance_quantity = db.Column(db.Integer, default=0)
    transit_quantity = db.Column(db.Integer, default=0)

    equipment = db.relationship('Equipment', back_populates='status')

    serialize_rules = ('-equipment.status', )


class FeaturedEquipment(db.Model, SerializerMixin):
    __tablename__="featured_equipments"
    id = db.Column(db.Integer, primary_key = True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))
    equipment = db.relationship('Equipment', back_populates='featured_equipment')

    serialize_rules = ('-equipment.featured_equipment', )


class UserFavorite(db.Model, SerializerMixin):
    __tablename__="user_favorites"

    id = db.Column(db.Integer, primary_key = True)


    equipment_id = db.Column(db.Integer, db.ForeignKey('equipments.id'), nullable= True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'), nullable= True)

    equipment = db.relationship('Equipment', back_populates='user_favorite')
    user = db.relationship('User', back_populates="user_favorite" )
    owner = db.relationship("EquipmentOwner", back_populates="user_favorite")

    serialize_rules = ('-equipment.user_favorite','-user.user_favorite')

class OwnerFavorite(db.Model, SerializerMixin):
    __tablename__="owner_favorites"

    id = db.Column(db.Integer, primary_key = True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'), nullable= True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= True)


    user = db.relationship('User', back_populates="owner_favorite" )
    owner = db.relationship("EquipmentOwner", back_populates="owner_favorite")

    serialize_rules = ('-user','-owner',)

class RentalAgreement(db.Model, SerializerMixin):
    __tablename__ = "agreements"

    id = db.Column(db.Integer, primary_key=True)
    
    rental_start_date = db.Column(db.String) 

    rental_end_date = db.Column(db.String)
    # Yes / No
    delivery = db.Column(db.Boolean, nullable= True)
    delivery_address = db.Column(db.String, nullable= True)

    user_decision = db.Column(db.String)
    owner_decision = db.Column(db.String)
    revisions = db.Column(db.Integer, default=0)

    agreement_status = db.Column(db.String)

    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    cart_item_id = db.Column(db.Integer, db.ForeignKey('cart_items.id'))

    created_at = db.Column(
    db.DateTime, nullable=False,
    default=datetime.utcnow,
    )

    updated_at = db.Column(
    db.DateTime, nullable=False,
    default=datetime.utcnow,
    onupdate=datetime.utcnow
    )

    user = db.relationship(
        "User", back_populates="agreements"
    )

    
    owner = db.relationship(
        "EquipmentOwner", back_populates="agreements"
    )
    cart_item = db.relationship(
    'CartItem', back_populates='agreements', cascade="all, delete")
    
    comment = db.relationship('AgreementComment', back_populates='agreements', cascade="all, delete")

    review = db.relationship('Review', back_populates="agreements")
    
    serialize_rules = ('-owner', '-user', '-cart_item.agreements', '-cart_item.cart.user.user_favorite','-comment.agreements', '-cart_item.equipment.featured_equipment', '-cart_item.equipment.user_favorite', '-review.agreements')


class AgreementComment(db.Model, SerializerMixin):
    __tablename__="agreement_comments"

    id = db.Column(db.Integer, primary_key=True)

    comment = db.Column(db.String)

    origin = db.Column(db.String)

    created_at = db.Column(
    db.DateTime, nullable=True,
    default=datetime.utcnow,
    )

    updated_at = db.Column(
    db.DateTime, nullable=True,
    default=datetime.utcnow,
    onupdate=datetime.utcnow
    )

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'), nullable= True)
    agreement_id = db.Column(db.Integer, db.ForeignKey('agreements.id'))


    agreements = db.relationship('RentalAgreement', back_populates ='comment')

    serialize_rules = ('-agreements.comment', )
    
class Cart(db.Model, SerializerMixin):
    __tablename__ = "carts"
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Integer)
    cart_name = db.Column(db.String, nullable=True)
    cart_status = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    #We'll try this cascade delete first : https://docs.sqlalchemy.org/en/20/orm/cascades.html#cascade-delete-orphan
    cart_item = db.relationship('CartItem', back_populates='cart', cascade="all, delete")
    user = db.relationship ('User', back_populates='cart')

    serialize_rules = ('-cart_item.cart','-cart_item.equipment.agreements','-cart_item.equipment.owner','-user.cart','-user.user_inboxes','-user.agreements', '-user.review','-cart_item.review')



    def calculate_total(self):
        self.total = sum(cart_item.total_cost for cart_item in self.cart_item if cart_item.agreements and cart_item.agreements[0].agreement_status == 'both-accepted')
        db.session.add(self) 
        db.session.commit() 
        return self.total


class CartItem(db.Model, SerializerMixin):
    __tablename__ = "cart_items"
    id = db.Column(db.Integer, primary_key= True)

    price_cents_at_addition = db.Column(db.Integer)
    price_cents_if_changed = db.Column(db.Integer, nullable = True)
    quantity = db.Column(db.Integer, default=1)
    rental_rate = db.Column(db.String)
    rental_length = db.Column(db.Integer, default=1)

    created_at = db.Column(
    db.DateTime, nullable=False,
    default=datetime.utcnow,
    )

    updated_at = db.Column(
    db.DateTime, nullable=False,
    default=datetime.utcnow,
    onupdate=datetime.utcnow
    )
    
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'))
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))

    cart = db.relationship('Cart', back_populates='cart_item')
    equipment = db.relationship('Equipment', back_populates='cart_item')
    agreements = db.relationship('RentalAgreement',back_populates="cart_item", cascade="all, delete")



    serialize_rules = ('-cart.cart_item', '-equipment.cart_item', '-agreements,','-agreements.owner','-agreements.user','-review.cart_item','-review.user', '-review.owner' ,'-equipment.owner')

    @property
    def total_cost(self):
        # Use price_cents_if_changed if it exists and is a valid integer, otherwise use price_cents_at_addition
        price = self.price_cents_if_changed if self.price_cents_if_changed is not None else self.price_cents_at_addition

        if all(isinstance(value, int) and value > 0 for value in [price, self.rental_length, self.quantity]):
            return (price * self.rental_length) * self.quantity
        else:
            raise ValueError("Invalid values for price, rental length, or quantity. All must be positive integers.")
        

        
class OrderHistory(db.Model, SerializerMixin):
    __tablename__="order_history"

    id = db.Column(db.Integer, primary_key=True)
    order_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.Integer)  # For monetary values
    payment_status = db.Column(db.String(50))
    payment_method = db.Column(db.String(50))
    order_status = db.Column(db.String(50))
    delivery_address = db.Column(db.String)
    order_details = db.Column(db.String) 
    estimated_delivery_date = db.Column(db.DateTime)
    actual_delivery_date = db.Column(db.DateTime)
    cancellation_date = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)
    actual_return_date = db.Column(db.DateTime)
    notes = db.Column(db.String)
    order_number = db.Column(db.String)

    individual_item_total = db.Column(db.Integer)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipments.id'))

    user = db.relationship('User', back_populates='orders')
    owner = db.relationship("EquipmentOwner", back_populates="orders")
    equipment = db.relationship('Equipment', back_populates='orders')

    serialize_rules = ('-user.review','-user.agreements','-user.user_inboxes','-user.cart','-user.orders', '-user.user_favorite','-user.owner_favorite','-owner.agreements','-owner.owner_inboxes','-owner.review','-owner.owner_favorite','-owner.user_favorite','-owner.orders','-owner.equipment','-equipment.cart_item', '-equipment.equipment_price', '-equipment.featured_equipment',  '-equipment.user_favorite', '-equipment.state_history', '-equipment.status', '-equipment.equipment_state_summary', '-equipment.orders',)


class PaymentRecord(db.Model, SerializerMixin):
    __tablename__="payment_records"

    id = db.Column(db.Integer, primary_key=True)
    payment_intent_id = db.Column(db.String(255), nullable=True, unique=True)
    status = db.Column(db.String(50), nullable=True)
    amount_received = db.Column(db.Integer, nullable=True)
    currency = db.Column(db.String(3), nullable=True, default='USD')
    payment_method = db.Column(db.String(50), nullable=True)
    order_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', back_populates='payment_record')

    serialize_rules = ('user.payment_record',)


class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)

    review_stars = db.Column(db.Integer)
    review_comment = db.Column(db.String)
    reviewer_type = db.Column(db.String) # Owner Or User 

    created_at = db.Column(
    db.DateTime, nullable=True,
    default=datetime.utcnow,
    )

    updated_at = db.Column(
    db.DateTime, nullable=True,
    default=datetime.utcnow,
    onupdate=datetime.utcnow
    )

    agreement_id = db.Column(db.Integer, db.ForeignKey('agreements.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))

    agreements = db.relationship('RentalAgreement',back_populates="review")
    user = db.relationship ('User', back_populates='review')
    owner = db.relationship("EquipmentOwner", back_populates="review")

    serialize_rules = ('-cart_item.review', '-user.review', '-owner.review', '-agreements.review')



class Message(db.Model, SerializerMixin):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    recipient_id = db.Column(db.Integer)
    sender_id = db.Column(db.Integer)

    context_id = db.Column(db.Integer, nullable = True)
    user_type = db.Column(db.String)

    content = db.Column(db.String)
    message_status = db.Column(db.String, nullable = True)

    created_at = db.Column(
    db.DateTime, nullable=False,
    default=datetime.utcnow,
    )

    thread_id = db.Column(db.Integer, db.ForeignKey('threads.id'))
    thread = db.relationship('Thread', back_populates='messages')


    serialize_rules = ('-thread.user_inboxes', '-thread.user_inboxes.thread', '-thread.owner_inboxes', '-thread.owner_inboxes.thread' )



class Thread(db.Model, SerializerMixin):
    __tablename__ = "threads"

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String, nullable=True)

    messages = db.relationship('Message', back_populates='thread', cascade="all, delete")
    user_inboxes = db.relationship("UserInbox", back_populates="thread")
    owner_inboxes = db.relationship("OwnerInbox", back_populates="thread")

    serialize_rules = ('-user_inboxes.thread', '-owner_inboxes.thread','-user_inboxes.user.agreements', '-user_inboxes.user.cart', '-user_inboxes.user.review', '-user_inboxes.user.orders', '-user_inboxes.user.user_favorite','-user_inboxes.user.owner_favorite', '-user_inboxes.user._password_hash','-owner_inboxes.owner._password_hash','-owner_inboxes.owner.equipment', '-owner_inboxes.owner.agreements', '-owner_inboxes.owner.owner_favorite', '-owner_inboxes.owner.orders', '-owner_inboxes.owner.user_favorite', '-owner_inboxes.owner.user_favorite','-messages.thread')

class UserInbox(db.Model, SerializerMixin):
    __tablename__ = "user_inboxes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    thread_id = db.Column(db.Integer, db.ForeignKey('threads.id'))

    user = db.relationship("User", back_populates="user_inboxes")
    thread = db.relationship("Thread", back_populates="user_inboxes", cascade="all, delete")

    serialize_rules = ('-user.user_inboxes', '-thread.user_inboxes', '-thread.owner_inboxes')

class OwnerInbox(db.Model, SerializerMixin):
    __tablename__ = "owner_inboxes"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'))
    thread_id = db.Column(db.Integer, db.ForeignKey('threads.id'))

    owner = db.relationship("EquipmentOwner", back_populates="owner_inboxes")
    thread = db.relationship("Thread", back_populates="owner_inboxes", cascade="all, delete")

    serialize_rules = ('-owner.owner_inboxes', '-thread.owner_inboxes', '-thread.user_inboxes')

