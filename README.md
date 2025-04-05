# AI Sign Language Interpreter Tool

Welcome to the AI Sign Language Interpreter Tool! This is a smart program created by a group of students to help people understand sign language using a webcam and artificial intelligence (AI). It is designed to make communication easier for deaf individuals and teach others about sign language in a fun way. This project was developed by Adarsh Kumar, Anurag Anand Jha, and Sukhpreet Kaur.

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Requirements](#requirements)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Description
The AI Sign Language Interpreter Tool uses a webcam to watch hand signs and tells you what they mean. It can detect common signs, let you add new ones, and even talk to you through a chatbot. This tool is great for learning sign language and helping people connect better. This is a group project by Adarsh Kumar, Anurag Anand Jha, and Sukhpreet Kaur, showcasing our teamwork and skills.

## Features
- **Detect Signs**: Reads your hand signs and shows the meaning.
- **Learn Signs**: Teaches you how to do common sign language gestures.
- **Add Custom Signs**: Lets you create and save your own signs.
- **Chat Bot**: Answers your questions by typing or voice.
- **History**: Keeps a record of the signs you show.
- **Speak Out**: Speaks the meaning of the sign aloud.
- **Easy to Use**: Works with a simple interface on your computer.

## Installation
Follow these steps to set up the tool on your computer:

1. **Clone the Repository**:
   - Open your terminal or command prompt.
   - Type this command and press Enter:
   - https://github.com/Adarsh-Kumar6534/ai-sign-language-interpreter.git
2. **Create a Virtual Environment** (optional but recommended):
- Go to the project folder:
-  Create a virtual environment
-  - Activate it:
- On Windows: `venv\Scripts\activate`
- On Mac/Linux: `source venv/bin/activate`

3. **Install Dependencies**:
- Make sure you have Python 3.7 or higher.
- Install the required libraries by running:

4. **Get a Gemini API Key**:
- Sign up at [Google AI Studio](https://aistudio.google.com/) to get a free API key.
- Add your API key to the code by replacing the empty string in `GEMINI_API_KEY = ""` in the script.

5. **Run the Tool**:
- Start the program by typing:
- Make sure your webcam is connected.

## Usage
- **Start the Program**: Open the tool and connect your webcam.
- **Detect Signs**: Click "DETECT" and show a sign to the camera.
- **Learn Signs**: Click "LEARN SIGN" to see examples.
- **Add Custom Signs**: Click "ADD CUSTOM SIGN" to teach new gestures.
- **Use Chat Bot**: Click "CHAT BOT" to ask questions or use voice input.
- **Reset**: Click "RESET" to stop or clear the screen.
- **Retry Camera**: Click "RETRY CAMERA" if the webcam doesn’t work.

## How It Works
- The tool uses your webcam to see your hand movements.
- AI (Mediapipe and Gemini) analyzes the signs and matches them to known gestures.
- It shows the meaning on the screen and can speak it using text-to-speech.
- The chatbot uses AI to answer your questions, and voice input lets you talk to it.
- Custom signs are saved, and history is stored for later.

## Requirements
- **Hardware**: A computer with a webcam and microphone.
- **Software**:
- Python 3.7 or higher
- Libraries: `customtkinter`, `opencv-python`, `mediapipe`, `google-generativeai`, `gtts`, `playsound`, `speechrecognition`, `pyaudio`
- **Internet**: Needed for the Gemini API and voice recognition.

## Contributing
We welcome help to make this tool better! Here’s how you can contribute:
1. Fork this repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes and test them.
4. Commit your changes: `git commit -m "Add new feature"`.
5. Push to your branch: `git push origin feature-name`.
6. Open a pull request on GitHub.

Please follow the code style and add comments to your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
- **Inventors**:
- Adarsh Kumar (adarshsingh6534@gmail.com)
- Anurag Anand Jha (tanaykumarjhaind@gmail.com)
- Sukhpreet Kaur (sukhgill2572@gmail.com)
- **GitHub**: [https://github.com/your-username/ai-sign-language-interpreter](https://github.com/Adarsh-Kumar6534/ai-sign-language-interpreter)
- **Questions**: Feel free to open an issue on GitHub or email us!

---

