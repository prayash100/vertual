from flask import Flask, render_template, Response
import cv2
import pygame
import threading

app = Flask(__name__)

# Face detection cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Initialize pygame for sound playback
pygame.init()

# Function to play the birthday sound
def play_birthday_sound():
    pygame.mixer.init()
    pygame.mixer.music.load('static/doremon.mp3')
    pygame.mixer.music.play()

# Function to generate frames for the webcam feed
def generate_frames():
    text_size = 0.6  # Initial text size for animation
    text_size_increase = 0.001  # Size increase for animation
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # If faces are detected, add animated text
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                # Add the animated text above the face
                font = cv2.FONT_HERSHEY_COMPLEX
                texts = ["Today's Princess", "Tomorrow's Queen"]

                # Vibrant gradient color for text
                text_color = (147, 112, 219)  # Purple-pink shade

                # Position the text centered above the face
                for i, text in enumerate(texts):
                    (text_width, text_height), baseline = cv2.getTextSize(text, font, text_size, 2)
                    text_x = x + w // 2 - text_width // 2  # Center the text horizontally
                    text_y = y - 50 - i * 40  # Position above the face with spacing
                    cv2.putText(frame, text, (text_x, text_y), font, text_size, text_color, 2, cv2.LINE_AA)

                # Text animation (increasing size)
                text_size += text_size_increase  # Increase text size for animation effect
                if text_size > 0.8:  # Reset size after a certain point for smooth looping
                    text_size = 0.6

            # Play the birthday sound in a separate thread if it's not already playing
            if not pygame.mixer.music.get_busy():  # Check if the sound is not already playing
                threading.Thread(target=play_birthday_sound).start()

        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame as part of the HTTP response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route for displaying the webcam feed
@app.route('/')
def index():
    return render_template('index.html')

# Route for streaming the webcam feed
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)