from tkinter import *
import cv2
import face_recognition
import getpass
import os
from PIL import Image, ImageTk

# Usernames and their passwords
user_passwords = {
    "sanju": "sanju123",
    "yashu": "yashu123",
    "prasanna": "prasanna123",
    "ujju": "ujju123"
}

root = Tk()  # create root window
root.title("Face Recognition System")  # title of the GUI window
root.maxsize(900, 600)  # specify the max size the window can expand to
root.config(bg="skyblue")  # specify background color

# Create left and right frames
left_frame = Frame(root, width=200, height=400, bg='grey')
left_frame.grid(row=0, column=0, padx=10, pady=5)

right_frame = Frame(root, width=650, height=400, bg='grey')
right_frame.grid(row=0, column=1, padx=10, pady=5)

# Create frames and labels in left_frame
Label(left_frame, text="Original Image").grid(row=0, column=0, padx=5, pady=5)

# Function to capture images and store them in a folder
def capture_images():
    name = name_entry.get()
    image_folder = f"/Users/nadellaujwala/Documents/SE PROJECT/{name}"
    os.makedirs(image_folder, exist_ok=True)
    
    video_capture = cv2.VideoCapture(0)
    for i in range(5):
        ret, frame = video_capture.read()
        cv2.imwrite(f"{image_folder}/image_{i+1}.jpg", frame)
        cv2.imshow("Capturing Images", frame)
        cv2.waitKey(1000)  # Pause for 1 second between each capture
    video_capture.release()
    cv2.destroyAllWindows()

    # After capturing images, call recognize_and_verify function
    recognize_and_verify()
# Function to recognize faces and verify passwords
def recognize_and_verify():
    # Load known face encodings and names
    known_face_encodings = []
    known_face_names = []
    
    # Load known faces and their names here
    known_persons = ["sanju", "yashu", "prasanna", "ujju"]
    for name in known_persons:
        known_person_image = face_recognition.load_image_file(f"/Users/nadellaujwala/Documents/SE PROJECT/{name}.jpg")
        known_person_encoding = face_recognition.face_encodings(known_person_image)[0]
        known_face_encodings.append(known_person_encoding)
        known_face_names.append(name.capitalize())
    
    # Initialize webcam
    video_capture = cv2.VideoCapture(0)

    # Flag to track if a person is recognized
    recognized = False

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        if not recognized:  
            # Find all face locations in the current frame
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Check if the face matches any known faces
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                    # Draw a box around the face and label with the name
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

                    recognized = True  
                    break  

            # Convert the frame to RGB format for displaying in Tkinter
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb_frame)
            imgtk = ImageTk.PhotoImage(image=img)
            
            # Update the label with the current frame
            original_image_label.imgtk = imgtk
            original_image_label.config(image=imgtk)
            original_image_label.update()

            # Inside recognize_and_verify function, after confirming the name
            name = name.lower()  # Convert name to lowercase
            confirm = input(f"Are you {name.capitalize()}? (yes/no): ")
            if confirm.lower() == "yes":
                name_label.config(text=f"Hi {name.capitalize()}, please enter your password:")
                name_entry.delete(0, END)
                password_input = name_entry.get()

                if user_passwords.get(name) == password_input:  # Check password using lowercase name
                    result_label.config(text="Password correct, access granted.", fg="green")
                else:
                    result_label.config(text="Password incorrect, access denied.", fg="red")
                break

        else:
            cv2.imshow("Video", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

# Main function
def main():
    name = input("Enter your name: ")
    capture_images(name)
    command = input("Do you want to access or enter the website now? (yes/no): ")
    if command.lower() == "yes":
        recognize_and_verify()

if __name__ == "__main__":
    main()

# Label to display live camera feed
original_image_label = Label(left_frame)
original_image_label.grid(row=1, column=0, padx=5, pady=5)

# Entry and Label widgets for name and password input
name_label = Label(left_frame, text="Enter Your Name:")
name_label.grid(row=2, column=0, padx=5, pady=5)
name_entry = Entry(left_frame)
name_entry.grid(row=3, column=0, padx=5, pady=5)

# Result label for displaying access status
result_label = Label(left_frame, text="", fg="black")
result_label.grid(row=4, column=0, padx=5, pady=5)

# Buttons to trigger the functions
capture_btn = Button(left_frame, text="Capture Images", command=capture_images)
capture_btn.grid(row=5, column=0, padx=5, pady=5)

verify_btn = Button(left_frame, text="Verify Identity", command=recognize_and_verify)
verify_btn.grid(row=6, column=0, padx=5, pady=5)

root.mainloop()
