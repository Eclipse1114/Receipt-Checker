import cv2
import pytesseract
import numpy as np
import streamlit as st

st.title("Receipt Checker")
files = st.file_uploader("Upload Receipt", type=[
  ".jpg",
  ".jpeg",
  ".png",
  ".webp",
  ".bmp",
  ".tiff"
], accept_multiple_files=True)

submit = st.button("Start Extraction")

x = 0
categories = {
    "Dairy": ["milk", "cheese", "yogurt", "butter", "cream"],
    "Produce": ["apple", "banana", "lettuce", "tomato", "potato"],
    "Bakery": ["bread", "bagel", "muffin", "donut"],
    "Meat": ["chicken", "beef", "pork", "turkey", "steak"],
    "Beverages": ["water", "juice", "soda", "coffee", "tea"],
    "Snacks": ["chips", "cookie", "cracker", "candy"],
}

def categorize_item(item):
    item = item.lower()

    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in item:
                return category

    return "Other"

test_items = [
    "Organic Bananas",
    "Whole Milk (1 gal)",
    "Bread (Whole Grain)",
    "Eggs (12 ct)",
    "Cheddar Cheese",
    "Lettuce (Head)",
    "Apples (Honeycrisp)"
]

total = len(files)

if submit:
  for file in files:
    st.write(f"{x} of {total} scanned.")
    img = cv2.imdecode(
      np.frombuffer(file.getvalue(), np.uint8),
      cv2.IMREAD_COLOR
    )
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    x += 1
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(thresh)
    st.write(text)
  for item in test_items:
    st.write(item, "→", categorize_item(item))
  st.write("All Files Scanned")
