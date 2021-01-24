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

labels = [' - 50K', '50K - 70K', '70K - 90K', '90K - 120K', '120K - 150K', '150K - 300K', '300K - 600K']
vector = pickle.load(open('./models/fitted_vectorizer.pkl','rb'))
model =  pickle.load(open('./models/finalized_sgd_model.pkl','rb'))

def salary_predictor_func(text_data, model, vector):
    result = model.predict(vector.transform(text_data))
    return result

def main():
    st.header('Salary Predictor based on Job Description/Summary App')
    st.markdown("Using Machine Learning and NLP techniques we can develop an application that can predict fairly accurate on salary **only using their job postings' descriptions**")
    st.markdown("This algorithm was trained scrapping data from the [Indeed.com website](indeed.com), a well-known website for job hunting. You can take a look at the entire code repo [here](https://github.com/cristobalza/job_nlp_project).")
    st.markdown('#### Instructions')

    st.markdown('- Step 1: Input desired text data - Copy and Paste job description into the text area')
    st.markdown('- Step 2: Press `Predict Salary` button and see how .')

    text = st.text_area('Enter your Text', 'Type here' , height= 800)
    if st.button('Predict Salary'):
        user_input = text
        data = [user_input]
        result = salary_predictor_func(data, model, vector)
        st.subheader(labels[result[0]])

    link = '[cristobalza.com](http://cristobalza.com)'
    st.markdown('Check my website and other projects @ '+link, unsafe_allow_html=True)



if __name__ == "__main__":
    main()
    # temp()