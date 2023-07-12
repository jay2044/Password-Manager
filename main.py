from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
from os import path

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_list += [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_list += [random.choice(numbers) for _ in range(random.randint(2, 4))]

    random.shuffle(password_list)

    password = "".join(password_list)
    password_text.delete("1.0", "end")
    password_text.insert("1.0", password)

    # Copy the password to the clipboard
    pyperclip.copy(password)


def write_password(website, user, password):
    password_data = {
        "website": website,
        "user": user,
        "password": password
    }

    try:
        if not path.exists("data.json"):
            with open("data.json", "w") as data_file:
                json.dump([password_data], data_file, indent=4)
        else:
            with open("data.json", "r") as data_file:
                passwords = json.load(data_file)
                passwords.append(password_data)

            with open("data.json", "w") as data_file:
                json.dump(passwords, data_file, indent=4)
    except IOError:
        messagebox.showerror(title="Error", message="Unable to write password data to file.")
        return


def read_passwords():
    try:
        if not path.exists("data.json"):
            return []

        with open("data.json", "r") as data_file:
            passwords = json.load(data_file)
            return passwords
    except (IOError, json.JSONDecodeError):
        messagebox.showerror(title="Error", message="Unable to read password data from file.")
        return []


def update_passwords(passwords):
    try:
        with open("data.json", "w") as data_file:
            json.dump(passwords, data_file, indent=4)
    except IOError:
        messagebox.showerror(title="Error", message="Unable to update password data.")
        return


def search_password():
    website = website_text.get("1.0", "end-1c").strip()
    if not website:
        messagebox.showerror(title="Error", message="Please enter a website!")
        return

    passwords = read_passwords()
    found_passwords = []

    for password_data in passwords:
        if password_data["website"].lower() == website.lower() and password_data["user"].lower() == user_text.get("1.0", "end-1c").strip().lower():
            found_passwords.append(password_data)

    if found_passwords:
        messagebox.showinfo(title="Search Results", message=f"Found {len(found_passwords)} password(s) for {website}")
        password_text.delete("1.0", "end")
        for password_data in found_passwords:
            password_text.insert("1.0", password_data['password'])

            # Copy the password to the clipboard
            pyperclip.copy(password_data['password'])

    else:
        messagebox.showinfo(title="Search Results", message=f"No passwords found for {website} and the entered username")


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_text.get("1.0", "end-1c").strip()
    user = user_text.get("1.0", "end-1c").strip()
    password = password_text.get("1.0", "end-1c").strip()

    if not website or not user or not password:
        messagebox.showerror(title="Error", message="Please fill in all fields!")
        return

    try:
        write_password(website, user, password)
        messagebox.showinfo(title="Success", message="Password saved successfully!")

        # Clear the fields after saving
        website_text.delete("1.0", "end")
        password_text.delete("1.0", "end")
    except:
        messagebox.showerror(title="Error", message="An error occurred while saving the password.")
        return


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)

website_label = Label(window, text="Website: ")
website_text = Text(window, height=1, width=30)
website_text.focus()

user_label = Label(window, text="Email/Username: ")
user_text = Text(window, height=1, width=30)
user_text.insert("1.0", "jayaadithya1@gmail.com")

password_label = Label(window, text="Password: ")
password_text = Text(window, height=1, width=30)

generate_button = Button(window, text="Generate", command=generate_password)
search_button = Button(window, text="Search", command=search_password)
add_button = Button(window, text="Add", width=30, command=save)

canvas.grid(row=0, column=0, rowspan=3)
website_label.grid(row=0, column=1, sticky="E")
website_text.grid(row=0, column=2, sticky="W")
search_button.grid(row=0, column=3, padx=10)
user_label.grid(row=1, column=1, sticky="E")
user_text.grid(row=1, column=2, sticky="W")
password_label.grid(row=2, column=1, sticky="E")
password_text.grid(row=2, column=2, sticky="W")
generate_button.grid(row=2, column=3)
add_button.grid(row=3, column=1, columnspan=5, pady=10)

window.mainloop()
