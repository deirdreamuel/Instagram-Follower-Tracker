import ig_selenium

from PIL import Image, ImageTk

import tkinter as tk
from tkinter import Scrollbar
from tkinter import Listbox
from tkinter import Label
from tkinter import StringVar
from tkinter import Entry
from tkinter import PhotoImage
from tkinter import Button


#----------extract Data from instagram.com and calculate--------------- 
def reciprocate():
    button.configure(text="processing...")
    status.configure(text="Status: Logging in...", fg="white")
    root.update()

    #initialize reciprocate class
    try: 
        ig = ig_selenium.reciprocate(username.get(), password.get())
        ig.login()

        #get profile info
        profile = ig.getProfileStats()
        profileName = profile[5]
        followersCount = extractCount(profile[3])
        followingCount = extractCount(profile[4])

        #update bottom window
        listbox.insert(tk.END, "")
        listbox.insert(tk.END, profileName)
        listbox.insert(tk.END, '{:<20}{:>25}'.format("Followers ", followersCount))
        listbox.insert(tk.END, '{:<20}{:>25}'.format("Following ", followingCount))
        listbox.insert(tk.END, "")

        #get followers and following
        status.configure(text="Status: Extracting Followers...", fg="white")
        root.update()
        followers = ig.getFollowers(int(followersCount))

        status.configure(text="Status: Extracting Following...", fg="white")
        root.update()
        following = ig.getFollowing(int(followingCount))

    except:
        status.configure(text="Error: Trouble Logging in, Please Check Username & Password and Disable 2FA", fg="red")
        button.configure(text="RECIPROCATE")
        listbox.delete(0, tk.END)
        ig.endReciprocate()
        raise
    
    #update bottom window
    status.configure(text="Status: Calculating", fg="white")
    root.update()

    #get result
    unfollow = unfollowing(followers, following)
    follow   = notfollowing(followers, following)

    listbox.insert(tk.END, "PEOPLE NOT FOLLOWING YOU BACK: ")
    for user in unfollow:
        listbox.insert(tk.END, user)
    listbox.insert(tk.END, "")
    listbox.insert(tk.END,"UNRECIPROCATED COUNT: " + str(len(unfollow)))
    
    listbox.insert(tk.END, "")
    listbox.insert(tk.END, "____________________________________________")
    listbox.insert(tk.END, "")
    listbox.insert(tk.END, "")

    listbox.insert(tk.END, "PEOPLE YOU ARE NOT FOLLOWING BACK: ")
    for user in follow:
        listbox.insert(tk.END, user)
    listbox.insert(tk.END, "")
    listbox.insert(tk.END,"UNRECIPROCATED COUNT: " + str(len(follow)))

    listbox.insert(tk.END, "")
    listbox.insert(tk.END, "")
    status.configure(text="Status: Success", fg="green")
    ig.endReciprocate()

    button.configure(text="RECIPROCATE")

#-------------calculate users that is not following you--------------
def unfollowing(followers, following):
    unfollowArr = []
    unfollowArr = list(set(following) - set(followers))

    return sorted(unfollowArr)

def notfollowing(followers, following):
    followArr = []
    followArr = list(set(followers) - set(following))

    return sorted(followArr)

def extractCount(s):
    arr = s.split()
    return arr[0]

#------------MAIN LOOP-------------------
if __name__ == "__main__":

    root = tk.Tk()  #initialize window
    root.title("IG RECIPROCATE")
    root.configure(bg="black")
    root.resizable(False, False)

    #application logo
    image = Image.open("./assets/logo.png")
    image = image.resize((300, 150), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(image)
    label = Label(image=image, bg="black")
    label.grid(row=0, column=0, columnspan=2)

    font_label = "helvetica 16 bold"
    font_entry = "helvetica 12 bold"
    
    #username input
    username_label = Label(root, text="USERNAME: ", fg="white", bg="black", font=font_label)
    username_label.grid(row=1, column=0, sticky="nesw")
    username = StringVar()
    username_entry = Entry(root, textvariable=username, fg="white", bg="black", borderwidth=0, font=font_entry, justify="center")
    username_entry.grid(row=1, column=1)  

    #password input
    password_label = Label(root, text="PASSWORD: ", fg="white", bg="black", font=font_label)
    password_label.grid(row=2, column=0)
    password = StringVar()
    password_entry = Entry(root, textvariable=password, show='*', fg="white", bg="black", borderwidth=0, font=font_entry, justify="center")
    password_entry.grid(row=2, column=1)

    #button to reciprocate
    button = Button(root, text="RECIPROCATE", fg="black", command=reciprocate, background="blue", width=30, font="helvetica 16 bold italic")
    button.grid(row=10, column = 0, columnspan=2,sticky='S', pady=20)

    #program status
    status = tk.Label(root, text="Status: Please Login", fg="white", bg="black", font="helvetica 12 bold")
    status.grid(row=11,column = 0, columnspan=2, sticky='S')

    #text field for results
    scrollbar = Scrollbar(root, bg="black")
    scrollbar.grid(row=12, column=2, sticky='E')
    listbox = Listbox(root, yscrollcommand=scrollbar.set, width = 70, bg="black", fg="white", justify="center", font="helvetica 12")
    listbox.grid(row=12, column=0, columnspan=2, sticky="E")

    #--------------------------------------------------------------------------------------------------
    root.mainloop()