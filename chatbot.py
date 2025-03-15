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
        st.write("Ask me about the top 20 cryptocurrencies prices (LIVE PRICES IN USD) or say hi. Examples:")
        st.write("- 'What’s the price of Bitcoin?'")
        st.write("- 'How much is Solana?'")
        st.write("- 'What is Ethereum?'")
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
        st.write("This chatbot answers crypto queries and greetings, fetching live prices for the top 20 coins via CoinGecko!")
        st.subheader("Project Overview:")
        st.write("1. NLP and Logistic Regression handle intents.")
        st.write("2. Streamlit powers the interface with real-time price data.")
        st.subheader("Dataset:")
        st.write("- Intents: e.g., 'crypto_price_bitcoin', 'greeting'")
        st.write("- Live data: Sourced from CoinGecko API")

if __name__ == '__main__':
    main()