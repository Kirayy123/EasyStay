import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AATP.settings")
import django
django.setup()
from faker import Faker
from faker.providers import DynamicProvider
from EasyStay.models import hotel, user, hotelmanager

fake = Faker()
feature_provider = DynamicProvider(
    provider_name='features',
    elements=["en-suite","swimming pool", "tennis court", "beach access", "hot tub", "sauna", "gym", "concierge service",
              "family friendly", "dog friendly", "cat friendly","city views", "restaurant", "free breakfast"]
)

numberOfentries = 200
fake.add_provider(feature_provider)

names = []
addresses = []
phoneNumbers = []
countries = []
emails = []
passwords = []
descriptions = []
hotelIDs = []
managerIDs = []

for x in range(numberOfentries):
    hotelIDs.append(fake.pyint())
    names.append(fake.name())
    addresses.append(fake.street_address())
    phoneNumbers.append(fake.phone_number())
    countries.append(fake.country())
    emails.append(fake.free_email())
    passwords.append(fake.password(length = 10))
    descriptions.append(fake.paragraph(nb_sentences = 3))
    


def add_hotel(mID):
    h = hotel.objects.get_or_create(hotel_id=fake.pyint(),
                                    city= fake.city(),
                                    manager_id= mID,
                                    name= fake.company(),
                                    )[0]
    h.location = fake.street_address()
    
    h.description = fake.paragraph(nb_sentences = 3)
    h.email = fake.free_email()
    facility = ""
    for i in range(6):
        facility += fake.features() + ", "
    h.facility = facility
    h.save()

def add_manager(mID):
    m = hotelmanager.objects.get_or_create(manage_id= mID,
                                           hotel_name= fake.company(),
                                           email= fake.free_email())[0]
   
    


def populate():
    counter= 1
    for i in range(400):
        manID = counter
        counter += 1 
        add_manager(manID)
        add_hotel(counter)
        
if __name__ == '__main__':
    
    populate()


    