from tkinter import *
from tkinter import messagebox as msg
import sqlite3 as db
from tkinter import ttk as table

try:
    conn = db.connect('myDb.db')
    print("Connection Established: Connected to myDb Database!")
    cursor = conn.cursor()
except db.DatabaseError:
    print(db.DatabaseError)

def readData():
    cursor.execute("SELECT * FROM PRODUCT")
    data = cursor.fetchall()

    readWindow = Toplevel(main)
    readWindow.title("Database Table")

    myTable = table.Treeview(readWindow)

    myTable['columns'] = ("PRODUCT_ID", "PRODUCT_CATEGORY", "PRODUCT_NAME", "PRODUCT_BRAND")
    # Creating Columns
    myTable.column("#0", width=0, stretch=NO)
    myTable.column("PRODUCT_ID", width=40, anchor=CENTER)
    myTable.column("PRODUCT_CATEGORY", width=120, anchor=W)
    myTable.column("PRODUCT_NAME", width=120, anchor=W)
    myTable.column("PRODUCT_BRAND", width=120, anchor=W)
    # Creating Heading
    myTable.heading("#0", text="")
    myTable.heading("PRODUCT_ID", text="ID")
    myTable.heading("PRODUCT_CATEGORY", text="CATEGORY")
    myTable.heading("PRODUCT_NAME", text="NAME")
    myTable.heading("PRODUCT_BRAND", text="BRAND")

    myTable.pack()
    for row in data:
        print(row)
        myTable.insert(parent='', index='end', values=row)

def updateData():
    def updateEntry():
        executeUpdateButton.grid(row=5, column=0, columnspan=2)
        idEntry.config(state="normal")
        notChecked = 0
        if categoryVar.get() == notChecked:
            categoryEntry.config(state="disabled")
        else:
            categoryEntry.config(state="normal")
        if nameVar.get() == notChecked:
            nameEntry.config(state="disabled")
        else:
            nameEntry.config(state="normal")
        if brandVar.get() == notChecked:
            brandEntry.config(state="disabled")
        else:
            brandEntry.config(state="normal")
        chooseWindow.destroy()

    def onClosingChooseWindow():
        idEntry.config(state="normal")
        showButton()
        enableAllFields()
        clearFields()
        chooseWindow.destroy()
    hideButton()
    idEntry.config(state="disabled")
    categoryEntry.config(state="disabled")
    nameEntry.config(state="disabled")
    brandEntry.config(state="disabled")

    chooseWindow = Toplevel(main)
    chooseWindow.title("UPDATE ENTRY")
    chooseWindow.geometry("200x120")

    nameUpdate = Label(chooseWindow, text="Check entry you want to update: ")
    categoryVar = IntVar()
    nameVar = IntVar()
    brandVar = IntVar()
    categoryCheckButton = Checkbutton(chooseWindow, text="Product Category", variable=categoryVar)
    nameCheckButton = Checkbutton(chooseWindow, text="Product Name", variable=nameVar)
    brandCheckButton = Checkbutton(chooseWindow, text="Product Brand", variable=brandVar)
    submitButton = Button(chooseWindow, text="Update Selected", command=updateEntry)

    nameUpdate.pack()
    categoryCheckButton.pack()
    nameCheckButton.pack()
    brandCheckButton.pack()
    submitButton.pack()
    chooseWindow.protocol("WM_DELETE_WINDOW", onClosingChooseWindow)

def deleteData():
    isPressed = True
    categoryEntry.config(state="disabled")
    nameEntry.config(state="disabled")
    brandEntry.config(state="disabled")
    insertButton.config(state="disabled")
    updateButton.config(state="disabled")
    readButton.config(state="disabled")

    if isPressed:
        isPressed = False
        print(isPressed)
        try:
            productId = int(idEntry.get())
            if not isIdAlreadyExist(productId):
                msg.showerror("UPDATE ENTRY", "Update Failed! ProductId didn't exist in Database")
                clearFields()
                enableAllFields()
                return
            if isPressed is False:
                enableAllFields()
            try:
                with conn:
                    cursor.execute("DELETE FROM PRODUCT WHERE PRODUCT_ID=?", (productId,))
                    msg.showinfo("DELETE ENTRY", "Entry Deleted Successfully")
            except db.DatabaseError:
                msg.showerror("DELETE ENTRY", "Deletion Failed! PRODUCT_ID didn't exist in Database")
        except ValueError:
            print("Value Error Catch Go on!")
    clearFields()

def insertData():
    productId = int(idEntry.get())
    productCategory = str(categoryEntry.get()).strip()
    productName = str(nameEntry.get()).strip()
    productBrand = str(brandEntry.get()).strip()
    if isIdAlreadyExist(productId):
        msg.showerror("INSERT DATA", "Insertion Failed! ProductId already exist in Database")
        clearFields()
        return
    if not isEmptyFields(productCategory, productName, productBrand):
        return
    with conn:
        # cursor.execute("""INSERT INTO PRODUCT VALUES (?, ?, ?, ?)""",
        # (int(idEntry.get()), str(categoryEntry.get()), str(nameEntry.get()), str(brandEntry.get())))
        insert = "INSERT INTO PRODUCT VALUES (:id, :category, :name, :brand)"
        values = {'id': productId,
                  'category': productCategory,
                  'name': productName,
                  'brand': productBrand
                  }
        cursor.execute(insert, values)
        clearFields()
        msg.showinfo("SAVE ENTRY", "Entry inserted Successfully")

def hideButton():
    insertButton.grid_forget()
    deleteButton.grid_forget()
    readButton.grid_forget()
    updateButton.grid_forget()

def showButton():
    readButton.grid(row=6, column=1)
    updateButton.grid(row=5, column=1)
    deleteButton.grid(row=6, column=0)
    insertButton.grid(row=5, column=0)
    idEntry.focus_set()

def executeUpdate():
    showButton()
    productId = int(idEntry.get())
    if not isIdAlreadyExist(productId):
        executeUpdateButton.grid_forget()
        clearFields()
        enableAllFields()
        idEntry.config(state="normal")
        msg.showerror("UPDATE DATA", "Insertion Failed! ProductId already exist in Database")
        return
    productCategory = str(categoryEntry.get()).strip()
    productName = str(nameEntry.get()).strip()
    productBrand = str(brandEntry.get()).strip()

    cursor.execute("SELECT * FROM PRODUCT WHERE PRODUCT_ID=:id", {'id': productId})
    selectedEntry = cursor.fetchone()
    blank = 0
    if len(productCategory) == blank:
        productCategory = selectedEntry[1]
    if len(productName) == blank:
        productName = selectedEntry[2]
    if len(productBrand) == blank:
        productBrand = selectedEntry[3]
    try:
        with conn:
            update = """UPDATE PRODUCT SET
                        PRODUCT_CATEGORY=:category,
                        PRODUCT_NAME=:name,
                        PRODUCT_BRAND=:brand
                        WHERE PRODUCT_ID=:id"""
            values = {'id': productId,
                      'category': productCategory,
                      'name': productName,
                      'brand': productBrand
                      }
            cursor.execute(update, values)
            executeUpdateButton.grid_forget()
            clearFields()
            enableAllFields()
            idEntry.config(state="normal")
            msg.showinfo("UPDATE ENTRY", "Entry Updated Successfully")
    except db.DatabaseError:
        print(db.DatabaseError)

def enableAllFields():
    categoryEntry.config(state="normal")
    nameEntry.config(state="normal")
    brandEntry.config(state="normal")
    insertButton.config(state="normal")
    updateButton.config(state="normal")
    readButton.config(state="normal")
    deleteButton.config(state="normal")

def clearFields():
    idEntry.delete(0, END)
    categoryEntry.delete(0, END)
    nameEntry.delete(0, END)
    brandEntry.delete(0, END)
    idEntry.focus_set()

def isEmptyFields(productCategory, productName, productBrand):
    isEmptyField = bool(len(productCategory) != 0 and len(productName) != 0 and len(productBrand) != 0)
    if isEmptyField:
        return True
    else:
        msg.showerror("UPDATE ENTRY", "Insert Failed! All fields must not be empty")
        return False

def isIdAlreadyExist(productId):
    cursor.execute("SELECT PRODUCT_ID FROM PRODUCT")
    id_column = cursor.fetchall()
    for val in id_column:
        if productId in val:
            return True

def on_closing():
    conn.close()
    print("Connection Closed!")
    main.destroy()


main = Tk()
main.title("Product Management System")
main.resizable(False, False)
main.config(bg="wheat3")

productLabel = Label(main, text="Product Information", bg="wheat3")
idLabel = Label(main, text="Product Id", bg="wheat3")
idEntry = Entry(main)
categoryLabel = Label(main, text="Product Category", bg="wheat3")
categoryEntry = Entry(main)
nameLabel = Label(main, text="Product Name", bg="wheat3")
nameEntry = Entry(main)
brandLabel = Label(main, text="Product Brand", bg="wheat3")
brandEntry = Entry(main)
readButton = Button(main, text="READ ENTRY", height=2, command=readData)
updateButton = Button(main, text="UPDATE ENTRY", height=2, command=updateData)
deleteButton = Button(main, text="DELETE ENTRY", height=2, command=deleteData)
insertButton = Button(main, text="SAVE ENTRY", height=2, command=insertData)
executeUpdateButton = Button(main, text="UPDATE ENTRY", height=2, command=executeUpdate)

productLabel.grid(row=0, column=0, columnspan=2, pady=10)
idLabel.grid(row=1, column=0, pady=10, padx=20)
idEntry.grid(row=1, column=1, pady=10, padx=20)
categoryLabel.grid(row=2, column=0, pady=10, padx=20)
categoryEntry.grid(row=2, column=1, pady=10, padx=20)
nameLabel.grid(row=3, column=0, pady=10, padx=20)
nameEntry.grid(row=3, column=1, pady=10, padx=20)
brandLabel.grid(row=4, column=0, pady=10, padx=20)
brandEntry.grid(row=4, column=1, pady=10, padx=20)

insertButton.grid(row=5, column=0, pady=10, padx=20)
updateButton.grid(row=5, column=1, pady=10, padx=20)
readButton.grid(row=6, column=1, pady=10, padx=20)
deleteButton.grid(row=6, column=0, pady=10, padx=20)

main.protocol("WM_DELETE_WINDOW", on_closing)
main.mainloop()