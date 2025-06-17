from models import db, User, EquipmentOwner, Equipment, RentalAgreement, EquipmentImage, Thread, UserInbox, OwnerInbox, Message, Cart, CartItem, EquipmentPrice, FeaturedEquipment, Review, UserFavorite, OwnerFavorite, AgreementComment, EquipmentStateHistory, EquipmentStateSummary, EquipmentStatus, OrderHistory, PaymentRecord
from app import app
from random import randint
from datetime import datetime, timedelta
import stripe
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../.env.local')

# Function to clear all data from the database
def clear_all_database_data():
    print("Clearing all data from the database...")
    models_to_clear = [AgreementComment, Review, RentalAgreement, CartItem, Cart, EquipmentStatus, 
                       EquipmentStateSummary, EquipmentStateHistory, EquipmentPrice, FeaturedEquipment, 
                       OrderHistory, UserFavorite, OwnerFavorite, Equipment, UserInbox, OwnerInbox, 
                       EquipmentOwner, PaymentRecord, User, EquipmentImage, Message, Thread]
    
    for model in models_to_clear:
        model.query.delete()
    db.session.commit()

# Function to generate a random date within the last 30 days
def generate_random_date_within_30_days():
    current_date = datetime.now()
    thirty_days_ago = current_date - timedelta(days=30)
    return thirty_days_ago + timedelta(days=randint(0, 30))

# Function to add sample users
def add_sample_users():
    sample_users = [
        User(firstName="Jacob", lastName="Smith", date_of_birth=datetime(1980, 3, 25), email="jacob.smith01@EquipMe.com", phone="212-555-0180", country="US", state="NY", city="New York", address="75 W 3rd St", postal_code="10003", profession="Construction Worker", bio="Experienced in construction with 15+ years on-site", profileImage="https://avatarfiles.alphacoders.com/224/224246.png"),
        User(firstName="Olivia", lastName="Taylor", date_of_birth=datetime(1990, 7, 14), email="olivia.taylor22@EquipMe.com", phone="312-555-2341", country="US", state="IL", city="Chicago", address="435 W Armitage Ave", postal_code="60614", profession="Heavy Equipment Operator", bio="Specialized in operating cranes and bulldozers", profileImage="https://avatarfiles.alphacoders.com/366/366869.png"),
        User(firstName="Ethan", lastName="Brown", date_of_birth=datetime(1985, 11, 9), email="ethan.brown33@EquipMe.com", phone="713-555-3252", country="US", state="TX", city="Houston", address="1400 W Loop N Fwy", postal_code="77008", profession="Industrial Mechanic", bio="Skilled mechanic with a focus on heavy industrial machines", profileImage="https://avatarfiles.alphacoders.com/325/325695.png")
    ]
    
    db.session.add_all(sample_users)
    db.session.commit()

    # Hash passwords for users
    user_password = '123'
    for user in sample_users:
        user.password_hash = user_password
    db.session.commit()

# Function to add sample equipment owners
def add_sample_equipment_owners():
    equipment_owners = [
        EquipmentOwner(firstName="Liam", lastName="Jones", date_of_birth=datetime(1975, 2, 12), country="US", state="CA", city="Los Angeles", address="50 Sunset Blvd", postal_code="90028", profession="Plumbing", bio="Plumbing expert with high-quality tools and service", phone="323-555-8765", email="liam.jones@EquipMe.com", profileImage="https://avatarfiles.alphacoders.com/290/290163.png"),
        EquipmentOwner(firstName="Mia", lastName="Davis", date_of_birth=datetime(1988, 10, 3), country="US", state="FL", city="Miami", address="345 Ocean Dr", postal_code="33139", profession="Construction Equipment Rental", bio="Renting reliable construction machinery in Miami", phone="305-555-6543", email="mia.davis@EquipMe.com", profileImage="https://avatarfiles.alphacoders.com/352/352560.png")
    ]
    
    db.session.add_all(equipment_owners)
    db.session.commit()

    # Hashing owner passwords
    owner_password = '123'
    for owner in equipment_owners:
        owner.password_hash = owner_password
    db.session.commit()

# Function to add sample equipment
def add_sample_equipment():
    sample_equipment = [
        Equipment(name='Backhoe', type='Heavy Machinery', make='Caterpillar', model='420F', description="Caterpillar backhoe for heavy lifting and digging", owner_id=1),
        Equipment(name='Forklift', type='Industrial Vehicle', make='Toyota', model='7FB25', description="Toyota forklift, reliable for warehouse lifting", owner_id=2)
    ]
    
    db.session.add_all(sample_equipment)
    db.session.commit()

# Function to add sample equipment statuses
def add_sample_equipment_status():
    sample_equipment_status = [
        EquipmentStatus(equipment_id=1, total_quantity=5, available_quantity=5, reserved_quantity=0, rented_quantity=0, maintenance_quantity=0, transit_quantity=0),
        EquipmentStatus(equipment_id=2, total_quantity=3, available_quantity=3, reserved_quantity=0, rented_quantity=0, maintenance_quantity=0, transit_quantity=0)
    ]
    
    db.session.add_all(sample_equipment_status)
    db.session.commit()

# Function to add sample rental agreements
def add_sample_rental_agreements():
    sample_rental_agreements = [
        RentalAgreement(rental_start_date=datetime(2023, 9, 15, 10, 30), rental_end_date=datetime(2023, 9, 18, 10, 30), owner_decision="accept", user_decision="accept", agreement_status="both-accepted", owner_id=1, user_id=1, equipment_id=1, created_at=datetime(2023, 9, 15), updated_at=datetime(2023, 9, 15))
    ]
    
    db.session.add_all(sample_rental_agreements)
    db.session.commit()

# Running all seed functions
if __name__ == '__main__':
    with app.app_context():
        clear_all_database_data()
        add_sample_users()
        add_sample_equipment_owners()
        add_sample_equipment()
        add_sample_equipment_status()
        add_sample_rental_agreements()
        print("Database successfully seeded.")
