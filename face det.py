import cv2
import os

alg="haarcascade_frontalface_default.xml"  # mention the directory correctly
haar=cv2.CascadeClassifier(alg)
datasets="datasets"  # mention the directory to store dataset
name="sk"    # name for the folder name in datasets, change names for the next time while u doing the dataset creation process 

cam=cv2.VideoCapture(0)   # if u r using webcam type (0) or u r using additional camera means type (1)
path=os.path.join(datasets, name)
if not os.path.isdir(path):
    os.mkdir(path)

(width,height)=(130,100)
count=1

while count<61:   # It'll take 60 images, u can change it for ur wish
    print(count,end=" - ")
    img=cam.read()[1]
    grayImg=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=haar.detectMultiScale(grayImg,1.3,5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        onlyFace=grayImg[y:y+h,x:x+w]
        resizeImg=cv2.resize(onlyFace,(width,height))
        cv2.imwrite("%s/%s.png"%(path,count),resizeImg)
        count+=1

    cv2.imshow("FaceDetection",img)
    key=cv2.waitKey(10)
    
    print("Face Captured Successfully")
    if key==27:     # 27 represent the keyboard value for esc button
        break

cam.release()
cv2.destroyAllWindows()
