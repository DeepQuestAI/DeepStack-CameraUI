# DeepStack-CameraUI
DeepStack-CameraUI is a real-time computer vision web-application. Powered by Deepstack and Streamlit, this application performs realtime AI processing such as **object detection**, **face recognition**, **face detection** and **custom detection** on video frames from WebCam, Wired Camera or IP camera through an interactive web interface.

# Installation

To run DeepStack-CameraUI, you need to install the following:
* **Python 3.8** 

  - [Windows](https://www.python.org/ftp/python/3.8.0/python-3.8.0-amd64.exe) 
  - [MacOS](https://www.python.org/ftp/python/3.8.0/python-3.8.0-macosx10.9.pkg)
  - [Ubuntu](https://www.python.org/ftp/python/3.8.0/Python-3.8.0.tar.xz)

* [Deepstack](https://docs.deepstack.cc/object-detection/index.html) 
* Clone the reporsitory 
* Install the dependencies by navigating into the project repository with `pip install -r requiremnets.txt`

# Run DeepStack-CameraUI
To run DeepStack-CameraUI, follow these steps :

* Step 1 : Run deepStack 
  * First run deepstack with this command:
```
docker run -e VISION-FACE=True -v localstorage:/datastore -p 80:5000 deepquestai/deepstack
```

Check [Deepstack Documantation](https://docs.deepstack.cc/) ,then navigate to the src folder and run the streamlit app using :

* * Navigate to the src folder and run the app using the command:
```
streamlit run app.py
```

Then go to your browser to load the app by visiting the link `https://localhost:8501`.
* step 2 :  Configure settings and start Detection
  * Select your API
  * Enter Deepstack URL (E.g: `http://localhost:80`)
  * Enter your camera address 
    * For a WebCam, it will be 0 Windows and -1 on Ubuntu
    * For IP Camera, type in the full address of video stream for the camera (E.g `http://192.43.51.1:9091/video`)
  - Press the **Start** button

Now you will see real-time detection and video feed from your camera displayed in the main app interface.

# DeepStack-CameraUI Interface
The interface of this web application is composed of two sections;  the **side-bar** which is the place where all configurations are set up and the **main interface** where the live detections are displayed.

## Deepstack-CameraUI Settings
The side-bar compresses different elements detailed below:

* **Choose the APIs**

This widgect allows you to select which API techniques delivered by this application to run among the following **object detection**, **face recognition**, **face registration**, **face deregistration**, **face detection** and **custom detection**.

* **DeepStack URL**

To connect to Deepstack server you must provide the right URL to Deepstack like `http://localhost:80` or any other `url:port` on which DeepStack is running, locally or on the cloud. 
For more information check [Deepstack documentation](https://docs.deepstack.cc/)

* **Camera Address**

The camera address can be a webCam or IP camera

**WebCam** : can be 0, 1 or the index of the camera as the camera address if you are using a WebCam or any other cable connected to your local machine (for Ubuntu, the camera index start from -1 )

**IP camera** :  IP camera URL can require credentials or not. A sample is which doesn't have/require other credentials is `http://180.234.23.1:9090/video` and a sample which requires credentials is `http://username:password@180.234.23.1:9090/video`.

Supply all the information related to his IP canera such as **User name**, **password**, **IP address**, **port** and **media**.

-
  - _User name_: A string to identify oneself i.e: nikeo, paul 
  - _Password_: can be anything.
  - _IP address_ *: the Internet Protocol of the camera should be in the format `192.168.1.199`
  - _Port_ * : represents the LAN port E.g: 8900, 8081
  - _Video stream path_: used to access the ip camera video can be `video` or `media` etc.

The terms ending with * are **compulsory**.

When you have a password and name, the IP camera address should have the following format
```
http://admin:password@IP Address:Port/Video stream path
```
Otherwise,
```
http://IP Address:Port/Video stream path
```
Kindly paste your IP camera URL into your browser to confirm it is loading a live feed before feeding into DeepStack-CameraUI.

* **Custom Model Name**

This widget accepts the name of your custom model, it is optional only required when **custom detection** is selected.

* **Start**

This button should be clicked on to begin the program execution.

* **Webhook URL**

The URL inputted will receive the detailed informations about the content of the detections being captured in real-time and the raw input video frames as base64.

* **Webhook Api Key**

The definition here

* **Webhook Forward Images**

Here you can decide to receive the images of the live detection through the webhook URL or not.

# DeepStack-CameraUI Techniques
DeepStack-CameraUI delivers real-time detection through these six different techniques.

### Object detection
The object detection API locates and classifies 80 different kinds of objects in a live streaming.

To use this API, you need to enable the detection API when starting DeepStack with docker through this command

```
docker run -e VISION-DETECTION=True -v localstorage:/datastore -p 80:5000 deepquestai/deepstack
```

### Face detection
The face detection API aims at detecting faces in the real-time live streaming.
To use this API, you need to enable the detection API when starting DeepStack with docker through this command

```
docker run -e VISION-FACE=True -v localstorage:/datastore -p 80:5000 deepquestai/deepstack
```

### Face Registration
The face Registration API goal's is to allow you to enroll a person's name or id and image on Deepstack server for future use like face recognition. The face recognition API is dependent of this API.

To use this API, you need to enable the face API when starting DeepStack with docker through this command

```
docker run -e VISION-FACE=True -v localstorage:/datastore -p 80:5000 deepquestai/deepstack
```

### Face Deregistration
The face deregistration API goal's is to allow you to erase a person's name and image from Deepstack server. 

To use this API, you need to enable the face API when starting DeepStack with docker through this command

```
docker run -e VISION-FACE=True -v localstorage:/datastore -p 80:5000 deepquestai/deepstack
```

### Face Recognition
The face recognition API goal's is to identify faces by their name or id, as previously registered to DeepStack server, when it fails to recognize a face it defaults it to **Unknown** face in the live stream.
To use this API, you need to enable the face API when starting DeepStack with docker through this command


```
docker run -e VISION-FACE=True -v localstorage:/datastore -p 80:5000 deepquestai/deepstack
```

### Custom detection
The custom detection API allows you to perform detection on personal/ specific object. To learn more about training custom model check this [documentation](https://docs.deepstack.cc/custom-models/index.html).

To activate this API, you need to enable the detection API when starting DeepStack with docker through this command

```
docker run -v /path-to/custom-models-folder:/modelstore/detection -p 80:5000 deepquestai/deepstack
```

To test the custom detection API, you can make use of  a custom model built by DeepStack called **[Logo Detection](https://github.com/OlafenwaMoses/DeepStack_OpenLogo)** to detection human actions such as eating, reading, 
calling etc.


# Run DeepStack-CameraUI with Webhook
A webhook is a lightweight API that power one-way data transmission and trigger by event. In our case, this API is trigger when the webhook URL is defined,
this webhook goal's is to transfer in real-time all the detections captured through any above mentioned APIs to a recipient.

This API is is dependent to few components which are:
- **Webhook URL**: The receiver address, it can be a URL or an email address
- **Webhook API Key**: the webhook api personal key , it is optional
- **Webhook Forward Images**:  a function to send detection images to the receipient. it is optioanal.


To run DeepStack-CameraUI with webhook,
1. kindly install [Flask](https://flask.palletsprojects.com/en/2.0.x/installation/) 
2. Move the **script** folder, Install the periquisites using `pip install -r requirements.txt`
3. Run the flasK app with `flask run`.
4. Insert `http://127.0.0.1:5000/webhook ` as  webhook URL on Deepstack-cameraUI and click on **Start**.

The live detections would displayed on the flask app terminal.



