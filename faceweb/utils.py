import cv2 as cv
import easyocr
from .models import AllowedPerson  # Adjust import path based on your project structure
import logging
import os
                         

                    # ignore this ......


def capture_image_and_compare(): # this is just a normal opencv code , 
    cap = None
    try:
        # Path to your cascade classifier XML file for license plate detection
        haar_cascade = "models/numberplate.xml"

        # Check if the cascade classifier file exists
        if not os.path.isfile(haar_cascade):
            logging.error(f"Cascade classifier file '{haar_cascade}' not found.")
            return

        # Initialize video capture from default camera (index 0)
        cap = cv.VideoCapture(0)
        if not cap.isOpened():
            logging.error("Failed to open camera.")
            return
        
        cap.set(3, 640)  # Set width
        cap.set(4, 480)  # Set height

        min_area = 500  # Minimum area threshold for license plate detection
        count = 0  # Counter for saving images

        # Load cascade classifier for license plate detection
        plate_cascade = cv.CascadeClassifier(haar_cascade)
        if plate_cascade.empty():
            logging.error("Failed to load cascade classifier.")
            return

        # Initialize EasyOCR reader for text extraction
        reader = easyocr.Reader(['en'], gpu=True)  # Adjust languages and GPU usage as needed

        while True:
            # Capture frame-by-frame
            success, frame = cap.read()

            if not success:
                continue

            # Convert frame to grayscale for license plate detection
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            # Detect license plates in the frame
            plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

            for (x, y, w, h) in plates:
                area = w * h
                if area > min_area:
                    # Draw rectangle around detected license plate
                    cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)

                    # Extract license plate region
                    img_cro = frame[y:y + h, x:x + w]

                    # Perform OCR on license plate region
                    result = reader.readtext(img_cro)

                    for (bbox, text, prob) in result:
                        # Display recognized text on the frame
                        cv.putText(frame, text, (x, y - 5), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), thickness=2)

            # Display the resulting frame
            cv.imshow("result", frame)

            # Check for key press events
            key_press = cv.waitKey(1) & 0xFF
            if key_press == ord('s'):
                # Save the scanned license plate image
                cv.imwrite("plates/scaned_img" + str(count) + ".jpeg", img_cro)
                cv.rectangle(frame, (0, 500), (440, 500), (0, 255, 0), cv.FILLED)
                cv.putText(frame, "plate_saved", (75, 175), cv.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 2)
                print(text)  # Print extracted text to console
                cv.imshow("result", frame)
                cv.waitKey(500)
                count += 1
            elif key_press == ord('q'):
                break

    except cv.error as e:
        logging.error(f"OpenCV error occurred: {str(e)}")
    except Exception as e:
        logging.error(f"Error occurred during EasyOCR operation: {str(e)}")

    finally:
        if cap is not None:
            cap.release()
        # Release the capture and destroy all OpenCV windows
        # cap.release()
        cv.destroyAllWindows()

# ------------------------------------end of utils.py faceweb---------------------------------------------------------------





# import cv2 as cv
# import easyocr
# from .models import AllowedPerson  # Adjust import path based on your project structure

# def capture_image_and_compare():
#     # Path to your cascade classifier XML file for license plate detection
#     haar_cascade = "face_recognisation/models/numberplate.xml"

#     # Initialize video capture from default camera (index 0)
#     cap = cv.VideoCapture(0)
#     cap.set(3, 640)  # Set width
#     cap.set(4, 480)  # Set height

#     min_area = 500  # Minimum area threshold for license plate detection
#     count = 0  # Counter for saving images

#     # Load cascade classifier for license plate detection
#     plate_cascade = cv.CascadeClassifier(haar_cascade)

#     # Initialize EasyOCR reader for text extraction
#     reader = easyocr.Reader(['en'], gpu=True)  # Adjust languages and GPU usage as needed

#     while True:
#         # Capture frame-by-frame
#         success, frame = cap.read()

#         if not success:
#             continue

#         # Convert frame to grayscale for license plate detection
#         gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

#         # Detect license plates in the frame
#         plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

#         for (x, y, w, h) in plates:
#             area = w * h
#             if area > min_area:
#                 # Draw rectangle around detected license plate
#                 cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)

#                 # Extract license plate region
#                 img_cro = frame[y:y + h, x:x + w]

#                 # Perform OCR on license plate region
#                 result = reader.readtext(img_cro)

#                 for (bbox, text, prob) in result:
#                     # Display recognized text on the frame
#                     cv.putText(frame, text, (x, y - 5), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), thickness=2)

#         # Display the resulting frame
#         cv.imshow("result", frame)

#         # Check for key press events
#         key_press = cv.waitKey(1) & 0xFF
#         if key_press == ord('s'):
#             # Save the scanned license plate image
#             cv.imwrite("plates/scaned_img" + str(count) + ".jpeg", img_cro)
#             cv.rectangle(frame, (0, 500), (440, 500), (0, 255, 0), cv.FILLED)
#             cv.putText(frame, "plate_saved", (75, 175), cv.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 2)
#             print(text)  # Print extracted text to console
#             cv.imshow("result", frame)
#             cv.waitKey(500)
#             count += 1
#         elif key_press == ord('q'):
#             break

#     # Release the capture and destroy all OpenCV windows
#     cap.release()
#     cv.destroyAllWindows()        
