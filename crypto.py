from cryptography.fernet import Fernet
from tkinter import messagebox
import base64
import hashlib

def encryptData(data, password):
    key = base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

    f = Fernet(key)
    encData = f.encrypt(data)
    print("Data berhasil terenkripsi")
    return encData

def decryptData(data, password):
    try:
        key = base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

        f = Fernet(key)
        decData = f.decrypt(data)
        print("Data berhasil didekripsi")
        return decData
    except:
        print("[!] Password atau data invalid")
        messagebox.showerror("Gagal", "Ekstraksi file gagal ! \nPassword yang anda masukan salah")
        exit()

