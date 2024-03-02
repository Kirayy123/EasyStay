import os
import csv
import random
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AATP.settings")
import django
django.setup()
from faker import Faker
from faker.providers import DynamicProvider
from EasyStay.models import hotel, user, hotelmanager, roomtype

fake = Faker()

roomtypes = { "Single" : (100,"images/room_single.jpeg",2), "Double" : (200,"images/room_double.jpeg",4), "VIP" : 
             (500,"images/room_vip.jpeg",4), "Penthouse" : (400,"images/room_penthouse.jpeg",6), 
             "Self-Catered" : (300,"images/room_self.jpeg",5), "Deluxe" : (250,"images/room_deluxe.jpeg",2)}


roomtypesPhotos =  {"Single" : "images/room_single.jpeg","Double" : "images/room_double.jpeg","VIP" : "images/room_vip.jpeg","Penthouse" : "images/room_penthouse.jpeg","Self-Catered" : "images/room_self.jpeg","Deluxe" : "images/room_deluxe.jpeg"  }
room_facility=["Hot-Tub", "Sauna", "Kitchen", "Dog-Friendly", "Sea Views", "Lounge", "Luxury", "Basic"]
hotel_facility = ["en-suite","swimming pool", "tennis court", "beach access", "hot tub", "sauna", "gym", "concierge service",
              "family friendly", "dog friendly", "cat friendly","city views", "restaurant", "free breakfast"]

feature_provider = DynamicProvider(
    provider_name='features',
    elements=hotel_facility
)

roomFacility_Provider = DynamicProvider(
    provider_name= "room_facility",
    elements=room_facility
)
numberOfentries = 200
fake.add_provider(feature_provider)
fake.add_provider(roomFacility_Provider)


city_country = {}

def concatRandom(list, range):
    sample = random.sample(list, range)
    str = ""
    for x in sample:
        if(x == sample[len(sample) - 1]):
            str += x
        else:
            str += x + ","
    return str
    


def add_hotel(ID, man):
    h = hotel.objects.get_or_create(hotel_id=ID,
                                    city= fake.city(),
                                    manager= man,
                                    name= fake.company(),
                                    )[0]
    h.location = fake.street_address()
    
    h.description = fake.paragraph(nb_sentences = 5)
    h.email = fake.free_email()
    h.star = random.randint(1,5)
    h.image = "images/hotel.jpg"
    h.facility = concatRandom(hotel_facility, 6)
    h.phone= fake.phone_number()
    h.save()
    return h

def add_manager(mID):
    m = hotelmanager.objects.get_or_create(manage_id= mID,
                                           hotel_name= fake.company(),
                                           email= fake.free_email())[0]
    m.phone = fake.phone_number()
    m.save()
    return m

def add_roomtype(rid,hID, key):

    rType = key
    rPrice = roomtypes[key][0]
    rphoto = roomtypes[key][1]
    rGuests = roomtypes[key][2]
    r = roomtype.objects.get_or_create(id=rid,
                                       hotel=hID,
                                       type=rType,
                                       price=rPrice,
                                       facility=concatRandom(room_facility,2),
                                       image=rphoto,
                                       guests=rGuests
                                       )[0]
    r.save

def assign_roomtypes(i, hID):
    returnv = i
    roomrange =random.randint(2,6)
    keys = list(roomtypes.keys())
    types = random.sample(keys, roomrange)
    typeindex = 0
    for x in range(roomrange):        
        add_roomtype(returnv + x, hID,types[typeindex])
        returnv += x
        typeindex += 1
    return returnv



def populate():  
    roomtypesCount = 0
    for i in range(150):   
        m = add_manager(i)
        h = add_hotel(i, m)
        roomtypesCount = assign_roomtypes(roomtypesCount,h)
        roomtypesCount += 1

def iterate_existing_hotels():     
    for h in hotel.objects.all():
        url = "images/hotel.jpg"
        h.image = url       
        h.save()

def iterate_existing_managers(hotelname):
    for m in hotelmanager.objects.all():
        m.hotel_name = hotelname
        m.phone = fake.phone_number()
        
if __name__ == '__main__':
    populate()

    