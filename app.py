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

import warnings
warnings.filterwarnings('ignore')

labels = [' Less than 50K',
            'Between 50K and 70K',
            'Between 70K and 90K',
            'Between 90K and 120K',
            'Between 120K and 150K', 
            'Between 150K and 300K', 
            'Between 300K and 600K'
            ]
vector = pickle.load(open('./binary_models/fitted_vectorizer.pkl','rb'))
model =  pickle.load(open('./binary_models/finalized_sgd_model.pkl','rb'))
        
def predict(text):
    user_input = text
    data = [user_input]
    result = salary_predictor_func(data, model, vector)
    return st.subheader(labels[result[0]])

def salary_predictor_func(text_data, model, vector):
    result = model.predict(vector.transform(text_data))
    return result

def input_description(text):
    if st.button('Predict Salary'):
        if len(text) > 50:
            return predict(text) 
        else:
            st.warning("Please use a job description with more than 50 words")
            return st.stop()
def main():
    st.header('Salary Predictor based on Job Description/Summary App')
    st.markdown("Using Machine Learning and NLP techniques we can develop an application that can predict fairly accurate on salary **only using their job postings' descriptions**")
    st.markdown("This algorithm was trained scrapping data from the [Indeed.com website](indeed.com), a well-known website for job hunting. You can take a look at the entire code repo [here](https://github.com/cristobalza/job_nlp_project).")
    link = '[cristobalza.com](http://cristobalza.com)'
    st.markdown('Check my website for more Machine Learning Projects @ '+link, unsafe_allow_html=True)
    st.markdown('#### Instructions')

    st.markdown('- Step 1: Press the checkbox and input desired text data - Copy and Paste job description into the text area. Job description must be at least 50 words long.')
    st.markdown('- Step 2: Press `Predict Salary` button and see how much your job description will be measure by the salary.')
    st.markdown('- Step 3: If you desire a new prediction, press the checkbox and repeat Step 1.')

    agree = st.checkbox('Press this checkbox to load and reload the text field')
    if agree:
        input_description(st.text_area('Enter your Text', 'Type here' , height= 400))


        


if __name__ == "__main__":
    main()