<p align="center">
  <img width="200" height="200" src="assets/logo.png">
</p>



<p align="center">
  <img width="120" height="22" src="https://img.shields.io/badge/platform-linux--64-brightgreen">
  <img width="100" height="22" src="https://img.shields.io/badge/python-%3E%3D3.5-brightgreen">
  <img width="140" height="22" src="https://img.shields.io/badge/tensorflow-1.12.x%20--%201.15.0-brightgreen">
</p>


# Qoala Ai Library
This project contains the collection of deep learning model wrappers from Qoala.id data science team.

## News
| Horey                                                       |        Version     |   
| ----------------------------------------------------------- | ------------------ | 
| multi-label object detector (stable)                        |      >=v0.4.19     |
| Deeplab Semantic segmentation was released (stable)         |      >=v0.1.18     |
| Object landmark(keypoints) was released (stable)            |      >=v0.4.18     |

## Features
- Object classificatiom (inception, resnet, densenet)
- Object detection (yolo-v3)
- Semantic segmentation (deepplab)
- Ensemble (for object classification)
- Landmark (keypoints)
- Some tensor utils


<p align="center">
  <img width="600" height="130" src="assets/classification.png">
  <h5 align="center"> Image Classification </h5>
</p>
<p align="center">
  <img width="150" height="150" src="assets/landmark.png">
  <img width="150" height="150" src="assets/detection.jpg">
  <img width="150" height="150" src="assets/segmentation1.jpg">
  <img width="150" height="150" src="assets/segmentation2.jpg">
  <h5 align="center"> Landmark | Object Detection | Segmentation </h5>
</p>


## Todo
- [x] Densenet image classification
- [x] Resnet-121 image classification
- [x] Inception image classification
- [x] Ensemble for image classification
- [x] Yolo-v3 object detection
- [x] Yolo-v3 Multi classes object detction
- [x] DeepLab semantic segmentation
- [x] TF Lite for image classification
- [x] TF lite for object detection (YOLO)
- [ ] TF lite for semantic segmentation
- [x] Apply object detector threshoding in ML-engine
- [ ] SSD object detection
- [ ] instance segmentation
- [ ] tensorRt
- [ ] Efficient Net
- [x] Landmark/keypoints detection
- [ ] object similarity

## Requirements
- tensorflow-gpu==1.13.1 - 1.15.2 (`pip3 install tensorflow-gpu`)
- comdutils (`pip3 install comdutils`)
- numpy
- opencv-python=3.4.2

## Package Installation
- `pip3 install -r requirements.txt`
- `pip3 install qoalai`

## Available Docker
- download the docker image
- `docker pull ...`






