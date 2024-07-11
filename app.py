from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai 

genai.configure(api_key = os.environ.get('GOOGLE_API_KEY'))

#func to load genimi pro vision
model = genai.GenerativeModel('gemini-pro-vision')

def gemini_get_response(input, image, prompt):
    response = model.generate_content([input, image[0],prompt]) #in gemini it takes parameters in list
    return response.text


def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{'mime_type':uploaded_file.type,"data":bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")


st.set_page_config(page_title= 'MultiLangugae Invoice Extractor')
st.header('Gemini App')
input = st.text_input('Input Prompt', key='input')
uploaded_file = st.file_uploader('Choose an image of invoice...', type = ["jpg","jpeg","png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption = 'Uploaded Image.', use_column_width=True)
submit = st.button("Tell me about the invouce")

input_prompt = """
You are expert in understanding invoices. We will uplaod an image as invoices and you have to answer any questions based on uploaded invoice image
"""
#if submit button is clicked
if submit:
    image_data = input_image_details(uploaded_file)
    response = gemini_get_response(input_prompt,image_data,input)
    st.subheader('The Response is')
    st.write(response )



