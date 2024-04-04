import streamlit as st
import pandas as pd
import numpy as np
import hmac
from itertools import *
st.title("Merging multiple Sheets in a Excel File")

def combinations_sheets(list_of_sheets):
    combo_sheets=[]
    for i in range(2,len(list_of_sheets)+1):
        res=list(combinations(list_of_sheets,i))
        combo_sheets.extend(res)
    return combo_sheets

def excel_data(path,sheetslist):
    cols=pd.read_excel(path,sheetslist[0]).columns
    merge_dataframe=pd.DataFrame(columns=cols)
    for i in sheetslist:
        read_data=pd.read_excel(path,i)
        for index,rows in read_data.iterrows():
            merge_dataframe.loc[merge_dataframe.shape[0]]=rows.to_dict()
    return merge_dataframe

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()


uploaded_file=st.sidebar.file_uploader("Upload your Excel File",type=['csv','xlsx'])
if uploaded_file is not None:
    read_file=pd.ExcelFile(uploaded_file,engine='openpyxl')
    number_of_sheets=read_file.sheet_names
    st.write("File Uploaded Succesfully")
    combo_selector=st.sidebar.selectbox("Select sheets to merge",options=combinations_sheets(number_of_sheets))
    if combo_selector in combinations_sheets(number_of_sheets):
        resultant_dataframe=excel_data(uploaded_file,combo_selector).drop_duplicates(keep='first')
        st.write(resultant_dataframe)

        
