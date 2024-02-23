from faker import Faker

fake = Faker(['en_US', 'it_IT', 'en_GB', 'fr_FR','es','cs_CZ','de_DE', 'zh_CN'])
numberOfentries = 200

names = []
addresses = []
phoneNumbers = []
countries = []
emails = []
passwords = []
reviews = []
refNumbers = []



for x in range(numberOfentries):
    names.append(fake.name())
    addresses.append(fake.address())
    phoneNumbers.append(fake.phone_number())
    countries.append(fake.country())
    emails.append(fake.free_email())
    passwords.append(fake.password(length = 10))
    reviews.append(fake.paragraph(nb_sentences = 3))
    refNumbers.append(fake.bothify(text = '??:########', letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

for x in range(50):
    print(addresses[x])