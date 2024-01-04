from subprocess import call,STDOUT
from hide2frame import extractData, hideData
from crypto import encryptData, decryptData
from PIL import Image
from tkinter import messagebox

import cv2
import os
import glob
import shutil 
import time

path = "C:/Viganografi"
if not os.path.exists(path):
    os.makedirs(path)
    print("[INFO] Folder berhasil dibuat")
else :
    pass

if not os.path.exists(path + "/output"):
    os.makedirs(path + "/output")
    print("[INFO] Folder berhasil dibuat")
else :
    pass

if not os.path.exists(path + "/extracted file"):
    os.makedirs(path + "/extracted file")
    print("[INFO] Folder berhasil dibuat")
else :
    pass


def get_frames(videoName):

    #ekstrak frame dari video

    if not os.path.exists(path + "/tmp/frame"):
        os.makedirs(path + "/tmp/frame")
    frame_path = path + "/tmp/frame/Frame%d.png"
    print("[INFO] tmp folder berhasil dibuat")
    
    call(
        ["ffmpeg", "-i", videoName, frame_path],
        stdout=open(os.devnull, "w"), stderr=STDOUT
    )
    print("Ekstrak Frame Selesai")

def get_audio(videoName):

    #ekstrak audio dari video

    if not os.path.exists(path + "/tmp/audio"):
        os.makedirs(path + "/tmp/audio")
    vName = os.path.basename(videoName)
    audio_path = path + "/tmp/audio/audio_" + ''.join(vName.split('.')[:-1]) + ".aac"
    
    call(
        ["ffmpeg", "-i", videoName, "-map", "0:a", "-q:a", "0", "-acodec", "copy", audio_path],
        stdout=open(os.devnull, "w"), stderr=STDOUT
    )
    print("Ekstrak Audio Selesai")

    return audio_path

def hideDataFile(videoName, fileName, password):

    #proses penyisipan file dan pembuatan video dari frame

    try:
        start = time.time()
        
        if not os.path.exists(path + "/tmp/silent video"):
            os.makedirs(path + "/tmp/silent video")

        get_frames(videoName)
        audio = get_audio(videoName)
        hideData(fileName, password)

        capture = cv2.VideoCapture(videoName)
        fps = capture.get(cv2.CAP_PROP_FPS)
        fps = str(fps)
        vName = os.path.basename(videoName)
        
        silent_video = path  + "/tmp/silent video/no_sound_" + ''.join(vName.split('.')[:-1]) + ".mp4"
        call(
            ["ffmpeg", "-framerate", fps, "-i", "C:/Viganografi/tmp/frame/Frame%d.png", "-c:v", "copy", silent_video],
            stdout=open(os.devnull, "w"), stderr=STDOUT
        )
        
        if not os.path.exists(path + "/output"):
            os.makedirs(path + "/output")
            print("[INFO] Folder berhasil dibuat")
        else :
            pass

        output_name = path + "/output/Embedded_Video_" + ''.join(vName.split('.')[:-1]) + ".mp4" 
        for i in range(1, 1000):
            if os.path.isfile(output_name):
                output_name = path + "/output/Embedded_Video_" + "".join(vName.split('.')[:-1]) + str(i) + ".mp4"
            else:
                output_name
        call(
            ["ffmpeg", "-i", silent_video, "-i", audio, "-c", "copy", "-map", "0:v", "-map", "1:a", output_name],
            stdout=open(os.devnull, "w"), stderr=STDOUT
        )
        clean_tmp()
        print("sukses")
        
        end = time.time()
        total = end - start
        count_time = "{:.3f}".format(total)
        messagebox.showinfo("Sukses", "Penyisipan file berhasil ! \nVideo disimpan di \n" + output_name + "\nWaktu penyisipan : " + count_time + " detik")
    except:
        clean_tmp()
        print("Penyisipan gagal")


def extractDataFile(videoName, password):
    
    #ekstraksi file dari video embedded

    try:
        start = time.time()
        
        get_frames(videoName)
        path = extractData(password)
        clean_tmp()
        
        end = time.time()
        total = end - start
        count_time = "{:.3f}".format(total)
        messagebox.showinfo("Sukses", "Ekstraksi file berhasil ! \nFile disimpan di \n" +path+ "\nWaktu ekstraksi : " + count_time + " detik")
    except:
        clean_tmp()
        messagebox.showinfo("Info", "Tidak ada file rahasia")
        
def clean_tmp(path="C:/Viganografi/tmp"):

    #menghapus folder tmp

    if os.path.exists(path):
        shutil.rmtree(path)
        print("[INFO] tmp folder berhasil dihapus")
