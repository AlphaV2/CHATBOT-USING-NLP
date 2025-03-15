# CHATBOT-USING-NLP
A Natural Language Processing (NLP)-powered chatbot built with Python, Streamlit, and Scikit-learn to answer cryptocurrency-related queries and fetch live prices for the top 20 cryptocurrencies using the CoinGecko API. Whether you’re curious about Bitcoin’s price, Ethereum’s basics, or just want a friendly greeting, this chatbot has you covered!
Features

NLP-Driven Intent Recognition: Uses TF-IDF vectorization and Logistic Regression to classify user intents from a custom intents.json dataset.
Live Crypto Prices: Fetches real-time prices for the top 20 cryptocurrencies (e.g., Bitcoin, Ethereum, Solana) via the CoinGecko API.
Interactive Web Interface: Built with Streamlit, featuring a Home chat interface, Conversation History, and About section.
Conversation Logging: Saves chat history to a chat_log.csv file with timestamps.
Extensible Design: Easily add more intents or cryptocurrencies by updating intents.json and the code’s crypto_map.

Top 20 Cryptocurrencies Supported

The chatbot fetches live prices for these coins (as of March 2025):

    Bitcoin (BTC)
    Ethereum (ETH)
    Tether (USDT)
    Binance Coin (BNB)
    Solana (SOL)
    XRP (Ripple)
    USD Coin (USDC)
    Cardano (ADA)
    Dogecoin (DOGE)
    Avalanche (AVAX)
    Shiba Inu (SHIB)
    Chainlink (LINK)
    Polkadot (DOT)
    TRON (TRX)
    Polygon (MATIC)
    Toncoin (TON)
    Internet Computer (ICP)
    Wrapped Bitcoin (WBTC)
    Aptos (APT)
    NEAR Protocol (NEAR)

Prerequisites

    Python 3.8+: Ensure Python is installed on your system.
    Dependencies: Install required libraries via pip (see Installation).
    Internet Connection: Required for fetching live prices from CoinGecko.


Installation:

    Clone the Repository:
    bash
    git clone https://github.com/yourusername/crypto-chatbot.git
    cd crypto-chatbot

Install Dependencies:
Create a virtual environment (optional but recommended) and install the required packages:
bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt

The requirements.txt file should contain:
text

    streamlit>=1.0.0
    scikit-learn>=1.0.0
    nltk>=3.6.0
    requests>=2.26.0

    Download NLTK Data:
    The code automatically downloads the punkt tokenizer during the first run.

    Ensure Files Are Present:
        main.py: The main script.
        intents.json: The intent dataset (included in the repo).

Usage

Run the Chatbot: Start the Streamlit app:
    bash

    streamlit run main.py
    Open your browser to http://localhost:8501.
    Interact with the Chatbot:
        Home: Type queries like:
            "What’s Bitcoin’s price?"
            "How much is Ethereum?"
            "What is Bitcoin?"
            "Hi!"
        Conversation History: View past interactions saved in chat_log.csv.
        About: Learn about the project.
    Exit: Type "goodbye" or "bye" to stop the chat.

Project Structure
text
crypto-chatbot/
├── main.py              # Main script with chatbot logic
├── intents.json         # Intent dataset for NLP training
├── chat_log.csv         # Generated file for conversation history
├── requirements.txt     # List of Python dependencies
└── README.md            # Project documentation
How It Works

    NLP Pipeline:
        Uses TfidfVectorizer to convert user input into numerical features.
        Trains a LogisticRegression model on intents from intents.json to predict user intent.
    Live Price Fetching:
        Queries the CoinGecko API (/simple/price) for real-time prices of the top 20 cryptocurrencies.
        Maps intent tags (e.g., "crypto_price_bitcoin") to CoinGecko IDs (e.g., "bitcoin") for dynamic responses.
    Streamlit Interface:
        Provides a user-friendly web app with a sidebar menu for navigation.

Example Interactions
User Input	Chatbot Response Example
"What’s Bitcoin’s price?"	"The current price of Bitcoin is $65,432 USD."
"How much is Solana?"	"The current price of Solana is $142 USD."
"What is Ethereum?"	"Ethereum’s a platform for apps and smart contracts."
"Hi!"	"Hey there! Ready to talk crypto?"
"Bye"	"Catch you later! Keep your keys safe."
Extending the Project

    Add More Coins: Update the crypto_map in main.py and add corresponding intents in intents.json.
    Enhance Intents: Expand intents.json with more topics (e.g., DeFi, staking, market trends).
    Improve NLP: Replace Logistic Regression with a more advanced model (e.g., BERT) for better intent recognition.
    Caching: Store API responses temporarily to reduce requests and handle CoinGecko’s rate limits.

Troubleshooting

    No Price Data: Ensure an internet connection and that CoinGecko’s API is operational. Check debug output (Predicted tag = ...) for intent mismatches.
    Dependency Errors: Verify all packages are installed (pip install -r requirements.txt).
    File Not Found: Ensure intents.json is in the same directory as main.py.

Contributing

Contributions are welcome! To contribute:

    Fork the repository.
    Create a new branch (git checkout -b feature/your-feature).
    Make your changes and commit (git commit -m "Add your feature").
    Push to your branch (git push origin feature/your-feature).
    Open a Pull Request.

Please follow the Code of Conduct (feel free to add one).
License

This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments

    CoinGecko: For providing a free API to fetch live cryptocurrency prices.
    Streamlit: For an awesome framework to build interactive web apps.
    Scikit-learn & NLTK: For powerful NLP tools.

Contact

For questions or suggestions, feel free to open an issue or reach out via GitHub: (https://github.com/AlphaV2).

Happy coding, and may your portfolio always be in the green! 🚀


