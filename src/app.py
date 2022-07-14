import cv2
import streamlit as st
from deepstack_sdk import ServerConfig, Detection, Face
from PIL import Image
import numpy as np
import base64
import uuid
import time
import requests
import threading

# To increase the width of sidebar
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 440px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 440px;
        margin-left: -440px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# sidebar components

logo = Image.open("deepstack_logo.png")
app_logo = logo.resize((100, 100))
st.sidebar.image(app_logo)

st.sidebar.title("Settings")
selected_box = st.sidebar.selectbox(
    'Choose an API',
    ('Object Detection', 'Face Registration', 'Face Deregistration', 'Face Recognition', 'Face Detection', 'Custom Detection')
)

deepstack_url = st.sidebar.text_input("Enter your DeepStack URL", placeholder="http://localhost:80")
config = ServerConfig("{}".format(deepstack_url))

camera_address = st.sidebar.text_input("Enter your Camera Address", placeholder="0 or http://admin:password@192.168.1.134:8081/video")

custom_name = st.sidebar.text_input("Custom Model Name  (Optional)", placeholder="actionnetv2")

run = st.sidebar.button('Start >>>')

webhook_url = st.sidebar.text_input("WebHook URL (Optional)", placeholder="your Webhook url")
webhook_api_key = st.sidebar.text_input("WebHook API Key (Optional)", placeholder="your API key")

webhook_forward_images = st.sidebar.selectbox('Webhook Forward Images (Optional)', ('False', 'True'))

webhook_triggered = False
webhook_data = {}


def welcome(title):
    app_logo2 = logo.resize((40, 40))
    st.image(app_logo2)
    st.header(f"DeepStack-CameraUI {title}")
    st.text("Configure the Camera and DeepStack API in the sidebar")
    st.text("The Camera and Detections will show below")


def image_base64_converter(img):
    retval, buffer = cv2.imencode('.jpg', img)
    img_base64 = base64.b64encode(buffer)
    return img_base64.decode("utf-8")


def uuid_generator():
    result = uuid.uuid4()
    uuid_key = str(result)
    return uuid_key


def run_webhook():
    global webhook_data
    global webhook_triggered

    while True:
        if webhook_data and webhook_triggered and len(list(webhook_data)) > 0:
            queued_data_values_batch = list(webhook_data.values())
            webhook_data.clear()
            try:
                requests.post(webhook_url, json=queued_data_values_batch)
            except:
                st.error("Webhook URL Unavailable ")
        time.sleep(1)


def webhook_thread():
    global webhook_triggered
    webhook_run_thread = threading.Thread(target=run_webhook)
    webhook_run_thread.start()


client_id = uuid_generator()


def object_detection():
    detection = Detection(config)

    global webhook_data
    global webhook_triggered
    webhook_thread()
    frame = st.image([])
    if camera_address.isdigit():
        camera = cv2.VideoCapture(int(camera_address))
    else:
        camera = cv2.VideoCapture('{}'.format(camera_address))

    object_detection_active = True
    if webhook_url and webhook_triggered is False:
        webhook_triggered = True

    while run:
        if object_detection_active is False:
            break
        else:
            _, img = camera.read()
            if img is None:
                st.error("Check your settings !")
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            response = detection.detectObject(img, output=None)
            objdetec_data = []
            for obj in response:
                cv2.rectangle(img, (obj.x_min, obj.y_min), (obj.x_max, obj.y_max), (255, 0, 0), 2)
                cv2.putText(img, obj.label + ' ' + "({})".format(str(obj.confidence)), (obj.x_min, obj.y_min - 10),
                            cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 0, 0), 3)
                if webhook_url:
                    objdetec_data.append(
                        {"label": obj.label, "confidence": obj.confidence, "x_min": obj.x_min, "x_max": obj.x_max, "y_min": obj.y_min,
                         "y_max": obj.y_max})
            if webhook_url and len(objdetec_data) > 0:
                obj_uuid = uuid_generator()
                webhook_data_obj_detection = {"type": "vision", "id": obj_uuid, "client_id": client_id, "version": "v1", "webhook_url": webhook_url,
                                              "webhook_api_key": webhook_api_key, "api": "object_detection", 'data': objdetec_data}
                if webhook_forward_images == 'True':
                    webhook_data_obj_detection['image'] = image_base64_converter(img)
                else:
                    webhook_data_obj_detection['image'] = " "
                webhook_data[obj_uuid] = webhook_data_obj_detection
            frame.image(img)

    if st.button('Stop', key='stop_btn1'):
        object_detection_active = False
        camera.release()
        cv2.destroyAllWindows()


def face_detection():
    face_detector = Face(config)

    global webhook_data
    global webhook_triggered
    webhook_thread()

    frame = st.image([])
    if camera_address.isdigit():
        camera = cv2.VideoCapture(int(camera_address))
    else:
        camera = cv2.VideoCapture('{}'.format(camera_address))

    face_detection_active = True
    if webhook_url and webhook_triggered is False:
        webhook_triggered = True

    while run:
        if face_detection_active is False:
            break
        else:
            _, img = camera.read()
            if img is None:
                st.error("Check your settings !")
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            response = face_detector.detectFace(img, output=None)
            facedetec_data = []
            for obj in response:
                cv2.rectangle(img, (obj.x_min, obj.y_min), (obj.x_max, obj.y_max), (255, 0, 0), 2)
                cv2.putText(img, str(obj.confidence), (obj.x_min, obj.y_min - 10), cv2.FONT_HERSHEY_COMPLEX,
                            0.8, (255, 0, 0), 3)
                if webhook_url:
                    facedetec_data.append({"confidence": obj.confidence, "x_min": obj.x_min, "x_max": obj.x_max, "y_min": obj.y_min,
                                           "y_max": obj.y_max})
            if webhook_url and len(facedetec_data) > 0:
                face_detect_uuid = uuid_generator()
                webhook_data_face_detection = {"type": "vision", "id": face_detect_uuid, "client_id": client_id, "version": "v1",
                                               "webhook_url": webhook_url, "webhook_api_key": webhook_api_key, "api": "face_detection",
                                               'data': facedetec_data}
                if webhook_forward_images == 'True':
                    webhook_data_face_detection['image'] = image_base64_converter(img)
                else:
                    webhook_data_face_detection['image'] = " "
                webhook_data[face_detect_uuid] = webhook_data_face_detection
            frame.image(img)

    if st.button('Stop', key='stop_btn2'):
        face_detection_active = False
        camera.release()
        cv2.destroyAllWindows()


def face_recognition():
    st.info("Perform Face Registration to Recognize a specific face")
    face_recognizer = Face(config)

    global webhook_data
    global webhook_triggered
    webhook_thread()

    frame = st.image([])
    if camera_address.isdigit():
        camera = cv2.VideoCapture(int(camera_address))

    else:
        camera = cv2.VideoCapture('{}'.format(camera_address))

    face_recognition_active = True
    if webhook_url and webhook_triggered is False:
        webhook_triggered = True
    while run:
        if face_recognition_active is False:
            break
        else:
            _, img = camera.read()
            if img is None:
                st.error("Check your settings !")
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            response = face_recognizer.recognizeFace(img, output=None)
            facerecog_data = []
            for obj in response:
                cv2.rectangle(img, (obj.x_min, obj.y_min), (obj.x_max, obj.y_max), (255, 0, 0), 2)
                cv2.putText(img, obj.userid + ' ' + "({})".format(str(obj.confidence)), (obj.x_min, obj.y_min - 10),
                            cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 0, 0), 3)
                if webhook_url:
                    facerecog_data.append(
                        {"user ID": obj.userid, "confidence": obj.confidence, "x_min": obj.x_min, "x_max": obj.x_max,
                         "y_min": obj.y_min, "y_max": obj.y_max})
            if webhook_url and len(facerecog_data) > 0:
                face_recog_uuid = uuid_generator()
                webhook_data_face_recog = {"type": "vision", "id": face_recog_uuid, "client_id": client_id, "version": "v1",
                                           "webhook_url": webhook_url,
                                           "webhook_api_key": webhook_api_key, "api": "face_recognition", 'data': facerecog_data}
                if webhook_forward_images == 'True':
                    webhook_data_face_recog['image'] = image_base64_converter(img)
                else:
                    webhook_data_face_recog['image'] = " "
                webhook_data[face_recog_uuid] = webhook_data_face_recog
            frame.image(img)

    if st.button('Stop', key='stop_btn3'):
        face_recognition_active = False
        camera.release()
        cv2.destroyAllWindows()


def face_registration():
    st.header(f"DeepStack-CameraUI Face Registration")
    st.text("Configure the Camera and DeepStack API in the sidebar")
    face_recognizer = Face(config)
    face_name = st.text_input("Enter the name to register", placeholder="Jane Amos", key='userid')
    face_files = st.file_uploader("Upload a face image that matches the Name above", accept_multiple_files=True,
                                  type=["jpg", "jpeg", 'png'])
    global webhook_data
    global webhook_triggered
    webhook_thread()
    if webhook_url and webhook_triggered is False:
        webhook_triggered = True

    if face_files and face_name is not None:
        for face_file in face_files:
            image = Image.open(face_file)
            img_arr = np.array(image)
            response = face_recognizer.registerFace([img_arr], face_name)
            if response:
                if webhook_url:
                    face_regis_uuid = uuid_generator()
                    webhook_data_face_regist = {"type": "vision", "id": face_regis_uuid, "client_id": client_id, "version": "v1",
                                                "webhook_url": webhook_url, "webhook_api_key": webhook_api_key, "api": "face_registration",
                                                'data': {"user ID": face_name}}
                    if webhook_forward_images == 'True':
                        webhook_data_face_regist['image'] = image_base64_converter(img_arr)
                    else:
                        webhook_data_face_regist['image'] = " "
                    webhook_data[face_regis_uuid] = webhook_data_face_regist
                st.success("Successfull Face Registration")
            else:
                st.error("Face Registration Failure")


def face_deregistration():
    st.header(f"DeepStack-CameraUI Face Deregistration")
    st.text("Configure the Camera and DeepStack API in the sidebar")

    global webhook_data
    global webhook_triggered
    webhook_thread()
    if webhook_url and webhook_triggered is False:
        webhook_triggered = True
    face_recognizer = Face(config)
    if face_recognizer.listFaces() is not None:
        name_option = st.selectbox("Names previously registered", face_recognizer.listFaces())
        if name_option:
            if st.button(f"Delete {name_option}"):
                face_recognizer.deleteFace(f"{name_option}")
                if webhook_url:
                    face_deregis_uuid = uuid_generator()

                    webhook_data_face_deregist = {"type": "vision", "id": face_deregis_uuid, "client_id": client_id, "version": "v1",
                                                  "webhook_url": webhook_url,
                                                  "webhook_api_key": webhook_api_key, "api": "face_deregistration", 'data': {"user ID": name_option}}
                    webhook_data[face_deregis_uuid] = webhook_data_face_deregist

                st.success(f"Successfully Deleted {name_option}")

    else:
        st.info("No Face Registered")


def custom_detection():
    custom_model_detector = Detection(config, custom_name)

    global webhook_data
    global webhook_triggered
    webhook_thread()

    frame = st.image([])
    if camera_address.isdigit():
        camera = cv2.VideoCapture(int(camera_address))
    else:
        camera = cv2.VideoCapture('{}'.format(camera_address))
    custom_detection_active = True
    if webhook_url and webhook_triggered is False:
        webhook_triggered = True

    while run:
        if custom_detection_active is False:
            break
        else:
            _, img = camera.read()
            if img is None:
                st.error("Check your settings !")
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            response = custom_model_detector.detectObject(img, output=None)
            custom_detec_data = []
            for obj in response:
                cv2.rectangle(img, (obj.x_min, obj.y_min), (obj.x_max, obj.y_max), (255, 0, 0), 2)
                cv2.putText(img, obj.label + ' ' + "({})".format(str(obj.confidence)), (obj.x_min, obj.y_min - 10),
                            cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 0, 0), 3)
                if webhook_url:
                    custom_detec_data.append({"name": obj.label, "confidence": obj.confidence, "x_min": obj.x_min, "x_max": obj.x_max,
                                              "y_min": obj.y_min, "y_max": obj.y_max})
            if webhook_url and len(custom_detec_data) > 0:
                custom_detect_uuid = uuid_generator()
                webhook_data_custom_detect = {"type": "vision", "id": custom_detect_uuid, "client_id": client_id, "version": "v1",
                                              "webhook_url": webhook_url,
                                              "webhook_api_key": webhook_api_key, "api": "custom_detection", 'data': custom_detec_data}
                if webhook_forward_images == 'True':
                    webhook_data_custom_detect['image'] = image_base64_converter(img)
                else:
                    webhook_data_custom_detect['image'] = " "
                webhook_data[custom_detect_uuid] = webhook_data_custom_detect
            frame.image(img)

    if st.button('Stop', key='stop_btn4'):
        custom_detection_active = False
        camera.release()
        cv2.destroyAllWindows()


if selected_box == 'Object Detection':
    welcome('Object Detection')
    object_detection()

if selected_box == 'Face Registration':
    face_registration()
if selected_box == 'Face Deregistration':
    face_deregistration()
if selected_box == 'Face Recognition':
    welcome('Face Recognition')
    face_recognition()
if selected_box == 'Face Detection':
    welcome('Face Detection')
    face_detection()
if selected_box == 'Custom Detection':
    welcome('Custom Detection')
    custom_detection()
