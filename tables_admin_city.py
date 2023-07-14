import sqlite3
from nicegui import ui

conn = sqlite3.connect("DB/test.db", check_same_thread=False)
cursor = conn.cursor()

get_id = ui.label()

selected_data = []

mytable = ui.aggrid({
    "columnDefs":[
        {'headerName':"IdC","field":"idC"},
        {'headerName':"Name","field":"name"},
    ],
    "rowData":[],
    "rowSelection":"multiple"
})

def show():
    cursor.execute('''SELECT * FROM Cities''')
    res = cursor.fetchall()
    mydata = []
    for row in res:
        # AND CONVERT TO DICT JSON ARRAY
        data = {}
        for i, col in enumerate(cursor.description):
            data[col[0]] = row [i]
        mydata.append(data)
    print(mydata)
    mytable.options['rowData'] = sorted(mydata, key=lambda data:data['name'])

show()

def addnewdata():
    try:
        cursor.execute('''SELECT name FROM Cities''')
        name_res = cursor.fetchall()
        name_final_result = [i[0] for i in name_res]

        if add_name.value not in name_final_result:
            cursor.execute('''INSERT INTO Cities (name) VALUES (?)''', (add_name.value,))
            conn.commit()
            # SHOW NOTIF IF SUCCES ADD TO TABLE
            ui.notify(f"succes add new data {add_name.value}", color="blue")
            # AND CLOSE THE DIALOG
            new_data_dialog.close()
            # CLEAR INPUT NAME
            add_name.value = ""
            show()
            mytable.update()
        else:
            # SHOW NOTIF IF UNSUCCES ADD TO TABLE
            ui.notify(f"City already existent", color="bg-red")
            add_name.value = ""
    except Exception as e:
        print(e)

# CREATE DIALOG FOR INPUT NAME AND AGE
with ui.dialog() as new_data_dialog:
    with ui.card():
        add_name = ui.input(label="add name")
        ui.button("add new", on_click=addnewdata)

def opendata(e):
    # OPEN DIALOG FOR ADD NEW DATA TO TABLE
    new_data_dialog.open()


# REMOVE DATA
async def removedata():
    # SELECT WHAT YOU WANT TO REMOVE
    row = await mytable.get_selected_row()

    if row == None:
        ui.notify("No data selecte", color="red")
        return
    
    # AND REMOVE mydata
    cursor.execute('''DELETE FROM Cities WHERE name=?''', (row["name"],))
    conn.commit()

    # AND NOTIFY REMOVE
    ui.notify("delete", color="red")
    #mytable.options['rowData'] = sorted(mydata, key=lambda data:data['name'])
    show()
    mytable.update()


def savedata():
    # UPDATE DATA YOU SELECTED FROM TABLE
    for d in mydata:
        # IF NAME IN MYDATA == IN SELECT THEN CHANGE
        if d['name'] == selected_data['name']:
            mydata.remove(d)
            # SHOW NOTIF
            ui.notify("success edit", color="blue")
            # AND CLOSE DIALOG
            dialogedit.close()
    mydata.append({"idC":idC_edit.value,"name":name_edit.value})
    # UPDATE THE TABLE
    mytable.options['rowData'] = sorted(mydata, key=lambda data:data['name'])
    mytable.update()

# CREATE DIALOG FOR EDIT NAME AND AGE
with ui.dialog() as dialogedit:
    with ui.card():
        idC_edit = ui.input(label="idC")
        name_edit = ui.input(label="name")
        ui.button("Save data", on_click=savedata)


# EDIT DATA
async def editdata():
    # CREATE VARIABLE selected_data FOR EDIT AND CALL
    # selected_data VARIABLE FROM ANOTHER FUNCTION
    global selected_data

    # AND GET YOUR SELECTED FROM CLICK SELECT TABLE
    selected_data = await mytable.get_selected_row()

    # AND IF NO SELECTED DATA GIVE ALERT NO DATA SELECTED
    if selected_data == None:
        ui.notify("No data selecte", color="red")
        return
    
    # SET NAME_EDIT AND AGE_EDIT FROM SELECTED TABLE
    name_edit.value = selected_data['name']
    idC_edit.value = selected_data['idC']

    # AND OPEN DIALOG
    dialogedit.open()

# CREATE ADD EDIT DELETE BUTTON
with ui.row():
    ui.button("Add", on_click=lambda e: opendata(e))
    ui.button("Remove", on_click=removedata)
    ui.button("Edit", on_click=editdata)

ui.run()