import cv2
import pytesseract
import numpy as np
import streamlit as st
import re

# -----------------------------
# Categories
# -----------------------------

categories = {
    "Dairy": ["milk", "cheese", "yogurt", "butter", "cream", "egg"],
    "Produce": ["apple", "banana", "lettuce", "tomato", "potato"],
    "Bakery": ["bread", "bagel", "muffin", "donut"],
    "Meat": ["chicken", "beef", "pork", "turkey", "steak"],
    "Beverages": ["water", "juice", "soda", "coffee", "tea"],
    "Snacks": ["chips", "cookie", "cracker", "candy"],
}


# -----------------------------
# Categorize an item
# -----------------------------

def categorize_item(item):
    item = item.lower()

    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in item:
                return category

    return "Other"


# -----------------------------
# Parse an OCR line
# -----------------------------

def parse_item(line):
    # Find all prices in the line
    prices = re.findall(r"\$?\d+\.\d{2}", line)

    # If there aren't any prices, this probably isn't an item
    if not prices:
        return None

    # The last price should be the item's total
    price = float(prices[-1].replace("$", ""))

    # Remove the prices from the line
    item = re.sub(r"\$?\d+\.\d{2}", "", line).strip()

    # Remove the quantity at the beginning
    item = re.sub(r"^\d+\s+", "", item)

    # Make sure something is left
    if not item:
        return None

    return item, price


# -----------------------------
# Streamlit UI
# -----------------------------

st.title("Receipt Checker")

files = st.file_uploader(
    "Upload Receipt",
    type=[
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".bmp",
        ".tiff"
    ],
    accept_multiple_files=True
)

submit = st.button("Start Extraction")


# -----------------------------
# Process receipts
# -----------------------------

if submit:

    total = 1

    if total == 0:
        st.warning("Please upload at least one receipt.")

    else:

        for x, file in enumerate(files, start=1):

            st.write(f"{x} of {total} scanned.")

            # Read uploaded image
            img = cv2.imdecode(
                np.frombuffer(file.getvalue(), np.uint8),
                cv2.IMREAD_COLOR
            )

            # Convert to grayscale
            gray = cv2.cvtColor(
                img,
                cv2.COLOR_BGR2GRAY
            )

            # Threshold image
            _, thresh = cv2.threshold(
                gray,
                150,
                255,
                cv2.THRESH_BINARY
            )

            # OCR
            text = pytesseract.image_to_string(thresh)

            st.subheader(file.name)

            # Store category totals for this receipt
            category_totals = {}

            # Process each OCR line
            lines = text.splitlines()

            for line in lines:

                result = parse_item(line)

                if result:

                    item, price = result

                    category = categorize_item(item)

                    # Add price to category
                    if category not in category_totals:
                        category_totals[category] = 0

                    category_totals[category] += price

                    # Show what the program found
                    st.write(
                        f"{item} → ${price:.2f} → {category}"
                    )

            # -----------------------------
            # Category totals
            # -----------------------------

            st.write("### Category Totals")

            for category, amount in category_totals.items():
                st.write(
                    f"**{category}:** ${amount:.2f}"
                )

        st.write("All Files Scanned")
