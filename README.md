# W.I.M.P: What's in my pantry -- Unihack 2024

Have you ever looked at your pantry and realised that some of your produce has expired? Ever wondered what could be done to avoid continually falling into the pitfall of food waste due to expired goods? Us too!

Our team wanted to tackle the problem of food wastage that hits close to home. We often find ourselves throwing out our groceries after we have forgotten to use them. To counter this issue, we developed a web application that detects items in your pantry and keeps track of their expiration dates.

W.I.M.P. (It actually works full loop with the hardward!): http://ec2-3-106-231-109.ap-southeast-2.compute.amazonaws.com:3000

## Set Up

### Front-end

We use typescript and react here. 

- Install npm package:

`npm install`

- Run npm:

`npm start`

### Back-end

We use Python, Flask, and Tensorflow. 

- Go to back-end directory then install the library:

`pip install -r requirements.txt`

- Download the model and place it at model folder

yolov4: [download here](https://github.com/onnx/models/blob/main/validated/vision/object_detection_segmentation/yolov4/model/yolov4.onnx)

You can test the model on a notebook 'konran_v2/back-end/notebook/yolov4_inference.ipynb'.

- Run Flask:

`flask --app server run --debug`

## Server

We host our W.I.M.P on AWS EC2 for you to access it from anywhere.

Thanks Unihack 2024 for the credits.

More information can be found: https://devpost.com/software/konran-v2 (Please vote for us :))

