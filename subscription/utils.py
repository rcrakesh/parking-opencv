import cv2
from django.http import HttpResponse
from pymongo import MongoClient

# Initialize MongoDB client (assuming it's a global connection)
client = MongoClient('mongodb://localhost:27017/')
db = client['usere']  # Replace with your actual database name
collection = db['subscription_subscription']  # Replace with your actual collection name

def verify_subscription():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        yield HttpResponse("Unable to access webcam.")

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                yield HttpResponse("Error capturing frame from webcam.")

            detector = cv2.QRCodeDetector()
            data, _, _ = detector.detectAndDecode(frame)

            if data:
                lines = data.strip().split('\n')
                subscription_id = None
                for line in lines:
                    if line.startswith('subscription_id:'):
                        subscription_id = line.split(':')[1].strip()
                        break

                if subscription_id:
                    try:
                        query = {'subscription_id': int(subscription_id)}
                        result = collection.find_one(query)

                        if result:
                            print(f"Subscription ID {subscription_id} verified in MongoDB")
                            yield frame
                        else:
                            print(f"Subscription ID {subscription_id} not found in MongoDB")
                            yield None

                    except Exception as e:
                        print(f"Error verifying subscription in MongoDB: {str(e)}")
                        yield None

            else:
                yield None

    except Exception as e:
        yield HttpResponse(f"Error processing webcam feed: {str(e)}")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        yield HttpResponse("No QR code found or subscription ID not verified.")
