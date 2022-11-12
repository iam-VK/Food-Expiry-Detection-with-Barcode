# MYSQL QUERIES:
# create database fooddb;
# create table productlist(bcode varchar(25),
#                             pid varchar(25) NOT NULL unique,
#                             mfg date NOT NULL unique,
#                             exp date NOT NULL unique,
#                             PRIMARY KEY(bcode));
# insert into productlist(bcode,pid,mfg,exp) values
#                               (0716270001660,"Lays","2022-10-22","2022-04-22"),
#                               (0745125097060,"Milk","2022-11-12","2022-11-14"),
#                               (0705632085943,"Maggie","2022-04-10","2022-12-10"),
#                               (2260001001958,"Cheese","2022-07-06","2022-10-04");

import cv2
from pyzbar.pyzbar import decode
from pyzbar import pyzbar
from PIL import Image
import mysql.connector
from datetime import date

barcode_info=''

fooddb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="fooddb"
)
dbcom=fooddb.cursor()

def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y , w, h = barcode.rect
        
        global barcode_info 
        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
        
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
    return frame

def scanner(loc):
    img = Image.open(loc)
    result = decode(img)
    code=""

    for i in result:
        code+=str(i)
    return result[0].data.decode("utf-8")

def getDetails(bcode):
    dbcom.execute("Select pid,mfg,exp from fooddb.productlist where bcode={}".format(bcode))

    result=dbcom.fetchone()
    name=result[0]
    mfg=result[1]
    exp=result[2]

    print("Product Name      : ",name)
    print("Manufactured Date : ",mfg)
    print("Expiry Date       : ",exp)
    print()
    print("Result            : ","Item is EDIBLE" if (date.today()<exp) else "Item EXPIRED")

def main():
    global barcode_info
    userchoice=int(input('''Preffered barcode scanning choice:\n
                            1.Scan by uploading file\n
                            2.Scan from camera\n
                            Selected option: '''))
    if userchoice==1:
        source=input("File Path: ")
        barcode_info=scanner(source)
    
    elif userchoice==2:
        camera = cv2.VideoCapture(0)
        ret, frame = camera.read()
        
        while ret:
            ret, frame = camera.read()
            frame = read_barcodes(frame)
            cv2.imshow('Barcode/QR code reader', frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break
            if barcode_info!='':
                break

        print(barcode_info)
        camera.release()
        cv2.destroyAllWindows()
    
    else:
        print("Invalid choice")
        exit()

    print("\nSMART SYSTEM FOR DETECTING FOOD IS EDIBLE/EXPIRED")
    
    print("\nBar code          : ",barcode_info)
    getDetails(barcode_info)


if __name__ == '__main__':
    main()
