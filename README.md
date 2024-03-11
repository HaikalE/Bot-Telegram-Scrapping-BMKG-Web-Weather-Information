![Telegram-bots-2-1 (1)](https://github.com/HaikalE/Bot-Telegram-Scrapping-BMKG-Web-Weather-Information/assets/89823572/ff63b9b4-81a2-4e56-b766-81af258a702a)

This Telegram bot retrieves weather information by scraping the BMKG (Badan Meteorologi, Klimatologi, dan Geofisika) website. Users can interact with the bot to get weather forecasts for different dates and cities in Indonesia.

## Features
- `/weather` command to initiate weather inquiry.
- Interactive buttons for selecting the date and city.
- Weather information includes temperature, humidity, wind speed, and weather conditions.
- Error handling for invalid selections and unavailable data.
- Help command (`/help`) to guide users on how to interact with the bot.

## Requirements
- Python 3.7 or higher
- `requests`, `bs4`, `aiogram` libraries
- BMKG Weather Scraper module

## Usage
1. Install the required Python libraries:
    ```bash
    pip install requests bs4 aiogram
    ```

2. Clone the repository:
    ```bash
    git clone https://github.com/your_username/your_repository.git
    ```

3. Navigate to the project directory:
    ```bash
    cd your_repository
    ```

4. Run the bot:
    ```bash
    python main.py
    ```

5. Start interacting with the bot on Telegram.

## How to Contribute
1. Fork the repository.
2. Create a new branch for your feature or bug fix:
    ```bash
    git checkout -b feature/your-feature
    ```
3. Make your changes and commit them:
    ```bash
    git commit -m "Add your feature or fix"
    ```
4. Push to your branch:
    ```bash
    git push origin feature/your-feature
    ```
5. Create a pull request.

## Contributors
- Muhammad Haikal Rahman (https://github.com/haikale)

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
