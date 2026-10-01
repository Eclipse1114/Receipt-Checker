import cv2
import pytesseract
import numpy as np
import re
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

def parse_item(line):
    # Look for prices at the end of the line
    match = re.search(r"(.+?)\s+\$?(\d+\.\d{2})$", line)

    if match:
        item = match.group(1).strip()
        price = float(match.group(2))
        return item, price

    return None

test_lines = [
    "1 Organic Bananas 0.59 0.59",
    "2 Whole Milk (1 gal) 3.49 6.98",
    "1 Bread (Whole Grain) 2.99 2.99",
    "1 Eggs (12 ct) 3.79 3.79",
    "1 Cheddar Cheese 4.49 4.49",
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
    for line in test_lines:
      result = parse_item(line)

      if result:
        item, price = result
        st.write(item, "→", price, "→", categorize_item(item))
  st.write("All Files Scanned")
