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

x = 0
total = len(files)

for file in files:
  st.write(f"{x} of {total} scanned.")
  img = cv2.imread(
    np.frombuffer(file.getvalue(), np.uint8),
    cv2.IMREAD_COLOR
  )
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  x += 1
  _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
  text = pytesseract.image_to_string(thresh)
  st.write(text)
