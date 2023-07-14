import sqlite3
from nicegui import ui

conn = sqlite3.connect("DB/test.db", check_same_thread=False)
cursor = conn.cursor()


@ui.page('/admin_locations_stations')
def admin_locations_stations():
    cursor.execute('''SELECT idL FROM Locations WHERE tag IN ("church", "public")''')
    idL_res = cursor.fetchall()
    idL_final_result = [i[0] for i in idL_res]

    cursor.execute('''SELECT name FROM Locations WHERE tag IN ("church", "public")''')
    name_res = cursor.fetchall()
    name_final_result = [j[0] for j in name_res]


    dictionary = {}
    for key in idL_final_result:
        dictionary.setdefault(key,[])
    for i in range (len(name_final_result)):
        dictionary[idL_final_result[i]].append(name_final_result[i])

    idL =  ui.select(dictionary, label="First location").classes("w-full")
    print(idL.value)
    idL2 =  ui.select(dictionary, label="Second location").classes("w-full")



    cursor.execute('''SELECT idL FROM Locations WHERE tag LIKE 'bus station' ''')
    idL34_res = cursor.fetchall()
    idL34_final_result = [i[0] for i in idL34_res]

    cursor.execute('''SELECT name FROM Locations WHERE tag LIKE 'bus station' ''')
    name34_res = cursor.fetchall()
    name34_final_result = [j[0] for j in name34_res]

    dictionary1 = {}
    for key in idL34_final_result:
        dictionary1.setdefault(key,[])
    for i in range (len(name34_final_result)):
        dictionary1[idL34_final_result[i]].append(name34_final_result[i])


    idL3 =  ui.select(dictionary1, label="First station").classes("w-full")
    idL4 =  ui.select(dictionary1, label="Second station").classes("w-full")

    print(idL.value)


    # CREATE ID TEXT FOR GET ID WHEN YOU CLICK EDIT AND DELETE BUTTON
    get_id = ui.label()


    # ADD NEW DATA
    def addnewdata():
        try:
            if idL.value != idL2.value and idL3.value != idL4.value:
                cursor.execute('''INSERT INTO LocationsStations  (idL, idL2, idL3, idL4) VALUES(?,?,?,?)''',(idL.value, idL2.value, idL3.value, idL4.value))
                conn.commit()
                # SHOW NOTIF IF SUCCESS ADD TO TABLE
                ui.notify(f"success add new data {idL.value}, {idL2.value} and stations: {idL3.value}, {idL4.value}",color="blue")

                # CLEAR INPUT station_in AND station_out
                idL.value = ""
                idL2.value = ""
                idL3.value = ""
                idL4.value = ""
                # CLEAR ALL DATA IN LIST AND GET AGAIN
                list_alldata.clear()
                get_all_data()
            else:
                # SHOW NOTIF IF UNSUCCES ADD TO TABLE
                ui.notify(f"WRONG INPUT", color="bg-red")

        except Exception as e:
            ui.notify(f"WRONG INPUT", color="bg-red")
            print(e)

    ui.button("add new LocationsStations",
        on_click=addnewdata
        )

    list_alldata = ui.column()

    # FUNCTION FOR SAVE EDIT AFTER YOU CLICK SAVE IN DIALOG
    def saveandedit(e):
        try:
            query = '''UPDATE LocationsStations SET idL = ?, idL2 = ?, idL3 = ?, idL4 = ? WHERE idLS = ?'''
            cursor.execute(query,(edit_idL.value, edit_idL2.value, edit_idL3.value, edit_idL4.value, get_id.text))
            conn.commit()

            # AND SHOW NOTIF IF SUCCESS EDIT
            ui.notify("success edit", color="green")
            # CLOSE EDIT DIALOG
            editdialog.close()

            # CLEAR list_alldata AND CALL FUNCTION GET TABLE AGAIN
            list_alldata.clear()
            get_all_data()

        except Exception as e:
            print(e )


    # CREATE DIALOG EDIT
    with ui.dialog() as editdialog:
        with ui.card():
            ui.label("Edit Data").classes("font-xl font-weight")

            # THIS INPUT IS GET VALUE FROM station_in textfield AND AUTO SET HERE
            edit_idL = ui.input().bind_value_from(idL, "value")
            edit_idL2 = ui.input().bind_value_from(idL2, "value")
            edit_idL3 = ui.input().bind_value_from(idL3, "value")
            edit_idL4 = ui.input().bind_value_from(idL4, "value")

            # CREATE BUTTON SAVE EDIT AND CLOSE BUTTON
            with ui.row().classes("justify-between"):
                ui.button("save", on_click=lambda e : saveandedit(e))
                # FOR CLOSE DIALOG
                ui.button("close", on_click=editdialog.close).classes("bg-red")



    # FOR EDIT FUNCTION
    def editdata(x):
        # NOW GET ID FROM CLICKING EDIT BUTTON

        get_id.text = x.default_slot.children[0].text

        # SET NAME TEXTFIELD FROM YOU CLICKING EDIT BUTTON
        idL.value = x.default_slot.children[1].text
        idL2.value = x.default_slot.children[2].text
        idL3.value = x.default_slot.children[3].text
        idL4.value = x.default_slot.children[4].text

        # OPEN THE DIALOG EDIT
        editdialog.open()
        ui.update()




    # FOR DELETE
    def delete_twopointroutes(x):
        # GET ID FROM YOU CLICKING DELETE BUTTON

        get_id.text = x.default_slot.children[0].text
        cursor.execute('''DELETE FROM LocationsStations WHERE idLS=?''',(get_id.text,))
        conn.commit()

        # CLEAR ALL DATA THEN CALL FUNCTION AGAIN FROM TABLE
        list_alldata.clear()
        get_all_data() 

        # SHOW NOTIF IF YOU SUCCEED DELETING DATA FROM TABLE
        ui.notify("success delete",color="red")


    # GET ALL DATA FROM TABLE
    def get_all_data():
        cursor.execute('''SELECT * FROM LocationsStations ''')
        res = cursor.fetchall()
        result = []
        for row in res:
            # CCONVERT TO DICT JSON ARRAY
            data = {}
            for i, col in enumerate(cursor.description):
                data[col[0]] = row[i]
            result.append(data)
        print(result)


        # AFTER GET ALL DATA FROM TABLE THE CREATE CARD TO SEE DATA IN SCREEN APP
        for x in result:
            with list_alldata:
                # CREATE CARD FOR EDIT AND DELETE AND DATA
                with ui.card():
                    with ui.column():
                        with ui.row().classes("justify-between w-full") as carddata:
                            ui.label(x['idLS'])
                            ui.label(x['idL'])
                            ui.label(x['idL2'])
                            ui.label(x['idL3'])
                            ui.label(x['idL4'])
                        with ui.row():
                            # CREATE EDIT AND DELETE BUTTON
                            ui.button("edit").on("click", lambda e, carddata = carddata : editdata(carddata))

                            # DELETE
                            ui.button("delete").on("click", lambda e, carddata = carddata : delete_twopointroutes(carddata)).classes("bg-red")


    # AND CALL FUNCTION WHEN APP FIRST OPENS OR IS RUNNING
    get_all_data()



#ui.run()