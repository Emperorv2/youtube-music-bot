import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from pytube import YouTube

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Command to start the bot
async def start(update: Update, context):
    await update.message.reply_text('Welcome! Send me a YouTube link, and I will play the audio for you.')

# Command to handle YouTube links
async def handle_youtube_link(update: Update, context):
    url = update.message.text
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_file = audio_stream.download(output_path='.', filename='audio.mp3')
        
        await update.message.reply_audio(audio=open(audio_file, 'rb'))
        os.remove(audio_file)  # Clean up the file after sending
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text('Sorry, something went wrong. Please try again.')

# Main function to run the bot
def main():
    # Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your bot's token
    application = ApplicationBuilder().token('YOUR_TELEGRAM_BOT_TOKEN').build()

    # Add handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_youtube_link))

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()