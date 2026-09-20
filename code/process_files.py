"""
process_files.py — Part 3: many files, one after another, with a running total.

The same job as process_file.py, but the app now remembers what it has already
done: how many files have been processed, how many packages that came to, and a
one-line summary of each file — and it keeps remembering across uploads.

That is the hard part, and it is hard for a specific reason: every interaction
reruns this whole script from the top, so an ordinary variable like
`files_processed = 0` is reset to zero on every rerun. Anything that has to
survive a rerun lives in `st.session_state` instead, and is initialised only
once — the first time the script runs.

The other trap is the uploader itself. Once a file has been chosen it stays
chosen on every rerun, so an app that processes "whenever there is a file" would
count the same file again on every interaction. Processing happens on a button
click instead: `st.button` is True only on the one rerun the click caused.

Run it:  Run and Debug -> "Streamlit Run: Current File"   (see README Reference #1)
Test it: pytest tests/test_streamlit.py -k process_files
"""
import streamlit as st
from packaging_parser import calc_total_units, get_unit, parse_packaging
import json

# Initialise session state
if "files_processed" not in st.session_state:
    st.session_state.files_processed = []
if "packages_processed" not in st.session_state:
    st.session_state.packages_processed = 0
if "file_summaries" not in st.session_state:
    st.session_state.file_summaries = []


st.title("Process File of Packages")

uploaded_file= st.file_uploader("Upload package file:", key="package_file")
button_clicked = st.button("Process File", key="process")

if st.session_state.packages_processed == 0:
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Files processed", len(st.session_state.files_processed))

    with col2:
        st.metric("Packages processed", st.session_state.packages_processed)

if button_clicked and uploaded_file is not None:
    if uploaded_file.name not in st.session_state.files_processed:
        # Read bytes from the file
        bytes_data = uploaded_file.read()
        # Decode bytes to a string using UTF-8 encoding
        text = bytes_data.decode('utf-8')
        st.session_state.files_processed.append(uploaded_file.name)

        package_count = 0
        packages_list = []
        for line in text.splitlines():
            stripped_line = line.strip()
            if stripped_line:
                package = parse_packaging(stripped_line)
                packages_list.append(package)
                total = calc_total_units(package)
                unit = get_unit(package)
                package_count += 1

        original_name = uploaded_file.name  
        json_name = original_name.replace('.txt', '.json')
        save_path = f'data/{json_name}'
        with open(save_path, 'w') as json_file:
            json.dump(packages_list, json_file)

        st.session_state.files_processed.append(uploaded_file.name)
        st.session_state.packages_processed += package_count

        with col1:
            st.metric("Files processed", len(st.session_state.files_processed))

        with col2:
            st.metric("Packages processed", st.session_state.packages_processed)

        st.session_state.file_summaries.append(f"{package_count} packages written to {save_path}")
        for summary in st.session_state.file_summaries:
            st.info(summary)
    else:
        st.info(f"File {uploaded_file.name} already processed.")