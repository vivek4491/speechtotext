
import speech_recognition as sr
import keyboard
import threading
import time
from fpdf import FPDF

# Flag to control when to stop listening
stop_listening = False

def check_for_stop():
    """Check for the 'e' key press to stop speech recognition."""
    global stop_listening
    while True:
        if keyboard.is_pressed('e'):  # If 'e' key is pressed, set flag to stop
            stop_listening = True
            print("Stopping speech recognition...")  # Notify that recognition will stop
            break
        time.sleep(0.1)  # Check every 100ms for the 'e' key press

def save_to_pdf(text_lines):
    """Save recognized text lines to a PDF file."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add each line to the PDF
    for line in text_lines:
        pdf.cell(200, 10, txt=line, ln=True)

    # Save the PDF
    pdf.output("output.pdf")
    print("The recognized text has been saved to output.pdf")

def speech_to_text():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Press 's' to start speech recognition and 'e' to stop it.")

    text_lines = []  # List to store recognized text

    while True:
        if keyboard.is_pressed('s'):  # Start when 's' key is pressed
            print("Speech recognition started. Press 'e' to stop.")
            
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
                print("Listening for speech...")

                global stop_listening
                stop_listening = False

                # Start a thread to listen for the 'e' key press
                key_thread = threading.Thread(target=check_for_stop)
                key_thread.daemon = True  # Allow thread to exit when the main program exits
                key_thread.start()

                while not stop_listening:  # Keep listening until 'e' is pressed
                    try:
                        # Listen continuously without timeout until 'e' is pressed
                        audio_data = recognizer.listen(source, timeout=None, phrase_time_limit=None)
                        print("Recognizing...")

                        # Convert speech to text
                        text = recognizer.recognize_google(audio_data)
                        print("You said:", text)

                        # Add recognized text to the list
                        text_lines.append(text)

                    except sr.UnknownValueError:
                        print("Sorry, I could not understand the audio.")
                    except sr.RequestError as e:
                        print("Could not request results; check your network connection:", e)
                    except Exception as e:
                        print("An error occurred:", e)

            # Save the recognized text to a PDF after 'e' is pressed
            save_to_pdf(text_lines)
            break  # Break out of the loop after saving the PDF

# Run the function
if __name__ == "__main__":
    speech_to_text()