import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC

model = make_pipeline(TfidfVectorizer(), SVC(probability=True))

test_data = [
    "phone",
    "computer",
    "banana",
    "Ford",
    "orange",
    "dog",
    "tea",
    "bacon"
]

answers = [
    "technology",
    "technology",
    "groceries",
    "cars",
    "groceries",
    "animals",
    "groceries",
    "groceries"
]

model.fit(test_data, answers)

for item in test_data:
    guess = model.predict([item])[0]
    st.write(f"{item} = {guess}")
