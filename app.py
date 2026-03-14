import streamlit as st
import sqlite3
import pandas as pd
from nlp_engine import extract_ingredients, get_database_items, match_items_to_db

# --- Page Setup ---
st.set_page_config(page_title="Smart Grocery Basket", page_icon="🛒", layout="centered")

def get_prices_for_basket(matched_items):
    """Queries the database to find the price of our matched items at every supermarket."""
    if not matched_items:
        return pd.DataFrame()
        
    conn = sqlite3.connect('groceries.db')
    
    # Create a SQL query that asks for the prices of only the items in our basket
    placeholders = ', '.join(['?'] * len(matched_items))
    query = f"""
        SELECT item_name, supermarket, price 
        FROM products 
        WHERE item_name IN ({placeholders})
    """
    
    # Load the results into a Pandas DataFrame for easy math
    df = pd.read_sql_query(query, conn, params=matched_items)
    conn.close()
    return df

# --- UI Design ---
st.title("🛒 Smart Grocery Optimizer")
st.markdown("""
Type your messy, natural-language grocery list below. 
Our NLP engine will extract the items, match them to real products, and find the cheapest supermarket for your basket!
""")

# The text box where the user types
user_input = st.text_area("What do you need to buy?", value="I need some milk, a loaf of bread, and chicken for dinner.", height=100)

if st.button("Optimize My Basket", type="primary"):
    with st.spinner("Analyzing text and crunching prices..."):
        
        # 1. Run the NLP Engine (from your nlp_engine.py file)
        db_items = get_database_items()
        messy_items = extract_ingredients(user_input)
        final_basket = match_items_to_db(messy_items, db_items)
        
        # Remove duplicates just in case
        final_basket = list(set(final_basket)) 
        
        if not final_basket:
            st.warning("Could not find any matching grocery items in your text. Try being more specific!")
        else:
            st.success(f"Successfully extracted {len(final_basket)} items from your text!")
            
            # 2. Get the Prices
            price_df = get_prices_for_basket(final_basket)
            
            # Group the prices by supermarket and calculate the total basket cost
            totals = price_df.groupby('supermarket')['price'].sum().reset_index()
            totals = totals.sort_values(by='price', ascending=True) # Sort cheapest to most expensive
            
            # 3. Display the Winner
            cheapest_store = totals.iloc[0]['supermarket']
            cheapest_price = totals.iloc[0]['price']
            
            st.subheader(f"🏆 Cheapest Option: {cheapest_store}")
            st.markdown(f"**Total Basket Cost: £{cheapest_price:.2f}**")
            
            st.divider()
            
            # 4. Show the detailed breakdown
            st.subheader("Price Breakdown by Supermarket")
            
            # We use Streamlit columns to show the stores side-by-side
            cols = st.columns(len(totals))
            
            for index, row in totals.iterrows():
                store = row['supermarket']
                total = row['price']
                
                # Get the specific items for this store
                store_items = price_df[price_df['supermarket'] == store]
                
                with cols[index]:
                    st.markdown(f"### {store}")
                    st.markdown(f"**Total: £{total:.2f}**")
                    for _, item_row in store_items.iterrows():
                        st.write(f"- {item_row['item_name']}: £{item_row['price']:.2f}")