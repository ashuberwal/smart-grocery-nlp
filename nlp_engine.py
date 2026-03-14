import spacy
import sqlite3
from rapidfuzz import process

# 1. Load the NLP model
print("Loading AI Model (this takes a second)...")
nlp = spacy.load("en_core_web_sm")

def get_database_items():
    """Fetches all unique product names from our SQLite database."""
    conn = sqlite3.connect('groceries.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT item_name FROM products")
    
    # Extract the items from the database rows into a simple Python list
    db_items = [row[0] for row in cursor.fetchall()]
    conn.close()
    return db_items

def extract_ingredients(user_text):
    """Uses spaCy NLP to extract the core nouns from a messy sentence."""
    doc = nlp(user_text)
    extracted_items = []
    
    # We look at 'noun chunks' (e.g., "some fresh milk", "two eggs")
    for chunk in doc.noun_chunks:
        # Ignore pronouns like "I", "We", "It" (e.g., "I need milk" -> skip "I")
        if chunk.root.pos_ != "PRON":
            extracted_items.append(chunk.text.lower())
            
    return extracted_items

def match_items_to_db(extracted_items, db_items):
    """Fuzzy matches the user's messy text to our clean database items."""
    shopping_list = []
    
    for item in extracted_items:
        # extractOne finds the closest match in the database list
        # It returns a tuple: (Best Match String, Confidence Score, Index)
        best_match = process.extractOne(item, db_items)
        
        # If the AI is more than 50% confident it's a match, we accept it
        if best_match and best_match[1] > 50.0:
            matched_product = best_match[0]
            confidence = round(best_match[1], 1)
            print(f"✅ Matched '{item}' ---> {matched_product} (Confidence: {confidence}%)")
            shopping_list.append(matched_product)
        else:
            print(f"❌ Could not find a good match for '{item}' in the database.")
            
    return shopping_list

# --- Testing the Engine ---
if __name__ == '__main__':
    # Grab the clean items from our database
    valid_db_items = get_database_items()
    
    # A messy, real-world user input
    user_input = "I really need to buy some milk, maybe a loaf of bread, and some chicken for dinner."
    print(f"\nUser Input: '{user_input}'\n")
    
    # Step A: Extract the messy items
    messy_items = extract_ingredients(user_input)
    print(f"1. NLP Extracted Concepts: {messy_items}\n")
    
    # Step B: Match them to the database
    print("2. Fuzzy Matching to Database:")
    final_list = match_items_to_db(messy_items, valid_db_items)