import streamlit as st
import pandas as pd
import json
import sys
import os

# Load preselected words from a JSON file passed as a command-line argument

with open("./data/synonyms_to_check.json", "r") as f:
    preselected_words = json.load(f)
# Extract categories dynamically from the dictionary keys
categories = list(preselected_words.keys())

# Function to handle categorization
def categorize_words():
    # Create dictionary with preselected words for each category
    categorized = {cat: preselected_words[cat].copy() for cat in categories}

    # Create a list to hold words that are removed from categories
    available_words = []

    # Create checkboxes for each word
    st.subheader("Validation des synonymes :")

    # Create a multi-select for each category
    for cat in categories:
        # Allow user to modify the preselected words
        selected_words = st.multiselect(
            f"Sélectionner/Désélectionner les synonymes pour: {cat}",
            preselected_words[cat],
            default=categorized[cat],
            key=cat
        )
        categorized[cat] = selected_words

        # Find words that were removed from the category
        removed_from_category = [word for word in preselected_words[cat] if word not in selected_words]
        available_words.extend(removed_from_category)
        
         # Allow user to modify the preselected words
        selected_words_2 = st.text_area(
            f"Ajouter des synonymes pour: {cat} (séparez-les par des virgules)",
            #value=", ",
            key=f"add_{cat}"
        )
        
        # Split the input by commas to get the words
        manual_terms = [word.strip() for word in selected_words_2.split(",") if len(word) > 1]
        categorized[cat].extend(manual_terms)

    # Remove duplicates from available words
    available_words = list(set(available_words))

    # Display the list of available words that can be added back
    
   # for cat in categories:
     #   add_back_words = st.multiselect(
      #      f"Ajouter des mots à: {cat}",
    #        available_words,
    #        key=f"add_{cat}"
     #   )
    #    categorized[cat].extend(add_back_words)
        # Remove added words from the available list
    #    available_words = [word for word in available_words if word not in add_back_words]

    return categorized

# Export functionality
def export_results(categorized):
    # Option to download the result
    st.subheader("Exporter les résultats")

    export_option = st.radio("Choisir le format d'export:", ["JSON", "CSV"])

    if export_option == "JSON":
        # Export as JSON
        json_data = json.dumps(categorized, indent=2)
        st.download_button(
            label="Télécharger les résultats (JSON)",
            data=json_data,
            file_name="categorized_words.json",
            mime="application/json"
        )
    elif export_option == "CSV":
        # Convert to DataFrame and export as CSV
        df = pd.DataFrame([(cat, word) for cat, words in categorized.items() for word in words], columns=["Category", "Word"])
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="Télécharger les résultats (CSV)",
            data=csv_data,
            file_name="categorized_words.csv",
            mime="text/csv"
        )

# Streamlit app interface
def main():
    st.title("Application de validation de synonymes")

    # Categorize words
    categorized = categorize_words()

    # Display the categorized results
    st.subheader("Résultats de la validation:")
   # st.subheader("Mots disponibles à ajouter:")
    st.write(categorized)

    # Provide export options
    export_results(categorized)

if __name__ == "__main__":
    main()