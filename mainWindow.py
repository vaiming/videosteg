from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.filedialog import askopenfile
from hide2frame import extractData, hideData
from crypto import encryptData, decryptData
from os import path
import tkinter.font as font
import os.path
import sys
from main import hideDataFile, extractDataFile

def main():
    root = Tk()
    root.title("ViGanografi")
    root.configure(bg='#C0C0C0')
    root.resizable(False, False)
    window_width = 600
    window_height = 360

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()    
 
    position_top = int(screen_height/2 - window_height/2)
    position_right = int(screen_width/2 - window_width/2)
    root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')


    def hideWindow():
        root.destroy()
        hW = Tk()
        hW.title("Viganografi")
        hW.configure(bg='#C0C0C0')
        hW.resizable(False, False)

        window1_width = 600
        window1_height = 400
        
        screen1_width = hW.winfo_screenwidth()
        screen1_height = hW.winfo_screenheight()
        nPosition_top = int(screen1_height/2 - window1_height/2)
        nPosition_right = int(screen1_width/2 - window1_width/2)
        hW.geometry(f'{window1_width}x{window1_height}+{nPosition_right}+{nPosition_top}')
        
        def browse_video():
            file = filedialog.askopenfile(mode='r', filetypes=[('Video Files', '*.mp4')])
            if file:
                filepath = os.path.abspath(file.name)
                eV.delete(0, 'end')
                eV.insert(END, filepath)

        def browse_file():
            file = filedialog.askopenfile(mode='r', filetypes=[('File Files', '*.docx'), ('Pdf Files', '*.pdf')])
            if file:
                filepath = path.abspath(file.name)
                eF.delete(0, 'end')
                eF.insert(END, filepath) 

        def hide_command():
            videoName = eV.get()
            fileName = eF.get()
            password = eP.get()
            if not (videoName or fileName or password) :
                messagebox.showwarning("Warning", "Isilah kolom Path Video, File, dan Password !")
            elif not videoName :
                messagebox.showwarning("Warning", "Isilah kolom Path Video !")
            elif not fileName :
                messagebox.showwarning("Warning", "Isilah kolom Path File !")
            elif not password :
                messagebox.showwarning("Warning", "Isilah kolom Password !")
            elif not (path.exists(videoName) or path.exists(fileName)) :
                messagebox.showwarning("Warning", " Path Video dan File tidak ditemukan !\n Silahkan periksa kembali")
            elif not path.exists(videoName) :
                messagebox.showwarning("Warning", " Path Video tidak ditemukan !\n Silahkan periksa kembali")
            elif not path.exists(fileName) :
                messagebox.showwarning("Warning", " Path File tidak ditemukan !\n Silahkan periksa kembali")
            else :                
                hideDataFile(videoName, fileName, password)

        def clear():
            eV.delete(0, 'end')
            eF.delete(0, 'end')
            eP.delete(0, 'end')

        def backMenu():
            hW.destroy()
            main()
        
        fontBtn = ("Hungry Charlie Serif", 12, "bold")
        fontLbl = font.Font(family="Altone", size=9)
        title = Label(hW, text="Hide File", font=("Hungry Charlie Serif", 20, "bold"), 
                padx=600, pady=15, bg="#E5E4E2")
        title.pack(pady=5)

        lV = Label(hW, text="Pilih Path Video :", font=fontLbl, bg='#C0C0C0')
        lV.pack(pady=5)        
        eV = Entry(hW, width=65)
        eV.pack()        
        bV = Button(hW, text="Pilih Video", command=browse_video, font=fontLbl)
        bV.pack(pady=8)
        
        lF = Label(hW, text="Pilih Path File :", font=fontLbl, bg='#C0C0C0')
        lF.pack(pady=5)
        eF = Entry(hW, width=65)
        eF.pack()        
        bF = Button(hW, text="Pilih File", command=browse_file, font=fontLbl)
        bF.pack(pady=8)

        lP = Label(hW, text="Password :", font=fontLbl, bg='#C0C0C0')
        lP.pack(pady=5)
        eP = Entry(hW, width=65)
        eP.pack()

        Button(hW, text='Sisipkan', font=("Hungry Charlie Serif", 11, "bold"), command=hide_command).place(x=115, y=345)
        Button(hW, text='Bersihkan', font=("Hungry Charlie Serif", 11, "bold"), command=clear).place(x=262, y=345)
        Button(hW, text='Kembali', font=("Hungry Charlie Serif", 11, "bold"), command=backMenu).place(x=415, y=345)
        
        hW.mainloop()

    def extractWindow():
        root.destroy()
        eW = Tk()
        eW.title("Viganografi")
        eW.configure(bg='#C0C0C0')
        eW.resizable(False, False)

        window1_width = 580
        window1_height = 325
        
        screen1_width = eW.winfo_screenwidth()
        screen1_height = eW.winfo_screenheight()
        nPosition_top = int(screen1_height/2 - window1_height/2)
        nPosition_right = int(screen1_width/2 - window1_width/2)
        eW.geometry(f'{window1_width}x{window1_height}+{nPosition_right}+{nPosition_top}')
        
        def browse_video():
            file = filedialog.askopenfile(mode='r', filetypes=[('Video Files', '*.mp4')])
            if file:
                filepath = os.path.abspath(file.name)
                eV.delete(0, 'end')
                eV.insert(END, filepath)

        def browse_file():
            file = filedialog.askopenfile(mode='r', filetypes=[('File Files', '*.docx'), ('Pdf Files', '*.pdf')])
            if file:
                filepath = os.path.abspath(file.name)
                eF.delete(0, 'end')
                eF.insert(END, filepath) 

        def extract_command():
            videoName = eV.get()
            password = eP.get()
            if not (videoName or password) :
                messagebox.showwarning("Warning", "Isilah kolom Path Video dan Password !")
            elif not videoName :
                messagebox.showwarning("Warning", "Isilah kolom Path Video !")
            elif not password :
                messagebox.showwarning("Warning", "Isilah kolom Password !")
            elif not path.exists(videoName) :
                messagebox.showwarning("Warning", " Path Video tidak ditemukan !\n Silahkan periksa kembali")
            else :                
                extractDataFile(videoName, password)

        def clear():
            eV.delete(0, 'end')
            eP.delete(0, 'end')

        def backMenu():
            eW.destroy()
            main()

        fontt = ("Hungry Charlie Serif", 12, "bold")
        fontLbl = font.Font(family="Altone", size=9)
        Label(eW, text="Extract File", font=("Hungry Charlie Serif", 20, "bold"), 
                padx=600, pady=15, bg="#E5E4E2").pack(pady=5)

        lV = Label(eW, text="Pilih Path Video Embedded:", font=fontLbl, bg='#C0C0C0')
        lV.pack(pady=5)
        eV = Entry(eW, width=60)
        eV.pack()
        bV = Button(eW, text="Pilih Video", command=browse_video, font=fontLbl)
        bV.pack(pady=8)

        lP = Label(eW, text="Password :", font=fontLbl, bg='#C0C0C0')
        lP.pack(pady=5)
        eP = Entry(eW, width=60)
        eP.pack()

        Button(eW, text='Ekstrak', font=("Hungry Charlie Serif", 11, "bold"), padx=8, command=extract_command).place(x=105, y=275)
        Button(eW, text='Bersihkan', font=("Hungry Charlie Serif", 11, "bold"), command=clear).place(x=254, y=275)
        Button(eW, text='Kembali', font=("Hungry Charlie Serif", 11, "bold"), command=backMenu).place(x=410, y=275)
        
        eW.mainloop()

    fontt = ("Hungry Charlie Serif", 12, "bold")
    Label(root, text="Pilih Mode", font=("Hungry Charlie Serif", 20, "bold"), 
            padx=600, pady=15, bg="#E5E4E2").pack(pady=5)
    hideBtn = Button(root, text='Hide File', font=fontt, padx=38, pady=55, command=hideWindow)
    hideBtn.place(x=90, y=120)

    extractBtn = Button(root, text='Extract File', font=fontt, padx=26, pady=55, command=extractWindow)
    extractBtn.place(x=350, y=120)
    
    root.mainloop()


if __name__ == "__main__":    
    main()
