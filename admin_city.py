#THE ADMIN PAGE (Purpose: interacting with the DB to popupate the static tables.)
import sqlite3
from nicegui import ui
from admin_locations import admin_location
from admin_commontransport import admin_commontransport
from admin_locations_stations import admin_locations_stations

conn = sqlite3.connect("DB/test.db", check_same_thread=False)
cursor = conn.cursor()


@ui.page('/admin_city')
def admin_city():
    name =  ui.input(label="City name").classes("w-full")

    # CREATE ID TEXT FOR GET ID WHEN YOU CLICK EDIT AND DELETE BUTTON
    get_id = ui.label()

    #ADD NEW DATA
    def addnewdata():
        try:
            cursor.execute('''SELECT name FROM Cities''')
            name_res = cursor.fetchall()
            name_final_result = [i[0] for i in name_res]

            if name.value not in name_final_result:
                cursor.execute('''INSERT INTO Cities (name) VALUES (?)''', (name.value,))
                conn.commit()
                # SHOW NOTIF IF SUCCES ADD TO TABLE
                ui.notify(f"succes add new data {name.value}", color="blue")

                # CLEAR INPUT NAME
                name.value = ""
                #CLEAR ALL DATA IN LIST AND GET AGAIN
                list_alldata.clear()
                get_all_data()
            else:
                # SHOW NOTIF IF UNSUCCES ADD TO TABLE
                ui.notify(f"City already existent", color="bg-red")
        except Exception as e:
            print(e)

    ui.button("add new City",
        on_click=addnewdata      
        )



    list_alldata = ui.column()


    # FUNCTION FOR SAVING EDIT AFTER CLICKING SAVE IN DIALOG
    def saveandedit(e):
        try:
            query = '''UPDATE Cities SET name =? WHERE idC=?'''
            cursor.execute(query,(edit_name.value, get_id.text))
            conn.commit()

            # SHOW NOTIF IF SUCCES EDIT
            ui.notify("succes edit!", color="green")
            # AND CLOSE EDIT DIALOG
            editdialog.close()

            # CLEAR list_alldata AND CALL FUNCTION GET TABLE AGAIN
            list_alldata.clear()
            get_all_data()
        except Exception as e:
            print(e)



    # CREATE DIALOG EDIT
    with ui.dialog() as editdialog:
        with ui.card():
            ui.label("Edit City").classes("front-xl font-weight")

            # THIS INPUT IS GET VALUE FROM name TEXTFIELD ANS AUTO SET HERE
            edit_name = ui.input().bind_value_from(name, "value")


            # AND CREATE BUTTON SAVE EDIT AND CLOSE BUTTON
            with ui.row().classes("justify-between"):
                ui.button("save", on_click= lambda e: saveandedit(e))
                # FOR CLOSE DIALOG
                ui.button("close", on_click= editdialog.close).classes("bg-red")




    # FOR EDIT FUNCTION
    def editdata(x):
        # AND NOW GET ID FROM CLICKING EDIT BUTTON
        get_id.text = x.default_slot.children[0].text

        # AND SET NAME TEXTFIELD FROM CLICKING EDIT BUTTON
        name.value = x.default_slot.children[1].text

        # AND OPEN THE DIALOG EDIT
        editdialog.open()
        ui.update()



    # FOR DELETE
    def delete_city(x):
        # GET ID FROM CLICKING BUTTON DELETE
        try:
            get_id.text = x.default_slot.children[0].text

            cursor.execute('''SELECT idC FROM Locations''')
            idC_res = cursor.fetchall()
            idC_final_result = [i[0] for i in idC_res]

            if get_id.text not in idC_final_result:
                cursor.execute('''DELETE FROM Cities WHERE idC=?''',(get_id.text,))
                conn.commit()

                # CLEAN ALL DATA THEN CALL FUNCTION AGAIN FROM TABLE
                list_alldata.clear()
                get_all_data()

                # AND SHOW NOTIF IF YOU SUCCESFULY DELETE DATA FROM TABLE
                ui.notify("succes delete", color="red")
            else:
                # SHOW NOTIF IF UNSUCCES ADD TO TABLE
                ui.notify(f"There are Locations linked to this City", color="bg-red")
        except Exception as e:
            print(e)



    # GET ALL DATA FROM TABLE
    def get_all_data():
        cursor.execute('''SELECT * FROM Cities''')
        res = cursor.fetchall()
        result = []
        for row in res:
            # AND CONVERT TO DICT JSON ARRAY
            data = {}
            for i, col in enumerate(cursor.description):
                data[col[0]] = row [i]
            result.append(data)
        print(result)

        # AND NOW AFTER GET ALL DATA FROM TABLE THEN CREATE CARD
        # FOR SEE DATA IN SCREEN APP
        for x in result:
            with list_alldata:
                # CREATE CARD FOR EDIT AND DELETE DATA
                with ui.card():
                    with ui.column():
                        with ui.row().classes("justify-between w-full") as carddata:
                            ui.label(x['idC'])
                            ui.label(x['name'])
                            
                        with ui.row():
                            # AND CREATE EDIT AND DELETE BUTTON
                            ui.button("edit").on("click", lambda e, carddata=carddata : editdata(carddata))

                            # CREATE A DIALOG TO CHECK IF YOU'RE SURE ABOUT DELETING THE CITY
                            with ui.dialog() as dialog, ui.card():
                                ui.label('Are you sure you want to delete this City?')
                                ui.button('No', on_click=dialog.close)
                                ui.button('Yes', on_click=lambda e, carddata=carddata : delete_city(carddata)).classes("bg-red")
                            # AND DELETE
                            ui.button("delete").on("click", dialog.open).classes("bg-red")


    # AND CALL FUNTION WHEN APP FIRST OPEN OR RUNNING
    get_all_data()

@ui.page('/admin_control')
def admin_control():
    ui.link('Edit City table', admin_city)
    ui.link('Edit Locations table', admin_location)
    ui.link('Edit Locations_Stations table', admin_locations_stations)
    ui.link('Edit CommonTransport table', admin_commontransport)


ui.run()