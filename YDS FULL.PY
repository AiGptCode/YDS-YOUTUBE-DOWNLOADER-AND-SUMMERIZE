from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
from pytube import YouTube
from moviepy.editor import AudioFileClip
import openai
import logging

# Set your OpenAI API key here
OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'

# Load TELEGRAM_API_KEY from an environment variable or set it directly
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')

# Initialize the OpenAI API client
openai.api_key = OPENAI_API_KEY

# Initialize the logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name)

# Initialize the Updater with your API key
updater = Updater(token=TELEGRAM_API_KEY, use_context=True)
dispatcher = updater.dispatcher

# Command handler for '/start'
def start(update: Update, context: CallbackContext):
    user_name = update.message.from_user.first_name
    update.message.reply_text(f"Hi {user_name}, welcome to the bot!\nPlease send me a YouTube link to get started! 🎬")

# Function to download a YouTube video and extract audio
def download_video_and_extract_audio(url, output_dir):
    try:
        # Download the YouTube video
        yt = YouTube(url)
        video_stream = yt.streams.filter(only_video=True, file_extension='mp4').first()
        video_file_path = video_stream.download(output_path=output_dir)

        # Extract the audio from the video
        audio = AudioFileClip(video_file_path)
        audio_file_path = os.path.join(output_dir, f"{yt.title}.mp3")
        audio.write_audiofile(audio_file_path)

        return audio_file_path
    except Exception as e:
        logger.error(f"Error while processing YouTube video: {e}")
        return None

# Function to handle text messages
def text_message(update: Update, context: CallbackContext):
    text = update.message.text

    if any(text.startswith(prefix) for prefix in ['http://', 'https://', 'www.youtube.com', 'youtu.be']):
        update.message.reply_text('Please send me a YouTube link')
        update.message.reply_text('Downloading video and extracting audio...')
        update.message.reply_chat_action(action='typing')

        output_dir = "downloads"  # Directory to save downloaded video and extracted audio
        os.makedirs(output_dir, exist_ok=True)

        audio_file_path = download_video_and_extract_audio(text, output_dir)

        if audio_file_path:
            update.message.reply_text('Summarizing content...')
            update.message.reply_chat_action(action='typing')
            ai_response = openaiHandler(audio_file_path)
            update.message.reply_text(ai_response)
        else:
            update.message.reply_text('An error occurred while processing the video. Please try again.')

    else:
        update.message.reply_text('Please send me a YouTube link')

# Function to summarize audio content using OpenAI
def openaiHandler(audio_file_path):
    try:
        # Load the audio content
        with open(audio_file_path, 'rb') as audio_file:
            audio_content = audio_file.read()

        # Make an API call to OpenAI to summarize the audio content
        response = openai.Completion.create(
            engine="davinci",
            prompt=f"Summarize the following audio: '{audio_file_path}'",
            max_tokens=50  # Adjust the number of tokens for desired summary length
        )

        summary = response.choices[0].text

        return summary
    except Exception as e:
        logger.error(f"Error while using OpenAI to summarize audio: {e}")
        return "An error occurred while summarizing the content."

# Add command and message handlers to the dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, text_message))

# Start the bot and keep it running
updater.start_polling()
updater.idle()
