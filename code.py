import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC

model = make_pipeline(TfidfVectorizer(), SVC(probability=True))

test_data = [
    # Technology
    "phone",
    "computer",
    "tablet",
    "laptop",
    "headphones",
    "keyboard",
    "mouse",

    # Groceries
    "banana",
    "orange",
    "apple",
    "cheese",
    "milk",
    "bread",
    "bacon",
    "tea",

    # Cars
    "Ford",
    "Chevy",
    "Toyota",
    "Honda",
    "Tesla",
    "truck",
    "sedan",

    # Animals
    "dog",
    "cat",
    "bear",
    "lion",
    "tiger",
    "horse",
    "rabbit"
]

answers = [
    # Technology
    "technology", "technology", "technology", "technology",
    "technology", "technology", "technology",

    # Groceries
    "groceries", "groceries", "groceries", "groceries",
    "groceries", "groceries", "groceries", "groceries",

    # Cars
    "cars", "cars", "cars", "cars", "cars", "cars", "cars",

    # Animals
    "animals", "animals", "animals", "animals",
    "animals", "animals", "animals"
]

model.fit(test_data, answers)

items = [
    "iPhone",
    "monitor",
    "grapes",
    "Honda",
    "wolf",
    "butter"
]

for item in items:
    print(item, "=", model.predict([item])[0])

for item in test:
    guess = model.predict([item])[0]
    st.write(f"{item} = {guess}")
