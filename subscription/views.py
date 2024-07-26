import random
from bson import ObjectId   # Import ObjectId from bson package
from io import BytesIO
import qrcode
import stripe
import datetime
import logging
from .models import Subscription
import logging
from pymongo import MongoClient
import cv2
import numpy as np
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.views.decorators.cache import never_cache



# Set your Stripe API key
stripe.api_key = 'sk_test_51PcK4aBxHtcfRKbS5C5mXqnEatESaLZ9pJMmm9FTfF8SfwPT9rLTxm8t4QNYI8qgb5hF5F5Tfy00wjweccavHPNq001vLeu8F7'

def create_subscription(request):# this is to create subscription part , currently not in use , ignore this 
    if request.method == "POST":
        user_id = request.POST.get('user_id')

        # subscription_id = generate_short_id()
        
        # Create subscription data and insert into MongoDB collection
        subscription_data = {
            'user_id': user_id,
            'is_active': True,
            'subscription_id': str(ObjectId())
        }
        subscription_collection = db.subscription
        subscription_collection.insert_one(subscription_data)
        
        # Generate QR code for the subscription ID
        qr_code_buffer = generate_qr_code(subscription_data['subscription_id'])
        
        # Return QR code image as HTTP response
        return HttpResponse(qr_code_buffer.getvalue(), content_type="image/png")


    return render(request, 'faceweb/create_subscription.html')


# views.py

import io
import random
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import DailyPass


@csrf_exempt
def generate_qrcode_dailypass(request):
    if request.method == 'POST':
        # Extract form data
        reference_name = request.POST.get('reference_name', '')
        company = request.POST.get('company', '')
        num_people = int(request.POST.get('num_people', 1))

        # Generate pass code
        pass_code = random.randint(100, 9999)

        # Generate daily pass
        daily_pass = DailyPass.objects.create(
            pass_code=pass_code,
            valid_from=timezone.now(),
            valid_to=timezone.now() + timezone.timedelta(days=1),
            company = company,
            num_people=num_people,
            reference_name=reference_name,
        )

        # Generate QR code data
        qr_data = f"Reference Name: {reference_name}\nValid From: {timezone.now()}\nValid to: {timezone.now() + timezone.timedelta(days=1)}\nNumber of People: {num_people}\nCompany Name: {company}\npass_code: {pass_code}"

        # Generate QR code image
        qr = qrcode.make(qr_data)

        # Prepare response as a downloadable PNG file
        response = HttpResponse(content_type="image/png")
        qr.save(response, "PNG")
        response['Content-Disposition'] = 'attachment; filename="dailypass.png"'

        return response

    return render(request, 'dailypass.html')


# def generate_pass_code():
#     # Generate a unique pass code (example logic, adjust as needed)
#     return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=20))



# Replace with your actual MongoDB client setup

client = MongoClient('mongodb://localhost:27017/') # database setup 
db = client['usere']  # Replace with your actual database name
collection = db['subscription_subscription']


def generate_qrcode(request): # generating the qr_code and storing to database 
    if request.method == 'POST':
        # Extract form data
        first_name = request.POST.get('first_name', '')
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')
        cname = request.POST.get('cname', '')
        user_id = request.POST.get('user_id', '')

        # Generate subscription ID
        subscription_id = random.randint(100, 9999)

        # Construct QR code data including subscription ID
        qr_data = f"First Name: {first_name}\nEmail: {email}\nUsername: {username}\nCompany Name: {cname}\nUser ID: {user_id}\nsubscription_id: {subscription_id}\n"

        # Save subscription data to database using Django model
        subscription = Subscription.objects.create(
            user_id=user_id,
            first_name=first_name,
            email=email,
            username=username,
            company_name=cname,
            subscription_id=subscription_id
        )

        # Generate QR code image
        qr = qrcode.make(qr_data)

        # Prepare response as a downloadable PNG file
        response = HttpResponse(content_type="image/png")
        qr.save(response, "PNG")
        response['Content-Disposition'] = 'attachment; filename="qrcode.png"'

        return response

    return render(request, 'details.html')

import cv2
from pyzbar.pyzbar import decode
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['usere']
collection = db['subscription_subscription']
import cv2
from django.shortcuts import render
from pyzbar.pyzbar import decode
from pymongo import MongoClient

# Assuming your MongoDB client setup is here

import cv2
import threading
from django.http import StreamingHttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
import pymongo

# MongoDB setup

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['usere']  # Replace with your MongoDB database name
collection = db['subscription_subscription']



def verify_sb_in_mongodb(subscription_id):# verification of text from mongodb
    try:
        # Query MongoDB to find if the text exists in the collection
        query = {'subscription_id':int(subscription_id)}  # Replace 'text_field_name' with the actual field name in your MongoDB documents
        result = collection.find_one(query)

        if result:
            return True  # Text found in MongoDB
        else:
            return False  # Text not found in MongoDB

    except Exception as e:
        logging.error(f"Error verifying text in MongoDB: {str(e)}")
        return False  # Return False on error or if text is not found

import cv2
from django.http import HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from pyzbar.pyzbar import decode as pyzbar_decode
import logging
from pymongo import MongoClient

@csrf_exempt
def gene(cap):
    # Initialize MongoDB connection
    client = MongoClient('mongodb://localhost:27017/')  # Database setup
    db = client['usere']  # Replace with your actual database name
    collection = db['subscription_subscription']

    while True:
        success, frame = cap.read()

        if not success:
            continue

        # Convert frame to grayscale for faster QR code detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect QR codes in the frame
        decoded_objects = pyzbar_decode(gray)

        subscription_id = None  # Initialize subscription_id variable

        for obj in decoded_objects:
            # Decode QR code data
            data = obj.data.decode('utf-8')
            logging.info(f"QR Code detected: {data}")  # Log QR code data to terminal
            x, y, w, h = obj.rect  # Rectangle coordinates
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            print(data)
            if 'subscription_id:' in data:
                parts = data.split('subscription_id:')

                if len(parts) > 1:
                    subscription_id = parts[1].strip()  # Extract subscription_id part
                    print(f"Extracted subscription_id: '{subscription_id}'")  # Print with quotes to reveal hidden characters
                else:
                    print("Failed to extract subscription_id from the QR code data.")
            else:
                print("No valid subscription_id found in the QR code data.")
  
            if subscription_id:
                try:
                    # Verify subscription_id in MongoDB
                    query = {'subscription_id': int(subscription_id)}
                    result = collection.find_one(query)

                    if result:
                        cv2.putText(frame, "Access Granted!", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), thickness=2)
                    else:
                        cv2.putText(frame, "Access Denied!", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), thickness=2)

                    break  # Assuming only one QR code needs to be processed

                except Exception as e:
                    logging.error(f"Error verifying subscription in MongoDB: {str(e)}")
                    return HttpResponse("Error verifying subscription in MongoDB.")

        if not subscription_id:
            cv2.putText(frame, "No valid QR code found.", (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), thickness=2)

        _, frame_bytes = cv2.imencode('.jpg', frame)
        frame_bytes = frame_bytes.tobytes()

        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@csrf_exempt
def video_feed2(request):
    cap = cv2.VideoCapture(0)
    return StreamingHttpResponse(gene(cap), content_type='multipart/x-mixed-replace; boundary=frame')


def verify_sub(request):
    return render(request, 'verify_sub.html')

import cv2
from pyzbar.pyzbar import decode as pyzbar_decode
from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import render
from pymongo import MongoClient
import logging
from django.views.decorators.csrf import csrf_exempt

# Initialize MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['usere']
collection = db['subscription_dailypass']

@csrf_exempt
def gene1(cap):
    client = MongoClient('mongodb://localhost:27017/')  # Database setup
    db = client['usere']  # Replace with your actual database name
    collection = db['subscription_dailypass']
    while True:
        success, frame = cap.read()
        if not success:
            continue

        # Convert frame to grayscale for faster QR code detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect QR codes in the frame
        decoded_objects = pyzbar_decode(gray)

        pass_code = None  # Initialize pass_code variable

        for obj in decoded_objects:
            # Decode QR code data
            data = obj.data.decode('utf-8')
            logging.info(f"QR Code detected: {data}")
            x, y, w, h = obj.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            if 'pass_code:' in data:
                parts = data.split('pass_code:')
                if len(parts) > 1:
                    pass_code = parts[1].strip()
                else:
                    logging.info("Failed to extract pass_code from the QR code data.")
            else:
                logging.info("No valid pass_code found in the QR code data.")
            print(pass_code)
            if pass_code:
                try:
                    # Verify pass_code in MongoDB
                    query = {'pass_code': int(pass_code)}
                    result = collection.find_one(query)

                    if result:
                        cv2.putText(frame, "Access Granted!", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), thickness=2)
                    else:
                        cv2.putText(frame, "Access Denied!", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), thickness=2)

                    break  # Assuming only one QR code needs to be processed

                except Exception as e:
                    logging.error(f"Error verifying pass_code in MongoDB: {str(e)}")
                    return HttpResponse("Error verifying pass_code in MongoDB.")

        if not pass_code:
            cv2.putText(frame, "No valid QR code found.", (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), thickness=2)

        _, frame_bytes = cv2.imencode('.jpg', frame)
        frame_bytes = frame_bytes.tobytes()

        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    # Release video capture when done
    cap.release()

@csrf_exempt
def video_feed3(request):
    cap = cv2.VideoCapture(0)
    return StreamingHttpResponse(gene1(cap), content_type='multipart/x-mixed-replace; boundary=frame')

def Dpass(request):
    return render(request, 'Dpass.html')









import cv2
import logging
from pymongo import MongoClient
from pyzbar.pyzbar import decode as pyzbar_decode
from django.http import HttpResponse
from django.shortcuts import render

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['usere']  # Replace with your actual database name
collection = db['subscription_subscription']






def generate_qr_code(request):# just ignore code not in use 
    # Generate QR code
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4,)
    qr.add_data("Some data")  
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Prepare response
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)
    
    # Return the image as HTTP response
    return HttpResponse(buffer.getvalue(), content_type="image/png")






# ------------------------------------end of views.py subscription-----------------------------------------------------------






# Assuming your data format is 'subscription_id:<ID>'
            # if data.startswith('subscription_id:'):
            #     subscription_id = data.split(':')[1].strip()
            
            #     try:
            #         # Verify subscription_id in MongoDB
            #         query = {'subscription_id': int(subscription_id)}
            #         result = collection.find_one(query)

            #         if result:
            #             cv2.putText(frame, "Access Granted!", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), thickness=2)
            #         else:
            #             cv2.putText(frame, "Access Denied!", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), thickness=2)

            #     except Exception as e:
            #         logging.error(f"Error verifying subscription in MongoDB: {str(e)}")
            # else:
            #     print("no qr code")
        # Convert frame to bytes for streaming response















# # Function to detect QR codes and verify subscription in MongoDB
# def detect_and_verify_qr(request):
#     if request.method == 'POST':
#         try:
#             # Initialize video capture from webcam (index 0)
#             cap = cv2.VideoCapture(0)
            
#             # Read frame from the video capture
#             ret, frame = cap.read()
            
#             if ret:
#                 # Convert frame to grayscale for QR code detection
#                 gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
#                 # Decode QR codes in the frame
#                 decoded_objects = pyzbar_decode(gray)
                
#                 for obj in decoded_objects:
#                     data = obj.data.decode('utf-8')
#                     logging.info(f"QR Code detected: {data}")

#                     # Assuming data format is 'subscription_id:<ID>'
#                     if data.startswith('subscription_id:'):
#                         subscription_id = data.split(':')[1].strip()

#                         try:
#                             # Verify subscription_id in MongoDB
#                             query = {'subscription_id': int(subscription_id)}
#                             result = collection.find_one(query)

#                             if result:
#                                 return HttpResponse("Access Granted!")
#                             else:
#                                 return HttpResponse("Access Denied!")

#                         except Exception as e:
#                             logging.error(f"Error verifying subscription in MongoDB: {str(e)}")
#                             return HttpResponse("Error verifying subscription in MongoDB")

#                 # If no QR code with subscription ID format is found
#                 return HttpResponse("No valid subscription QR code found.")

#         except Exception as e:
#             logging.error(f"Error processing QR code detection: {str(e)}")
#             return HttpResponse("Error processing QR code detection")

#     # If not a POST request, render the initial form or page
#     return render(request, 'verify_subscription.html')



# from pyzbar.pyzbar import decode as pyzbar_decode
# def decode(frame):
#     try:
#         # Detect QR codes in the frame
#         decoded_objects = pyzbar_decode(frame)
#     except Exception as e:
#         print(f"Error decoding QR codes: {e}")
#         decoded_objects = []

#     # Return decoded objects
#     return decoded_objects

# # Video feed processing function
# @csrf_exempt
# def video_feed2(request):
#     cap = cv2.VideoCapture(0)

#     def generate():
#         while True:
#             success, frame = cap.read()

#             if not success:
#                 continue

#             # Convert frame to grayscale for faster QR code detection
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#             # Detect QR codes in the frame
#             decoded_objects = decode(gray)

#             for obj in decoded_objects:
#                 data = obj.data.decode('utf-8')
#                 logging.info(f"QR Code detected: {data}")

#                 x, y, w, h = obj.rect  # Rectangle coordinates
#                 cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

#                 # Assuming your data format is 'subscription_id:<ID>'
#                 if data.startswith('subscription_id:'):
#                     subscription_id = data.split(':')[1].strip()

#                     try:
#                         # Verify subscription_id in MongoDB
#                         query = {'subscription_id': int(subscription_id)}
#                         result = collection.find_one(query)

#                         if result:
#                             cv2.putText(frame, "Access Granted!", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), thickness=2)
#                         else:
#                             cv2.putText(frame, "Access Denied!", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), thickness=2)

#                     except Exception as e:
#                         logging.error(f"Error verifying subscription in MongoDB: {str(e)}")

#             # Convert frame to bytes for streaming response
#             _, frame_bytes = cv2.imencode('.jpg', frame)
#             frame_bytes = frame_bytes.tobytes()

#             yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

#     return StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')

# @csrf_exempt
# def gene(cap):
#     while True:
#         success, frame = cap.read()

#         if not success:
#             continue

#         # Convert frame to grayscale for faster QR code detection
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         # Detect QR codes in the frame
#         decoded_objects = decode(gray)

#         for obj in decoded_objects:
#             data = obj.data.decode('utf-8')
#             logging.info(f"QR Code detected: {data}")

#             x, y, w, h = obj.rect  # Rectangle coordinates
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

#             # Assuming your data format is 'subscription_id:<ID>'
#             if data.startswith('subscription_id:'):
#                 subscription_id = data.split(':')[1].strip()

#                 try:
#                     # Verify subscription_id in MongoDB
#                     query = {'subscription_id': int(subscription_id)}
#                     result = collection.find_one(query)

#                     if result:
#                         cv2.putText(frame, "Access Granted!", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), thickness=2)
#                     else:
#                         cv2.putText(frame, "Access Denied!", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), thickness=2)

#                 except Exception as e:
#                     logging.error(f"Error verifying subscription in MongoDB: {str(e)}")

#         # Convert frame to bytes for streaming response
#         _, frame_bytes = cv2.imencode('.jpg', frame)
#         frame_bytes = frame_bytes.tobytes()

#         yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# @csrf_exempt
# def video_feed2(request):
#     cap = cv2.VideoCapture(0)
#     return StreamingHttpResponse(gene(cap), content_type='multipart/x-mixed-replace; boundary=frame')


    # def stream():
    #     cap = cv2.VideoCapture(0)
    #     if not cap.isOpened():
    #         logging.error("Unable to access webcam.")
    #         yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n\r\n'
    #         return

    #     for frame in gen(cap):
    #         yield frame

    #     cap.release()

    # return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')
 #  if verify_text_in_mongodb(text):
                        #     cv2.putText(frame, "Access Granted!", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), thickness=2)
                        # else:
                        #     cv2.putText(frame, "Access Denied!", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), thickness=2)
                      














# def generate_qrcode(request):
#     if request.method == 'POST':
#         # Extract form data
#         first_name = request.POST.get('first_name', '')
#         email = request.POST.get('email', '')
#         username = request.POST.get('username', '')
#         cname = request.POST.get('cname', '')
#         user_id = request.POST.get('user_id','')

#         # Generate subscription ID
#         subscription_id = random.randint(100, 9999)

#         # Construct QR code data including subscription ID
#         qr_data = f"First Name: {first_name}\nEmail: {email}\nUsername: {username}\nCompany Name: {cname}\nUser ID: {user_id}\nSubscription ID: {subscription_id}\n"

#         # Insert subscription data into MongoDB collection
#         subscription_data = {
#             'user_id': user_id,
#             'first_name': first_name,
#             'Email': email,
#             'Username': username,
#             'Company Name': cname,
#             'is_active': True,
#             'subscription_id': subscription_id
#         }
#         subscription_collection = mongo_db.subscription
#         subscription_collection.insert_one(subscription_data)

#         # Generate QR code image
#         qr = qrcode.make(qr_data)

#         # Prepare response as a downloadable PNG file
#         response = HttpResponse(content_type="image/png")
#         qr.save(response, "PNG")
#         response['Content-Disposition'] = 'attachment; filename="qrcode.png"'

#         return response

#     return render(request, 'details.html')


# ==========================================


# def generate_qr_code(subscription_id):
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )
#     qr.add_data(subscription_id)
#     qr.make(fit=True)

#     img = qr.make_image(fill='black', back_color='white')
#     buffer = BytesIO()
#     img.save(buffer, format="PNG")
#     buffer.seek(0)

#     response = HttpResponse(buffer, content_type='image/png')
#     response['Content-Disposition'] = 'attachment; filename="subb.png"'

#     return response



# def verify_subscription(request):
#     if request.method == "POST":
#         qr_code_image = request.FILES.get('qr_code')  # Assuming 'qr_code' is the name of your input file field
#         if qr_code_image:
#             # Decode QR code image using OpenCV
#             img = cv2.imdecode(np.frombuffer(qr_code_image.read(), np.uint8), cv2.IMREAD_COLOR)
#             detector = cv2.QRCodeDetector()
#             data, _ = detector.detectAndDecodeMulti(img)
            
#             if data:
#                 subscription_id = data
#                 try:
#                     # Check if subscription ID exists in Django model
                     
#                     if  Subscription.objects.find(subscription_id=subscription_id):
                    
#                     # if subscription.is_active:
#                         return HttpResponse("Subscription is active.")
#                     else:
#                         return HttpResponse("Subscription is inactive.")
#                 except Subscription.DoesNotExist:
#                     return HttpResponse("Subscription not found.")
#             else:
#                 return HttpResponse("No QR code found in the image.")
#         else:
#             return HttpResponse("No QR code image uploaded.")
    
#     return render(request, 'faceweb/verify_subscription.html')





# def verify_sub_in_mongodb(subscription_id):
#     try:
#         # Query MongoDB to find if the text exists in the collection
#         query = {'subscription_id': subscription_id}  # Replace 'text_field_name' with the actual field name in your MongoDB documents
#         result = collection.find_one(query)

#         if result:
#             return True  # Text found in MongoDB
#         else:
#             return False  # Text not found in MongoDB

#     except Exception as e:
#         logging.error(f"Error verifying sub in MongoDB: {str(e)}")
#         return False




# from .models import Subscription  # Import your Subscription model

# Assuming you have pymongo configured and imported as 'client' and 'collection' defined



# def verify_subscription(request):
#     if request.method == "POST":
#         qr_code_image = request.FILES.get('qr_code')  # Assuming 'qr_code' is the name of your input file field
#         if qr_code_image:
#             try:
#                 # Decode QR code image using OpenCV
#                 img = cv2.imdecode(np.frombuffer(qr_code_image.read(), np.uint8), cv2.IMREAD_COLOR)
#                 detector = cv2.QRCodeDetector()
#                 data, _ = detector.detectAndDecodeMulti(img)
                
#                 if data:
#                     subscription_id = data
#                     try:
#                         # Check if subscription ID exists in Django model
#                         try:
#                             subscription = Subscription.objects.get(subscription_id=subscription_id)
#                             if subscription.is_active:
#                                 return HttpResponse("Subscription is active.")
#                             else:
#                                 return HttpResponse("Subscription is inactive.")
#                         except Subscription.DoesNotExist:
#                             # Check if subscription ID exists in MongoDB
#                             if verify_sub_in_mongodb(subscription_id):
#                                 return HttpResponse("Subscription is active in MongoDB.")
#                             else:
#                                 return HttpResponse("Subscription not found in Django or MongoDB.")
                    
#                     except Exception as e:
#                         return HttpResponse(f"Error: {str(e)}")
                
#                 else:
#                     return HttpResponse("No QR code found in the image.")
            
#             except Exception as e:
#                 return HttpResponse(f"Error decoding QR code: {str(e)}")
        
#         else:
#             return HttpResponse("No QR code image uploaded.")
    
#     return render(request, 'faceweb/verify_subscription.html')



# def verify_sub_in_mongodb(subscription_id):
#     try:
#         # Query MongoDB to find if the subscription ID exists in the collection
#         query = {'subscription_id': subscription_id}  # Replace 'subscription_id' with the actual field name in your MongoDB documents
#         result = collection.find_one(query)

#         if result:
#             return True  # Subscription ID found in MongoDB
#         else:
#             return False  # Subscription ID not found in MongoDB

#     except Exception as e:
#         logging.error(f"Error verifying subscription in MongoDB: {str(e)}")
#         return False


# import cv2
# import numpy as np
# from django.shortcuts import render, HttpResponse
# from .models import Subscription  # Import your Subscription model

# # Assuming you have pymongo configured and imported as 'client' and 'collection' defined

# def verify_subscription(request):
#     if request.method == "POST":
#         qr_code_image = request.FILES.get('qr_code')  # Assuming 'qr_code' is the name of your input file field
#         if qr_code_image:
#             try:
#                 # Decode QR code image using OpenCV
#                 img = cv2.imdecode(np.frombuffer(qr_code_image.read(), np.uint8), cv2.IMREAD_COLOR)
#                 detector = cv2.QRCodeDetector()
#                 # Use detectAndDecode to get data and points
#                 data, points, _ = detector.detectAndDecodeMulti(img)
                
#                 if data:
#                     subscription_id = data
#                     try:
#                         # Check if subscription ID exists in Django model
#                         try:
#                             subscription = Subscription.objects.get(subscription_id=subscription_id)
#                             if subscription.is_active:
#                                 return HttpResponse("Subscription is active.")
#                             else:
#                                 return HttpResponse("Subscription is inactive.")
#                         except Subscription.DoesNotExist:
#                             # Check if subscription ID exists in MongoDB
#                             if verify_sub_in_mongodb(subscription_id):
#                                 return HttpResponse("Subscription is active in MongoDB.")
#                             else:
#                                 return HttpResponse("Subscription not found in Django or MongoDB.")
                    
#                     except Exception as e:
#                         return HttpResponse(f"Error: {str(e)}")
                
#                 else:
#                     return HttpResponse("No QR code found in the image.")
            
#             except Exception as e:
#                 return HttpResponse(f"Error decoding QR code: {str(e)}")
        
#         else:
#             return HttpResponse("No QR code image uploaded.")
    
#     return render(request, 'faceweb/verify_subscription.html')

# def verify_sub_in_mongodb(subscription_id):
#     try:
#         # Query MongoDB to find if the subscription ID exists in the collection
#         query = {'subscription_id': subscription_id}  # Replace 'subscription_id' with the actual field name in your MongoDB documents
#         result = collection.find_one(query)

#         if result:
#             return True  # Subscription ID found in MongoDB
#         else:
#             return False  # Subscription ID not found in MongoDB

#     except Exception as e:
#         logging.error(f"Error verifying subscription in MongoDB: {str(e)}")
#         return False
# import cv2
# import numpy as np
# from django.shortcuts import render, HttpResponse
# from .models import Subscription  # Import your Subscription model

# # Assuming you have pymongo configured and imported as 'client' and 'collection' defined

# def verify_subscription(request):
#     if request.method == "POST":
#         qr_code_image = request.FILES.get('qr_code')  # Assuming 'qr_code' is the name of your input file field
#         if qr_code_image:
#             try:
#                 # Decode QR code image using OpenCV
#                 img = cv2.imdecode(np.frombuffer(qr_code_image.read(), np.uint8), cv2.IMREAD_COLOR)
#                 detector = cv2.QRCodeDetector()
#                 # Use detectAndDecode to get data and points
#                 data, _, _ = detector.detectAndDecodeMulti(img)
                
#                 if data:
#                     # Extract subscription ID (adjust as needed)
#                     subscription_id = data.strip()  # Clean up any leading/trailing whitespace
#                     # Check if subscription ID exists in Django model
#                     try:
#                         if verify_sub_in_mongodb(subscription_id):
#                                 return HttpResponse("Subscription is active in both Django and MongoDB. Access granted.")
#                         else:
#                                 return HttpResponse("Subscription is active in Django, but inactive in MongoDB. Access denied.")
#                     except :
#                         # Check if subscription ID exists in MongoDB
#                         if verify_sub_in_mongodb(subscription_id):
#                             return HttpResponse("Subscription is active in MongoDB. Access granted.")
#                         else:
#                             return HttpResponse("Subscription not found in Django or MongoDB. Access denied.")
                    
#                 else:
#                     return HttpResponse("No QR code found in the image.")
            
#             except Exception as e:
#                 return HttpResponse(f"Error decoding QR code: {str(e)}")
        
#         else:
#             return HttpResponse("No QR code image uploaded.")
    
#     return render(request, 'faceweb/verify_subscription.html')

# def verify_sub_in_mongodb(subscription_id):
#     try:
#         # Query MongoDB to find if the subscription ID exists in the collection
#         query = {'subscription_id': subscription_id}  # Replace 'subscription_id' with the actual field name in your MongoDB documents
#         result = db.find_one(query)

#         if result:
#             # Assuming MongoDB has an 'is_active' field as well
#             if result.get('is_active', False):
#                 return True  # Subscription is active in MongoDB
#             else:
#                 return False  # Subscription is inactive in MongoDB

#         else:
#             return False  # Subscription ID not found in MongoDB

#     except Exception as e:
#         logging.error(f"Error verifying subscription in MongoDB: {str(e)}")
#         return False


# Assuming you have pymongo configured and imported as 'pymongo' and 'collection' defined

'''def verify_subscription(request):
    if request.method == "POST":
        qr_code_image = request.FILES.get('qr_code')  # Assuming 'qr_code' is the name of your input file field
        if qr_code_image:
            try:
                # Decode QR code image using OpenCV
                img = cv2.imdecode(np.frombuffer(qr_code_image.read(), np.uint8), cv2.IMREAD_COLOR)
                detector = cv2.QRCodeDetector()
                # Use detectAndDecode to get data and points
                data, _, _ = detector.detectAndDecodeMulti(img)
                
                if data:
                    # Extract subscription ID (adjust as needed)
                    subscription_id = data.strip()  # Clean up any leading/trailing whitespace
                    
                    # Check if subscription ID exists in MongoDB
                    if verify_sub_in_mongodb(subscription_id):
                        return HttpResponse("Subscription found and active. Access granted.")
                    else:
                        return HttpResponse("Subscription not found or inactive. Access denied.")
                    
                else:
                    return HttpResponse("No QR code found in the image.")
            
            except Exception as e:
                return HttpResponse(f"Error decoding QR code: {str(e)}")
        
        else:
            return HttpResponse("No QR code image uploaded.")
    
    return render(request, 'faceweb/verify_subscription.html')

def verify_sub_in_mongodb(subscription_id):
    try:
        # Query MongoDB to find if the subscription ID exists in the collection
        query = {'subscription_id': subscription_id}  # Replace 'subscription_id' with the actual field name in your MongoDB documents
        result = collection.find_one(query)

        if result and result.get('is_active', False):
            return True  # Subscription is active in MongoDB
        else:
            return False  # Subscription not found or inactive in MongoDB

    except Exception as e:
        logging.error(f"Error verifying subscription in MongoDB: {str(e)}")
        return False'''


# import cv2
# import numpy as np
# from django.shortcuts import render, HttpResponse
# # from .models import Subscription  # Import your Subscription model

# # Assuming you have pymongo configured and imported as 'client' and 'collection' defined

# def verify_subscription(request):
#     if request.method == "POST":
#         qr_code_image = request.FILES.get('qr_code')  # Assuming 'qr_code' is the name of your input file field
#         if qr_code_image:
#             try:
#                 # Decode QR code image using OpenCV
#                 img = cv2.imdecode(np.frombuffer(qr_code_image.read(), np.uint8), cv2.IMREAD_COLOR)
#                 detector = cv2.QRCodeDetector()
                
#                 # Detect and decode QR code
#                 data, _, _ = detector.detectAndDecode(img)
                
#                 if data:
#                     # Extract subscription ID (adjust as needed)
#                     subscription_id = data.strip()  # Clean up any leading/trailing whitespace
                    
#                     # Extract first 5 characters of subscription ID
#                     subscription_id_first_five = subscription_id[:5]
                    
#                     # Check if subscription ID exists in MongoDB
#                     if verify_sub_in_mongodb(subscription_id_first_five):
#                         return HttpResponse("Subscription found and active. Access granted.")
#                     else:
#                         return HttpResponse("Subscription not found or inactive. Access denied.")
                    
#                 else:
#                     return HttpResponse("No QR code found in the image.")
            
#             except Exception as e:
#                 return HttpResponse(f"Error decoding QR code: {str(e)}")
        
#         else:
#             return HttpResponse("No QR code image uploaded.")
    
#     return render(request, 'faceweb/verify_subscription.html')

# def verify_sub_in_mongodb(subscription_id_first_five):
#     try:
#         # Query MongoDB to find if any subscription ID starts with the provided first five characters
#         query = {'subscription_id': {'$regex': f'^{subscription_id_first_five}'}}
#         result = collection.find_one(query)

#         if result and result.get('is_active', True):
#             return True  # Subscription is active in MongoDB
#         else:
#             return False  # Subscription not found or inactive in MongoDB

#     except Exception as e:
#         logging.error(f"Error verifying subscription in MongoDB: {str(e)}")
#         return False


# subscriptions/views.py
# from urllib import response


 # return file_path
# def save_qr_code_view(request, subscription_id):
#     # Define path where QR code image will be saved
#     save_path = 'webapp/qrcode/qr_code.png'  # Adjust this path as per your server's directory structure
    
#     # Generate QR code image and save to file
#     saved_path = generate_qr_code(subscription_id, save_path)
    
#     # Optionally, return a response or redirect to indicate success
#     return HttpResponse(f'QR code saved to {saved_path}')
# ===================================================================
# def generate_short_id():
#     return ''.join(random.choices('0123456789', k=5))


# def create_subscription(request):
#     if request.method == "POST":
#         user_id = request.POST.get('user_id')

#         subscription_id = generate_short_id()
        
#         # Create subscription data and insert into MongoDB collection
#         subscription_data = {
#             'user_id': user_id,
#             'is_active': True,
#             'subscription_id': str(ObjectId())
#         }
#         subscription_collection = mongo_db.subscription
#         subscription_collection.insert_one(subscription_data)
        
#         # Generate QR code for the subscription ID
#         qr_code_buffer = generate_qr_code(subscription_data['subscription_id'])
        
#         # Return QR code image as HTTP response
#         response = HttpResponse(qr_code_buffer.getvalue(), content_type="image/png")
#         response['Content-Disposition'] = 'attachment; filename="subb.png"'
        
        # return response
# 
# =======================================



# def generate_qrcode(request):
#     if request.method == 'POST':
#         # Extract form data
#         first_name = request.POST.get('first_name', '')
#         last_name = request.POST.get('last_name', '')
#         email = request.POST.get('email', '')
#         username = request.POST.get('username', '')
#         cname = request.POST.get('cname', '')
#         user_id = request.POST.get('user_id','')
#         # count = 0
#         # Construct QR code data
#         subscription_id = str(ObjectId())
#         qr_data = f"First Name: {first_name}\nEmail: {email}\nUsername: {username}\nCompany Name: {cname}\nuserid: {user_id}\nSubscription ID: {subscription_id}\n"
#         subscription_data = {
#             'user_id': user_id,
#             'first_name': first_name,
#             'Email': email,
#             'Username': username,
#             'Company Name': cname,
#             'is_active': True,
#             'subscription_id': str(ObjectId())
#         }
       
#         subscription_collection = mongo_db.subscription
#         subscription_collection.insert_one(subscription_data)
        
#         # Generate QR code image
#         qr = qrcode.make(qr_data)
#         qr.save("cs.png")
#         # count +=1
#         #  cv.imwrite("plates/scaned_img" + str(count) + ".jpeg", img_cro)

#         # Prepare response as a downloadable PNG file
#         response = HttpResponse(content_type="image/png")
#         qr.save(response, "PNG")
#         response['Content-Disposition'] = 'attachment; filename="qrcode.png"'

#         return response

#     return render(request, 'details.html')-------------------------------------------

'''
def generate_qrcode(request):
    if request.method == 'POST':
        # Extract form data
        first_name = request.POST.get('first_name', '')
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')
        cname = request.POST.get('cname', '')
        user_id = request.POST.get('user_id','')

        # Generate subscription ID
        subscription_id = random.randint(10000, 999999)

        # Construct QR code data including subscription ID
        qr_data = f"First Name: {first_name}\nEmail: {email}\nUsername: {username}\nCompany Name: {cname}\nUser ID: {user_id}\nSubscription ID: {subscription_id}\n"

        # Insert subscription data into MongoDB collection
        subscription_data = {
            'user_id': user_id,
            'first_name': first_name,
            'Email': email,
            'Username': username,
            'Company Name': cname,
            'is_active': True,
            'subscription_id': subscription_id
        }
        subscription_collection = mongo_db.subscription
        subscription_collection.insert_one(subscription_data)

        # Generate QR code image
        qr = qrcode.make(qr_data)

        # Prepare response as a downloadable PNG file
        response = HttpResponse(content_type="image/png")
        qr.save(response, "PNG")
        response['Content-Disposition'] = 'attachment; filename="qrcode.png"'

        return response

    return render(request, 'details.html')


'''
# ----------------------------------------------------------------------------------------------
# import cv2
# from pyzbar.pyzbar import decode
# from pymongo import MongoClient
# from django.shortcuts import render, HttpResponse
# import numpy as np

# def verify_subscription(request):
#     if request.method == "POST":
#         try:
#             # Initialize video capture (0 is usually the webcam)
#             cap = cv2.VideoCapture(0)

#             while True:
#                 # Read frame-by-frame
#                 ret, frame = cap.read()

#                 if not ret:
#                     return HttpResponse("Error capturing frame from webcam.")

#                 # Decode the QR codes in the frame
#                 decoded_objects = decode(frame)

#                 for obj in decoded_objects:
#                     # Extract QR code data
#                     qr_data = obj.data.decode('utf-8').strip()

#                     # Assuming subscription ID is encoded in the QR code as 'subscription_id: ####'
#                     if qr_data.startswith('subscription_id:'):
#                         subscription_id = qr_data.split(':')[1].strip()

#                         # Verify subscription ID in MongoDB
#                         try:
#                             client = MongoClient('mongodb://localhost:27017/')
#                             db = client['your_database_name']  # Replace with your actual database name
#                             collection = db['subscription_subscription']

#                             # Query MongoDB to find the subscription ID in the collection
#                             query = {'subscription_id': int(subscription_id)}
#                             result = collection.find_one(query)

#                             if result:
#                                 print(f"Subscription ID {subscription_id} verified in MongoDB")
#                                 return HttpResponse("Subscription Verified")
#                             else:
#                                 print(f"Subscription ID {subscription_id} not found in MongoDB")
#                                 return HttpResponse("Subscription Not Verified")

#                         except Exception as e:
#                             print(f"Error verifying subscription in MongoDB: {str(e)}")
#                             return HttpResponse("Error verifying subscription in MongoDB")

#                     # Display QR code bounding box and data on the frame
#                     points = obj.polygon
#                     if len(points) == 4:
#                         pts = [(point.x, point.y) for point in points]
#                         cv2.polylines(frame, [np.array(pts, dtype=np.int32)], isClosed=True, color=(0, 255, 0), thickness=2)
#                     cv2.putText(frame, f'{obj.type}: {obj.data.decode("utf-8")}', (obj.rect.left, obj.rect.top - 10),
#                                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

#                 # Display the frame with QR code data
#                 cv2.imshow('QR Code Scanner', frame)

#                 # Break the loop on 'q' key press
#                 if cv2.waitKey(1) & 0xFF == ord('q'):
#                     break

#             # Release the capture and close windows
#             cap.release()
#             cv2.destroyAllWindows()

#             return HttpResponse("No QR code found or subscription ID not verified.")

#         except Exception as e:
#             return HttpResponse(f"Error processing webcam feed: {str(e)}")

#     return render(request, 'verify_subscription.html')
















# Function to process video feed and verify subscriptions
# def generate_video_feed(cap):
#     try:
#         while True:
#             ret, frame = cap.read()

#             if not ret:
#                 raise Exception("Error capturing frame from webcam.")

#             # Detect QR codes
#             detector = cv2.QRCodeDetector()
#             data, _, _ = detector.detectAndDecode(frame)

#             if data:
#                 lines = data.strip().split('\n')
#                 subscription_id = None
#                 for line in lines:
#                     if line.startswith('subscription_id:'):
#                         subscription_id = line.split(':')[1].strip()
#                         break

#                 if subscription_id:
#                     try:
#                         query = {'subscription_id': int(subscription_id)}
#                         result = collection.find_one(query)

#                         if result:
#                             print(f"Subscription ID {subscription_id} verified in MongoDB")
#                             # Encode frame as JPEG and yield for streaming
#                             _, jpeg = cv2.imencode('.jpg', frame)
#                             yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

#                         else:
#                             print(f"Subscription ID {subscription_id} not found in MongoDB")
#                             yield None

#                     except Exception as e:
#                         print(f"Error verifying subscription in MongoDB: {str(e)}")
#                         yield None

#             else:
#                 yield None

#     except Exception as e:
#         print(f"Error processing webcam feed: {str(e)}")
#         yield None

#     finally:
#         cap.release()

# # Video feed view function
# @csrf_exempt
# def video_feed2(request):
#     cap = cv2.VideoCapture(0)  # Open default camera (index 0)

#     if not cap.isOpened():
#         return HttpResponseServerError("Unable to access webcam.")

#     return StreamingHttpResponse(generate_video_feed(cap), content_type='multipart/x-mixed-replace; boundary=frame')


# def verify_subscription(request): # verifying the generated qr code 
#     if request.method == "POST":
#         qr_code_image = request.FILES.get('qr_code')
        
#         if qr_code_image:
#             try:
#                 # Decode QR code image
#                 img = cv2.imdecode(np.frombuffer(qr_code_image.read(), np.uint8), cv2.IMREAD_COLOR)
#                 detector = cv2.QRCodeDetector()
#                 data, _, _ = detector.detectAndDecode(img)

#                 if data:
#                     # Split data into lines and extract subscription_id
#                     lines = data.strip().split('\n')
#                     subscription_id = None
#                     for line in lines:
#                         if line.startswith('subscription_id:'):
#                             subscription_id = line.split(':')[1].strip()
#                             break
#                     if subscription_id:            
#                     # subscription_id = data.strip()  # Assuming subscription ID is encoded in the QR code
                    
#                     # Verify subscription ID in MongoDB
#                         try:
#                             client = MongoClient('mongodb://localhost:27017/')
#                             db = client['usere']  # Replace with your actual database name
#                             collection = db['subscription_subscription']

#                             # Query MongoDB to find the subscription ID in the collection
#                             query = {'subscription_id': int(subscription_id)}
#                             result = collection.find_one(query)

#                             if result:
#                                 print(f"Subscription ID {subscription_id} verified in MongoDB")
#                                 return HttpResponse("Subscription Verified")
#                             else:
#                                 print(f"Subscription ID {subscription_id} not found in MongoDB")
#                                 return HttpResponse("Subscription Not Verified")

#                         except Exception as e:
#                             print(f"Error verifying subscription in MongoDB: {str(e)}")
#                             return HttpResponse("Error verifying subscription in MongoDB")

#                     else:
#                         return HttpResponse("No QR code found in the image.")
            
#             except Exception as e:
#                 return HttpResponse(f"Error decoding QR code: {str(e)}")
        
#         else:
#             return HttpResponse("No QR code image uploaded.")
    
#     return render(request, 'verify_subscription.html')
# from django.http import StreamingHttpResponse
# import cv2
# from pymongo import MongoClient


# def verify_subscription():
#     cap = cv2.VideoCapture(0)

#     if not cap.isOpened():
#         yield HttpResponse("Unable to access webcam.")

#     try:
#         while True:
#             ret, frame = cap.read()

#             if not ret:
#                 yield HttpResponse("Error capturing frame from webcam.")

#             detector = cv2.QRCodeDetector()
#             data, _, _ = detector.detectAndDecode(frame)

#             if data:
#                 lines = data.strip().split('\n')
#                 subscription_id = None
#                 for line in lines:
#                     if line.startswith('subscription_id:'):
#                         subscription_id = line.split(':')[1].strip()
#                         break

#                 if subscription_id:
#                     try:
#                         query = {'subscription_id': int(subscription_id)}
#                         result = collection.find_one(query)

#                         if result:
#                             print(f"Subscription ID {subscription_id} verified in MongoDB")
#                             yield frame
#                         else:
#                             print(f"Subscription ID {subscription_id} not found in MongoDB")
#                             yield None

#                     except Exception as e:
#                         print(f"Error verifying subscription in MongoDB: {str(e)}")
#                         yield None

#             else:
#                 yield None

#     except Exception as e:
#         yield HttpResponse(f"Error processing webcam feed: {str(e)}")

#     finally:
#         cap.release()
#         cv2.destroyAllWindows()
#         yield HttpResponse("No QR code found or subscription ID not verified.")

# def video_feed2(request):
#     def stream():
#         for frame in verify_subscription():
#             if frame is None:
#                 yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n\r\n'  # Placeholder for no frame
#             else:
#                 _, frame_bytes = cv2.imencode('.jpg', frame)
#                 frame_bytes = frame_bytes.tobytes()
#                 yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

#     return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')



# def verify_sub(request):
#     return render(request, 'verify_subscription.html')

# from django.http import StreamingHttpResponse
# from django.shortcuts import render
# import cv2
# from .utils import verify_subscription  # Import verify_subscription from utils.py

# from django.http import StreamingHttpResponse
# from django.shortcuts import render
# import cv2
# from .utils import verify_subscription
# from django.http import StreamingHttpResponse, HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# import cv2
# from pyzbar.pyzbar import decode
# from pymongo import MongoClient
# import logging


# client = MongoClient('mongodb://localhost:27017/') # database setup 
# db = client['usere']  # Replace with your actual database name
# collection = db['subscription_subscription']




# def verify_text_in_mongodb(subscription_id):# verification of text from mongodb
#     try:
#         # Query MongoDB to find if the text exists in the collection
#         query = {'subscription_id': subscription_id}  # Replace 'text_field_name' with the actual field name in your MongoDB documents
#         result = collection.find_one(query)

#         if result:
#             return True  # Text found in MongoDB
#         else:
#             return False  # Text not found in MongoDB

#     except Exception as e:
#         logging.error(f"Error verifying text in MongoDB: {str(e)}")
#         return False  # Return False on error or if text is not found

# import cv2
# import logging
# from pymongo import MongoClient
# from pyzbar.pyzbar import decode as pyzbar_decode
# from django.http import StreamingHttpResponse
# from django.views.decorators.csrf import csrf_exempt

# # MongoDB connection
# client = MongoClient('mongodb://localhost:27017/')
# db = client['usere']  # Replace with your actual database name
# collection = db['subscription_subscription']

# # Function to decode QR codes in a given frame
# def decode(frame):
#     try:
#         # Detect QR codes in the frame
#         decoded_objects = pyzbar_decode(frame)
#     except Exception as e:
#         print(f"Error decoding QR codes: {e}")
#         decoded_objects = []

#     # Return decoded objects
#     return decoded_objects

# # Generator function for streaming video feed
# def generate_video_feed(cap):
#     while True:
#         # Read frame-by-frame
#         ret, frame = cap.read()

#         if not ret:
#             break

#         # Convert frame to grayscale for faster QR code detection
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         # Decode the QR codes in the frame
#         decoded_objects = decode(gray)

#         for obj in decoded_objects:
#             # Extract text data from QR code
#             qr_data = obj.data.decode('utf-8')
#             logging.info(f"QR Code detected: {qr_data}")

#             # Process QR code data if it starts with 'subscription_id:'
#             if qr_data.startswith('subscription_id:'):
#                 subscription_id = qr_data.split(':')[1].strip()

#                 try:
#                     # Verify subscription_id in MongoDB
#                     query = {'subscription_id': int(subscription_id)}
#                     result = collection.find_one(query)

#                     if result:
#                         cv2.putText(frame, "Access Granted!", (obj.rect.left, obj.rect.top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#                     else:
#                         cv2.putText(frame, "Access Denied!", (obj.rect.left, obj.rect.top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

#                 except Exception as e:
#                     logging.error(f"Error verifying subscription in MongoDB: {str(e)}")

#         # Convert frame to bytes for streaming response
#         _, frame_bytes = cv2.imencode('.jpg', frame)
#         frame_bytes = frame_bytes.tobytes()

#         yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# # Video feed view function
# @csrf_exempt
# def video_feed2(request):
#     cap = cv2.VideoCapture(0)  # Open default camera (index 0)
#     return StreamingHttpResponse(generate_video_feed(cap), content_type='multipart/x-mixed-replace; boundary=frame')

# =============================================/=


# @csrf_exempt
# def gene1(cap):
#     # Initialize MongoDB connection
#     client = MongoClient('mongodb://localhost:27017/')  # Database setup
#     db = client['usere']  # Replace with your actual database name
#     collection = db['subscription_dailypass']

#     while True:
#         success, frame = cap.read()

#         if not success:
#             continue

#         # Convert frame to grayscale for faster QR code detection
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         # Detect QR codes in the frame
#         decoded_objects = pyzbar_decode(gray)

#         pass_code = None  # Initialize subscription_id variable

#         for obj in decoded_objects:
#             # Decode QR code data
#             data = obj.data.decode('utf-8')
#             logging.info(f"QR Code detected: {data}")  # Log QR code data to terminal
#             x, y, w, h = obj.rect  # Rectangle coordinates
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#             print(data)
#             if 'pass_code:' in data:
#                 parts = data.split('pass_code:')

#                 if len(parts) > 1:
#                     pass_code = parts[1].strip()  # Extract subscription_id part
#                     print(f"Extracted pass_code '{pass_code}'")  # Print with quotes to reveal hidden characters
#                 else:
#                     print("Failed to extract pass_code from the QR code data.")
#             else:
#                 print("No valid pass_code found in the QR code data.")
  
#             if pass_code:
#                 try:
#                     # Verify subscription_id in MongoDB
#                     query = {'pass_code': int(pass_code)}
#                     result = collection.find_one(query)

#                     if result:
#                         cv2.putText(frame, "Access Granted!", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), thickness=2)
#                     else:
#                         cv2.putText(frame, "Access Denied!", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), thickness=2)

#                     break  # Assuming only one QR code needs to be processed

#                 except Exception as e:
#                     logging.error(f"Error verifying pass_code in MongoDB: {str(e)}")
#                     return HttpResponse("Error verifying pass_code in MongoDB.")

#         if not pass_code:
#             cv2.putText(frame, "No valid QR code found.", (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), thickness=2)

#         _, frame_bytes = cv2.imencode('.jpg', frame)
#         frame_bytes = frame_bytes.tobytes()

#         yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# @csrf_exempt
# def video_feed3(request):
#     cap = cv2.VideoCapture(0)
#     return StreamingHttpResponse(gene1(cap), content_type='multipart/x-mixed-replace; boundary=frame')

# def Dpass(request):
#     return render(request, 'Dpass.html')


