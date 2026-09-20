"""
process_file.py — Part 2: one file of package descriptions, uploaded.

A Streamlit app that accepts an uploaded text file with one package description
per line, shows the total for every line, and writes the parsed packages to a
JSON file in the `data/` folder — `data/packaging1.txt` in, `data/packaging1.json`
out.

New here: an uploaded file arrives as **bytes**, not text, so it has to be
decoded before it can be split into lines. And a text file usually ends with a
newline, so the last "line" is empty and must be skipped rather than parsed.

Run it:  Run and Debug -> "Streamlit Run: Current File"   (see README Reference #1)
Test it: pytest tests/test_streamlit.py -k process_file
"""

# --- The page ---------------------------------------------------------------------
#
# Less scaffolding this time. The steps are described, but which widget and which
# function does each job — and what to call the result — is now yours to work out.
# `one_package.py` is your worked example for anything structural, and README
# Reference #4 and #5 cover the two things that are new here.

import streamlit as st
from packaging_parser import calc_total_units, get_unit, parse_packaging
import json

st.title("Process File of Packages")

uploaded_file = st.file_uploader("Upload a text file of package data:", key="package_file")

if uploaded_file is not None:
    # Read bytes from the file
    bytes_data = uploaded_file.read()
    # Decode bytes to a string using UTF-8 encoding
    text = bytes_data.decode('utf-8')

    data = []
    for line in text.splitlines():
        stripped_line = line.strip()
        if stripped_line:
            package = parse_packaging(stripped_line)
            total = calc_total_units(package)
            unit = get_unit(package)
            data.append((stripped_line, total, unit))
            st.info(f"{stripped_line} ➡️ Total 📦 Size: {total} {unit}")

    original_name = uploaded_file.name  
    json_name = original_name.replace('.txt', '.json')
    save_path = f'data/{json_name}'
    with open(save_path, 'w') as json_file:
        json.dump(data, json_file)

    st.write(f' {len(data)} packages written to {save_path}')