import cv2
import os
import numpy as np
import face_recognition
import pickle
import cvzone
from datetime import datetime
from firebase_admin import credentials, db, storage
import firebase_admin


class FaceRecognitionService:
    def __init__(self, encode_file_path):
        self.encode_list_known, self.student_ids = self.load_encodings(encode_file_path)

    def load_encodings(self, file_path):
        
        print("Loading Encode File ...")
        
        with open(file_path, 'rb') as file:
            encode_list_known_with_ids = pickle.load(file)
        print("Encode File Loaded")
        return encode_list_known_with_ids

    def detect_faces(self, img):
        
        img_resized = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        img_resized = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(img_resized)
        face_encodings = face_recognition.face_encodings(img_resized, face_locations)
        return face_locations, face_encodings

    def match_face(self, encode_cur_frame):
        
        matches = face_recognition.compare_faces(self.encode_list_known, encode_cur_frame)
        
        face_distances = face_recognition.face_distance(self.encode_list_known, encode_cur_frame)
        match_index = np.argmin(face_distances)
        return matches, match_index, face_distances


class FirebaseService:
    def __init__(self, cred_path, db_url, storage_bucket):
        self.initialize_firebase(cred_path, db_url, storage_bucket)
        self.bucket = storage.bucket()

    def initialize_firebase(self, cred_path, db_url, storage_bucket):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': db_url,
            'storageBucket': storage_bucket
        })

    def get_student_info(self, student_id):
        
        return db.reference(f'Students/{student_id}').get()

    def update_attendance(self, student_id, attendance_data):
        ref = db.reference(f'Students/{student_id}')
        ref.child('total_attendance').set(attendance_data['total_attendance'])
        ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def get_student_image(self, student_id):
        
        blob = self.bucket.get_blob(f'Images/{student_id}.png')
        array = np.frombuffer(blob.download_as_string(), np.uint8)
        return cv2.imdecode(array, cv2.COLOR_BGRA2BGR)


class UIService:
    def __init__(self, background_path, mode_folder_path):
        
        self.img_background = cv2.imread(background_path)
        self.img_mode_list = self.load_mode_images(mode_folder_path)

    def load_mode_images(self, folder_path):
        mode_images = []
        mode_paths = os.listdir(folder_path)
        for path in mode_paths:
            mode_images.append(cv2.imread(os.path.join(folder_path, path)))
        return mode_images

    def update_ui(self, img, img_student, student_info, mode_type, counter):
        self.img_background[162:162 + 480, 55:55 + 640] = img
        self.img_background[44:44 + 633, 808:808 + 414] = self.img_mode_list[mode_type]

        if counter <= 10:
            self.display_student_info(student_info)
            
            self.img_background[175:175 + 216, 909:909 + 216] = img_student

        cv2.imshow("Face Attendance", self.img_background)

    def display_student_info(self, student_info):
        
        cv2.putText(self.img_background, str(student_info['total_attendance']), (861, 125),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
        cv2.putText(self.img_background, str(student_info['major']), (1006, 550),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(self.img_background, str(student_info['standing']), (910, 625),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
        # Add more fields as needed


class AttendanceSystem:
    def __init__(self):
        self.face_recognition_service = FaceRecognitionService('EncodeFile.p')
        self.firebase_service = FirebaseService("serviceAccountKey.json",
                                                "https://faceattendancerealtime-33ca0-default-rtdb.firebaseio.com/",
                                                "faceattendancerealtime-33ca0.appspot.com")
        self.ui_service = UIService('Resources/background.png', 'Resources/Modes')
        self.cap = self.setup_camera()

    def setup_camera(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)
        return cap

    def run(self):
        mode_type = 0
        counter = 0
        student_id = -1
        img_student = []

        while True:
            success, img = self.cap.read()
            face_locations, face_encodings = self.face_recognition_service.detect_faces(img)

            if face_locations:
                for encode_face, face_loc in zip(face_encodings, face_locations):
                    matches, match_index, face_distances = self.face_recognition_service.match_face(encode_face)

                    if matches[match_index]:
                        student_id = self.face_recognition_service.student_ids[match_index]
                        if counter == 0:
                            counter = 1
                            mode_type = 1

                if counter != 0:
                    student_info = self.firebase_service.get_student_info(student_id)
                    img_student = self.firebase_service.get_student_image(student_id)
                    seconds_elapsed = (datetime.now() - datetime.strptime(student_info['last_attendance_time'],
                                                                          "%Y-%m-%d %H:%M:%S")).total_seconds()

                    if seconds_elapsed > 30:
                        student_info['total_attendance'] += 1
                        self.firebase_service.update_attendance(student_id, student_info)
                    else:
                        mode_type = 3
                        counter = 0

                self.ui_service.update_ui(img, img_student, student_info, mode_type, counter)
                counter = (counter + 1) % 20
            else:
                mode_type = 0
                counter = 0

            cv2.waitKey(1)


if __name__ == "__main__":
    system = AttendanceSystem()
    system.run()
