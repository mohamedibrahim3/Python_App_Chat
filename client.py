from tkinter.font import BOLD
from matplotlib.colors import cnames
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import customtkinter
from PIL import Image, ImageTk
import socket
import threading
import queue

# Global Variables
Name = ''

# Functions

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# Create the root window
root = customtkinter.CTk()

# Create the main window
root.title("Chat App")
root.resizable(False, False)
root.geometry("500x500")

# Create the main window label
frame1 = customtkinter.CTkFrame(root)
frame1.pack(pady=30, padx=30)
frame1.place(relx=0.5, rely=0.5, anchor='center')

# frame1.grid(row=0, column=0, pady = 10, padx = 10)
def openChatApplication():
    global newWindow
    newWindow = customtkinter.CTk()
    
    newWindow.title("Chat App")
    newWindow.resizable(False, False)
    newWindow.geometry("500x500")
    
    global client_socket
    
    # create socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get local machine name
    host = socket.gethostname()

    # specify a port to connect
    port = 5000

    # connect to the server
    client_socket.connect((host, port))
    
    # start a thread to receive messages
    threading.Thread(target=receive_messages, daemon=True).start()
    
    # start a thread to process messages
    global message_queue
    
    message_queue = queue.Queue()
    # process_messages()
    client_socket.sendall(Name.encode())
    
    # creates the chatRoom
    createChatRoom(newWindow)
    
    newWindow.mainloop()
    root.destroy()

# Create the main window label
def getNameBtnClicked():
    # Get the name from the entry box
    global Name
    Name = getName.get()
    # if the name is empty, show an error message
    if Name == '':
        errorName.grid(row=0, column=0, padx=10, pady=10)
    else:
        # if the name is not empty, hide the current window and open the chat application
        root.destroy()  # Hide the current window
        openChatApplication()
        
# receives messages from the server
def receive_messages():
    while True: 
        data = client_socket.recv(1024).decode()
        if not data:
            break
        message_queue.put(data)

# sends messages to the server
def send_message(MessageEntry, messageBox):
    message = MessageEntry.get()
    # if the message is not empty, send it to the server
    if message != '':
        client_socket.sendall(message.encode())
        messageBox.insert("end", f'You: {message}\n')
    
    # close the connection if client sends 'bye'
    if message.lower() == 'bye':
        client_socket.close()
        messageBox.insert("end", f'\n\nYou have left the chat')
    
    # clear the message entry box
    MessageEntry.delete(0, 'end')
   
# processes messages from the server 
def process_messages():
    while True:
        try:
            message = message_queue.get(block=False)
            messageBox.insert(tk.END, f'{message}\n')
        except queue.Empty:
            break
    newWindow.after(100, process_messages)

# creates the chat room
def createChatRoom(newWindow):
    # create the frame for the chat room
    frame2 = customtkinter.CTkFrame(newWindow)
    frame2.pack(pady=10, padx=10)
    
    # create the label for the chat room
    new_window_label = customtkinter.CTkLabel(frame2, text="Welcome " + str(Name) + "!", font=("Helvetica", 24))
    new_window_label.grid(row=0, column=0, pady = 10, padx = 10)
    
    # create the frame for the chat room
    frame3 = customtkinter.CTkFrame(newWindow)
    frame3.pack(pady=10, padx=10)

    # create the message box
    global messageBox
    messageBox = customtkinter.CTkTextbox(frame3, width=400 ,height=300, corner_radius=8, font=("Helvetica", 16))
    
    # create the message box
    messageBox.insert("0.0", "Welcome to the chat app!\n\n")
    messageBox.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

    # create the message entry box
    messageEntry = customtkinter.CTkEntry(frame3, placeholder_text="Enter your message", width=250, height=35, corner_radius=8, font=("Helvetica", 16))
    messageEntry.grid(row=5, column=0, padx=10, pady=10)

    # create the button to send the message
    sendButton = customtkinter.CTkButton(frame3, text="Send", command=lambda: send_message(messageEntry, messageBox), width=120, height=35, corner_radius=8, font=("Helvetica", 16))
    sendButton.grid(row=5, column=1, padx=10, pady=10)
    process_messages()

# Create the main window label
getName = customtkinter.CTkEntry(frame1, placeholder_text="Enter your name", width=250, height=50, corner_radius=8, font=("Helvetica", 16))
getName.grid(row=1, column=0, padx=10, pady=10)

# create the error message
errorName = customtkinter.CTkLabel(frame1, text="*Please enter a valid name", text_color="red", font=("Helvetica", 16))
errorName.pack_forget()

# create the button
getNameBtn = customtkinter.CTkButton(frame1, text="Enter", command=getNameBtnClicked, width=120, height=35, corner_radius=10,  font=("Helvetica", 16))
getNameBtn.grid(row=2, column=0, padx=10, pady=10)

root.mainloop()
