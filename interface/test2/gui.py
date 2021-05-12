from tkinter import *

root = Tk()

# title and dimensions
root.title("Chat Bot")
root.geometry('400x500')

# main menu
main_menu = Menu(root)
main_menu.add_command(label='File')
main_menu.add_command(label='Edit')
main_menu.add_command(label='Quit')
root.config(menu=main_menu)

# chat area
chatWindow = Text(root, bd=1, bg='black', width=50, height=8)
chatWindow.place(x=6, y=6, height=385, width=370)

# message area
messageWindow = Text(root, bg='black', width=30, height=4)
messageWindow.place(x=128, y=400, height=88, width = 260)

# send button
Button=Button(root, text='Send', bg='white', activebackground='light blue', width=12, height=5)
Button.place(x=6, y=400, height=88, width=120)

# scrollbar
scrollbar = Scrollbar(root, command=chatWindow.yview())
scrollbar.place(x=375, y=5, height=385)

root.mainloop()