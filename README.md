## Telegram Bot YDS
# YOUTUBE-DOWNLOADER-AND-SUMMERIZE

# Telegram YouTube Audio Summarizer Bot
 
This is a Telegram bot that can download audio from YouTube videos and summarize the content using OpenAI's GPT-3 engine. It's a handy tool for quickly extracting insights from YouTube content.

## Prerequisites

Before using the bot, make sure you have the following prerequisites:

- Python 3.7 or higher
- python-telegram-bot library
- pytube library
- moviepy library
- openai library
- An OpenAI API key

You can install the required Python libraries by running:

```bash
pip install -r requirements.txt
```

## Getting Started

1. Clone this repository to your local machine.

2. Set up your OpenAI API key by replacing `'YOUR_OPENAI_API_KEY'` in the code with your actual API key.

3. Create a bot on Telegram and get your TELEGRAM_API_KEY. You can follow the [Telegram BotFather](https://core.telegram.org/bots#botfather) guide to create a bot and obtain the API key.

4. Set your TELEGRAM_API_KEY by replacing `'YOUR_TELEGRAM_API_KEY'` in the code with your actual API key.

5. Run the bot:

```bash
python Yts full.py
```

6. Start a chat with your bot on Telegram and send it a YouTube link. It will download the video, extract the audio, and provide a summary of the content.

## Usage

- Send a YouTube link to the bot.
- The bot will download the video, extract audio, and summarize the content using OpenAI's GPT-3 engine.
- Enjoy quick insights from YouTube videos!

## Customization

You can customize the bot's behavior by modifying the code. For example, you can adjust the summarization length by changing the `max_tokens` in the `openaiHandler` function.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the developers of the Telegram Bot API, pytube, moviepy, and OpenAI for their fantastic libraries.
