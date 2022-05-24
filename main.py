from tkinter import *
from tkinter import messagebox as ms
import sqlite3
import json

lastid = 0


with sqlite3.connect('database.db') as db:
    c = db.cursor()

c.execute('CREATE TABLE IF NOT EXISTS text(id INT ,username TEXT NOT NULL,text TEXT);')
c.execute('CREATE TABLE IF NOT EXISTS user ( id INT PRIMARY KEY, username TEXT NOT NULL,password TEXT NOT NULL);')
db.commit()
db.close()




class main:
    def __init__(self, master):
        self.master = master
        self.username = StringVar()
        self.password = StringVar()
        self.n_username = StringVar()
        self.n_password = StringVar()
        self.texts= StringVar()
        self.frames()
        self.user= StringVar()
        self.id= 0
        self.listbox= None

    # Login Function
    def login(self):
        with sqlite3.connect('database.db') as db:
            c = db.cursor()

        find_user = ('SELECT * FROM user WHERE username = ? and password = ?')
        c.execute(find_user, [(self.username.get()), (self.password.get())])
        result = c.fetchall()
        c.execute('SELECT id FROM user WHERE username = ?', [(self.username.get())])
        self.id = c.fetchall()
        for row in self.id:
            self.id = row[0]
        if result:
            self.user= self.username.get()
            self.log.pack_forget()
            self.textf()
        else:
            ms.showerror('Error','Username Not Found.')


    def textf(self):
        with sqlite3.connect('database.db') as db:
            c = db.cursor()
        self.head.pack_forget()
        self.head['pady'] = 10
        self.text_f = Frame(self.master)
        Label(self.text_f, text='Enter Your Entry', font=('IMPACT', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.text_f, textvariable=self.texts, bd=5, font=('', 15)).grid(row=0, column=1)
        Button(self.text_f, text='Insert', command=self.text, font=('', 15), bd=5, padx=5).grid(row=1, column=1)
        self.listbox = Listbox(self.text_f, height=30, width=90, font=('', 15))
        self.listbox.grid(row=3, column=0, columnspan=3)

        c.execute('SELECT text FROM text WHERE username = ?', (self.user,))
        songs = c.fetchall()
        db.commit()
        self.text_f.pack()
        for item in songs:
            self.listbox.insert(END, item[0])

    def Insert(self):
        pass


    def text(self):
        with sqlite3.connect('database.db') as db:
            c = db.cursor()
        try:

            ms.showinfo('Success', 'Text insertion successful')
            c.execute('INSERT INTO text(id,username,text) VALUES (?,?,?)', (self.id,self.user, self.texts.get()))
            db.commit()
            self.listbox.insert(END,self.texts.get())

        except Exception as e:
            print(e)
            ms.showerror('Text Insertion failed')
            pass



    def new_user(self):
        with sqlite3.connect('database.db') as db:
            c = db.cursor()

        with open('last.json', 'r') as f:
            k = json.load(f)
            lastid=k['lastid']

        find_user = ('SELECT username FROM user WHERE username = ?')
        c.execute(find_user, [(self.n_username.get())])
        if c.fetchall():
            ms.showerror('Error!', 'Username Taken')
        else:
            ms.showinfo('Success!', 'Account Created!')
            self.loga()
        insert = 'INSERT INTO user(id,username,password) VALUES(?,?,?)'
        c.execute(insert, [(lastid),(self.n_username.get()), (self.n_password.get())])
        db.commit()
        with open('last.json', 'w') as n:
            y={"lastid":lastid+1}
            json.dump(y, n)



    def loga(self):
        self.username.set('')
        self.password.set('')
        self.crf.pack_forget()
        self.head['text'] = 'LOGIN'
        self.log.pack()



    def back(self):
        self.crf.pack_forget()
        self.frames()

    def cr(self):
        self.n_username.set('')
        self.n_password.set('')
        self.log.pack_forget()
        self.head['text'] = 'Create Account'
        self.crf.pack()

    def frames(self):
        self.head = Label(self.master, text='LOGIN', font=(35), pady=10)
        self.head.pack()
        self.log = Frame(self.master, padx=10, pady=10)
        Label(self.log, text='Username: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.log, textvariable=self.username, bd=5, font=('', 15)).grid(row=0, column=1)
        Label(self.log, text='Password: ', font=('', 20), pady=5, padx=5).grid(sticky=W)

        Entry(self.log, textvariable=self.password, bd=5, font=('', 15), show='*').grid(row=1, column=1)
        Button(self.log, text=' Login ', bd=3, font=('', 15), padx=10, pady=10, command=self.login).grid()
        Button(self.log, text=' Create Account ', bd=3, font=('', 15), padx=10, pady=10, command=self.cr).grid(row=2,
                                                                                                              column=1)
        self.log.pack()


        self.crf = Frame(self.master, padx=10, pady=10)
        Label(self.crf, text='Username: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.crf, textvariable=self.n_username, bd=5, font=('', 15)).grid(row=0, column=1)
        Label(self.crf, text='Password: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.crf, textvariable=self.n_password, bd=5, font=('', 15), show='*').grid(row=1, column=1)
        Button(self.crf, text='Create Account', bd=3, font=('', 15), padx=5, pady=5, command=self.new_user).grid()
        Button(self.crf, text='Go to Login', bd=3, font=('', 15), padx=5, pady=5, command=self.back).grid(row=2,
                                                                                                         column=1)


if __name__ == '__main__':
    root = Tk()
    root.title('Login')
    root.geometry('950x600')
    root.config(background='white')
    main(root)
    root.mainloop()