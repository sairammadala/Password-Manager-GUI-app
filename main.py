from tkinter import *
from random import *
from data import *
import pandas as pd
import os
from tkinter.messagebox import *
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    password = ""
    for i in range(4):
        password += choice(letters)
        password += choice(numbers)
        password += choice(symbols)
    password = list(password)
    shuffle(password)
    password = ''.join(password)
    passwd_entry.delete(0, END)
    passwd_entry.insert(END, string=password)

# --------------------------Search csv file ------------------------------------#

def find():
    text = website_entry.get()
    not_found = False
    try:
        if os.stat("user_data.csv").st_size !=0:
            data = pd.read_csv("user_data.csv")
            print(data["Website"])
            if text in data["Website"]:
                print("YES")
                uname = data[text]["email"]
                pwd = data[text]["password"]
                showinfo(title="info", message=f"username: {uname}\npassword: {pwd}")
            else:
                not_found = True
        else:
            not_found = True
    except FileNotFoundError:
        not_found = True
    finally:
        if not_found:
            showerror(title="Invalid data", message="NOT FOUND")


# ---------------------------- SAVE PASSWORD ------------------------------- #
if os.stat("user_data.csv").st_size == 0:
    print("file is empty")
    user_data = pd.DataFrame(columns=["Website", "Username", "Password"])
    user_data.to_csv("user_data.csv", mode='w', index_label=False)


def save_data():
    website_name = website_entry.get()
    uid = email_or_uid_entry.get()
    pwd = passwd_entry.get()
    if len(website_name) != 0 and len(uid) != 0 and len(pwd) != 0:
        is_ok = askyesno(title="Confirmation", message=f"You entered the following details:\nwebsite: {website_name}"
                                                          f"\nusername: {uid}\npassword: {pwd}")
        if is_ok:
            data = pd.DataFrame([[website_name, uid, pwd]])
            data.to_csv("user_data.csv", mode="a", header=False, index=False)
    else:
        showwarning(title="Warning", message="All fields are mandatory")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
canvas = Canvas(width=200, height=200, highlightthickness=4)
#canvas.config(bg="yellow")
canvas.grid(column=0, row=0, columnspan=3)
locker_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=locker_img)

# adding labels to the interface
website_label = Label(text="Website")
website_label.grid(row=1, column=0)

email_or_uid_label = Label(text="Email/Username")
email_or_uid_label.grid(column=0, row=2)

passwd_label = Label(text="Password")
passwd_label.grid(row=3, column=0)

#adding entries to the interface
website_entry = Entry(width=45)
website_entry.insert(END, string="www.google.com")
website_entry.grid(column=1, row=1, columnspan=2)

email_or_uid_entry = Entry(width=45)
email_or_uid_entry.insert(END, string="xyz@gmail.com")
email_or_uid_entry.grid(column=1, row=2, columnspan=2)

passwd_entry = Entry(width=20)
passwd_entry.grid(column=1, row=3)

#adding buttons to the interface
search = Button(text="search", command=find)
search.config(width=20, bg="white")
search.grid(row=1, column=2)

passwd_generator = Button(text="Generate Password", command=generate_password)
passwd_generator.config(width=20, bg="white")
passwd_generator.grid(row=3, column=2)

save = Button(text="ADD", highlightthickness=0, command=save_data)
save.config(width=20, bg="white")
save.grid(column=0, row=4, columnspan=3)

window.mainloop()