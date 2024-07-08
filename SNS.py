from RPLCD.i2c import CharLCD
import cv2
import torch
from picamera2 import Picamera2
from PIL import Image
import numpy as np
import smtplib
from email.mime.text import 	
  
# Initialize LCD
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')  # Use custom dataset model

# Initialize Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.start()
  
# Define the speed limit list
speed = [30, 40, 50, 60, 70, 80, 90, 100]
 
def lcd_write(w):
    lcd.clear()
    lcd.write_string(w)


def send_email(current_speed, object_speed):
    message = f"You were speeding! Speed limit: {speed_limits}km/h, your speed: {current_speed}km/h"
    smtp = smtplib.SMTP('smtp.gmail.com')
    smtp.starttls
    smtp.login('leehh7255@naver.com','')
    msg = MIMEText(message)
    msg['Subject'] = Speed warning
    msg['To'] = leehh7255@naver.com
    smtp.sendmail('leehh7255@gmail.com','leehh7255@naver.com',msg.as_string())
    smtp.quit()


while True:
    try:
        # Get user input for current speed
        user_input = input("Enter the current speed (or 'q' to quit): ")
        if user_input.lower() == 'q':
            break
        current_speed = int(user_input)
        lcd_write(str(current_speed) + "km/h")
 
        frame = picam2.capture_array()
        results = model(frame)
        annotated_frame = np.squeeze(results.render())
 
        # Check if any detected object's speed is higher than current speed
        
        is_camera = False
        for *box, conf, cls in results.xyxy[0]:
            x1, y1, x2, y2 = [int(i) for i in box]
            label = model.names[int(cls)]
            if label == 'camera':
                is_camera = True
            speed_limits = speed[int(cls)]  
         
        if speed_limits < current_speed:
                lcd_write("Speeding! limits: " + str(speed_limits))
                if is_camera:
                     lcd_write("Speeding! limits: " + str(speed_limits) + "with Camera!")
		    send_email(current_speed, speed_limits)
        else:
            lcd_write(str(current_speed) + "km/h")

  
        cv2.imshow('Detected Objects', annotated_frame)
        cv2.waitKey(1)
 
    except ValueError:
        print("Invalid input. Please enter a number or 'q' to quit.")
    except KeyboardInterrupt:
        print("\nProgram terminated.")
         break

picam2.stop()
cv2.destroyAllWindows()
