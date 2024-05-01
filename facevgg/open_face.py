import cv2
from pathlib import Path

data_dirc = Path('/home/pranav/Code/facevgg/data')
empty_dirc = Path('/home/pranav/Code/facevgg/face_data')


def find_face(img_path, processed_dir):
    img = cv2.imread(str(img_path.resolve()))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
        faces = img[y:y + h, x:x + w]
        loc = processed_dir.joinpath(img_path.parent.name,img_path.name)
        # print(loc.resolve())
        cv2.imwrite(str(loc.resolve()), faces)
    

def data_processer(img_folder, processed_dir):
    files = img_folder.iterdir()

    for file in files:
        print(file.name)
        find_face(file,processed_dir)

if __name__=='__main__':
    print('main')
    # find_face('./data/Aaron_Guiel/Aaron_Guiel_0001.jpg')
    folders = data_dirc.iterdir()
    i=0
    for folder in folders:
        i+=1
        print('\t\t\t\t\tProcessing folder no.',i)
        empty_dirc.joinpath(folder.name).mkdir(exist_ok=True)
        data_processer(folder,empty_dirc)
    print('Data processing completed successfully...')