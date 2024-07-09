# SpeedingNotificationSystem
Final Project for IoT System (24-1)


## 1. Introduction

![Aspose Words a21fcd2c-e9a1-47a5-9439-54b0a5e4bc33 003](https://github.com/MillionKiwi/SpeedingNotificationSystem/assets/127092247/6021a217-c1e7-4dfd-8435-d93b91310653)

**Picture 1: Crackdown status by type of traffic violation (Source: Korea National Police Agency)**



 Speeding is a serious cause of traffic accidents, but the number of people speeding is increasing year by year. However, many people are not aware of speeding, but rather trust their driving abilities and memory, and even have their navigation systems turned off. I wanted to create a system that would make it easier for people to know that they are speeding even without it.

## 2. HW Designs

![Aspose Words a21fcd2c-e9a1-47a5-9439-54b0a5e4bc33 004](https://github.com/MillionKiwi/SpeedingNotificationSystem/assets/127092247/76f83a87-a735-4208-8c12-6a67c2a95acd)

**Picture 2: Circuit of Project**

![Aspose Words a21fcd2c-e9a1-47a5-9439-54b0a5e4bc33 005](https://github.com/MillionKiwi/SpeedingNotificationSystem/assets/127092247/016fd3fe-1f10-4eae-ba52-94561d088f00)

**Picture 3: Picture of HW Circuit**

Hardware design is quite simple. As I aimed for a system for people who don't use a navigation system, I didn't want to make a system that bothers them audibly, so I mainly use an LCD module. The LCD module is enclosed in the Arduino kit and communicates using I2C BUS. There was no difficulty using it because I had dealt with it in the practice class. 


The next HW device is a speed camera and a camera module that detects speed signs. It has a 5MP OV5647 image sensor. It also has an Angle of View of 54 x 41, a fixed focus of 1M to infinity, and a max frame rate of 30 fps. The camera module has a ribbon cable of 15 cm through which it communicates with the MIPI Camera Serial Interface (CSI).

![Aspose Words a21fcd2c-e9a1-47a5-9439-54b0a5e4bc33 006](https://github.com/MillionKiwi/SpeedingNotificationSystem/assets/127092247/84141364-fa70-41d3-a19b-a92838ea8476)

**Picture 4: Purchase detail about Camera module**

I purchased the camera module through Aliexpress and used the one in the Arduino kit for the LCD module. Therefore, my HW Design costs a total of 7,040 won.


## 3. SW Design

![Aspose Words a21fcd2c-e9a1-47a5-9439-54b0a5e4bc33 008](https://github.com/MillionKiwi/SpeedingNotificationSystem/assets/127092247/7d5feb21-3b83-4e5d-8700-c7e76d0f00c7)

**Picture 5: Simple SW design of Project**

The first step was to train a YOLOv5 model using custom data. I gathered around 470 images using the Kakao map and conducted AI training. After the training, I obtained the 'best.pt' file, which contains the model's weight information. This allowed me to perform object detection on a Raspberry Pi using the 'best.pt' file.

For the image capture, I used a CSI camera module, which required a different approach compared to a standard USB webcam. The Raspberry Pi Bookworm operating system primarily utilizes the libcamera module. However, since OpenCV does not natively support libcamera, I implemented the image capture by importing it through the Picamera2 library.

To explain the code further:

When the user inputs the current speed through the keyboard, the Picamera2 captures an image, and the YOLOv5 model performs object detection. Based on the object labels, the code checks if there is a 'camera' object detected and determines the applicable speed limit. It then compares the user's current speed with the detected speed limit. If the user is speeding and a 'camera' object is undetected, the code displays "Speeding! + Speed limit" on the LCD. However, if the user is speeding and a 'camera' object is detected, the code not only displays the message on the LCD but also sends an email notification about the speeding violation.


## 4. Conclusion

![Aspose Words a21fcd2c-e9a1-47a5-9439-54b0a5e4bc33 009](https://github.com/MillionKiwi/SpeedingNotificationSystem/assets/127092247/b832601a-1969-4074-b3bf-3f097669cfd6)

**Picture 6: Captured picture of demo video**

![Aspose Words a21fcd2c-e9a1-47a5-9439-54b0a5e4bc33 010](https://github.com/MillionKiwi/SpeedingNotificationSystem/assets/127092247/d9cd1b21-0085-4340-8381-6e10c1ae45b2)

**Picture 7: Captured picture of demo video**

The speed camera detection in the demo video is quite accurate, but the speed sign detection accuracy is lacking. This is because the dataset I collected mainly includes images with one camera and one or two speed signs. In other words, all the photos contain the camera object. But there is a limited variety of speed sign data, primarily 30-100 km/h signs, leading to an imbalance in the training labels. To enhance the model's accuracy, especially for speed sign detection, I believe that adding more data, particularly images with a wider range of speed signs, will be beneficial.

Furthermore, the email notification function was not accurately implemented as originally designed. I plan to revisit and improve this feature. Instead of using the Google app password for authentication, I intend to explore alternative methods such as secondary authentication or integrating with a different mail server to ensure reliable email functionality.

Additionally, I plan to integrate a device such as an LED into the system to provide users with a more noticeable visual warning when speeding. This will complement the LCD and help attract the user's attention more effectively when the speed limit is exceeded

