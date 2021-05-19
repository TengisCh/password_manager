from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

SMALL_WIDTH = 21


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = password_letters + password_symbols +password_numbers

    shuffle(password_list)
    password = "".join(password_list)
    pyperclip.copy(password)
    pass_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_info():
    web = web_entry.get().capitalize()
    email = email_entry.get()
    password_ent = pass_entry.get()

    if web and email and password_ent:
        is_ok = messagebox.askokcancel("Confirmation", f"Website: {web}\nEmail: {email}\nPassword: {password_ent}\n"
                                                       f"Is it OK to save?")
        if is_ok:
            new_data = {web: {"Email": email, "Password": password_ent}}

            try:
                with open("data.json", "r") as data_file:
                    dic_data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                dic_data.update(new_data)
                with open("data.json", "w") as data_file:
                    json.dump(dic_data, data_file, indent=4)
            finally:
                web_entry.delete(0, END)
                pass_entry.delete(0, END)
                web_entry.focus()
    else:
        messagebox.showerror("Error", "Please fill all the fields")


# ---------------------------- SEARCH  ------------------------------- #
def search_name():
    search = web_entry.get().capitalize()
    try:
        with open("data.json", "r") as data_file:
            dic_data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror("Error", "No Data File Found")
    else:
        if search in dic_data:
            website = dic_data[search]
            email = website["Email"]
            password = website["Password"]
            pyperclip.copy(password)
            messagebox.showinfo("Request", f"Email: {email}\nPassword: {password}\n"
                                           f" ***********Password copied to the clipboard***********")
        else:
            messagebox.showerror("oops", "No detail of the website exist in our database")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# Label
web_label = Label(text="Website:")
web_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

pass_label = Label(text="Password:")
pass_label.grid(column=0, row=3)

# Entry
web_entry = Entry(width=SMALL_WIDTH)
web_entry.grid(column=1, row=1, padx=0)
web_entry.focus()

email_entry = Entry(width=40)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "MyEmail@gmail.com")

pass_entry = Entry(width=SMALL_WIDTH)
pass_entry.grid(column=1, row=3, padx=0)

# Button
search_button = Button(text="Search", command=search_name, width=15)
search_button.grid(column=2, row=1, padx=0)

generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3, padx=0)

add_button = Button(text="Add", width=36, command=save_info)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
