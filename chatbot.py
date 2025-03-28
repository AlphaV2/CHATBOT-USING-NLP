import os
import json
import datetime
import csv
import nltk
import ssl
import streamlit as st
import random
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from features.fear_greed import get_fear_greed_index  # New import

# Disable SSL verification (only if needed)
ssl._create_default_https_context = ssl._create_unverified_context
nltk.data.path.append(os.path.abspath("nltk_data"))
nltk.download('punkt', quiet=True)

# Load intents dynamically
file_path = os.path.join(os.path.dirname(__file__), "intents.json")
try:
    with open(file_path, "r", encoding='utf-8') as file:
        intents = json.load(file)
except FileNotFoundError:
    st.error("intents.json not found. Please ensure it’s in the project directory.")
    st.stop()

# Initialize vectorizer and classifier
vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
clf = LogisticRegression(random_state=0, max_iter=10000)

# Preprocess data
tags = []
patterns = []
for intent in intents:
    for pattern in intent['patterns']:
        tags.append(intent['tag'])
        patterns.append(pattern.lower())

# Train the model
x = vectorizer.fit_transform(patterns)
y = tags
clf.fit(x, y)

# Function to fetch live crypto prices from CoinGecko API
def get_crypto_price(crypto_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        price = data.get(crypto_id, {}).get('usd', 'unavailable')
        return f"${price}" if price != 'unavailable' else "Price unavailable right now."
    except requests.RequestException:
        return "Sorry, I couldn’t fetch the price—try again later!"

# Enhanced chatbot function
def chatbot(input_text):
    input_vec = vectorizer.transform([input_text.lower()])
    tag = clf.predict(input_vec)[0]
    st.write(f"Debug: Predicted tag = {tag}")  # Debugging output
    for intent in intents:
        if intent['tag'] == tag:
            # Handle dynamic price intents for top 20 coins
            crypto_map = {
                "crypto_price_bitcoin": "bitcoin",
                "crypto_price_ethereum": "ethereum",
                "crypto_price_tether": "tether",
                "crypto_price_binancecoin": "binancecoin",
                "crypto_price_solana": "solana",
                "crypto_price_xrp": "ripple",
                "crypto_price_usdcoin": "usd-coin",
                "crypto_price_cardano": "cardano",
                "crypto_price_dogecoin": "dogecoin",
                "crypto_price_avalanche": "avalanche-2",
                "crypto_price_shibainu": "shiba-inu",
                "crypto_price_chainlink": "chainlink",
                "crypto_price_polkadot": "polkadot",
                "crypto_price_tron": "tron",
                "crypto_price_polygon": "matic-network",
                "crypto_price_toncoin": "the-open-network",
                "crypto_price_internetcomputer": "internet-computer",
                "crypto_price_wrappedbitcoin": "wrapped-bitcoin",
                "crypto_price_aptos": "aptos",
                "crypto_price_near": "near"
            }
            if tag in crypto_map:
                crypto_id = crypto_map[tag]
                price = get_crypto_price(crypto_id)
                return f"The current price of {crypto_id.replace('-', ' ').capitalize()} is {price} USD."
            # Handle Fear and Greed Index
            elif tag == "fear_and_greed":
                return get_fear_greed_index()
            # Return static responses for non-price intents
            return random.choice(intent['responses'])
    return "Sorry, I didn’t catch that—try asking about crypto prices or something else!"

counter = 0

def main():
    global counter
    st.title("CRYPTO Q/A Chatbot using NLP")

    menu = ["Home", "Conversation History", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.write("Welcome to the CryptoQ chatbot!")
        st.write("Ask me about the top 20 cryptocurrencies prices (LIVE PRICES IN USD), the Fear & Greed Index, or say hi. Examples:")
        st.write("- 'What’s the price of Bitcoin?'")
        st.write("- 'How much is Solana?'")
        st.write("- 'What is the Fear and Greed Index?'")
        st.write("- 'Hello!'")

        if not os.path.exists('chat_log.csv'):
            with open('chat_log.csv', 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['User Input', 'Chatbot Response', 'Timestamp'])

        counter += 1
        user_input = st.text_input("You:", key=f"user_input_{counter}")

        if user_input:
            user_input_str = str(user_input)
            response = chatbot(user_input_str)
            st.text_area("Chatbot:", value=response, height=120, key=f"chatbot_response_{counter}")

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open('chat_log.csv', 'a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([user_input_str, response, timestamp])

            if response.lower() in ['goodbye', 'bye']:
                st.write("Thanks for chatting! See you later!")
                st.stop()

    elif choice == "Conversation History":
        st.header("Conversation History")
        try:
            with open('chat_log.csv', 'r', encoding='utf-8') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)  # Skip header
                for row in csv_reader:
                    st.text(f"User: {row[0]}")
                    st.text(f"Chatbot: {row[1]}")
                    st.text(f"Timestamp: {row[2]}")
                    st.markdown("---")
        except FileNotFoundError:
            st.write("No conversation history yet.")

    elif choice == "About":
        st.write("The Crypto Q/A Chatbot is an NLP-driven assistant designed to answer cryptocurrency queries and fetch live prices for the top 20 coins, built as part of an AICTE internship project.")
        
        st.subheader("Project Overview:")
        st.write("""
        This project combines natural language processing and real-time data integration to deliver an interactive crypto tool:
        1. **Intent Recognition**: Uses NLP techniques and Logistic Regression to classify user queries from a custom dataset.
        2. **Live Price Fetching**: Integrates the CoinGecko API to provide real-time prices for top cryptocurrencies.
        3. **Fear & Greed Index**: Uses CoinMarketCap API to fetch market sentiment data.
        4. **Web Interface**: Powered by Streamlit, offering a seamless chat experience with history tracking.
        """)

        st.subheader("Implementation Details:")
        st.write("""
        - **Core Logic**: 
        - `chatbot.py` orchestrates NLP, API calls, and UI rendering.
        - `fear_greed.py` handles Fear & Greed Index API integration.
        - Chatbot function maps intents to static or dynamic responses.
        - **NLP Pipeline**: 
        - TF-IDF Vectorizer converts text to features.
        - Logistic Regression predicts intents with high accuracy.
        - **Data Handling**: 
        - `intents.json` stores 50+ intents (e.g., greetings, price queries).
        - `chat_log.csv` logs conversations with timestamps.
        - **API Integration**: CoinGecko for prices, CoinMarketCap for Fear & Greed Index.
        """)

        st.subheader("Dataset:")
        st.write("""
        - **Intents**: 
        - Examples: 'crypto_price_bitcoin', 'greeting', 'fear_and_greed'.
        - Covers greetings, crypto basics, price queries, and market sentiment.
        - **Live Data**: 
        - Sourced from CoinGecko (prices) and CoinMarketCap (Fear & Greed).
        - **Structure**: JSON format with tags, patterns, and responses.
        """)

        st.subheader("Technologies Used:")
        st.write("""
        - **Python 3.8+**: Core language for development.
        - **Streamlit**: Interactive web app framework.
        - **Scikit-learn**: NLP and ML components (TF-IDF, Logistic Regression).
        - **NLTK**: Text preprocessing (Punkt tokenizer).
        - **Requests**: HTTP requests to CoinGecko and CoinMarketCap APIs.
        """)

        st.subheader("Future Scope:")
        st.write("""
        - Expand intents to include DeFi, staking, and market trends.
        - Upgrade to advanced NLP models (e.g., BERT) for better accuracy.
        - Add price and sentiment caching to reduce API calls.
        - Integrate additional APIs for news or trading insights.
        """)

        st.subheader("Acknowledgments:")
        st.write("""
        - Developed under AICTE internship guidance.
        - Powered by CoinGecko and CoinMarketCap APIs and open-source tools.
        - Inspired by the growing crypto community.
        """)

if __name__ == '__main__':
    main()