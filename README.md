# RandomFoodRuriBot

A Python-based Telegram chatbot that provides random food suggestions and integrates various AI-powered services, including GPT, Bard, and other tools. The bot is capable of handling different commands to interact with users, suggest foods, and more.

## Features

- **Food Suggestions**: Provides random food recommendations with specific commands like `/random`, `/addfood`, and `/showsoup`.
- **Multilingual Support**: Handles multi-language messages using translation APIs.
- **AI-Powered Chatbot**: Integrates GPT and Bard for advanced conversation handling.
- **Image Generation**: Allows users to generate images using commands like `/draw`.
- **Custom Commands**: Offers a variety of commands for interacting with the bot and managing food-related data.
- **Logging and Debugging**: Supports commands for showing logs and debugging.
- **System Information**: Provides VPS information and system control features.
  
## Commands

The bot supports the following commands:

- `/start`: Initializes the bot.
- `/help`: Shows the list of available commands.
- `/random`: Provides a random food suggestion.
- `/showlog`: Displays the bot's logs.
- `/addfood`: Allows users to add a new food to the suggestion list.
- `/addsoup`: Allows users to add a new soup to the suggestion list.
- `/showfood`: Displays the list of added foods.
- `/showsoup`: Displays the list of added soups.
- `/getinfovps`: Retrieves information about the VPS running the bot.
- `/getcontrol`: Gives control commands for the bot.
- `/spamsticker`: Sends a spam of stickers.
- `/replika`: Initiates the Replika chatbot for conversation.
- `/tkb`: Displays the timetable (if applicable).
- `/debug`: Debugging command for bot development.
- `/null`: No action command.
- `/gpt`: Access to OpenAI GPT chatbot for interactions.
- `/bard`: Access to Bard chatbot for interactions.
- `/draw`: Generates an image using Stable Diffusion.
- `/steps`: Configure steps for image generation.
- `/seeds`: Configure seed settings for image generation.
- `/cfg`: Configure settings for generating images.
- `/imgedit`: Edit images using specific parameters.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/RuriMeiko/randomfoodruribot.git
   ```

2. Navigate to the project directory:
   ```bash
   cd randomfoodruribot
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your credentials by editing the `credentials.py` file with the necessary API keys for services like OpenAI, Bard, Google Translate, and Telegram.

## Libraries Used

- **`telegram.ext` & `telegram`**: Telegram bot integration for handling commands.
- **`pydub`**: Audio processing (if applicable).
- **`openai`**: OpenAI GPT API integration.
- **`googletrans`**: Google Translate API for translation features.
- **`requests`**: For making HTTP requests.
- **`psutil`**: For system monitoring.
- **`Bard`**: API integration for the Bard chatbot.
- **`re`**: Regular expression operations.
- **`uuid`**: For generating unique IDs.
- **`tiktoken`**: Tokenizer for OpenAI models.
- **`random`**: For generating random food suggestions.
- **`json`**: For handling JSON data.

## Usage

1. **Set up your credentials**: Make sure to configure the required API keys in `credentials.py` for services like OpenAI, Bard, and Google Translate.
  
2. **Start the bot**: Once everything is set up, run the bot using:
   ```bash
   python bot.py
   ```

3. **Interact with the bot**: Send commands via Telegram to interact with the bot. Some example commands are:
   - `/start` to initialize the bot.
   - `/random` for a random food suggestion.
   - `/gpt` to start interacting with the GPT chatbot.

4. **Food Suggestions**: Use commands like `/addfood`, `/addsoup`, `/showfood`, and `/showsoup` to manage the list of food options and soups.

5. **Image Generation**: Use `/draw` to generate images, and customize settings with commands like `/steps`, `/seeds`, and `/cfg`.

## Example

```plaintext
User: /random
Bot: "How about sushi? 🍣"
```

## Troubleshooting

- **Missing Dependencies**: If you encounter issues with missing libraries, ensure all dependencies are installed with `pip install -r requirements.txt`.
- **API Key Issues**: Make sure all API keys are correctly configured in `credentials.py`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
