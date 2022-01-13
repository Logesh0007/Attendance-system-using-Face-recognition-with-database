import datetime
from datetime import date
import time
import os
import mysql.connector
import cv2
import numpy
import os
import imutils

con = mysql.connector.connect(host="localhost",user="****",password="****",database="****") # pls give ur username, password and database name 
cur = con.cursor()

register = []   # type the students name here, those who are not in this register list are not allowed to enter the class
presenters = []    # don't write anything it'll append the names who are all present 

name=""
name_of_person = ""

def face_authentication():
    global name_of_person
    name_check = input("Enter your name for authentication : ")     # its only for authentication purpose
    print("Please show your face to camera for security purpose")
    haar_file="D:\\Python\\Projects\\Attendance using facial recognition\\haarcascade_frontalface_default.xml"     # pls mention the correct directory of XML file   
    face_cascade=cv2.CascadeClassifier(haar_file)
    datasets="D:\\Python\\Projects\\Attendance using facial recognition\\datasets"    # pls mention the correct directory for datasets
    (images,labels,names,id)=([],[],{},0)
    cam=cv2.VideoCapture(0)
    for (subdirs,dirs,files) in os.walk(datasets):
        for subdir in dirs:
            names[id]=subdir
            subjectpath=os.path.join(datasets,subdir)
            for filename in os.listdir(subjectpath):
                path=subjectpath + '/' + filename
                label=id
                images.append(cv2.imread(path,0))
                labels.append(int(label))
            id+=1
    (width,height)=(130,100)
    (images,labels)=[numpy.array(lis) for lis in [images,labels]]
    model=cv2.face.FisherFaceRecognizer_create()
    model.train(images,labels)
    print("Detecting student's face")
    cnt=0
    while True:
        img=cam.read()[1]
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=face_cascade.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
            face=gray[y:y+h,x:x+w]
            face_resize=cv2.resize(face,(width,height))
            prediction=model.predict(face_resize)
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
            if prediction[1]<800:
                cv2.putText(img,"%s-%.0f"% (names[prediction[0]],prediction[1]),(x+0,y-20),cv2.FONT_HERSHEY_TRIPLEX,1,(0,255,255),2)
                print(names[prediction[0]])
                name_of_person=names[prediction[0]]
                if name_of_person in register:
                    cam.release()
                    cv2.destroyAllWindows()  
                    timing()
                cnt=0
                
            else:
                cnt+=1
                cv2.putText(img,"unknown",(x-10,y-10),cv2.FONT_HERSHEY_TRIPLEX,1,(0,255,255),2) 
                if (cnt>100):
                    print("Unknown Person")   
                    cv2.imwrite("unknown.png",img)
                    unknown_persons ="D:\\Python\\Projects\\Attendance using facial recognition\\unknown_persons"    # pls mention the correct directory for unknown persons
                    path = os.path.join(unknown_persons,name_check)
                    if not os.path.isdir(path):
                        os.mkdir(path)
                        cv2.imwrite("%s/%s.png"%(path,cnt),img)
                    cam.release()
                    cv2.destroyAllWindows()  
                    cnt=0
                    page_refresh()
        cv2.imshow("Face authentication",img)
        key=cv2.waitKey(10)
        if key==27:
            break        

def intro():
    print()
    print("\t\t\t\t---------------------")
    print("\t\t\t\t       WELCOME")
    print("\t\t\t\t---------------------")
    print()
    time.sleep(1)
    Date = date.today().strftime("%d:%m:%y")
    print("Today's date : ",Date)

    time.sleep(1)
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        print("Good morning")
    elif hour>=12 and hour<=18:
        print("Good afternoon")

    face_authentication()
        
def timing():
    t = datetime.datetime.now().strftime("%H:%M:%S")
    if t > "09:00:00":
        time.sleep(1)
        print()
        print("The time is",t)
        print("Its already late...,  Please type quickly")
        print()
        late_commer()
    else:
        time.sleep(1)
        print("The time is",t,"please type before 9am")
        print("or else u'll marked as a late comer")
        print()
        correct_time()

def correct_time():
    global name_of_person
    global name
    while True:         
        time.sleep(1)
        name = input("Enter your name                               :  ")
        print()
        print("wait a moment ....  checking for name verification")
        if name in register:
            time.sleep(1)
            print("------------------------------------------------")
            print(" **  You are in the class register  **")
            print("------------------------------------------------")
        else:
            time.sleep(2)
            print()
            print("You are not in the class register or You have already entered into the class")
            time.sleep(1)
            print("Please check the database")
            intro()
        time.sleep(1)
        print()
        
        year = input("Enter your class ( For eg. I, II, III, IV )   :  ")
        department = input("Enter your department                        :  ")
        sec = input("Enter your section ( For eg. a,b,c .... )     :  ")

        if name == name_of_person:
            print()
            print("Please wait...")
            time.sleep(1)
            print("Permission granted   !!!")
            time.sleep(2)
        else:
            print("Access denied ")
            time.sleep(1)
            print("Please show your face properly or your face may not be registered in the dataset")
            print("Check the dataset folder in your directory")
            time.sleep(1)
            intro()

        timing = datetime.datetime.now().strftime("%H:%M:%S")
        if timing <= "09:00:00":
            print()
            print("You came to the class at correct time")        
        else:
            print()
            print("please come to the class before 9am  ")

        query = "insert into attendance values ('{}','{}','{}','{}','{}')".format(name,year,department,sec,timing)
        cur.execute(query)
        con.commit()
        time.sleep(1)
        print()
        print("Your details are stored in Database successfully")
        time.sleep(1)
        print("please refresh the page for others to register their attendance")
        time.sleep(1)
        print()
        print("--------------------------")
        print("    Have a nice day : )")
        print("--------------------------")
        register.remove(name)
        presenters.append(name)
        page_refresh()


def page_refresh():
    print()
    print("1. Refresh")
    print("2. Register")
    print("3. Exit")
    choice = input("Enter your choice : ")
    if choice == '1':
        clear = lambda: os.system("cls")
        clear()
        intro()
    elif choice == '2':
        attendance_register()
    elif choice == '3':
        print("Thank you")
        exit()
    else:
        print("You have entered the wrong choice")
        time.sleep(2)
        print("Please choose the correct option")
        page_refresh()

def attendance_register():
    print()
    print("Present : ",presenters)
    print()
    print("Absentees : ",register)
    absent = input("Do you want to store the absentees list ( y / n ) : ")
    if absent == 'y':
        absentees()
    else:
        print("Thank you")
    page_refresh()
    
def late_commer():
    global name
    global name_of_person
    while True:
        time.sleep(1)
        name = input("Enter your name                               :  ")
        print()
        print("wait a moment ....  checking for name verification")
        if name in register:
            time.sleep(2)
            print("**  You are in the class register  **")
        else:
            time.sleep(2)
            print("You are not in the class register or You have already entered into the class")
            time.sleep(1)
            print("Please check the database")
            page_refresh()
        time.sleep(1)
        print()
        
        year = input("Enter your class ( For eg. I, II, III, IV )   :  ")
        department = input("Enter your department                        :  ")
        sec = input("Enter your section ( For eg. a,b,c .... )     :  ")
        if name == name_of_person:
            print()
            print("Please wait...")
            time.sleep(1)
            print("Permission granted   !!!")
            time.sleep(2)
        else:
            print("Access denied ")
            time.sleep(1)
            print("Please show your face properly or your face may not be registered in the dataset")
            print("Check the dataset folder in your directory")
            time.sleep(1)
            intro()

        timing = datetime.datetime.now().strftime("%H:%M:%S")
        if timing <= "09:00:00":
            print()
            print("You came to the class at correct time")        
        else:
            print()
            print("please come to the class before 9am  ")
            
        query = "insert into attendance values ('{}','{}','{}','{}','{}')".format(name,year,department,sec,timing)
        cur.execute(query)
        con.commit()
        time.sleep(1)
        print()
        print("Your details are stored in Database successfully")
        time.sleep(1)
        print("please refresh the page for others to register their attendance")
        time.sleep(1)
        print()
        print("--------------------------")
        print("    Have a nice day : )")
        print("--------------------------")
        register.remove(name)
        presenters.append(name)
        page_refresh()

def absentees():
    global name
    while True:
        print()
        for i in register:
            if len(register) == 0:
                break
            else:
                query = "insert into absentees values ('{}')".format(i)
                cur.execute(query)
                con.commit()
        print("Absentees list added successfully")
        time.sleep(2)
        page_refresh()
    
if __name__ == "__main__":
    intro()

