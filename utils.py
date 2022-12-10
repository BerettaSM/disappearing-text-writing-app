import webbrowser
from tkinter import messagebox


def about_messagebox():
    open_git = messagebox.askyesno(title='About', message="""Created by Ramon Saviato.


        Email: ramonsaviato@hotmail.com

        GitHub: BerettaSM

        View profile on GitHub?""")

    if open_git:
        open_github()


def open_github():
    webbrowser.open('https://github.com/BerettaSM')
