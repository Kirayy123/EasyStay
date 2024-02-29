from faker import Faker
from faker.providers import DynamicProvider
from EasyStay.models import hotel, user

fake = Faker(['en_US', 'it_IT', 'en_GB', 'fr_FR','es','cs_CZ','de_DE', 'zh_CN'])
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

for x in range(numberOfentries):
    names.append(fake.name())
    addresses.append(fake.address())
    phoneNumbers.append(fake.phone_number())
    countries.append(fake.country())
    emails.append(fake.free_email())
    passwords.append(fake.password(length = 10))
    descriptions.append(fake.paragraph(nb_sentences = 3))
    hotelIDs.append(fake.bothify(text = '??:########', letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

hotels = []

def add_hotel(i):
    h = hotel.objects.get_or_create()[0]
    h.location = fake.address()
    h.hotel_id = fake.bothify(text = '??:########', letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    h.description = fake.paragraph(nb_sentences = 3)
    h.email = fake.free_email()
    facility = ""
    for i in range(6):
        facility += fake.features() + ", "
    h.facility = facility

    