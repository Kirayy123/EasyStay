import os
import csv
import random
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AATP.settings")
import django
django.setup()
from faker import Faker
from faker.providers import DynamicProvider
from EasyStay.models import hotel, user, hotelmanager, roomtype, user, room, booking
from decimal import Decimal

#This is just to populate the database with a random asssortment of hotels,
# managers & room types. it usually results in about 500 hotels (number is utimately random)
# uses images in media file and  a csv of the most populated cities as well as the python Faker module

fake = Faker()

numpercity =10

roomtypes = { "Single" : (100,"images/room_single.jpeg",1), "Double" : (200,"images/room_double.jpeg",2), "VIP" : 
             (500,"images/room_vip.jpeg",4), "Penthouse" : (400,"images/room_penthouse.jpeg",6), 
             "Self-Catered" : (300,"images/room_self.jpeg",5), "Deluxe" : (250,"images/room_deluxe.jpeg",2)}


roomtypesPhotos =  {"Single" : "images/room_single.jpeg","Double" : "images/room_double.jpeg","VIP" : "images/room_vip.jpeg","Penthouse" : "images/room_penthouse.jpeg","Self-Catered" : "images/room_self.jpeg","Deluxe" : "images/room_deluxe.jpeg"  }
room_facility=["Hot-Tub", "Sauna", "Kitchen", "Dog-Friendly", "Sea Views", "Lounge", "Luxury", "Basic"]
hotel_facility = ['Wi-Fi','TV','Air conditioning','Private Bathroom','Room Service','Balcony','Sea View','Parking','Lift','Swimming Pool','Gym','Spa','Restaurant','Breakfast','Bar','Pets Friendly','Non-smoking Rooms','Conference Room','Facilities for disabled guests']





hotelphotos = os.listdir("media/hotels/")
photo_provider = DynamicProvider(
    provider_name='hotelPhotos',
    elements=os.listdir("media\\hotels")
)

feature_provider = DynamicProvider(
    provider_name='features',
    elements=hotel_facility
)

roomFacility_Provider = DynamicProvider(
    provider_name= "room_facility",
    elements=room_facility
)

#FROM CHAT GPT
hotelnames = DynamicProvider(
    provider_name='hotels',
    elements= [
    "Grand Plaza Hotel",
    "Sunset Resort and Spa",
    "City Lights Inn",
    "Oceanfront Suites",
    "Mountain View Lodge",
    "Royal Gardens Hotel",
    "Harborview Hotel & Suites",
    "Azure Skies Resort",
    "Golden Sands Inn",
    "Pinnacle Heights Resort",
    "Lakeside Retreat Hotel",
    "Urban Oasis Suites",
    "Riverside Lodge",
    "Epic Grand Hotel",
    "Coastal Breeze Inn",
    "Green Valley Resort",
    "Metropolitan Suites",
    "Whispering Pines Hotel",
    "Serenity Spa and Resort",
    "Silver Moon Inn",
    "Central Park Hotel",
    "Tranquil Haven Resort",
    "Evergreen Plaza Hotel",
    "Countryside Lodge",
    "Regal Horizon Suites",
    "Majestic Peaks Resort",
    "Emerald Isles Hotel",
    "Ambassador Plaza",
    "Skyline View Inn",
    "Tropical Bliss Resort",
    "Rosewood Retreat",
    "Sapphire Springs Hotel",
    "Sunrise Suites",
    "Garden Grove Inn",
    "Moonlit Mansion",
    "Crystal Clear Resort",
    "Luxury Lagoon Hotel",
    "Sunflower Inn",
    "Enchanted Escape Lodge",
    "Crimson Crown Hotel",
    "Silver Creek Retreat",
    "Harmony Heights Hotel",
    "Whirlwind West Resort",
    "Harbor Lights Inn",
    "Silent Woods Lodge",
    "Regency Towers Hotel",
    "Celestial City Suites",
    "Golden Gate Resort",
    "Palm Paradise Hotel",
]
)
#From GOOGLE GEMINI
hoteldesc = DynamicProvider(
    provider_name='descriptions',
    elements= [
        "Unwind in the lap of luxury at the Grand Majestic Hotel. Our opulent rooms offer unparalleled comfort, while our Michelin-starred restaurant boasts exquisite culinary creations. Stroll through manicured gardens, indulge in rejuvenating spa treatments, and experience the epitome of refined hospitality.",

"Embark on a historical journey at the Olde Town Inn. Nestled in a charming cobblestone street, this boutique hotel offers a glimpse into the past with its historical architecture and antique furnishings. Explore nearby museums and landmarks, savor traditional local cuisine, and immerse yourself in the rich cultural heritage.",

"Reclaim your balance at the Serenity Wellness Retreat. Nestled amidst rolling hills and serene landscapes, this tranquil haven offers personalized wellness programs, yoga and meditation classes, and healthy, delicious meals. Rejuvenate your mind, body, and spirit in a supportive and peaceful environment.",

"Experience the thrill of the city at the Pulse Hotel. Located in the heart of the bustling entertainment district, this vibrant hotel offers stylish rooms, pulsating nightlife options, and easy access to top attractions. Immerse yourself in the city's energy, explore the diverse culinary scene, and embrace the electrifying atmosphere.",

"Surrender to the charm of the French countryside at the Lavender Fields B&B. Surrounded by picturesque lavender fields and rolling vineyards, this intimate bed and breakfast offers a taste of rural tranquility. Savor homemade breakfasts on the terrace, explore charming villages, and experience the simple pleasures of country life.",

"Step back in time at the Victorian Manor. This meticulously restored Victorian mansion offers a unique blend of history and modern comfort. Explore beautifully decorated rooms, wander through manicured gardens, and enjoy afternoon tea in the grand salon, feeling transported to another era.",

"Embrace the spirit of adventure at the Wild Coast Lodge. Perched on a dramatic cliffside overlooking the ocean, this eco-friendly lodge offers stunning views, exciting outdoor activities like surfing and kayaking, and a focus on sustainable practices. Reconnect with nature, experience the thrill of adventure, and leave a positive impact.",

"Discover the magic of the desert at the Oasis Dunes Resort. Nestled amidst majestic sand dunes, this luxurious resort offers private villas with plunge pools, desert excursions by camelback or jeep, and stargazing under the vast desert sky. Experience the tranquility and beauty of the desert in unparalleled comfort.",

"Immerse yourself in the heart of the jungle at the Hidden Canopy Treehouse. Nestled high amongst the lush rainforest canopy, this unique hotel offers eco-friendly treehouses with breathtaking views, guided nature walks, and opportunities to encounter diverse wildlife. Experience the magic of the rainforest in a truly unforgettable setting.",

"Embrace the vibrant culture of Mexico at the Posada del Sol. This charming hotel, located in a traditional Mexican village, offers colorful rooms, authentic local cuisine, and opportunities to experience the warmth and hospitality of Mexican culture. Learn traditional crafts, participate in local festivals, and immerse yourself in the vibrant rhythm of life.",

"Unwind in the lap of luxury at the Grand Majestic Hotel, offering unparalleled comfort, Michelin-starred dining, and manicured gardens.",

"Embark on a historical journey at the Olde Town Inn, nestled in a charming cobblestone street with historical architecture, antique furnishings, and access to museums, landmarks, and local cuisine.",

"Reclaim your balance at the Serenity Wellness Retreat, offering personalized programs, yoga, meditation, healthy meals, and peaceful surroundings to rejuvenate mind, body, and spirit.",

"Experience the city's energy at the Pulse Hotel, located in the heart of the entertainment district with stylish rooms, pulsating nightlife, and top attractions nearby.",

"Surrender to the charm of the French countryside at the Lavender Fields B&B, surrounded by picturesque lavender fields and vineyards, offering homemade breakfasts, exploration of charming villages, and the simple pleasures of country life.",

"Step back in time at the Victorian Manor, a meticulously restored mansion offering a unique blend of history and modern comfort with beautifully decorated rooms, manicured gardens, and afternoon tea in the grand salon.",

"Embrace the spirit of adventure at the Wild Coast Lodge, perched on a dramatic cliffside with stunning views, exciting outdoor activities like surfing and kayaking, and a focus on sustainable practices.",

"Discover the magic of the desert at the Oasis Dunes Resort, nestled amidst majestic sand dunes, offering private villas with plunge pools, desert excursions, and stargazing under the vast desert sky.",

"Immerse yourself in the heart of the jungle at the Hidden Canopy Treehouse, offering eco-friendly treehouses with breathtaking views, guided nature walks, and opportunities to encounter diverse wildlife.",

"Embrace the vibrant culture of Mexico at the Posada del Sol, located in a traditional village, offering colorful rooms, authentic local cuisine, and opportunities to experience the warmth and hospitality of Mexican culture, including learning traditional crafts and participating in local festivals.",

"Unleash your inner child at the Sunway Lagoon Resort, Malaysia's premier theme park destination, featuring thrilling rides, water slides, a wildlife park, and a variety of restaurants and shops, perfect for families and adventure seekers.",

"Escape to a world of tranquility at the COMO Uma Canggu, Bali, where minimalist design meets Balinese serenity. Relax in luxurious accommodations, indulge in rejuvenating spa treatments, and savor exquisite cuisine, all amidst the lush rice paddies and beaches of Bali.",

"Embark on a culinary adventure at the Spices Hotel, Marrakech, Morocco. Immerse yourself in the vibrant colors and flavors of Moroccan culture, explore bustling souks, learn the secrets of traditional Moroccan cuisine in cooking classes, and savor delectable meals in the hotel's renowned restaurant.",

"Reconnect with nature at the Clayoquot Wilderness Resort, Canada, nestled amidst pristine wilderness on the edge of Vancouver Island. Go kayaking in sheltered coves, explore ancient rainforests on guided hikes, and witness the breathtaking beauty of the Canadian wilderness.",

"Experience the magic of the Northern Lights at the Ice Hotel, Sweden. Constructed entirely from ice and snow, this unique hotel offers an unforgettable arctic adventure. Explore the surrounding frozen landscape, witness the mesmerizing Northern Lights, and indulge in a truly once-in-a-lifetime experience.",

"Discover the rich history and culture of Prague at the Golden Star Hotel, Czech Republic. This historic hotel, dating back to the 15th century, offers elegant rooms, a charming atmosphere, and a central location close to iconic landmarks like the Charles Bridge and Prague Castle.",

"Immerse yourself in the vibrant energy of Tokyo at the Capsule Inn Asakusa, Japan. Experience the unique concept of capsule hotels, offering compact yet comfortable accommodations in a convenient location close to popular tourist attractions and local markets.",

"Step back in time at the Dunvegan Castle Hotel, Scotland. This historic castle, dating back to the 13th century, offers a glimpse into Scotland's rich history. Explore the castle grounds, wander through secret passages, and enjoy traditional Scottish fare in the hotel's award-winning restaurant.",

"Embrace the laid-back island lifestyle at the Manta Resort, Pemba Island, Tanzania. Stay in luxurious overwater bungalows, explore the vibrant coral reefs teeming with marine life, and experience the unspoiled beauty of this remote island paradise.",

"Rejuvenate your mind, body, and spirit at the Ananda in the Himalayas, India. Nestled amidst the foothills of the Himalayas, this luxurious resort offers a variety of wellness programs, yoga and meditation classes, and Ayurvedic treatments, all designed to promote holistic well-being."
    ]
)
numberOfentries = 200
fake.add_provider(feature_provider)
fake.add_provider(roomFacility_Provider)
fake.add_provider(hotelnames)
fake.add_provider(hoteldesc)
fake.add_provider(photo_provider)

file_path = 'worldcities.csv'
num_rows_to_read = 50  

#creates a string of hotel features that is then parsed by the view method to display them seperately
def concatRandom(list, range):
    sample = random.sample(list, range)
    str = "["
    for x in sample:
            str += "'" + x +"'" +","
    str += "]"
    return str
    


def add_hotel(ID, man, city, city_countries):
    h = hotel.objects.get_or_create(hotel_id= fake.bothify(text = "H########"),
                                    manager= man,
                                    city = city,
                                    name= fake.hotels(),
                                    country = city_countries[city],
                                    location = fake.street_address(),
                                    postcode = fake.postcode(),
                                    phone= fake.phone_number(),
                                    description = fake.descriptions(),
                                    facility = concatRandom(hotel_facility, 6)

                                    )[0]
    h.email = fake.free_email()
    h.star = random.randint(1,5)
    h.image = "hotels/" + fake.hotelPhotos()
    h.save()
    return h

def add_manager(mID):
    m = hotelmanager.objects.get_or_create(manage_id= fake.bothify(text= "M#########"),
                                           email= fake.free_email())[0]
    m.phone = fake.phone_number()
    m.password = fake.password()
    m.save()
    return m

def add_roomtype(rid,hID, key):
    rType = key
    rPrice = roomtypes[key][0]
    rphoto = roomtypes[key][1]
    rGuests = roomtypes[key][2]
    xid= fake.bothify(text = "#########")
    r = roomtype.objects.get_or_create(id=xid,
                                       hotel=hID,
                                       type=rType,
                                       price=rPrice,
                                       facility=concatRandom(hotel_facility, 3),
                                       image=rphoto,
                                       guests=rGuests
                                       )[0]
    r.save
    return xid


#Assigns a number of rooms to hotels based on a random range 2-6
def assign_roomtypes(i, hID):
    returnv = i
    roomrange =random.randint(2,6)
    keys = list(roomtypes.keys())
    types = random.sample(keys, roomrange)
    typeindex = 0
    for x in range(roomrange):        
        num = add_roomtype(returnv + x, hID,types[typeindex])
        add_user_room_booking(num)
        returnv += x
        typeindex += 1
    return returnv



def populatepercity(count, numpercity, city, city_countries):  
        roomtypesCount = count
        for i in range(numpercity):   
            m = add_manager(roomtypesCount)
            h = add_hotel(roomtypesCount, m, city, city_countries)
            roomtypesCount = assign_roomtypes(roomtypesCount,h)
            roomtypesCount += 1
        return roomtypesCount

def iterate_existing_hotels():     
    for h in hotel.objects.all():
        url = "images/hotel.jpg"
        h.image = url       
        h.save()

def iterate_existing_managers(hotelname):
    for m in hotelmanager.objects.all():
        m.hotel_name = hotelname
        m.phone = fake.phone_number()
        

def read_csv_to_dict():
    file_path = 'worldcities.csv'
    num_rows = 50
    data_dict = {}
    with open(file_path, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        row_count = 0
        for row in csv_reader:
            if num_rows is not None and row_count >= num_rows:
                break

            city = row.get('city')
            country = row.get('country')

            if city and country:
                data_dict[city] = country

            row_count += 1

    return data_dict

def add_user_room_booking(roomtype):
    user = add_user()
    room = add_room(roomtype)
    add_bookings(room, user)

def add_room(roomtype):
    num = fake.bothify(text = "#####")
    roomx = room.objects.get_or_create(
        Room_number = num,
        type_id = roomtype
    )[0]
    roomx.save()
    return roomx
def add_booking_checkin(roomnumber , userid):
    bookin = booking.objects.get_or_create(
        ref_num = fake.bothify(text = "B#########"),
        total_price = 500,
        status = 1,
        room_number = roomnumber,
        user = userid,
        reserved_name = fake.bothify(text = "??"),
        reserved_phone = fake.phone_number(),
        booking_date = fake.date_time(),
        from_date = fake.date(),
        to_date = fake.date()
        )[0]
    bookin.save()

def add_booking_checkedin(roomnumber , userid):
    bookin = booking.objects.get_or_create(
        ref_num = fake.bothify(text = "B#########"),
        total_price = 500,
        status = 2,
        room_number = roomnumber,
        user = userid,
        reserved_name = fake.bothify(text = "??"),
        reserved_phone = fake.phone_number(),
        booking_date = fake.date_time(),
        from_date = fake.date(),
        to_date = fake.date(),
        check_in_date = fake.date_time(),
        )[0]
    bookin.save()

def add_booking_checkedout(roomnumber , userid):
    bookin = booking.objects.get_or_create(
        ref_num = fake.bothify(text = "B#########"),
        total_price = 500,
        status = 3,
        is_paid = 1,
        room_number = roomnumber,
        user = userid,
        reserved_name = fake.bothify(text = "??"),
        reserved_phone = fake.phone_number(),
        booking_date = fake.date_time(),
        from_date = fake.date(),
        to_date = fake.date(),
        check_in_date = fake.date_time(),
        check_out_date = fake.date_time(),
        )[0]
    bookin.save()

def add_booking_checked_review(roomnumber , userid):
    bookin = booking.objects.get_or_create(
        ref_num = fake.bothify(text = "B#########"),
        total_price = 500,
        status = 3,
        is_paid = 1,
        room_number = roomnumber,
        user = userid,
        reserved_name = fake.bothify(text = "??"),
        reserved_phone = fake.phone_number(),
        booking_date = fake.date_time(),
        from_date = fake.date(),
        to_date = fake.date(),
        check_in_date = fake.date_time(),
        check_out_date = fake.date_time(),
        review_star = random.randint(1,5),
        review_comment = fake.descriptions(),
        review_date = fake.date_time(),
        )[0]
    bookin.save()

def add_bookings(roomid, userid):
    add_booking_checked_review(roomid, userid)
    add_booking_checkedin(roomid, userid)
    add_booking_checkedout(roomid, userid)
    add_booking_checkin(roomid, userid)

def add_user():
    id = fake.bothify(text = "#########")
    userx = user.objects.get_or_create(
        user_id= id,
        email = fake.free_email(),
        phone = fake.phone_number(),
        password = fake.password(),
        username = fake.name())[0]
    userx.save()
    return userx


def get_lat_long(city):
    file_path = 'worldcities.csv'
    data_dict = {}
    with open(file_path, 'r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row.get('city') == city:
                data_dict['lat'] = Decimal(row.get('lat'))
                data_dict['long'] = Decimal(row.get('lng'))
                break
    if data_dict["lat"] == '' or data_dict['long'] == '':
         data_dict['lat'] = 55.8617
         data_dict['long'] = 4.2583
    return data_dict



def populate():
    city_countries = read_csv_to_dict()
    roomcount = 0
    for key, country in city_countries.items():
        print(key)
        roomcount = populatepercity(roomcount,numpercity, key, city_countries)
        roomcount +=1
 
if __name__ == '__main__':
    populate()
