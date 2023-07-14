import sqlite3
from nicegui import ui
from collections import defaultdict

conn = sqlite3.connect("DB/test.db", check_same_thread=False)
cursor = conn.cursor()


@ui.page('/admin_location')
def admin_location():
    name =  ui.input(label="Location name").classes("w-full")

    tags = ["pharmacy", "hospital", "police", "attractions", "bus station"]
    tag =  ui.select(tags, label="Location tag").classes("w-full")

    coordX =  ui.input(label="Location coordX").classes("w-full")
    coordY =  ui.input(label="Location coordY").classes("w-full")
    open =  ui.input(label="Location open hours").classes("w-full")
    closed =  ui.input(label="Location closed hours").classes("w-full")

    cursor.execute('''SELECT idC FROM Cities''')
    idC_res = cursor.fetchall()
    idC_final_result = [i[0] for i in idC_res]

    cursor.execute('''SELECT name FROM Cities''')
    name_res = cursor.fetchall()
    name_final_result = [j[0] for j in name_res]

    dictionary = defaultdict(list)
    for key in idC_final_result:
        dictionary.setdefault(key,[])
    count = 0
    for i in idC_final_result:
        dictionary[i].append(name_final_result[count])
        count += 1

    ###################################################################################
    # u need to make select take the id of the city, not the name!!
    idC =  ui.select(dictionary, label="Select a City").classes("w-full")

    address = ui.input(label="Location address").classes("w-full")

    # CREATE ID TEXT FOR GETTING ID WHEN YOU CLICK EDIT AND DELETE BUTTON
    get_id = ui.label()


    #ADD NEW DATA
    def addnewdata():
        try:
            cursor.execute('''SELECT name FROM Locations''')
            loc_name_res = cursor.fetchall()
            loc_name_final_result = [i[0] for i in loc_name_res]

            if name.value not in loc_name_final_result:

                cursor.execute('''INSERT INTO Locations (name, tag, coordX, coordY, open, closed, idC, address) VALUES(?,?,?,?,?,?,?,?)''', (name.value, tag.value, coordX.value, coordY.value, open.value, closed.value, idC.value, address.value))
                conn.commit()
                #SHOW NOTIF IF SUCCESS ADD TO TABLE
                ui.notify(f"success add new data {name.value}", color="blue")

                #CLEAR INPUT NAME, TAG, COORDX AND Y, ...
                name.value = ""
                tag.value = ""
                coordX.value = ""
                coordY.value = ""
                open.value = ""
                closed.value = ""
                idC.value = ""
                address.value = ""
                #CLEAR ALL DATA IN LIST AND GET AGAIN
                list_alldata.clear()
                get_all_data()
            else:
                # SHOW NOTIF IF UNSUCCES ADD TO TABLE
                ui.notify(f"Location already existent", color="bg-red")

        except Exception as e:
            print(e)




    ui.button("add new data",
        on_click=addnewdata
        )

    list_alldata = ui.column()

    # FUNCTION FOR SAVE AND EDIT AFTER YOU CLICK "SAVE" IN DIALOG
    def saveandedit(e):
        try:
            query = '''UPDATE Locations SET name=?, tag=?, coordX=?, coordY=?, open=?, closed=?, idC=?, address=? WHERE idL=?'''
            cursor.execute(query,(edit_name.value, edit_tag.value, edit_coordX.value, edit_coordY.value, edit_open.value, edit_closed.value, edit_idC.value, edit_address.value, get_id.text))
            conn.commit()

            # AND SHOW NOTIF IF SUCCESS EDIT
            ui.notify("success edit", color="green")
            # AND CLOSE EDIT DIALOG
            editdialog.close()

            # AND CLEAR list_alldata AND CALL FUNCTION GET TABLE AGAIN
            list_alldata.clear()
            get_all_data()

        except Exception as e:
            print(e)



    # AND NOW CREATE DIALOG EDIT
    with ui.dialog() as editdialog:
        with ui.card():
            ui.label("Edit Data").classes("front-xl front-weight")

            # THIS INPUT IS GET VALUE FROM name, tag, ... textfields AND AUTO SET HERE
            edit_name = ui.input().bind_value_from(name, "value")
            edit_tag = ui.input().bind_value_from(tag, "value")
            edit_coordX = ui.input().bind_value_from(coordX, "value")
            edit_coordY = ui.input().bind_value_from(coordY, "value")
            edit_open = ui.input().bind_value_from(open, "value")
            edit_closed = ui.input().bind_value_from(closed, "value")
            edit_idC = ui.input().bind_value_from(idC, "value")
            edit_address = ui.input().bind_value_from(address, "value")

            # AND CREATE BUTTON SAVE EDIT AND CLOSE BUTTON
            with ui.row().classes("justify-between"):
                ui.button("save", on_click= lambda e : saveandedit(e))
                # FOR CLOSE DIALOG
                ui.button("close", on_click= editdialog.close).classes("bg-red")




    # FOR EDIT FUNCTION
    def editdata(x):
        # AND NOW GET ID FROM YOU CLICKING EDIT BUTTON

        get_id.text = x.default_slot.children[0].text

        # AND SET NAME TEXTFIELD FROM YOU CLICKING EDIT BUTTON
        name.value = x.default_slot.children[1].text
        tag.value = x.default_slot.children[2].text
        coordX.value = x.default_slot.children[3].text
        coordY.value = x.default_slot.children[4].text
        open.value = x.default_slot.children[5].text
        closed.value = x.default_slot.children[6].text
        idC.value = x.default_slot.children[7].text
        address.value = x.default_slot.children[8].text

        # AND OPEN THE DIALOG EDIT
        editdialog.open()
        ui.update()



    # FOR DELETE FUNCTION
    def detele_location(x):
        # GET ID FROM YOU CLICKING BUTTON DELETE

        get_id.text = x.default_slot.children[0].text
        cursor.execute('''DELETE FROM Locations WHERE idL=?''',(get_id.text,))
        conn.commit()

        # CLEAR ALL DATA THEN CALL FUNCTION AGAIN FROM TABLE
        list_alldata.clear()
        get_all_data()

        # SHOW NOTIF IF YOU SUCCEED DELETING DATA FROM TABLE
        ui.notify("success delete", color="red")




    # GET ALL DATA FROM TABLE
    def get_all_data():
        cursor.execute('''SELECT * FROM Locations ''')
        res = cursor.fetchall()
        result = []
        for row in res:
            # AND CONVERT TO DICT JSON ARRAY
            data = {}
            for i, col in enumerate(cursor.description):
                data[col[0]] = row[i]
            result.append(data)
        print(result)

        # AND NOW AFTER GET ALL DATA FROM TABLE THEN CREATE CARD
        # FOR SEE DATA IN SCREEN APP
        for x in result:
            with list_alldata:
                # CREATE CARD FOR EDIT AND DELETE AND DATA
                with ui.card():
                    with ui.column():
                        with ui.row().classes("justify-between w-full") as carddata:
                            ui.label(x['idL'])
                            ui.label(x['name'])
                            ui.label(x['tag'])
                            ui.label(x['coordX'])
                            ui.label(x['coordY'])
                            ui.label(x['open'])
                            ui.label(x['closed'])
                            ui.label(x['idC'])
                            ui.label(x['address'])
                        with ui.row():
                            # AND CREATE EDIT AND DELETE BUTTON
                            ui.button("edit").on("click", lambda e, carddata = carddata : editdata(carddata))

                            # AND DELETE
                            ui.button("delete").on("click", lambda e, carddata = carddata : detele_location(carddata)).classes("bg-red")


    # CALL FUNTION WHEN APP FIRST OPEN OR RUNNING
    get_all_data()

#ui.run()