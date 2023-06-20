import streamlit as st
import pandas as pd
import pickle
import numpy as np
import base64
import streamlit as st

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp
     {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

st.write('''
<style>
select {
    background-color: #444444;
    color: black;
}
</style>
''', unsafe_allow_html=True)

set_background('book5.jpg')

streamlit_style = """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@100&display=swap');

            html, body, [class*="css"]  {
            font-family: 'Roboto', sans-serif;
            }
            </style>
            """
st.markdown(streamlit_style ,unsafe_allow_html=True)


# Load the pickled model
with open('model_pickel.pkl', 'rb') as f:
    regressor = pickle.load(f)

def encode_input(input_data):
    """Encode input data in ASCII format"""
    return [s.encode('ascii', 'ignore') for s in input_data]

def convert_input(input_data):
    """Convert input data to numerical format"""
    return np.array(input_data).astype(float)

#country = {0:Belgium,1:France,2:Germany,3:Italy,4:Poland,5:Spain}
#store{0 : KaggleMart,1:KaggleRama}
#product = {0:Kaggle Advanced Techniques,1:Kaggle Getting Started,2:Kaggle Recipe Book  ,3:Kaggle for Kids: One Smart Goose}
stores = {'KaggleMart' : '0','KaggleRama' : '1'}
products = {'Kaggle Advanced Techniques' : '0','Kaggle Getting Started' : '1','Kaggle Recipe Book' : '2','Kaggle for Kids: One Smart Goose' : '3'}
countries = {'Belgium' : '0','France' : '1','Germany' : '2','Italy' : '3','Poland' : '4','Sapin' : '5'}
months = {'Janurary' : '1','Feburary' : '2','March' : '3','April' : '4','May' : '5','June' : '6','July' : '7','Agust' : '8','September' : '9','October' : '10','November' : '11','December' : '12'}

def sales_prediction(input_data):
    input_data[0] = countries[input_data[0]]
    input_data[1] = stores[input_data[1]]
    input_data[2] = products[input_data[2]]
    input_data[4] = months[input_data[4]]
    x = np.asarray(encode_input(input_data))
    x = convert_input(x)
    prediction = regressor.predict(x.reshape(1,-1))
    return prediction

def main():
    st.markdown("<h1 style='color:black;font_size : 3rem' border-radius: 10px>𝑩𝑶𝑶𝑲 𝑺𝑨𝑳𝑬𝑺 𝑷𝑹𝑬𝑫𝑰𝑪𝑻𝑰𝑶𝑵</h1>",unsafe_allow_html=True)
    store_options = ['KaggleMart', 'KaggleRama']
    country_options = ['Belgium','France','Germany','Italy','Poland','Spain']
    product_options = ['Kaggle Advanced Techniques','Kaggle Getting Started','Kaggle Recipe Book','Kaggle for Kids: One Smart Goose']
    months_options = ['Janurary','Feburary','March','April','May' ,'June','July','Agust','September','October','November','December']
    # Set the style for the selectbox
    # style = "background-color: #0077b6; color: white; font-weight: bold;"
    css = """
    <style>
    select:hover select:focus{
        background-color: #0077b6;
        color: white;
        font-weight: bold;
        outline: white;
    }
    </style>
    """

    country = st.selectbox('𝘾𝙤𝙪𝙣𝙩𝙧𝙮',country_options)
    store = st.selectbox('𝙎𝙩𝙤𝙧𝙚 ', store_options)
    product = st.selectbox('𝙋𝙧𝙤𝙙𝙪𝙘𝙩', product_options)
    year = st.text_input('𝙔𝙚𝙖𝙧')
    month = st.selectbox('𝙈𝙤𝙣𝙩𝙝', months_options)
    
    # st.write(country)

    pred = ''
    if st.button('Predict'):
        try:
            pred = sales_prediction([country,store,product,year,month])
        except Exception as e:
            print(e)
    # st.success("The Book Sales is {}".format(pred))
    st.markdown(
    f'<p style="background-color:#26282A;color:white;padding:10px; border-radius: 7px">The Book Sales is {pred}</p>',
    unsafe_allow_html=True
)

    

if __name__ == "__main__":
    main()