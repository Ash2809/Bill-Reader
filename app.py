import google.generativeai as genai
from PIL import Image
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro-vision")

def get_response(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response


def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{'mime_type':uploaded_file.type,"data":bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")
    

st.set_page_config("INVOICE READER")
st.header("MULTILINGUAL INVOICE READER")

uploaded_file = st.file_uploader('UPLOAD AN IMAGE', type = ["jpg","jpeg","png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image = image,caption = "Uploaded invoice is: ")


input = st.text_input("prompt",key = "input")

prompt = """You are a expert in understanding Invoices and you will be provided a Invoice image
you have to answer any questions based on the invoice image and translate the answer in english"""


submit = st.button("Submit")

if submit:
    image_data = input_image_details(uploaded_file)
    response = get_response(input,image_data,input)
    st.subheader("The answer is: ")
    st.write(response.text)

