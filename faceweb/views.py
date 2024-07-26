import datetime
import io
from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User , auth
from django.contrib.auth import authenticate
import os
import cv2
import logging
import pymongo
from django.http import StreamingHttpResponse, HttpResponse, JsonResponse
from django.shortcuts import render
from pyzbar.pyzbar import decode
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import easyocr
from datetime import datetime
from .models import vehicle_logout
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
# from .utils import capture_image_and_compare

# from webapp.utils import get_db_handle

# Create your views here.is just a webpage to print hello
def hello(request):
    return render(request, 'main.html')

# user register
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        Password1 = request.POST['password1']
        Password2 = request.POST['password2']
        user = User.objects.create_user(username=username, email=email, password=Password1, first_name=first_name, last_name=last_name)
        user.save();
        print("user created ")
        return render(request, 'home.html', {'user_created': False})
    else:

        return render(request , 'register.html')
# login part 

def login(request):
    if request.method == 'POST':
      username = request.POST['username']
      password = request.POST['password']

      user = auth.authenticate(username=username,password= password)

      if user is not None:
        auth.login(request,user)
        return render(request , 'home.html')
      else:
        messages.info(request, 'invalid credentials')
        return render(request,'login.html')
    else:
      return render(request , 'login.html')

  
def loginadmin(request):
    if request.method == 'POST':
        username = "admin"
        password = 123
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return render(request , 'admin1.html')
        else:
            messages.info(request, 'invalid credentials')
            return render(request,'loginadmin.html') 
    else:
       return render(request , 'loginadmin.html')
    
@never_cache
def logout(request):
    auth.logout(request)
    return render(request , 'home.html')
@never_cache
def logoutadmin(request):
    auth.logout(request)
    return render(request , 'admin1.html')

def home(response):
     return render(response,"faceweb/home.html")

def admin1(response):
     return render(response,"admin1.html")

# def home_view(request): 
#     # Redirect to the home page '/'
#     return redirect('admin1.html')


# details part to generate the qr code ----->
def details(request):
   return render(request,"details.html")

def dailypass(request):
   return render(request,"dailypass.html")


from django.shortcuts import render, redirect
from faceweb.forms import VehicleForm
import pymongo

url = 'mongodb://localhost:27017/' #this is mongodb url , its basically connection
client = pymongo.MongoClient(url) # same as up , object (url)

# Select the database and collection       mongodb://localhost:27017/
db = client['usere']  # Replace with your database name
collection = db['vehicle'] #declaring the connection 

def upload_vehicle(request):  # just to upload the vehicle to database 
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        # db_handle, collection, client = get_db_handle()
        if form.is_valid():
            form.save()
            return redirect('upload_success')  # Redirect to success page or image list
    else:
        form = VehicleForm()
    return render(request, 'upload_vehicle.html', {'form': form})

def upload_success(request):# success page of vehicle upload 
    return render(request, 'upload_success.html')





# Initialize MongoDB client and database
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['usere']  # Replace with your MongoDB database name
collection = db['vehicle']  # Replace with your MongoDB collection name
acollection = db['vehicle-login'] # different collection 


# Path to your cascade classifier XML file for license plate detection
haar_cascade = os.path.join(os.path.dirname(__file__), 'models', 'numberplate.xml')

# Initialize cascade classifier for license plate detection
plate_cascade = cv2.CascadeClassifier(haar_cascade)
if plate_cascade.empty():
    logging.error("Failed to load cascade classifier.")

# Initialize EasyOCR reader for text extraction
reader = easyocr.Reader(['en'], gpu=True)  # Adjust languages and GPU usage as needed

def verify_text_in_mongodb(text):# verification of text from mongodb
    try:
        # Query MongoDB to find if the text exists in the collection
        query = {'text': text}  # Replace 'text_field_name' with the actual field name in your MongoDB documents
        result = collection.find_one(query)

        if result:
            return True  # Text found in MongoDB
        else:
            return False  # Text not found in MongoDB

    except Exception as e:
        logging.error(f"Error verifying text in MongoDB: {str(e)}")
        return False  # Return False on error or if text is not found





# Initialize MongoDB client and database
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['usere']  # Replace with your MongoDB database name
acollection = db['vehicle_login']  # Replace with your MongoDB collection name




cap = cv2.VideoCapture(0)  # Initialize capture (0 for default camera)

reader = easyocr.Reader(['en'])  # Initialize EasyOCR reader for English text
from .models import vehicle_login



def capture_snapshot(request):# taking a picture of vehicle numberplate 
    if request.method == 'POST':
        success, frame = cap.read()
        
        if success:
            # Encode image to JPEG format
            _, img_bytes = cv2.imencode('.jpg', frame)
            img_b64 = io.BytesIO(img_bytes).read()

            # Extract text using EasyOCR
            results = reader.readtext(frame)

            # Extracted text
            extracted_text = '\n'.join([result[1] for result in results])

            # Extract image properties
            # height, width, _ = frame.shape  # Height and width of the image
            img_format = 'jpeg'  # Format of the image (in this case, JPEG)

            # Add current date and time to the document
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                vehicle_log = vehicle_login.objects.create(
                        image=img_b64,  # Assuming you have a field suitable for storing image data
                        timestamp=current_time,
                        format=img_format,
                        text=extracted_text.upper()
                    )
                message = 'Snapshot captured and saved successfully with text!'
            except Exception as e:
                message = f'Failed to save snapshot: {str(e)}'
        else:
            message = 'Failed to capture snapshot.'

    return render(request, 'indexlogout.html', {'message': message})




def capture_snapshot_logout(request):# taking a picture of vehicle numberplate 
    if request.method == 'POST':
        success, frame = cap.read()
        
        if success:
            # Encode image to JPEG format
            _, img_bytes = cv2.imencode('.jpg', frame)
            img_b64 = io.BytesIO(img_bytes).read()

            # Extract text using EasyOCR
            results = reader.readtext(frame)

            # Extracted text
            extracted_text = '\n'.join([result[1] for result in results])

            # Extract image properties
            # height, width, _ = frame.shape  # Height and width of the image
            img_format = 'jpeg'  # Format of the image (in this case, JPEG)

            # Add current date and time to the document
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                vehicle_log = vehicle_logout.objects.create(
                        image=img_b64,  # Assuming you have a field suitable for storing image data
                        timestamp=current_time,
                        format=img_format,
                        text=extracted_text.upper()
                    )
                message = 'Snapshot captured and saved successfully with text!'
            except Exception as e:
                message = f'Failed to save snapshot: {str(e)}'
        else:
            message = 'Failed to capture snapshot.'

    return render(request, 'indexlogout.html', {'message': message})


def gen(cap):# its a opencv code to sun in a webpage and verification of text also  
    min_area = 500
    # count = 0  # Initialize count for saving images

    while True:
        success, frame = cap.read()

        if not success:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

        for (x, y, w, h) in plates:
            area = w * h
            if area > min_area:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)

                img_cro = frame[y:y + h, x:x + w]

                try:
                    # Perform OCR on the detected license plate image
                    result = reader.readtext(img_cro)
                    for (bbox, text, prob) in result:
                        text = text.upper()
                        cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), thickness=2)

                        # Verify the extracted text against MongoDB
                        if verify_text_in_mongodb(text):
                            cv2.putText(frame, "Access Granted!", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), thickness=2)
                        else:
                            cv2.putText(frame, "Access Denied!", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), thickness=2)
                      
                except Exception as e:
                    logging.error(f"Error processing image: {str(e)}")

        # Convert frame to bytes for streaming response
        _, frame_bytes = cv2.imencode('.jpg', frame)
        frame_bytes = frame_bytes.tobytes()

        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@csrf_exempt
def video_feed(request):# its a video feed , to run in webpage , which is mentioned in urls.py
    return StreamingHttpResponse(gen(cv2.VideoCapture(0)), content_type='multipart/x-mixed-replace; boundary=frame')



def gen1(cap):# its a opencv code to sun in a webpage and verification of text also  
    min_area = 500
    # count = 0  # Initialize count for saving images

    while True:
        success, frame = cap.read()

        if not success:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

        for (x, y, w, h) in plates:
            area = w * h
            if area > min_area:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)

                img_cro = frame[y:y + h, x:x + w]

                try:
                    # Perform OCR on the detected license plate image
                    result = reader.readtext(img_cro)
                    for (bbox, text, prob) in result:
                        text = text.upper()
                        cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), thickness=2)

                except Exception as e:
                    logging.error(f"Error processing image: {str(e)}")

        # Convert frame to bytes for streaming response
        _, frame_bytes = cv2.imencode('.jpg', frame)
        frame_bytes = frame_bytes.tobytes()

        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@csrf_exempt # logout 
def video_feed1(request):# its a video feed , to run in webpage , which is mentioned in urls.py
    return StreamingHttpResponse(gen1(cv2.VideoCapture(0)), content_type='multipart/x-mixed-replace; boundary=frame')




@csrf_exempt
def scan_qr(request):# ignore for now 
    if request.method == 'GET':
        return render(request, 'scan_qr.html')
def index(request): # its a index page , to run all the opencv code , try on ur localhost , give /index and run 
    try:
        return render(request, 'index.html')
    except Exception as e:
        logging.error(f"Error rendering index.html: {str(e)}")
        
def indexlogout(request): # its a index page , to run all the opencv code , try on ur localhost , give /index and run 
    try:
        return render(request, 'indexlogout.html')
    except Exception as e:
        logging.error(f"Error rendering indexlogout.html: {str(e)}")



# -------------------------------------------------------end of views.py faceweb ---------------------------------------------------------------------







# @csrf_exempt
# def scan_qr_code_view(request):
#     if request.method == 'POST' and request.body:
#         try:
#             # Convert the image data from the request body
#             nparr = np.frombuffer(request.body, np.uint8)
            
#             # Decode the image using OpenCV
#             frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
#             if frame is None:
#                 logging.error("Failed to decode image.")
#                 return JsonResponse({'error': 'Failed to decode image'}, status=500)

#             # Verify frame shape and type for debugging purposes
#             logging.debug(f"Frame shape: {frame.shape}, Frame type: {type(frame)}")

#             # Scan QR code in the frame
#             qr_data = scan_qr_code(frame)
            
#             return JsonResponse({'qr_data': qr_data}, status=200)
#         except Exception as e:
#             logging.error(f"Error decoding QR code: {str(e)}")
#             return JsonResponse({'error': 'Error decoding QR code'}, status=500)

#     return JsonResponse({'error': 'POST request with image data required'}, status=400)



# def save_image_to_mongodb(image):
#     try:
#         # Perform OCR on the image
#         result = reader.readtext(image)
#         extracted_text = ''
#         for (bbox, text, prob) in result:
#             extracted_text += text.upper() + ' '

#         # Prepare data for MongoDB insertion
#         current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         entry = {
#             'plate_text': extracted_text.strip(),  # Strip to remove trailing space
#             'timestamp': current_datetime,
#             'image': cv2.imencode('.jpg', image)[1].tobytes()  # Save image binary directly to MongoDB
#         }

#         # Insert entry into MongoDB collection
#         acollection.insert_one(entry)

#         logging.info('Image and text saved to MongoDB.')

#     except Exception as e:
#         logging.error(f"Error saving image to MongoDB: {str(e)}")
# ==============================================================

# @csrf_exempt
# def save_image_to_db(request):
#     if request.method == 'POST':
#         try:
#             img_data = request.FILES['image']  # Assuming image is sent as a file in POST request
#             img_np = np.frombuffer(img_data.read(), np.uint8)
#             img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

#             # Perform OCR on the detected license plate image
#             result = reader.readtext(img)
#             extracted_text = ''
#             for (bbox, text, prob) in result:
#                 extracted_text += text.upper() + ' '

#             # Prepare data for MongoDB insertion
#             current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             entry = {
#                 'plate_text': extracted_text.strip(),  # Strip to remove trailing space
#                 'timestamp': current_datetime,
#                 'image': img_data.read()  # Save image binary directly to MongoDB
#             }

#             # Insert entry into MongoDB collection
#             acollection.insert_one(entry)

#             return JsonResponse({'message': 'Image and text saved to MongoDB.'})

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({'error': 'Invalid request method.'}, status=405)

# =====================================================

# import cv2 as cv
# import easyocr
# import os
# import logging
# import pymongo
# from django.http import StreamingHttpResponse, HttpResponse
# from django.shortcuts import render
# from pyzbar.pyzbar import decode

# # Initialize MongoDB client and database
# client = pymongo.MongoClient('mongodb://localhost:27017/')
# db = client['usere']  # Replace with your MongoDB database name
# collection = db['vehicle']  # Replace with your MongoDB collection name

# # Path to your cascade classifier XML file for license plate detection
# haar_cascade = os.path.join(os.path.dirname(__file__), 'models', 'numberplate.xml')

# # Initialize EasyOCR reader for text extraction
# reader = easyocr.Reader(['en'], gpu=True)  # Adjust languages and GPU usage as needed

# # Initialize cascade classifier for license plate detection
# plate_cascade = cv.CascadeClassifier(haar_cascade)
# if plate_cascade.empty():
#     logging.error("Failed to load cascade classifier.")

# def verify_text_in_mongodb(text):
#     try:
#         # Query MongoDB to find if the text exists in the collection
#         query = {'text': text}  # Replace 'text_field_name' with the actual field name in your MongoDB documents
#         result = collection.find_one(query)

#         if result:
#             return True  # Text found in MongoDB
#         else:
#             return False  # Text not found in MongoDB

#     except Exception as e:
#         logging.error(f"Error verifying text in MongoDB: {str(e)}")
#         return False  # Return False on error or if text is not found

# def scan_qr_code(image):
#     barcodes = decode(image)
#     for barcode in barcodes:
#         barcode_data = barcode.data.decode('utf-8')
#         return barcode_data  # Return scanned QR code data

# # def capture_image_and_compare():
# #     cap = cv.VideoCapture(0)  # Initialize VideoCapture object with webcam (change 0 to another index for different camera)

# #     while True:
# #         success, frame = cap.read()

# #         if not success:
# #             continue

# #         qr_code_data = scan_qr_code(frame)

# #         if qr_code_data:
# #             # Perform access control logic based on scanned QR code data
# #             if verify_employee(qr_code_data):  # Implement your employee verification logic
# #                 return True
# #             else:
# #                 return False

# #         # Display the frame with QR code detection (if needed)
# #         cv.imshow('QR Code Detection', frame)

# #         key = cv.waitKey(1) & 0xFF
# #         if key == ord('q'):
# #             break

# #     cap.release()
# #     cv.destroyAllWindows()

# def gen(cap):
#     min_area = 500
#     count = 0  # Initialize count for saving images

#     while True:
#         success, frame = cap.read()

#         if not success:
#             continue

#         gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

#         plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

#         for (x, y, w, h) in plates:
#             area = w * h
#             if area > min_area:
#                 cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)

#                 img_cro = frame[y:y + h, x:x + w]

#                 try:
#                     # Perform OCR on the detected license plate image
#                     result = reader.readtext(img_cro)
#                     for (bbox, text, prob) in result:
#                         text = text.upper()
#                         cv.putText(frame, text, (x, y - 5), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), thickness=2)

#                         # Verify the extracted text against MongoDB
#                         if verify_text_in_mongodb(text):
#                             cv.putText(frame, "Access Granted!", (x, y - 30), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), thickness=2)
#                         else:
#                             cv.putText(frame, "Access Denied!", (x, y - 30), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), thickness=2)

#                 except Exception as e:
#                     logging.error(f"Error processing image: {str(e)}")

#         # Display the processed frame
#         cv.imshow("result", frame)

#         # Save the frame on 's' key press
#         key_press = cv.waitKey(1) & 0xFF
#         if key_press == ord('s'):
#             try:
#                 # Specify the full path where you want to save the image
#                 save_path = os.path.join(os.path.dirname(__file__), f"plates/scaned_img{count}.jpeg")
#                 cv.imwrite(save_path, frame)
#                 cv.rectangle(frame, (0, 500), (440, 500), (0, 255, 0), cv.FILLED)
#                 cv.putText(frame, "plate_saved", (75, 175), cv.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 2)
#                 cv.imshow("result", frame)
#                 cv.waitKey(500)

#                 print("Image saved:", save_path)

#                 # Open a new window to display the saved image and verification status
#                 saved_image = cv.imread(save_path)
#                 verification_status = "Access Granted!" if verify_text_in_mongodb(text) else "Access Denied!"
#                 cv.putText(saved_image, verification_status, (20, 50), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0) if verify_text_in_mongodb(text) else (0, 0, 255), thickness=2)
#                 cv.imshow("Saved Image", saved_image)
#                 cv.waitKey(0)  # Wait for any key press to close the saved image window

#                 count += 1
#             except Exception as e:
#                 logging.error(f"Error saving image: {str(e)}")

#         # Convert frame to bytes for streaming response
#         _, frame_bytes = cv.imencode('.jpg', frame)
#         frame_bytes = frame_bytes.tobytes()

#         yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

#         if key_press == ord('q'):  # Check if 'q' is pressed to quit
#             break

#     cap.release()
#     cv.destroyAllWindows()

# def video_feed(request):
#     return StreamingHttpResponse(gen(cv.VideoCapture(0)), content_type='multipart/x-mixed-replace; boundary=frame')

# def access_control(request):
#     if request.method == 'GET':
#         if capture_image_and_compare():
#             return HttpResponse('Access granted!')
#         else:
#             return HttpResponse('Access denied!')

# def index(request):
#     try:
#         return render(request, 'index.html')
#     except Exception as e:
#         logging.error(f"Error rendering index.html: {str(e)}")

# ===========================


# def generate_qrcode(request):
#     if request.method == 'POST':
#         # Extract form data
#         first_name = request.POST.get('first_name', '')
#         last_name = request.POST.get('last_name', '')
#         email = request.POST.get('email', '')
#         username = request.POST.get('username', '')
#         cname = request.POST.get('cname', '')
#         # count = 0
#         # Construct QR code data
#         qr_data = f"First Name: {first_name}\nLast Name: {last_name}\nEmail: {email}\nUsername: {username}\nCompany Name: {cname}"

#         # Generate QR code image
#         qr = qrcode.make(qr_data)
#         qr.save("{first_name}.png")
#         # count +=1
#         #  cv.imwrite("plates/scaned_img" + str(count) + ".jpeg", img_cro)

#         # Prepare response as a downloadable PNG file
#         response = HttpResponse(content_type="image/png")
#         qr.save(response, "PNG")
#         response['Content-Disposition'] = 'attachment; filename="qrcode.png"'

#         return response

    # return render(request, 'details.html')

# views.py
            
# ===================================================================================
#     
# def scan_qr_code(frame):
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     barcodes = decode(gray)
#     qr_data = []

#     for barcode in barcodes:
#         qr_data.append(barcode.data.decode('utf-8'))
#         # Draw a rectangle around the QR code
#         (x, y, w, h) = barcode.rect
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         # Add QR code data as text on the frame
#         cv2.putText(frame, barcode.data.decode('utf-8'), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#     return qr_data
       
# from .utils import capture_image_and_compare

# def access_control(request):
#     if request.method == 'GET':
#         if capture_image_and_compare():
#             return HttpResponse('Access granted!')
#         else:
#             return HttpResponse('Access denied!')
