import speech_recognition as sr
from pydub import AudioSegment
import os
import argparse
import tempfile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def convert_audio_format(input_path, output_format="wav"):
    """Convert audio file to WAV format using pydub"""
    try:
        sound = AudioSegment.from_file(input_path)
        with tempfile.NamedTemporaryFile(suffix=f".{output_format}", delete=False) as temp_file:
            temp_path = temp_file.name
        sound.export(temp_path, format=output_format)
        return temp_path
    except Exception as e:
        raise Exception(f"Audio conversion failed: {str(e)}")

def transcribe_audio(audio_path, recognizer):
    """Transcribe audio file using Google Speech Recognition"""
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
        return recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        raise Exception("Google Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        raise Exception(f"Could not request results from Google Speech Recognition service; {e}")

def audio_to_text(audio_file_path, keep_converted=False):
    """Main function to convert audio file to text"""
    recognizer = sr.Recognizer()
    temp_path = None
    
    try:
        # Check file extension
        ext = os.path.splitext(audio_file_path)[1].lower()
        
        # Convert if not WAV or AIFF
        if ext not in ['.wav', '.aiff']:
            print(f"Converting {ext} file to WAV format...")
            temp_path = convert_audio_format(audio_file_path)
            audio_file_path = temp_path
        
        # Transcribe audio
        text = transcribe_audio(audio_file_path, recognizer)
        return text
        
    finally:
        # Clean up temporary file
        if temp_path and not keep_converted and os.path.exists(temp_path):
            os.unlink(temp_path)

def main():
    parser = argparse.ArgumentParser(
        description='Convert audio file to text using Google Speech Recognition',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('audio_path', nargs='?', help='Path to audio file')
    parser.add_argument('--keep', action='store_true', help='Keep converted audio file')
    args = parser.parse_args()

    if args.audio_path:
        # Command-line mode
        try:
            result = audio_to_text(args.audio_path, args.keep)
            print("\nTranscription Result:")
            print("--------------------")
            print(result)
        except Exception as e:
            print(f"\nError: {str(e)}")
    else:
        # Interactive mode
        print("Speech-to-Text Transcription Tool")
        print("---------------------------------")
        audio_path = input("Enter path to audio file: ").strip()
        
        if not audio_path:
            print("No file path provided. Exiting.")
            return
        
        try:
            print("\nProcessing...")
            result = audio_to_text(audio_path)
            print("\nTranscription Result:")
            print("--------------------")
            print(result)
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
