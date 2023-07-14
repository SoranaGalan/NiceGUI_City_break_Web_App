import sqlite3
from nicegui import ui

conn = sqlite3.connect("DB/test.db", check_same_thread=False)
cursor = conn.cursor()


@ui.page('/admin_commontransport')
def admin_commontransport():
    name =  ui.input(label="Name of common transport").classes("w-full")
    station_list =  ui.input(label="Station List").classes("w-full")

    # CREATE ID TEXT FOR GET ID WHEN YOU CLICK EDIT AND DELETE BUTTON
    get_id = ui.label()


    # ADD NEW DATA
    def addnewdata():
        try:
            cursor.execute('''SELECT name FROM CommonTransport''')
            name_res = cursor.fetchall()
            name_final_result = [i[0] for i in name_res]

            if name.value not in name_final_result:

                cursor.execute('''INSERT INTO CommonTransport (name, station_list) VALUES(?,?)''',(name.value, station_list.value))
                conn.commit()
                # SHOW NOTIF IF SUCCESS ADD TO TABLE
                ui.notify(f"success add new data {name.value}",color="blue")

                # CLEAR INPUT station_in AND station_out
                name.value = ""
                station_list.value = ""
                # CLEAR ALL DATA IN LIST AND GET AGAIN
                list_alldata.clear()
                get_all_data()
            else:
                # SHOW NOTIF IF UNSUCCES ADD TO TABLE
                ui.notify(f"Common transport already existent", color="bg-red")

        except Exception as e:
            print(e)

    ui.button("add new common transport",
        on_click=addnewdata
        )

    list_alldata = ui.column()

    # FUNCTION FOR SAVE EDIT AFTER YOU CLICK SAVE IN DIALOG
    def saveandedit(e):
        try:
            query = '''UPDATE CommonTransport SET name = ?, station_list = ? WHERE idCT = ?'''
            cursor.execute(query,(edit_name.value, edit_station_list.value, get_id.text))
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
            edit_name = ui.input().bind_value_from(name, "value")
            edit_station_list = ui.input().bind_value_from(station_list, "value")

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
        name.value = x.default_slot.children[1].text
        station_list.value = x.default_slot.children[2].text

        # OPEN THE DIALOG EDIT
        editdialog.open()
        ui.update()




    # FOR DELETE
    def delete_transport(x):
        # GET ID FROM YOU CLICKING DELETE BUTTON

        get_id.text = x.default_slot.children[0].text
        cursor.execute('''DELETE FROM CommonTransport WHERE idCT=?''',(get_id.text,))
        conn.commit()

        # CLEAR ALL DATA THEN CALL FUNCTION AGAIN FROM TABLE
        list_alldata.clear()
        get_all_data() 

        # SHOW NOTIF IF YOU SUCCEED DELETING DATA FROM TABLE
        ui.notify("success delete",color="red")


    # GET ALL DATA FROM TABLE
    def get_all_data():
        cursor.execute('''SELECT * FROM CommonTransport ''')
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
                            ui.label(x['idCT'])
                            ui.label(x['name'])
                            ui.label(x['station_list'])
                        with ui.row():
                            # CREATE EDIT AND DELETE BUTTON
                            ui.button("edit").on("click", lambda e, carddata = carddata : editdata(carddata))

                            # DELETE
                            ui.button("delete").on("click", lambda e, carddata = carddata : delete_transport(carddata)).classes("bg-red")


    # AND CALL FUNCTION WHEN APP FIRST OPENS OR IS RUNNING
    get_all_data()

#ui.run()