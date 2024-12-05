# 241_ML_Project_PPE_Segment

This project is for segmentation of PPE Detection, in this project, I use Yolov11 with segmentation options, we already have 3 scripts in this project. This model is based on YOLOv11 and is trained on a dataset of 400 images. The dataset is randomly split into a training set (84%), a validation set (12%), and a test set (4%). The training process is conducted on Google Colab using a T4 GPU and runs for 150 epochs.

To run this project, we already use anaconda prompt to create virtual environment for avoiding conflict in installing packages in python. 

:pushpin: **For install and running anaconda** : Visit page https://www.anaconda.com/

After installing, you can create virtual environment by this command : 
```bash
conda create -n <env-name> python=3.11.2
```

:pushpin: **Activate environment:** Activate environment in python
```bash
conda create -n <env-name> python=3.11.2
```
:pushpin:**OpenCV Install**
```bash
pip install opencv-python
```

:pushpin: **Install Ultrlytics** : Should be used version 8.0.196 for yolov8 and 8.0.0 for older version.
```bash
pip install ultralytics==8.0.196
```

# Overview workflow

This web application is designed to perform intelligent and efficient personal protective equipment (PPE) recognition. Users can choose between two operating modes:

Real-time recognition: The device's webcam will be activated to record images and videos. Immediately, the system will analyze the frames and display bounding boxes around the detected PPE objects, providing detailed information about the type of PPE (e.g., helmets, reflective vests, safety shoes).
Uploaded video processing: Users can upload videos for analysis. The system will process each frame of the video and generate an output video where the PPE objects are marked with bounding boxes and corresponding labels. This allows users to easily check and evaluate the use of PPE during work.

![Add_results](https://github.com/0607bkhanhhoang/241_ML_Project_PPE_Segment/blob/main/images/Flow.png)

:pushpin: To run web app appilcation, type
```bash
python flaskapp.py
```

## YOLO Weights

This folder contains 2 weight file best.pt and best_older_version.pt. 

- **best.pt** : The weight file for latest version of my model that is constructly runned with no loss classes and box.
- **best_older_version.pt**: This weigh file is for the highest accuracy model.

# Web Develop

## images

This folder contains images that are design to be frontend of GUI. The web is develop on the local IP of your computer and to interface for frontend, I use css for re-design my GUI and html for UI. And for text and fonts, .xml file will handle this case.

## static 

This folder will be the server for saving and loading data that 2 WEB saves. 

:pushpin: **Save from video**: Saving data from video and up to /static/files.
:pushpin: **Check from webcam**: Checking from webcam.

# Model Visualization 

## Confusion matrix 

A confusion matrix is a performance measurement tool for machine learning classification tasks, particularly useful in evaluating the accuracy of a model. It compares the predicted labels from a classification model with the true labels from the data. It is typically represented as a square matrix.

:pushpin:**Formula**
![Confusion_matrix](https://github.com/0607bkhanhhoang/241_ML_Project_PPE_Segment/blob/main/images/Formula.png)

:pushpin:**Results**
![Confusion_matrix_2](https://github.com/0607bkhanhhoang/241_ML_Project_PPE_Segment/blob/main/images/confusion_matrix.jpg)

## Precision Output

![Precision](https://github.com/0607bkhanhhoang/241_ML_Project_PPE_Segment/blob/main/images/precision.jpg)

## Test results

![Add_results](https://github.com/0607bkhanhhoang/241_ML_Project_PPE_Segment/blob/main/images/clothes_1.jpg)

![Add_results](https://github.com/0607bkhanhhoang/241_ML_Project_PPE_Segment/blob/main/images/clothes_2.jpg)






