import streamlit as st
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.style as style
style.use('fivethirtyeight')
import seaborn as sns
import time
from joblib import dump, load
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier





labels = ['0 - 50K', '50K - 70K', '70K - 90K', '90K - 120K', '120K - 150K', '150K - 300K', '300K - 600K']
vector = pickle.load(open('./models/fitted_vectorizer.pkl','rb'))
model =  pickle.load(open('./models/finalized_sgd_model.pkl','rb'))

def salary_predictor():
	description = request.form.get('description')
	result = model.predict(tfidf_vectorizer.transform([description]))

st.markdown('#### Instructions')

st.markdown('- Step 1: Input desired text data')
st.markdown('- Step 2: Press `Predict` button and see how toxic was your text.')

text = st.text_area('Enter your Text', 'Type here' )
if st.button('Predict Salary'):
    user_input = text
    data = [user_input]


    result = model.predict(vector)

    st.text(result)