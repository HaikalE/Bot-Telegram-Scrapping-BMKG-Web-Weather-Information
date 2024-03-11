import logging

import requests
from bs4 import BeautifulSoup

from bmkg_weather_scraper import scrape_weather_info

from telegram import ForceReply, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
weather_info = None
# Define a few command handlers. These usually take the two arguments update and
# context.
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! This bot is used to retrieve weather information by scraping the BMKG website.",
        reply_markup=ForceReply(selective=True),
    )


async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global weather_info
    """Send relevant weather information."""
    url = "https://www.bmkg.go.id/cuaca/prakiraan-cuaca-indonesia.bmkg"
    weather_info = scrape_weather_info(url)
    
    # Extract dates from the first index of each table
    dates = [table[0][0] for table in weather_info]
    
    # Create a list of InlineKeyboardButtons for each date
    keyboard = [
        [InlineKeyboardButton(date, callback_data=f"date_{index}")]
        for index, date in enumerate(dates, start=1)
    ]
    
    # Create an InlineKeyboardMarkup with the list of buttons
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("Choose the day:", reply_markup=reply_markup)
    
async def date_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global weather_info
    """Handle button press."""
    query = update.callback_query
    index = int(query.data.split('_')[1])-1
    await query.answer()
    print(index)
    # Check if the index is valid
    if index < 0 or index >= len(weather_info):
        await query.message.reply_text("Invalid selection.")
        return
    
    # Get cities for the selected date
    selected_date_info = weather_info[index]
    
    # Check if there is weather information available for the selected date
    if not selected_date_info:
        await query.message.reply_text("No weather information available for this date.")
        return
    
    # Extract cities for the selected date
    cities_info = selected_date_info[4:]
    cities = [city_info[0] for city_info in cities_info]
    
    # Create buttons for cities
    city_buttons = [
        [InlineKeyboardButton(city, callback_data=f"city_{index}_{city}")]
        for city in cities
    ]
    
    # Create an InlineKeyboardMarkup with the list of city buttons
    city_markup = InlineKeyboardMarkup(city_buttons)
    
    await query.message.reply_text("Select the city:", reply_markup=city_markup)




async def city_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle city button press."""
    query = update.callback_query
    data = query.data.split('_')
    date_index = int(data[1])
    city = data[2]
    
    await query.answer()
    
    # Get weather information for the selected date
    selected_date_info = weather_info[date_index]
    print("Index date ",date_index)
    print("Selected date info ",selected_date_info[2:4])
    # Find the information for the selected city
    city_info = None
    for info in selected_date_info[4:]:
        if info[0] == city:
            city_info = info
            break
    
    # If city information is found, construct the reply text
    if city_info :
        reply_text = f"Weather information for {city} on {selected_date_info[0][0]}:\n\n"

        #header 1
        for info in selected_date_info[2:3]: 
            if len(info) > 0 : 
                for info_item in info:
                    reply_text += f"{info_item}\n"
        
        #header 2
        for info in selected_date_info[3:4]:  
            if len(info) > 0 : 
                for info_item in info:
                    reply_text += f"{info_item}\n"

        reply_text+="\n"

        for info_item in city_info:
            reply_text += f"{info_item}\n"
        
        
        await query.message.reply_text(reply_text)
    else:
        await query.message.reply_text("No weather information available for this city on the selected date.")



async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Prompt the user to input a city name."""
    message = (
        "To inquire about the weather, please type /weather.\n\n"
        "And you can select the day and city\n"
    )
    await update.message.reply_text(message)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6901782915:AAGS3qLMPsWWqzabGKWmefR8YCsttr-UMqI").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("weather", weather))
    application.add_handler(CallbackQueryHandler(date_button, pattern=r"^date_\d+$"))
    application.add_handler(CallbackQueryHandler(city_button, pattern=r"^city_\d+_\w+$"))
    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
