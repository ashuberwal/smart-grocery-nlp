# 🛒 Smart Grocery Optimizer (NLP & ETL Pipeline)

A Proof of Concept (PoC) application demonstrating how to extract structured entities from messy, natural-language human input and match them against a relational database to optimize consumer pricing. 

## 🚀 Overview
Comparing weekly grocery prices across different UK supermarkets is tedious. This application solves that by allowing users to type a messy, conversational grocery list (e.g., *"I need 2 pints of milk, half a kilo of chicken breasts, and some wholemeal bread"*). 

The backend NLP engine extracts the core noun chunks, ignores irrelevant grammar, fuzzy-matches the items to a local SQLite database, and calculates the cheapest overall basket across Aldi, Tesco, and Sainsbury's.

## 🛠️ Tech Stack & Architecture
* **Frontend:** Streamlit (Python)
* **NLP Engine:** spaCy (`en_core_web_sm`)
* **Entity Matching:** RapidFuzz (Levenshtein distance calculation)
* **Database:** SQLite & Pandas (Data transformation and querying)

## 🧠 How the Pipeline Works
1. **Extraction:** The user inputs natural language text. The spaCy model processes the text and extracts `noun_chunks`, automatically filtering out pronouns and stop words.
2. **Transformation & Matching:** The `rapidfuzz` library takes the extracted noun chunks and compares them against the clean `item_name` column in our SQLite database, returning matches with a >50% confidence score.
3. **Price Calculation:** A dynamic SQL query fetches the prices for the matched basket items across all available supermarkets. Pandas groups and aggregates the totals.
4. **Delivery:** Streamlit renders the cheapest overall basket and provides a side-by-side receipt breakdown.

## 💻 How to Run Locally

**1. Clone the repository**
```bash
git clone [https://github.com/YOUR_USERNAME/smart-grocery-nlp.git](https://github.com/YOUR_USERNAME/smart-grocery-nlp.git)
cd smart-grocery-nlp
