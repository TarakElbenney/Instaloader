import instaloader
import tkinter as tk
from tkinter import filedialog
import os
import datetime

root = tk.Tk()
root.title("Profile Pic Downloader")
root.geometry("300x280")

user_var = tk.StringVar()
hours_var = tk.IntVar()

# Initial list of user accounts
initial_accounts = ['']
accounts = []

last_chosen_folder = ""  # Keep track of the last chosen folder

def download_posts_by_hours():
    username = user_var.get()
    hours = hours_var.get()
    loader = instaloader.Instaloader()

    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        current_datetime = datetime.datetime.now()
        target_datetime = current_datetime - datetime.timedelta(hours=hours)

        os.makedirs(last_chosen_folder, exist_ok=True)

        for post in profile.get_posts():
            if post.date >= target_datetime and post.date <= current_datetime:
                target_path = os.path.join(last_chosen_folder, post.date.strftime("%Y-%m-%d_%H-%M-%S"))
                if not os.path.exists(target_path + ".jpg"):
                    loader.download_post(post, target=target_path)
                    print(f"Downloaded post {post.url}")
                else:
                    print(f"Skipped post {post.url} (already downloaded)")

        print("Download complete!")

    except instaloader.exceptions.ProfileNotExistsException:
        print("The specified username does not exist on Instagram.")

def remove_account():
    selected_account = user_var.get()
    accounts.remove(selected_account)
    user_dropdown['menu'].delete(selected_account)
    print(f"Removed account: {selected_account}")

def add_account():
    new_account = user_var.get()
    if new_account not in accounts:
        accounts.append(new_account)
        user_dropdown['menu'].add_command(label=new_account, command=tk._setit(user_var, new_account))
        print(f"Added account: {new_account}")

def open_add_account_window():
    add_account_window = tk.Toplevel(root)
    add_account_window.title("Add Account")
    add_account_window.geometry("200x100")

    username_label = tk.Label(add_account_window, text="Username:")
    username_entry = tk.Entry(add_account_window, textvariable=user_var)
    save_button = tk.Button(add_account_window, text="Save", command=save_account)

    username_label.pack()
    username_entry.pack()
    save_button.pack()

def save_account():
    new_account = user_var.get()
    if new_account not in accounts:
        accounts.append(new_account)
        user_dropdown['menu'].add_command(label=new_account, command=tk._setit(user_var, new_account))
        print(f"Added account: {new_account}")

def save_accounts():
    with open("accounts.txt", "w") as file:
        for account in accounts:
            file.write(account + "\n")

def load_accounts():
    if os.path.exists("accounts.txt"):
        with open("accounts.txt", "r") as file:
            lines = file.readlines()
            accounts.extend([line.strip() for line in lines])

    # Add initial accounts if no accounts saved
    if len(accounts) == 0:
        accounts.extend(initial_accounts)

def choose_destination():
    global last_chosen_folder
    last_chosen_folder = filedialog.askdirectory()
    print(f"Selected destination: {last_chosen_folder}")

load_accounts()

user_label = tk.Label(root, text='Select Insta Id:', font=('calibre', 10, 'bold'))
user_dropdown = tk.OptionMenu(root, user_var, *accounts)

hours_label = tk.Label(root, text='Enter Hours:', font=('calibre', 10, 'bold'))
hours_entry = tk.Entry(root, textvariable=hours_var, font=('calibre', 10, 'normal'))

download_button = tk.Button(root, text='Download', command=download_posts_by_hours)

remove_button = tk.Button(root, text='Remove Account', command=remove_account)
add_button = tk.Button(root, text='Add Account', command=open_add_account_window)

choose_destination_button = tk.Button(root, text='Choose Destination', command=choose_destination)
save_button = tk.Button(root, text='Save', command=save_accounts)

user_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
user_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="we")
hours_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
hours_entry.grid(row=1, column=1, padx=10, pady=10, sticky="we")
download_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="we")
remove_button.grid(row=3, column=0, padx=10, pady=10, sticky="w")
add_button.grid(row=3, column=1, padx=10, pady=10, sticky="we")
choose_destination_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="we")
save_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="we")

root.grid_columnconfigure(1, weight=1)  # Expand the second column to fill any extra space
root.mainloop()