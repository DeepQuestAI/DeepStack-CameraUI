# DeepStack-CameraUI
DeepStack-CameraUI is a real-time computer vision web-application. Powered by Deepstack and Streamlit, this application performs realtime AI processing such as **object detection**, **face recognition**, **face detection** and **custom detection** on video frames from WebCam, Wired Camera or IP camera through an interactive web interface.

## DeepStack-CameraUI Interface
The interface of this web application is composed of two sections the **side-bar** which is the place where all configurations are set up and the **main interface** where the live detections are displayed.

### Deepstack-CameraUI Settings
The side-bar compresses different elements detailed below:

* **Choose the APIs**

This widject allows you to select which API techniques delivered by this application to run among the following **object detection**, **face recognition**, **face registration**, **face deregistration**, **face detection** and **custom detection**.

* **DeepStack URL**

To connect to Deepstack server the user must provide the right URL to Deepstack like `http://localhost:80` or `http://localhost:5670` depending on the URL port. 
Fro more information check the documentation https://docs.deepstack.cc/

* **Camera Address**

This is the crucial part of this application, the user must supply all the information related to his IP canera such **User name**, **password**, **IP address**, **port** and **media**.

- User name: A string to identify oneself i.e: nikeo, paul 
- Password can be anything.
- IP address *: the Internet Protocol of the camera should be in the format `192.168.1.199`
- Port* : represents the LAN port i.e: 8900, 8081
- Video stream path: used to access the ip camera video can be `video` or `media` etc.

The terms ending with * are **compulsory**.

When the user has a password and name, the camera address should have the following format
```
admin:password@IP Address:Port/Video stream path
```
Otherwise,
```
IP Address:Port/Video stream path
```


* **Custom Model Name**

This widget accepts the name of the custom model, its is optional only required when custom detection is selected.

* **Webhook URL**

The URL inputted will receive the detailed informations about the content of the detections being captured in real-time and the api running.

* **Webhook Api Key**

The definition here

* **Webhook Forward Images**

Here the user can decide to receive the images of the live detection through the webhook URL or not.


## Installations 

In order to install **Python 3.8** depending on any operating system 

- [Windows](https://www.python.org/ftp/python/3.8.0/python-3.8.0-amd64.exe) 
- [MacOS](https://www.python.org/ftp/python/3.8.0/python-3.8.0-macosx10.9.pkg)
- [Ubuntu](https://www.python.org/ftp/python/3.8.0/Python-3.8.0.tar.xz)

To install DeepStack kindly check this [page](https://docs.deepstack.cc/object-detection/index.html) and [DeepStack Python SDK](https://docs.deepstack.cc/python-sdk/index.html)  which allows you to use DeepStack APIs.

In order to install all the application's dependencies, run this command: 
```
pip install -r requiremnets.txt
```

## Run Web Application
To run this streamlit application **locally** , execute the following command in the app folder

First run Deepstack with all the apis if you prefer
```
deepstack --VISION-DETECTION True --VISION-FACE True --MODELSTORE-DETECTION "path to the custom action model" --PORT 80
```
Then navigate to the src folder and run the streamlit app using :
```
streamlit run app.py
```

## Deepstack-CameraUI Techniques
Deepstack-CameraUI delivers real-time detection through these six different techniques.

### Object detection
The object detection API locates and classifies 80 different kinds of objects in a live streaming.

To use this API, you need to enable the detection API when starting DeepStack through this command

- **Docker**
```
docker run -e VISION-DETECTION=True -v localstorage:/datastore -p 80:5000 deepquestai/deepstack
```

### Face detection
The facedetection API aims at identifying a face in the real-time live streaming.
To use this API, you need to enable the detection API when starting DeepStack through this command

- **Docker**
```
docker run -e VISION-FACE=True -v localstorage:/datastore -p 80:5000 deepquestai/deepstack
```

### Face Registration
The face Registration API goal's is to allow the user to enroll a person's name and image on Deepstack server for future use like face recognition. The face recognition API is dependent of this API.

To use this API, you need to enable the face API when starting DeepStack through this command

- **Docker**
```
docker run -e VISION-FACE=True -v localstorage:/datastore -p 80:5000 deepquestai/deepstack
```

### Face Deregistration
The face deregistration API goal's is to allow the user to erase a person's name and image from Deepstack server. 

To use this API, you need to enable the face API when starting DeepStack through this command
- **Docker**
```
docker run -e VISION-FACE=True -v localstorage:/datastore -p 80:5000 deepquestai/deepstack
```

### Face Recognition
The face recognition API goal's is to identify a face that has been previously register on Deepstack server, when it fails to recognize a face it portaits it as an **Unknown** face in the live stream.
To use this API, you need to enable the face API when starting DeepStack through this command

- **Docker**
```
docker run -e VISION-FACE=True -v localstorage:/datastore -p 80:5000 deepquestai/deepstack
```

### Custom detection
The custom detection API allows the user to perform detection on personal/ specific object. To acheive this, your must prepare your own dataset, trained model , deplayed model and store these elements into a folder.

To activate this API, you need to enable the detection API when starting DeepStack through this command

- **Docker**
```
docker run -v /path-to/custom-models-folder:/modelstore/detection -p 80:5000 deepquestai/deepstack
```

To test the custom detection API, I used a custom model built by DeepStack called **[ActionNet](https://github.com/OlafenwaMoses/DeepStack_ActionNET)** to detection human actions such as eating, reading, 
calling etc.


## Run Deeptsack-CameraUI with Webhook
A webhook is a lightweight API that power one-way data transmission and trigger by event. In our case, this API is trigger when the webhook URL is defined,
this webhook goal's is to transfer in real-time all the detections captured through any above mentioned APIs to a recipient.

This API is is dependent to few components which are:
- **Webhook URL**: The receiver address, it can be a URL or an email address
- **Webhook API Key**: the webhook api personal key , it is optional
- **Webhook Forward Images**:  a function to send detection images to the receipient. it is optioanal.

To run the webhook, Kindly install [Flask](https://flask.palletsprojects.com/en/2.0.x/installation/) and run the following commands:

- **DeepStack-CameraUI**

Move to the src folder and run the streamlit script: **app.py** 
```
 streamlit run app.py
```

- **Flask**

Move the script folder, inseert `http://127.0.0.1:5000/webhook ` in the app webhook URL widget and run this command:

```
Flask run
```
The detection would be vissible from the flask app terminal.



