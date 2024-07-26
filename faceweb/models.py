from django.db import models
from django.utils.safestring import mark_safe
from PIL import Image
from io import BytesIO
import base64
# from faceweb.forms import VehicleForm

class Vehicle(models.Model):  # just to add the vehicle image and current date and time ... ignore this 
    image = models.FileField(upload_to='vehicles/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vehicle Image {self.id}"


class vehicle_login(models.Model):# this is the vehicle login part with date and time 
    image = models.BinaryField()  # Store binary data for the image
    timestamp = models.DateTimeField()
    format = models.CharField(max_length=10)
    text = models.TextField() 
    def __str__(self):
        return f"Snapshot taken at {self.timestamp}"  
    
    def image_tag(self):
        if self.image:
            img = Image.open(BytesIO(self.image))
            return mark_safe(f'<img src="data:image/{self.format};base64,{base64.b64encode(self.image).decode()}" height="150" />')
        else:
            return '(No image)'

    image_tag.short_description = 'Image'


class vehicle_logout(models.Model):# this is the vehicle login part with date and time 
    image = models.BinaryField()  # Store binary data for the image
    timestamp = models.DateTimeField()
    format = models.CharField(max_length=10)
    text = models.TextField() 
    def __str__(self):
        return f"Snapshot taken at {self.timestamp}"  
    
    def image_tag(self):
        if self.image:
            img = Image.open(BytesIO(self.image))
            return mark_safe(f'<img src="data:image/{self.format};base64,{base64.b64encode(self.image).decode()}" height="150" />')
        else:
            return '(No image)'

    image_tag.short_description = 'Image'    
    
# ---------------------------------------------------end of models.py faceweb -------------------------------------------------    

# class AllowedPerson(models.Model):
#     name = models.CharField(max_length=100)
