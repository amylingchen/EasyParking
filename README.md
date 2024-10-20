![<video controls src="static/video/easyparking.mp4" title="Title"></video>](static/video/ox1jn-q78zo.gif)
# EasyParking
This project monitors the number and location of empty parking spaces by reading the image data from the parking lot cameras to determine if there is a vehicle parked in each space, thus helping students find the right space faster.

## Inspiration
When I parked at school, I often encountered the car park is full of cars, this time we need to browse through multiple car parks to find an empty parking space, so we made this project, you can intuitively find the right parking space in the mobile browser!

## What it does
This project monitors the number and location of empty parking spaces by reading the image data from the parking lot cameras to determine if there is a vehicle parked in each space, thus helping students find the right space faster.

## How we built it
Read the parking lot image data returned by the camera, use yolo8 to predict the parking lot image, and obtain whether there is a vehicle in each parking space
Predict the occupancy of each parking space and save it to the database.
The front-end web reads the return from the back-end and displays the occupancy ratio of each parking lot and the occupancy of each parking space.
