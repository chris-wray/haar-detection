from twilio.rest import Client
import cv2
#Account details
#8325249858
#facealert_pass

client = Client("ACdd9024946a5da743c5f59ceb2604051a", "688dcca5220db43800812a99418f6147")

my_number = "8325249858"
twilio_number = "2818843068"
message = 'body'
image = ('https://www.cutislaserclinics.com/wp-content/uploads/2018/02/Achieve-a-Youthful-V-Shape-Face.jpg')
client.api.account.messages.create(to = my_number, from_= twilio_number, media_url= image)