import uuid
from typing import Dict
from admin_city import admin_control


from nicegui import Client, ui
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import asyncio


from nicegui import app
import sqlite3
import hashlib

from leaflet import leaflet 

from email.message import EmailMessage
import ssl   # this is a standard technology for keeping an internet connection secure and 
# safeguarding any sensitive data that is being sent between two systems so this adds a layer of
# security and this is important if we want to send an e-mail with some important data
import smtplib
from random import randint

conn = sqlite3.connect("DB/test.db", check_same_thread=False)
cursor = conn.cursor()

# CREATE ID TEXT FOR GET ID
get_id = ui.label()

app.add_middleware(SessionMiddleware, secret_key='some_random_string')  # use your own secret key here



# in reality users and session_info would be persistent (e.g. database, file, ...) and passwords obviously hashed
#users = [('user1', 'pass1'), ('user2', 'pass2')]

# DB CONNECTION TO USERS TABLE
cursor.execute('''SELECT name FROM Users''')
name_res = cursor.fetchall()
name_final_result = [i[0] for i in name_res]

cursor.execute('''SELECT password FROM Users''')
password_res = cursor.fetchall()
password_final_result = [i[0] for i in password_res]

cursor.execute('''SELECT email FROM Users''')
email_res = cursor.fetchall()
email_final_result = [i[0] for i in email_res]

users=[]
for i in range(len(password_final_result)):
    users.append((name_final_result[i], password_final_result[i]))

def update_users():
    cursor.execute('''SELECT name FROM Users''')
    name_res = cursor.fetchall()
    name_final_result = [i[0] for i in name_res]

    cursor.execute('''SELECT password FROM Users''')
    password_res = cursor.fetchall()
    password_final_result = [i[0] for i in password_res]


    users=[]
    for i in range(len(password_final_result)):
        users.append((name_final_result[i], password_final_result[i]))
    return(users)

def update_name_list():
    cursor.execute('''SELECT name FROM Users''')
    name_res = cursor.fetchall()
    name_final_result = [i[0] for i in name_res]
    return(name_final_result)



session_info: Dict[str, Dict] = {}


def is_authenticated(request: Request) -> bool:
    return session_info.get(request.session.get('id'), {}).get('authenticated', False)


# funtion for generating random 4 digits code authentication
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

code = str(random_with_N_digits(4))

email_sender = 'soranaantogalan7@gmail.com'
email_password = 'bvvytqqtysjmxjae'


@ui.page('/home')
async def home(request: Request) -> None:
    with ui.column().classes('absolute inset-0'):
        ui.image('https://i.postimg.cc/Wz3XmPng/bucarest.jpg').classes('absolute inset-0').classes('items-center')
        ui.image('https://i.postimg.cc/Wz3XmPng/bucarest.jpg').classes('absolute').classes('items-center')
    
    with ui.card().style('opacity:0.7'):
        with ui.column():
            #ui.markdown(''' ''').classes('text-2xl').classes('absolute-top text-subtitle2 text-center')
            ui.markdown('''<br />**Discover Romania's Hidden Gems: Plan Your Perfect City Break with Ease!**''').classes('text-2xl').classes('absolute-top text-subtitle2 text-center')
            ui.markdown('''<br /> ''').classes('text-2xl')
            ui.markdown('''<br />&emsp;Welcome to my web application demo for my bachelor's degree, your ultimate 
            companion for crafting unforgettable city breaks in Romania. With our intuitive platform, you can 
            effortlessly plan and organize your dream getaway, tailored to your interests and preferences. Explore 
            the rich history and cultural treasures of Romanian cities as you handpick monuments to visit, receive 
            expert transport suggestions, and receive a personalized map with your city break itinerary. 
            Additionally, easily locate essential amenities like police stations, pharmacies, hospitals to ensure 
            a smooth and worry-free travel experience. Get ready to embark on an immersive journey through 
            Romania's captivating cities with my web app!''').classes('text-2xl')

    with ui.card().style('opacity:0.7'):
        with ui.column():
            #ui.markdown(''' ''').classes('text-2xl').classes('absolute-top text-subtitle2 text-center')
            ui.markdown('''<br />**Features and Benefits of my web app**''').classes('text-2xl').classes('absolute-top text-subtitle2 text-center')
            ui.markdown('''<br /> ''').classes('text-2xl')
            ui.markdown('''<br />&emsp;**1.** Personalized City Break Planning:<br />&emsp; &emsp; &emsp;&#9679;Select your desired city in 
            Romania and create your own unique city break experience.
            <br />&emsp; &emsp; &emsp;&#9679;Choose from a vast collection of iconic monuments to visit and create your personalized 
            itinerary.<br />&emsp;**2.** Expert Transport Suggestions:<br />&emsp; &emsp; &emsp;&#9679;Receive expert recommendations on 
            the most convenient and efficient ways to get around your chosen city.<br />&emsp; &emsp; &emsp;&#9679;Seamlessly navigate 
            public transportation options and optimize your travel time.<br />&emsp;**3.** Interactive City Break Map:<br />&emsp; &emsp; &emsp;&#9679;
            Access a dynamic map that showcases your customized city break plan, highlighting key attractions and points of interest.<br />&emsp; &emsp; &emsp;&#9679;
            Easily explore your itinerary and navigate your way through the city with confidence.<br />&emsp;**4.** Comprehensive Local Information:
            <br />&emsp; &emsp; &emsp;&#9679;Explore an extensive database of local amenities, including police stations, pharmacies, hospitals, and supermarkets.
            <br />&emsp; &emsp; &emsp;&#9679;Find essential services nearby, ensuring your safety, convenience, and peace of mind during your city break.
            <br />&emsp;**5.** Easy Account Management:<br />&emsp; &emsp; &emsp;&#9679;Create an account and enjoy personalized features and benefits.
            <br />&emsp; &emsp; &emsp;&#9679;Save your favorite itineraries, revisit past trips, and receive tailored recommendations based on your preferences.
            <br />&emsp;**6.** Requested Email with City Break Details:<br />&emsp; &emsp; &emsp;&#9679;Receive a detailed email with all the information about your 
            city break, including your itinerary, transport suggestions, and essential contacts.<br />&emsp; &emsp; &emsp;&#9679;
            Have all the necessary information at your fingertips, even when offline.''').classes('text-2xl')


    if not is_authenticated(request):
        with ui.header(elevated=True).style('background-color: #20963d').classes('items-center justify-between'):
            with ui.row().classes('items-center'):
                ui.button('LOG IN REGISTER', on_click=lambda: ui.open(login)).classes('w-32').props('flat color=invisible')
                ui.button('HOME').classes('w-32').props('flat color=invisible')
                ui.button('ABOUT US', on_click=lambda: ui.open(about_us)).classes('w-32').props('flat color=invisible')
            
    else:
        with ui.header(elevated=True).style('background-color: #20963d').classes('items-center justify-between'):
            with ui.row().classes('items-center'):
                ui.button('MY ACCOUT', on_click=lambda: ui.open(login)).classes('w-32').props('flat color=invisible')
                ui.button('HOME').classes('w-32').props('flat color=invisible')
                ui.button('ABOUT US', on_click=lambda: ui.open(about_us)).classes('w-32').props('flat color=invisible')
                ui.button('PLANS', on_click=lambda: ui.open(plans)).classes('w-32').props('flat color=invisible')
                ui.button('USEFUL MAPS', on_click=lambda: ui.open(useful_maps)).classes('w-32').props('flat color=invisible')
            
    with ui.footer().style('background-color: #20963d').classes('items-center justify-between'):
        with ui.row():
            ui.label("email:")
            ui.link('soranaantogalan@yahoo.com', 'https://www.yahoo.com/').style('color: #ffffff')
            ui.label(" ")
            ui.label("phone number: +40-749-620-311")
        ui.button('', on_click=lambda: ui.open('https://nicegui.io')).props('flat color=invisible round icon=img:https://nicegui.io/logo_square.png').style('background-color: #4fb357')       
    

@ui.page('/about_us')
async def about_us(request: Request) -> None:
    with ui.column().classes('absolute inset-0'):
        ui.image('https://i.postimg.cc/Wz3XmPng/bucarest.jpg').classes('absolute inset-0').classes('items-center')
        ui.image('https://i.postimg.cc/Wz3XmPng/bucarest.jpg').classes('absolute').classes('items-center')
    
    with ui.card().style('opacity:0.7'):
        with ui.column():
            #ui.markdown(''' ''').classes('text-2xl').classes('absolute-top text-subtitle2 text-center')
            ui.markdown('''<br />**About my app**''').classes('text-2xl').classes('absolute-top text-subtitle2 text-center')
            ui.markdown('''<br /> ''').classes('text-2xl')
            ui.markdown('''<br />&emsp;I developed this app with passion for helping travelers 
            unlock the hidden gems of Romania and create unforgettable city break experiences. With my user-friendly 
            platform, I strive to make travel planning effortless, personalized, and exciting.<br />&emsp;As a dedicated 
            enthusiast and technology lover, I have carefully crafted this web app to cater specifically to the needs of 
            those looking to explore the captivating cities of Romania. I understand that each traveler has unique 
            preferences and interests, and that's why my app empowers you to create your own city break adventure.
            <br />&emsp;I am committed to providing you with the tools and resources needed to design your dream 
            itinerary. From selecting the must-visit monuments that reflect Romania's rich history and culture, to 
            receiving expert transport suggestions and exploring interactive maps, my goal is to make your journey 
            seamless and enjoyable.<br />&emsp;In addition, I went the extra mile by offering comprehensive information 
            on local amenities like police stations, pharmacies and hospitals. I want to ensure that you have access to 
            everything you need during your city break, allowing you to focus on creating unforgettable memories.
            <br />&emsp;At my app, I value your trust and satisfaction. I'll continuously strive to enhance my 
            platform, incorporating user feedback and staying up-to-date with the latest travel trends and 
            technologies. Your journey is my priority, and I am dedicated to delivering a user experience that 
            exceeds your expectations.<br />&emsp;Join me on this exciting adventure through Romania's enchanting 
            cities. Discover the hidden gems, immerse yourself in the vibrant culture, and create memories that 
            will last a lifetime.<br />&emsp;Thank you for choosing my app as your trusted travel companion.
            <br /><br />&emsp;Happy exploring! <br />&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; 
            &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
            &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
            &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Your dev''').classes('text-2xl')

    with ui.footer().style('background-color: #20963d').classes('items-center justify-between'):
        with ui.row():
            ui.label("email:")
            ui.link('soranaantogalan@yahoo.com', 'https://www.yahoo.com/').style('color: #ffffff')
            ui.label(" ")
            ui.label("phone number: +40-749-620-311")
        ui.button('', on_click=lambda: ui.open('https://nicegui.io')).props('flat color=invisible round icon=img:https://nicegui.io/logo_square.png').style('background-color: #4fb357')       
    
    ui.label('About Us').classes('text-2xl')
    if not is_authenticated(request):
        with ui.header(elevated=True).style('background-color: #20963d').classes('items-center justify-between'):
            with ui.row().classes('items-center'):
                ui.button('LOG IN REGISTER', on_click=lambda: ui.open(login)).classes('w-32').props('flat color=invisible')
                ui.button('HOME', on_click=lambda: ui.open(home)).classes('w-32').props('flat color=invisible')
                ui.button('ABOUT US').classes('w-32').props('flat color=invisible')
            

    else:  
        with ui.header(elevated=True).style('background-color: #20963d').classes('items-center justify-between'):
            with ui.row().classes('items-center'):
                ui.button('MY ACCOUT', on_click=lambda: ui.open(login)).classes('w-32').props('flat color=invisible')
                ui.button('HOME', on_click=lambda: ui.open(home)).classes('w-32').props('flat color=invisible')
                ui.button('ABOUT US').classes('w-32').props('flat color=invisible')
                ui.button('PLANS', on_click=lambda: ui.open(plans)).classes('w-32').props('flat color=invisible')
                ui.button('USEFUL MAPS', on_click=lambda: ui.open(useful_maps)).classes('w-32').props('flat color=invisible')


##############################################################################################################
##############################################################################################################
#           City break plans page
##############################################################################################################
##############################################################################################################
locations4 = []

@ui.page('/plans')
async def plans(request: Request, client: Client) -> None:
    with ui.column().classes('absolute inset-0'):
        ui.image('https://i.postimg.cc/Wz3XmPng/bucarest.jpg').classes('absolute inset-0').classes('items-center')
        ui.image('https://i.postimg.cc/Wz3XmPng/bucarest.jpg').classes('absolute').classes('items-center')

    arr = []
    arr2 = []
    
    def change_select_locations():
        cursor.execute('''SELECT idC FROM Cities WHERE name=?''', (city.value,))
        idC_res = cursor.fetchall()
        idC_final_result = [i[0] for i in idC_res]
        city_id = idC_final_result[0]

        cursor.execute('''SELECT name FROM Locations WHERE idC=? AND tag=?''', (city_id, "attractions"))
        name_res = cursor.fetchall()
        name_final_result = [i[0] for i in name_res]


        if(len(name_final_result)==0):
            rowi.clear()
            with rowi:
                ui.label("SORRY, no attractions yet!")
        elif(len(name_final_result)!=0):
            rowi.clear()
            with rowi:
                for i in name_final_result:
                    checkbox = ui.checkbox(i, on_change=do)
                    arr.append(checkbox) 
    def do():
        for el in arr:
            if el.value == True and el.text not in arr2:
                arr2.append(el.text)
            if el.value == False and el.text in arr2:
                arr2.remove(el.text)
        print(arr2)

    cursor.execute('''SELECT name FROM Cities''')
    cities_name_res = cursor.fetchall()
    cities_name_final_result = [j[0] for j in cities_name_res]

    cursor.execute('''SELECT idC FROM Cities WHERE name=?''', (cities_name_final_result[0],))
    idC_res = cursor.fetchall()
    idC_final_result = [i[0] for i in idC_res]
    city_id = idC_final_result[0]


    cursor.execute('''SELECT name FROM Locations WHERE idC=? AND tag=?''', (city_id, "attractions"))
    name_res = cursor.fetchall()
    name_final_result = [i[0] for i in name_res]

    cursor.execute('''SELECT coordX FROM Locations WHERE idC=? AND tag=?''', (city_id, "attractions"))
    coordX_res = cursor.fetchall()
    coordX_final_result = [i[0] for i in coordX_res]

    cursor.execute('''SELECT coordY FROM Locations WHERE idC=? AND tag=?''', (city_id, "attractions"))
    coordY_res = cursor.fetchall()
    coordY_final_result = [i[0] for i in coordY_res]


    cursor.execute('''SELECT name FROM Locations WHERE idC=? AND tag=?''', (city_id, "attractions"))
    name_res = cursor.fetchall()
    name_final_result = [i[0] for i in name_res]
    

    with ui.card().style('opacity:0.7'):
        with ui.row():
            ui.label("Select a city:").classes('left-0 top-10 h-0 w-20')
            city = ui.select(options=cities_name_final_result, value=cities_name_final_result[0], on_change=change_select_locations).classes('left-0 top-10 h-16 w-40')

    with ui.card().style('opacity:0.7'):
        with ui.row() as rowi:
            for i in name_final_result:
                checkbox = ui.checkbox(i, on_change=do)
                arr.append(checkbox)

    map = leaflet().classes('object-cover h-96 w-full')
    await client.connected()
    #print(locations)
    map.set_multi_locations([(45,23,"Cluj")])


    with ui.footer().style('background-color: #20963d').classes('items-center justify-between'):
        with ui.row():
            ui.label("email:")
            ui.link('soranaantogalan@yahoo.com', 'https://www.yahoo.com/').style('color: #ffffff')
            ui.label(" ")
            ui.label("phone number: +40-749-620-311")
        ui.button('', on_click=lambda: ui.open('https://nicegui.io')).props('flat color=invisible round icon=img:https://nicegui.io/logo_square.png').style('background-color: #4fb357')       
    
    if not is_authenticated(request):
        with ui.header(elevated=True).style('background-color: #20963d').classes('items-center justify-between'):
            with ui.row().classes('items-center'):
                ui.button('LOG IN REGISTER', on_click=lambda: ui.open(login)).classes('w-32').props('flat color=invisible')
                ui.button('HOME', on_click=lambda: ui.open(home)).classes('w-32').props('flat color=invisible')
                ui.button('ABOUT US').classes('w-32').props('flat color=invisible')          
            

    if is_authenticated(request): 
        with ui.header(elevated=True).style('background-color: #20963d').classes('items-center justify-between'):
            with ui.row().classes('items-center'):
                ui.button('MY ACCOUT', on_click=lambda: ui.open(login)).classes('w-32').props('flat color=invisible')
                ui.button('HOME', on_click=lambda: ui.open(home)).classes('w-32').props('flat color=invisible')
                ui.button('ABOUT US', on_click=lambda: ui.open(about_us)).classes('w-32').props('flat color=invisible')
                ui.button('PLANS').classes('w-32').props('flat color=invisible')
                ui.button('USEFUL MAPS', on_click=lambda: ui.open(useful_maps)).classes('w-32').props('flat color=invisible')

locations = []
locations2 = []
locations3 = []

##############################################################################################################
##############################################################################################################
#           Useful maps page
##############################################################################################################
##############################################################################################################


@ui.page('/useful_maps')
async def useful_maps(client: Client):
    with ui.footer().style('background-color: #20963d').classes('items-center justify-between'):
        with ui.row():
            ui.label("email:")
            ui.link('soranaantogalan@yahoo.com', 'https://www.yahoo.com/').style('color: #ffffff')
            ui.label(" ")
            ui.label("phone number: +40-749-620-311")
        ui.button('', on_click=lambda: ui.open('https://nicegui.io')).props('flat color=invisible round icon=img:https://nicegui.io/logo_square.png').style('background-color: #4fb357')       

    async def change_display_locations():
        # tag = "pharmacy" for map

        cursor.execute('''SELECT idC FROM Cities WHERE name=?''', (city.value,))
        idC_res = cursor.fetchall()
        idC_final_result = [i[0] for i in idC_res]
        city_id = idC_final_result[0]

        cursor.execute('''SELECT coordX FROM Locations WHERE idC=? AND tag=?''', (city_id, "pharmacy"))
        coordX_res = cursor.fetchall()
        coordX_final_result = [i[0] for i in coordX_res]

        cursor.execute('''SELECT coordY FROM Locations WHERE idC=? AND tag=?''', (city_id, "pharmacy"))
        coordY_res = cursor.fetchall()
        coordY_final_result = [i[0] for i in coordY_res]

        cursor.execute('''SELECT name FROM Locations WHERE idC=? AND tag=?''', (city_id, "pharmacy"))
        name_res = cursor.fetchall()
        name_final_result = [i[0] for i in name_res]


        global locations
        loc = []
        locations = loc
        for i in range(len(name_final_result)):
            a = coordX_final_result[i]
            b = coordY_final_result[i]
            c = name_final_result[i]
            loc.append((a, b, c))
            locations = loc

        
        # tag = "hospital" for map2
        cursor.execute('''SELECT coordX FROM Locations WHERE idC=? AND tag =?''', (city_id, "hospital"))
        coordX_res = cursor.fetchall()
        coordX_final_result = [i[0] for i in coordX_res]


        cursor.execute('''SELECT coordY FROM Locations WHERE idC=? AND tag=?''', (city_id, "hospital"))
        coordY_res = cursor.fetchall()
        coordY_final_result = [i[0] for i in coordY_res]


        cursor.execute('''SELECT name FROM Locations WHERE idC=? AND tag=?''', (city_id, "hospital"))
        name_res = cursor.fetchall()
        name_final_result = [i[0] for i in name_res]

        loc = []
        for i in range(len(name_final_result)):
            a = coordX_final_result[i]
            b = coordY_final_result[i]
            c = name_final_result[i]
            global locations2
            loc.append((a, b, c))
            locations2 = loc


        # tag = "police" for map3
        cursor.execute('''SELECT coordX FROM Locations WHERE idC=? AND tag =?''', (city_id, "police"))
        coordX_res = cursor.fetchall()
        coordX_final_result = [i[0] for i in coordX_res]


        cursor.execute('''SELECT coordY FROM Locations WHERE idC=? AND tag=?''', (city_id, "police"))
        coordY_res = cursor.fetchall()
        coordY_final_result = [i[0] for i in coordY_res]


        cursor.execute('''SELECT name FROM Locations WHERE idC=? AND tag=?''', (city_id, "police"))
        name_res = cursor.fetchall()
        name_final_result = [i[0] for i in name_res]

        loc = []
        for i in range(len(name_final_result)):
            a = coordX_final_result[i]
            b = coordY_final_result[i]
            c = name_final_result[i]
            global locations3
            loc.append((a, b, c))
            locations3 = loc


        # MAP update
        map.set_multi_locations(locations)
        map2.set_multi_locations(locations2)
        map3.set_multi_locations(locations3)


    # GENERATE DEFAULT MAPS
    try:
        # tag = "pharmacy" for map
        cursor.execute('''SELECT name FROM Cities''')
        name_res = cursor.fetchall()
        name_final_result = [j[0] for j in name_res]
        

        cursor.execute('''SELECT idC FROM Cities WHERE name=?''', (name_final_result[0],))
        id_res = cursor.fetchall()
        id_final_result = [j[0] for j in id_res]
    

        cursor.execute('''SELECT coordX FROM Locations WHERE idC=? AND tag =?''', (id_final_result[0], "pharmacy"))
        coordX_res = cursor.fetchall()
        coordX_final_result = [i[0] for i in coordX_res]


        cursor.execute('''SELECT coordY FROM Locations WHERE idC=? AND tag=?''', (id_final_result[0], "pharmacy"))
        coordY_res = cursor.fetchall()
        coordY_final_result = [i[0] for i in coordY_res]


        cursor.execute('''SELECT name FROM Locations WHERE idC=? AND tag=?''', (id_final_result[0], "pharmacy"))
        name_res = cursor.fetchall()
        name_final_result = [i[0] for i in name_res]

        loc = []
        for i in range(len(name_final_result)):
            a = coordX_final_result[i]
            b = coordY_final_result[i]
            c = name_final_result[i]
            global locations
            loc.append((a, b, c))
            locations = loc


        # tag = "hospital" for map2
        cursor.execute('''SELECT coordX FROM Locations WHERE idC=? AND tag =?''', (id_final_result[0], "hospital"))
        coordX_res = cursor.fetchall()
        coordX_final_result = [i[0] for i in coordX_res]


        cursor.execute('''SELECT coordY FROM Locations WHERE idC=? AND tag=?''', (id_final_result[0], "hospital"))
        coordY_res = cursor.fetchall()
        coordY_final_result = [i[0] for i in coordY_res]


        cursor.execute('''SELECT name FROM Locations WHERE idC=? AND tag=?''', (id_final_result[0], "hospital"))
        name_res = cursor.fetchall()
        name_final_result = [i[0] for i in name_res]

        loc = []
        for i in range(len(name_final_result)):
            a = coordX_final_result[i]
            b = coordY_final_result[i]
            c = name_final_result[i]
            global locations2
            loc.append((a, b, c))
            locations2 = loc

        
        # tag = "police" for map3
        cursor.execute('''SELECT coordX FROM Locations WHERE idC=? AND tag =?''', (id_final_result[0], "police"))
        coordX_res = cursor.fetchall()
        coordX_final_result = [i[0] for i in coordX_res]



        
        ########################################################################################
        with ui.column().classes('absolute inset-0'):
            ui.image('https://i.postimg.cc/Wz3XmPng/bucarest.jpg').classes('absolute inset-0').classes('items-center')
            ui.image('https://i.postimg.cc/Wz3XmPng/bucarest.jpg').classes('absolute').classes('items-center')

        cursor.execute('''SELECT name FROM Cities''')
        cities_name_res = cursor.fetchall()
        cities_name_final_result = [j[0] for j in cities_name_res]

        with ui.card().style('opacity:0.7'):
            with ui.row():
                ui.label("Select a city:").classes('left-0 top-10 h-0 w-20')
                city = ui.select(options=cities_name_final_result, value=cities_name_final_result[0], on_change=change_display_locations).classes('left-0 top-10 h-16 w-40')



        # MAPS DISPLAY
        with ui.card().style('opacity:0.7'):
            ui.label('Pharmacies:').classes('text-2xl')
        map = leaflet().classes('object-cover h-96 w-full')
        await client.connected()
        #print(locations)
        map.set_multi_locations(locations)
        #map.clear_map()
        #print(locations)
        #map.set_multi_locations([(47,23,'LOC')])

        with ui.card().style('opacity:0.7'):
            ui.label('Hospitals:').classes('text-2xl')
        map2 = leaflet().classes('object-cover h-96 w-full')
        await client.connected()
        #print(locations)
        map2.set_multi_locations(locations2)

        with ui.card().style('opacity:0.7'):
            ui.label('Police stations:').classes('text-2xl')
        map3 = leaflet().classes('object-cover h-96 w-full')
        await client.connected()
        #print(locations)
        map3.set_multi_locations(locations3)

    except:
        print("You got no cities??")
        



 
    with ui.header(elevated=True).style('background-color: #20963d').classes('items-center justify-between'):
        with ui.row().classes('items-center'):
            ui.button('MY ACCOUT', on_click=lambda: ui.open(login)).classes('w-32').props('flat color=invisible')
            ui.button('HOME', on_click=lambda: ui.open(home)).classes('w-32').props('flat color=invisible')
            ui.button('ABOUT US', on_click=lambda: ui.open(about_us)).classes('w-32').props('flat color=invisible')
            ui.button('PLANS', on_click=lambda: ui.open(plans)).classes('w-32').props('flat color=invisible')
            ui.button('USEFUL MAPS').classes('w-32').props('flat color=invisible')
        




# LOGGED IN PAGE
@ui.page('/')
def page(request: Request) -> None:
    ui.image('https://i.postimg.cc/Wz3XmPng/bucarest.jpg').classes('absolute inset-0')
    if not is_authenticated(request):
        return RedirectResponse('/login')
    session = session_info[request.session['id']]

    def delete_account() -> None:
        # GET ID FROM YOU CLICKING DELETE ACCOUNT BUTTON
        cursor.execute('''SELECT idU FROM Users WHERE name=?''', (session["username"],))
        idC_res1 = cursor.fetchall()
        idC_final_result1 = [i[0] for i in idC_res1]
        get_id.text = idC_final_result1[0]
        #print(idC_final_result) ################################################
        cursor.execute('''DELETE FROM Users WHERE idU=?''',(get_id.text,))
        conn.commit()

        try:
            for el in users:
                if el[0] == session["username"]:
                    users.remove(el)

            name_final_result.remove(session["username"])
        except:
            pass
        
        # SHOW NOTIF IF YOU SUCCEED DELETING DATA FROM TABLE
        ui.notify("success delete",color="red")
        ui.open('/logout')
    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    def edit_name() -> None:
        old_name = session["username"]
        # GET ID FROM YOU CLICKING DELETE ACCOUNT BUTTON
        cursor.execute('''SELECT idU FROM Users WHERE name=?''', (old_name,))
        idC_res = cursor.fetchall()
        idC_final_result = [i[0] for i in idC_res]
        get_id.text = idC_final_result[0]

        def update_name():
            dialog3.close()

            name_final_result = update_name_list()
            if(new_name.value!="" and new_name.value != old_name and new_name.value not in name_final_result):
                #cursor.execute('''UPDATE Users SET name = {new_name.value} WHERE idU = {get_id.text}''')
                try:
                    query = '''UPDATE Users SET name =? WHERE idU=?'''
                    cursor.execute(query,(new_name.value, get_id.text))
                    conn.commit()


                    # SHOW NOTIF IF SUCCES EDIT
                    ui.notify("succes update name!", color="green")
                    ui.open('logout')
                    
                except Exception as e:
                    print(e)
            elif (new_name.value==""):
                pass
                #ui.notify("Empty",color='red')
            elif (new_name.value==old_name):
                ui.notify("You entered the same name.")
            else:
                ui.notify("Name already in use.")
            

        with ui.dialog() as dialog3, ui.card().classes('items-center justify-between'):
            new_name = ui.input('New username').on('keydown.enter', update_name)
            ui.button('Close', on_click = update_name)
        dialog3.open()

    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    def edit_password() -> None:
        old_name = session["username"]
        # GET ID FROM YOU CLICKING DELETE ACCOUNT BUTTON
        cursor.execute('''SELECT idU FROM Users WHERE name=?''', (old_name,))
        idC_res = cursor.fetchall()
        idC_final_result = [i[0] for i in idC_res]
        get_id.text = idC_final_result[0]


        def update_password():
            if new_password.value != '' and new_password.value != old_password.value:
                # convert the password to bytes
                new_password_bytes = new_password.value.encode('utf-8')
                # create a hash object using SHA-256 algorithm
                hash_object = hashlib.sha256()
                # update the hash object with the password bytes
                hash_object.update(new_password_bytes)
                # get the hash value as a hexadecimal string
                hash_value_new_password = hash_object.hexdigest()


                #print("update password")
                query = '''UPDATE Users SET password =? WHERE idU=?'''
                cursor.execute(query,(hash_value_new_password, get_id.text))
                conn.commit()
                dialog5.close()

                 # SHOW NOTIF IF SUCCES EDIT
                ui.notify("succes update!", color="green") 


            elif new_password.value == "":
                #ui.notify('Empty', color='red')
                dialog5.close()
                pass
            elif new_password.value == old_password.value:
                ui.notify('Same password', color='red')
                dialog5.close()

    
        def check_password():
            # convert the password to bytes
            old_password_bytes = old_password.value.encode('utf-8')
            # create a hash object using SHA-256 algorithm
            hash_object = hashlib.sha256()
            # update the hash object with the password bytes
            hash_object.update(old_password_bytes)
            # get the hash value as a hexadecimal string
            hash_value_old_password = hash_object.hexdigest()
            #print(hash_value)
            users = update_users()
            if (session["username"], hash_value_old_password) in users:

                dialog4.close()
                dialog5.open()
            elif (old_password.value == ""):
                pass
                dialog4.close()
            else:
                ui.notify('Wrong password', color='red')
                dialog4.close()
        
        with ui.dialog() as dialog4, ui.card().classes('items-center justify-between'):
            old_password = ui.input('Current password').props('type=password').on('keydown.enter', check_password)
            ui.button('Close', on_click = check_password)
        dialog4.open()

        with ui.dialog() as dialog5, ui.card().classes('items-center justify-between'):
            new_password = ui.input('New password').props('type=password').on('keydown.enter', update_password)
            ui.button('Close', on_click = update_password)
        dialog4.open()

    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    # CREATE ID TEXT FOR GET ID
    get_email = ui.label()
    check = 1
    def edit_email() -> None:

        name = session["username"]
        # GET ID FROM YOU CLICKING DELETE ACCOUNT BUTTON
        cursor.execute('''SELECT email FROM Users WHERE name=?''', (name,))
        idU_res = cursor.fetchall()
        idU_final_result = [i[0] for i in idU_res]
        get_email.text = idU_final_result[0]
        
        def check_email():
            cursor.execute('''SELECT email FROM Users''')
            email_res = cursor.fetchall()
            email_final_result = [i[0] for i in email_res]

            if new_email.value != '' and new_email.value != get_email.text and new_email.value not in email_final_result:
                new_code = str(random_with_N_digits(4))
                email_receiver = str(new_email.value)

                # now I have to define the subject and the body of the e-mail
                subject = "E-mail validation"
                body = """
                Your access code is :
                """ + new_code

                em = EmailMessage()   # object that I'll use to write the email
                # define some elements of the email
                em['From'] = email_sender
                em['To'] = email_receiver
                em['Subject'] = subject
                em.set_content(body)

                # in order to add a layer of security I'm going to import ssl
                context = ssl.create_default_context()
                try:
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                        smtp.login(email_sender, email_password)
                        smtp.sendmail(email_sender, email_receiver, em.as_string()) # em.as_string() --> here we have all 
                        # the email elements From, To, Subject, body and we're giving a proper form with this 
                        # as_string()

                    def open_dialog_code():
                        def check_equality():
                            inserted_code = val_code.value
                            
                            try:
                                dialog.close()
                                if(int(inserted_code)==int(new_code)):
                                    query = '''UPDATE Users SET email =? WHERE name=?'''
                                    cursor.execute(query,(new_email.value, name))
                                    conn.commit()
                                    # SHOW NOTIF IF SUCCESS ADD TO TABLE
                                    ui.notify("E-mail updated", color='blue')

                                    
                                    # CLEAR INPUT
                                    new_email.value = ""
                                    dialog.close()
                                    dialog6.close()
                                    
                                    
                                else:
                                    ui.notify(f"Wrong code, retry.", color='red')
                            except:
                                pass


                        with ui.dialog() as dialog, ui.card():
                            ui.label('Enter your code:')
                            val_code = ui.input('Value').on('keydown.enter', check_equality)
                            ui.button('Close', on_click=check_equality)
                        dialog.open()

                        if check == 1:
                            ui.button('Enter code', on_click=dialog.open)
                            add_one()

                    open_dialog_code()

                except:
                    ui.notify('Incorrect e-mail', color='red')
                
                

            elif new_email.value == "":
                ui.notify('Empty', color='red')
            elif new_email.value == get_email.text:
                ui.notify('Same e-mail', color='red')
            elif new_email.value in email_final_result:
                ui.notify('E-mail already in use', color='red')

    

        with ui.dialog() as dialog6, ui.card().classes('items-center justify-between'):
            new_email = ui.input('New e-mail').on('keydown.enter', check_email)
            with ui.row():
                ui.button('Close', on_click = dialog6.close)
                ui.button('Send e-mail', on_click=check_email)
        dialog6.open()
            

        
    with ui.dialog() as dialog, ui.card().classes('items-center justify-between'):
        ui.label('Are you sure you want to delete your account?')
        with ui.row():
            ui.button('No', on_click=dialog.close)
            ui.button('Yes', on_click=delete_account).classes("bg-red")

    with ui.column().classes('absolute left-10 top-10'):                            
        ui.button('Delete account', on_click=dialog.open)
        ui.button('Change name', on_click=edit_name)
        ui.button('Change password', on_click=edit_password)
        ui.button('Change e-mail', on_click=edit_email)

    with ui.column().classes('absolute-center items-center'):
        with ui.card().style('opacity:0.7'):
            ui.label(f'Hello {session["username"]}!').classes('text-2xl')
        # NOTE we navigate to a new page here to be able to modify the session cookie (it is only editable while a request is en-route)
        # see https://github.com/zauberzeug/nicegui/issues/527 for more details
        ui.button('', on_click=lambda: ui.open('/logout')).props('flat color=invisible round icon=logout').style('background-color: #4fb357')

    with ui.header(elevated=True).style('background-color: #20963d').classes('items-center justify-between'):
        with ui.row().classes('items-center'):
            ui.button('MY ACCOUT').classes('w-32').props('flat color=invisible')
            ui.button('HOME', on_click=lambda: ui.open(home)).classes('w-32').props('flat color=invisible')
            ui.button('ABOUT US', on_click=lambda: ui.open(about_us)).classes('w-32').props('flat color=invisible')
            ui.button('PLANS', on_click=lambda: ui.open(plans)).classes('w-32').props('flat color=invisible')
            ui.button('USEFUL MAPS', on_click=lambda: ui.open(useful_maps)).classes('w-32').props('flat color=invisible')
            
    with ui.footer().style('background-color: #20963d').classes('items-center justify-between'):
        with ui.row():
            ui.label("email:")
            ui.link('soranaantogalan@yahoo.com', 'https://www.yahoo.com/').style('color: #ffffff')
            ui.label(" ")
            ui.label("phone number: +40-749-620-311")
        ui.button('', on_click=lambda: ui.open('https://nicegui.io')).props('flat color=invisible round icon=img:https://nicegui.io/logo_square.png').style('background-color: #4fb357')       
    
check = 1
def add_one():
    global check
    check = check + 1     
def make_check_one():
    global check
    check = 1  


# LOG IN PAGE
@ui.page('/login')
def login(request: Request) -> None:
    ui.image('https://i.postimg.cc/Wz3XmPng/bucarest.jpg').classes('absolute inset-0')
    def try_login() -> None:  # local function to avoid passing username and password as arguments
        # convert the password to bytes
        password_bytes = password.value.encode('utf-8')
        # create a hash object using SHA-256 algorithm
        hash_object = hashlib.sha256()
        # update the hash object with the password bytes
        hash_object.update(password_bytes)
        # get the hash value as a hexadecimal string
        hash_value = hash_object.hexdigest()
        #print(hash_value)

        users = update_users()
        a = "admin"

        if(username.value == a and password.value == a):
            ui.open(admin_control)
            username.value = ""
            password.value = ""
        elif (username.value, hash_value) in users:
            session_info[request.session['id']] = {'username': username.value, 'authenticated': True}
            ui.open('/')
        else:
            ui.notify('Wrong username or password', color='negative')

    if is_authenticated(request):
        return RedirectResponse('/')
    request.session['id'] = str(uuid.uuid4())  # NOTE this stores a new session ID in the cookie of the client

    ################################################################################################
    ################################################################################################
    ################################################################################################
    ################################################################################################
    def recover():
        cursor.execute('''SELECT email FROM Users''')
        email_res = cursor.fetchall()
        email_final_result = [i[0] for i in email_res]


        new_code = str(random_with_N_digits(4))
        
        def display_email():
            if user_email.value not in email_final_result:
                ui.notify("incorrect e-mail", color="yellow")
            else:
                ui.notify("ok", color="yellow")


                query = '''SELECT name FROM Users WHERE email=?'''
                cursor.execute(query,(user_email.value,))
                name_res = cursor.fetchall()
                name_final_result = [i[0] for i in name_res]


                #new_code = str(random_with_N_digits(4))
                email_receiver = str(user_email.value)

                # now I have to define the subject and the body of the e-mail
                subject = "E-mail validation"
                body = "Your name is : " + str(name_final_result[0]) + "\nYour access code is :" + str(new_code)

                em = EmailMessage()   # object that I'll use to write the email
                # define some elements of the email
                em['From'] = email_sender
                em['To'] = email_receiver
                em['Subject'] = subject
                em.set_content(body)

                # in order to add a layer of security I'm going to import ssl
                context = ssl.create_default_context()
                try:
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                        smtp.login(email_sender, email_password)
                        smtp.sendmail(email_sender, email_receiver, em.as_string()) # em.as_string() --> here we have all 
                        # the email elements From, To, Subject, body and we're giving a proper form with this 
                        # as_string()
                    open_dialog_code()
                    
                except:
                    ui.notify('Incorrect e-mail', color='red')

        def check_equality():
            inserted_code = val_code.value
            
            try:
                dialog7.close()
                if(int(inserted_code)==int(new_code)):

                    query = '''SELECT password FROM Users WHERE email=?'''
                    cursor.execute(query,(user_email.value,))
                    pass_res = cursor.fetchall()
                    pass_final_result = [i[0] for i in pass_res]


                    def check_equality_pass():
                        # convert the password to bytes
                        new_password_bytes = new_pass.value.encode('utf-8')
                        # create a hash object using SHA-256 algorithm
                        hash_object = hashlib.sha256()
                        # update the hash object with the password bytes
                        hash_object.update(new_password_bytes)
                        # get the hash value as a hexadecimal string
                        hash_value_new_password = hash_object.hexdigest()


                        # convert the password to bytes
                        confirm_password_bytes = confirm_pass.value.encode('utf-8')
                        # create a hash object using SHA-256 algorithm
                        confirm_hash_object = hashlib.sha256()
                        # update the hash object with the password bytes
                        confirm_hash_object.update(confirm_password_bytes)
                        # get the hash value as a hexadecimal string
                        hash_value_confirm_password = confirm_hash_object.hexdigest()


                        if new_pass.value == '' or confirm_pass.value == '':
                            ui.notify("Empty", color='blue')
                            pass_dialog.close()
                        elif hash_value_new_password in pass_final_result or hash_value_confirm_password in pass_final_result:
                            ui.notify("Same password", color='blue')
                            pass_dialog.close()
                        elif new_pass.value == confirm_pass.value and new_pass.value != '' and confirm_pass.value != '' and hash_value_new_password not in pass_final_result:
                            #print("update password")
                            query = '''UPDATE Users SET password =? WHERE email=?'''
                            cursor.execute(query,(hash_value_new_password, user_email.value))
                            conn.commit()

                            # SHOW NOTIF IF SUCCES EDIT
                            ui.notify("Password updated", color='green')
                            dialog.close()
                            pass_dialog.close()
                        else:
                            new_pass.value = ""
                            confirm_pass.value = ""
                            ui.notify("Password not matching", color='red')

                    

                    with ui.dialog() as pass_dialog, ui.card().classes('items-center justify-between'):
                        ui.label('Enter your new password:')
                        new_pass = ui.input('password').props('type=password').on('keydown.enter', check_equality_pass)
                        confirm_pass = ui.input('confirm password').props('type=password').on('keydown.enter', check_equality_pass)
                        ui.button('Close', on_click=check_equality_pass)
                    pass_dialog.open()
                    
                    
                else:
                    ui.notify(f"Wrong code, retry.", color='red')
            except:
                pass   



        def open_dialog_code():
            dialog.open()

            if check == 1:
                ui.button('Enter code', on_click=dialog.open)
                add_one()
 




        with ui.dialog() as dialog, ui.card().classes('items-center justify-between'):
            make_check_one()
            val_code = ui.input('Enter your code').on('keydown.enter', check_equality)
            with ui.row():
                ui.button('Close', on_click=dialog.close)
                ui.button('Verify', on_click=check_equality)


        with ui.dialog() as dialog7, ui.card().classes('items-center justify-between'):
            user_email = ui.input('Your e-mail').on('keydown.enter', display_email)
            with ui.row():
                ui.button('Close', on_click = dialog7.close)
                ui.button('Send e-mail', on_click=display_email)
        dialog7.open()

        


    
    #with ui.card().classes('absolute-center items-center').props('flat color=invisible'):
    with ui.card().classes('absolute-center items-center'):
        username = ui.input('Username').on('keydown.enter', try_login)
        password = ui.input('Password').props('type=password').on('keydown.enter', try_login)
        ui.button('Log in', on_click=try_login)
        ui.button('Recover account', on_click=recover)
    ui.button('Register', on_click=lambda: ui.open(register)).classes('absolute left-10 top-10')

    with ui.header(elevated=True).style('background-color: #20963d').classes('items-center justify-between'):
        with ui.row().classes('items-center'):
            ui.button('LOG IN REGISTER').classes('w-32').props('flat color=invisible')
            ui.button('HOME', on_click=lambda: ui.open(home)).classes('w-32').props('flat color=invisible')
            ui.button('ABOUT US', on_click=lambda: ui.open(about_us)).classes('w-32').props('flat color=invisible')
       





# dumnb funtion to show "Enter code" button only once
check = 1



# REGISTERED PAGE
@ui.page('/register')
def register(request: Request) -> None:
    ui.image('https://i.postimg.cc/Wz3XmPng/bucarest.jpg').classes('absolute inset-0')
    
    cursor.execute('''SELECT email FROM Users''')
    email_res = cursor.fetchall()
    email_final_result = [i[0] for i in email_res]
    

    def try_register() -> None:
        if username.value == '' or password.value == '' or email.value == '':
            ui.notify('Empty', color='red')
        if password.value != confirm_password.value and username.value != '' and password.value != '':
            ui.notify('Password not matching', color='red')
            password.value = ""
            confirm_password.value = ""
        else:
            # convert the password to bytes
            password_bytes = password.value.encode('utf-8')
            # create a hash object using SHA-256 algorithm
            hash_object = hashlib.sha256()
            # update the hash object with the password bytes
            hash_object.update(password_bytes)
            # get the hash value as a hexadecimal string
            hash_value = hash_object.hexdigest()
            #print(hash_value)
            
            name_final_result = update_name_list()

            if username.value in name_final_result:
                ui.notify('Username already existent', color='red')
                username.value = ""

            if email.value in email_final_result:
                ui.notify('Email already in use', color='red')
                email.value = ""

            # ALL CONDITIONS HAVE BEEN CHECKED, YOU CAN ADD USER TO DB
            if username.value not in name_final_result and email.value not in email_final_result and username.value != '' and password.value != '':
                email_receiver = str(email.value)

                # now I have to define the subject and the body of the e-mail
                subject = "E-mail validation"
                body = """
                Your access code is :
                """ + code

                em = EmailMessage()   # object that I'll use to write the email
                # define some elements of the email
                em['From'] = email_sender
                em['To'] = email_receiver
                em['Subject'] = subject
                em.set_content(body)

                # in order to add a layer of security I'm going to import ssl
                context = ssl.create_default_context()
                try:
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                        smtp.login(email_sender, email_password)
                        smtp.sendmail(email_sender, email_receiver, em.as_string()) # em.as_string() --> here we have all 
                        # the email elements From, To, Subject, body and we're giving a proper form with this 
                        # as_string()


                    def open_dialog_code():
                        def check_equality():
                            dialog.close()
                            inserted_code = val_code.value
                            try:
                                if(int(inserted_code)==int(code)):
                                    users.append((username.value, hash_value))
                                    email_final_result.append(email.value)
                                    name_final_result.append(username.value)
                                    cursor.execute('''INSERT INTO Users (name, email, password, type) VALUES (?,?,?,?)''', (username.value, email.value, hash_value, "user"))
                                    conn.commit()
                                    # SHOW NOTIF IF SUCCESS ADD TO TABLE
                                    ui.notify(f"You have been registered, {username.value}", color='blue')

                                    
                                    # CLEAR INPUT username, email AND password
                                    username.value = ""
                                    email.value = ""
                                    password.value = ""
                                    confirm_password.value = ""

                                    ui.open('/login')
                                    make_check_one()
                                else:
                                    ui.notify(f"Wrong code, retry.", color='red')
                            except:
                                pass


                        with ui.dialog() as dialog, ui.card():
                            ui.label('Enter your code:')
                            val_code = ui.input('Value').on('keydown.enter', check_equality)
                            ui.button('Close', on_click=check_equality)
                        dialog.open()

                        if check == 1:
                            ui.button('Enter code', on_click=dialog.open)
                            add_one()

                    open_dialog_code()

                except:
                    ui.notify('Incorrect e-mail', color='red')
    

    with ui.card().classes('absolute-center items-center'):
        username = ui.input('Username').on('keydown.enter', try_register)
        email = ui.input('Email').on('keydown.enter', try_register)
        password = ui.input('Password').props('type=password').on('keydown.enter', try_register)
        confirm_password = ui.input('Confirm password').props('type=password').on('keydown.enter', try_register)
        ui.button('Send e-mail', on_click=try_register)
    ui.button('Log in', on_click=lambda: ui.open(login)).classes('absolute left-10 top-10')

    with ui.header(elevated=True).style('background-color: #20963d').classes('items-center justify-between'):
        with ui.row().classes('items-center'):
            ui.button('LOG IN REGISTER').classes('w-32').props('flat color=invisible')
            ui.button('HOME', on_click=lambda: ui.open(home)).classes('w-32').props('flat color=invisible')
            ui.button('ABOUT US', on_click=lambda: ui.open(about_us)).classes('w-32').props('flat color=invisible')
        
    

@ui.page('/logout')
def logout(request: Request) -> None:
    if is_authenticated(request):
        session_info.pop(request.session['id'])
        request.session['id'] = None
        return RedirectResponse('/login')
    return RedirectResponse('/')

ui.run()