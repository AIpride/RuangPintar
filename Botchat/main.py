from tkinter import*
import tkinter
import PIL
from PIL import ImageTk
from numpy import place # pip install Pillow
from tkinter import messagebox

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Masuk Ruang Pintar")
        self.root.geometry("1000x600")

        #BackgroundImage

        self.bg=ImageTk.PhotoImage(file="1.jpg")
        self.bg_image=Label(self.root,image=self.bg).place(x=0,y=0, relwidth=1, relheight=1)

        #LoginFrom
        Frame_login = Frame(self.root, bg="white")
        Frame_login.place(x=330,y=150,width=500,height=400)

        #Title&Subtitle
        title= Label(Frame_login, text="RUANG PINTAR", font=("Impact", 35,"bold"), fg="#6162FF", bg="white").place(x=90,y=30)
        subtitle= Label(Frame_login, text="Area Masuk Anggota siswa ", font=("Goudy old style", 15,"bold"), fg="#1d1d1d", bg="white").place(x=90,y=100)

        #Username
        lbl_user = Label(Frame_login, text="Nama Pengguna", font=("Goudy old style", 15,"bold"), fg="grey", bg="white").place(x=90,y=140)
        self.username = Entry(Frame_login,  font=("Goudy old style", 15), bg="#E7E6E6")
        self.username.place(x=90,y=170,width=320,height=35)  

        #Password
        lbl_Password = Label(Frame_login, text="Kata sandi", font=("Goudy old style", 15,"bold"), fg="grey", bg="white").place(x=90,y=210)
        self.Password = Entry(Frame_login,  font=("Goudy old style", 15), bg="#E7E6E6")
        self.Password.place(x=90,y=240,width=320,height=35)  

        #Button
        forget = Button (Frame_login, text="Tidak ingat kata sandi ?", bd=0,cursor="hand2",font=("Goudy old style", 12), fg="#6162FF", bg="white").place(x=90,y=280)
        sumbit = Button (Frame_login,command=self.check_function,cursor="hand2", text="Login ", bd=0,font=("Goudy old style", 15), bg="#6162FF", fg="white").place(x=90,y=320,width=180,height=40)

    def check_function(self):
        if self.username.get()==""or self.Password.get()=="":
            messagebox.showerror("Error","Semua bagian yang diperlukan belum terpenuhi ",parent=self.root)
        elif self.username.get()!="Rijalul Hadi"or self.Password.get()!="1234":
            messagebox.showerror("Error","Nama dan Password tidak Ditemukan",parent=self.root)
        else:
            messagebox.showinfo("Selamat Datang",f"Selamat datang {self.username.get()}")





root = Tk()
obj = Login(root)
root.mainloop()