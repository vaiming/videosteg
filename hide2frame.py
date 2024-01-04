from PIL import Image
from tkinter import messagebox

import crypto
import os.path
import glob

def changeLast2Bits(origBits: int, newBits: int) -> int:

    #mengubah 2 bit terakhir dan menggantinya dengan yang baru
    return (origBits >> 2) << 2 | newBits


def filesizeToBytes(data: bytes) -> bytes:

    #mengembalikan ukuran data ke dalam 8 byte
    return (len(data)).to_bytes(8, byteorder='big')


def serializeData(data: bytes, padding: int = 1) -> list:

    serializedData = list()
    for datum in data:
        serializedData.append((datum >> 6) & 0b11)
        serializedData.append((datum >> 4) & 0b11)
        serializedData.append((datum >> 2) & 0b11)
        serializedData.append((datum >> 0) & 0b11)

    while len(serializedData) % padding != 0:
        serializedData.append(0)

    return serializedData


def deserializeData(data: list) -> bytes:

    deserializeData = list()
    for i in range(0, len(data) - 4 + 1, 4):
        datum = (data[i] << 6) + (data[i + 1] << 4) + (data[i + 2] << 2) + (data[i + 3] << 0)
        deserializeData.append(datum)

    return bytes(deserializeData)

def max_frame(frame_path = "C:/Viganografi/tmp/frame/"):
    
    #mencari frame dengan ukuran terbesar
 
    list_of_files = filter( os.path.isfile, glob.glob(frame_path + '*'))
    max_file = max(list_of_files, key =  lambda x: os.stat(x).st_size)
    max_file = os.path.basename(max_file)

    return max_file

magic_numbers = {

    #untuk menjadi identitas data file

    "encryptedLSB" : 0x131199aa,
    "docx" : bytes([0x50, 0x4B, 0x03, 0x04]),
    "pdf" : bytes([0x25, 0x50, 0x44, 0x46])
}

def check_file(data):
    
    #mengecek ekstensi file

    file_head = data[:8]
    
    if file_head.startswith(magic_numbers['docx']):
        docx_extension = ".docx"
        return docx_extension
    elif file_head.startswith(magic_numbers['pdf']):
        pdf_extension = ".pdf"
        return pdf_extension
    else:
        print("Please input docx or pdf file")    

def hideData(fileName, password): 

    #proses penyembunyian data pada frame

    mF = max_frame()
    frameName = "C:/Viganografi/tmp/frame/" + mF

    image = Image.open(frameName).convert('RGB')
    pixels = image.load()

    with open(fileName, "rb") as fN:
        r_data = fN.read()
    print("[*] {} Ukuran file : {} bytes".format(fileName, len(r_data)))

    enc_data = crypto.encryptData(r_data, password)
    print("Ukuran maksimal hidden file : {} bytes".format((image.size[0] * image.size[1] * 6) // 8))
    print("[*] Ukuran data terenkripsi: {} bytes".format(len(enc_data)))
    data = (magic_numbers["encryptedLSB"]).to_bytes(4, byteorder='big') + filesizeToBytes(enc_data) + enc_data

    if len(data) > (image.size[0] * image.size[1] * 6) // 8:
        print("[*] Melebihi ukuran maksimal Hidden File")
        messagebox.showerror("Error", "Pilih file dengan ukuran yang lebih kecil ! \nUkuran maksimal hidden file : {} bytes".format((image.size[0] * image.size[1] * 6) // 8))
        exit()

    print("[*] Hiding file in image")
    data = serializeData(data, padding=3)
    data.reverse()

    imageX, imageY = 0, 0
    while data:
            #pixel pada index dan y
        pixel_val = pixels[imageX, imageY]

            #menyembunyikan data pada 3 channel dari setiap pixel
        pixel_val = (changeLast2Bits(pixel_val[0], data.pop()),
                    changeLast2Bits(pixel_val[1], data.pop()),
                    changeLast2Bits(pixel_val[2], data.pop()))

        #menyimpan pixel yang telah diubah ke dalam gambar
        pixels[imageX, imageY] = pixel_val

        if imageX == image.size[0] - 1:                        
            imageX = 0
            imageY += 1
        else:
            imageX += 1

    print(f"[+] Saving image to {mF}")
    image.save(frameName)
    

def extractData(password):
    
    #mengekstrak data file dari frame
    
    framePath = "C:/Viganografi/tmp/frame/*.png"

    for images in glob.glob(framePath):
        frame = Image.open(images).convert('RGB')
        pixels = frame.load()

        data = list()                                 
        for frameY in range(frame.size[1]):
            for frameX in range(frame.size[0]):
                if len(data) >= 48:
                    break

                pixel = pixels[frameX, frameY]

                #mengekstrak data rahasia pada tiap channel
                data.append(pixel[0] & 0b11)
                data.append(pixel[1] & 0b11) 
                data.append(pixel[2] & 0b11)
        
        if deserializeData(data)[:4] == bytes.fromhex(hex(magic_numbers["encryptedLSB"])[2:]):
            print("[*] Extracting hidden file from image")

            hiddenDataSize = int.from_bytes(deserializeData(data)[4:16], byteorder='big') * 4

            data = list()
            for frameY in range(frame.size[1]):
                for frameX in range(frame.size[0]):
                    if len(data) >= hiddenDataSize + 48:
                        break

                    pixel = pixels[frameX, frameY]

                    data.append(pixel[0] & 0b11)
                    data.append(pixel[1] & 0b11)
                    data.append(pixel[2] & 0b11)

            data = deserializeData(data[48:])
            final_data = crypto.decryptData(data, password)
            ext = check_file(final_data)
            
            filePath = "C:/Viganografi/extracted file/extracted_data"
            output_fileName = filePath + ext
            for i in range(1, 1000):
                if os.path.isfile(output_fileName):
                    output_fileName = filePath + str(i) + ext
                else:
                    output_fileName

            with open(output_fileName, 'wb') as f:
                f.write(final_data)
            
            return output_fileName
            print(f"[*] Size of hidden file recovered : {len(final_data)} bytes")
            exit()
        else:
            print("Tidak ada file rahasia")
        


        

    