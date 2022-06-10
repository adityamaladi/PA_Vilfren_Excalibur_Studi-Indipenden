# WEB library
import streamlit.components.v1 as components
from secrets import choice
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import requests
# import dlib
# opencv library
import face_recognition
from datetime import datetime
from PIL import Image
import pandas as pd
import numpy as np
import cv2
import os
import time

# [theme]
# primaryColor="#F63366"
# backgroundColor="#FFFFFF"
# secondaryBackgroundColor="#F0F2F6"
# textColor="#262730"
# font="sans serif"

#lottie hiasan
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
###################################


FRAME_WINDOW = st.image([])  # frame window

hide_st_style = """ 
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)  # hide streamlit menu

path = 'Images_Attendance'
images = []
classNames = []
myList = os.listdir(path)
#print(myList)

menu = ["HOME", "PRESENSI","DATA"]  # menu
choice = st.sidebar.selectbox("Menu", menu)  # sidebar menu
# Object notation


col1, col2, col3, col4 = st.columns(4)  # columns
# cap = cv2.VideoCapture(0)  # capture video



if choice == 'PRESENSI':
    st.markdown("<h2 style='text-align: center; color: black;'>AMBIL DAFTAR HADIR</h2>",
                unsafe_allow_html=True)  # title
    with col1:  # column 1
        st.subheader("PRESENSI")
        run = st.checkbox("MULAI PRESENSI")  # checkbox
    if run == True:
        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])
        print(classNames)

        def findEncodings(images):
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            return encodeList

        def markAttendance(name):
            with open ('Attendance.csv','r+')as f:
                myDataList = f.readlines()
                # print(myDataList)
                nameList = []
                for line in myDataList:
                    entry = line.split(',')
                    # print(entry[0])
                    nameList.append(entry[0])
                if name not in nameList:
                    now = datetime.now()
                    tString = now.strftime('%d:%m:%Y')
                    dtString = now.strftime('%H:%M:%S')
                    f.writelines(f'\n{name},{dtString},{tString}')

        encodeListKnown = findEncodings(images)
        print('Encoding Complete')
        cap = cv2.VideoCapture(0)

        while True:
            success, img = cap.read()
            # img = captureScreen()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                # print(faceDis)
                matchIndex = np.argmin(faceDis)
                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                # print(name)
                # else: name = "unknown"
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                markAttendance(name)
            FRAME_WINDOW.image(img)
            cv2.waitKey(1)

    else:
        pass


elif choice == 'DATA':
        df = pd.read_csv('Attendance.csv')
        st.subheader("HASIL PRESENSI")
        df = pd.read_csv('Attendance.csv')
        st.write(df)

        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')
        my_large_df = pd.read_csv('Attendance.csv')
        csv = convert_df(my_large_df)
        now = datetime.now()
        tString = now.strftime('%d:%m:%Y')
        if st.download_button(
            label="Download Data Absensi ",
            data=csv,
            file_name=f'Presensi Kelas/{tString}',
            mime='csv',
        ):
            st.success('File Berhasil Didowload')


elif choice == 'HOME':
    with st.container():
        lottie_url_loading = 'https://assets10.lottiefiles.com/private_files/lf30_esg1l8r1.json'
        lottie_loading = load_lottieurl(lottie_url_loading)
        with st_lottie_spinner(lottie_loading):
            time.sleep(5)
        # st.title("WELCOME MOTHERFUCKER")
        opeindo = Image.open('Images/Vilfren.jpg')
        st.image(opeindo, caption='Vilfrend Excalibur')

        st.write('##')
        st.write('##')
        left_column, right_column = st.columns(2)
        with left_column:
            st.subheader('PRESENSI')
            st.write(
            """
            - Didalam menu presensi anda bisa langsung mengklik "Mulai Presensi" Maka Mesin akan secara otomatis mengambil data wajah peserta didik.
            - Sebelum melakukan presensi pastian perangkat yang anda gunakan terhubung dengan WEBCAM "CCTV".
            - Ketika melakukan presensi peserta didik dianjurkan untung menghadap kamera WEBCAM "CCTV" Untuk memaksimalkan akurasi mesin.
            """)
            st.write('##')
        lottie_url_attendance = 'https://assets8.lottiefiles.com/packages/lf20_HQ3RPY.json'
        lottie_attendance = load_lottieurl(lottie_url_attendance)
        # lottie_attendance
        with right_column:
            st.write('##')
            st_lottie(
                lottie_attendance,
                reverse=False,
                loop = True,
                width=250
            )
            st.write('##')
            st.write('##')

        with left_column:
            st.subheader('DATA')
            st.write(
                """
                - Pada Menu data Terdapat Visualisai data yang akan muncul setelah anda melakukan presensi.
                - Pada Menu data anda juga bisa langsung mendowload hasil presensi dengan format CSV ke prangkat anda.
                """)
            st.write('##')
        lottie_url_list = 'https://assets2.lottiefiles.com/packages/lf20_pjagkisd.json'
        lottie_list = load_lottieurl(lottie_url_list)
        with right_column:
            st.write('##')
            st_lottie(
                lottie_list,
                reverse=False,
                loop=True,
                width=250
            )

        # with left_column:
        #     st.subheader('TENTANG')
        #     st.write(
        #         """
        #         - Pada Menu Tentang terdapat dokumentasi tentang projek absensi wajah otomatis ini.
        #         - Pada Menu Tentang anda bisa mengakses informasi terkait Kelompok Vilfriend Excalibur
        #         - Pada Menu Tentang Terdapat Profile dari Creator projek ini
        #         """)
        #     st.write('##')
        # lottie_url_team = 'https://assets1.lottiefiles.com/packages/lf20_VWOntT.json'
        # lottie_team = load_lottieurl(lottie_url_team)
        # with right_column:
        #     # st.write('#')
        #     st_lottie(
        #         lottie_team,
        #         reverse=False,
        #         loop=True,
        #         width=250
        #         )