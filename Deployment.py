#LIBRARIES
import streamlit as st
import subprocess
import pickle
import nltk
import pandas as pd
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.stem import  PorterStemmer 
import re
import os
import review_crawler


#LOAD PICKLE FILES
model = pickle.load(open('Models/best_model.pkl','rb')) 
vectorizer = pickle.load(open('Models/count_vectorizer.pkl','rb')) 

#FOR STREAMLIT
nltk.download('stopwords')

#TEXT PREPROCESSING
sw = set(stopwords.words('english'))
def text_preprocessing(review):
    # --TEXT PREPROCESSING--
    txt = TextBlob(review)
    result = txt.correct()
    removed_special_characters = re.sub("[^a-zA-Z]", " ", str(result))
    tokens = removed_special_characters.lower().split()
    stemmer = PorterStemmer()

    cleaned = []
    stemmed = []

    for token in tokens:
        if token not in sw:
            cleaned.append(token)
            
    for token in cleaned:
        token = stemmer.stem(token)
        stemmed.append(token)

    return " ".join(stemmed)

#TEXT CLASSIFICATION
def text_classification(review):
    # review = text_preprocessing(url)
    if len(review) < 1:
        st.write("  ")    
    else:
        with st.spinner("Classification in progress..."):
            cleaned_review = text_preprocessing(review)
            process = vectorizer.transform([cleaned_review]).toarray()
            prediction = model.predict(process)
            p = ''.join(str(i) for i in prediction)
            st.write(review)
        
            if p == 'True':
                st.success("The review entered is Legitimate.")
            if p == 'False':
                st.error("The review entered is Fake.")


#PAGE FORMATTING AND APPLICATION
def main():
    st.title("Fake Review Detection Of E-Commerce Electronic Products Using Machine Learning Techniques")


    #--IMPLEMENTATION OF THE CLASSIFIER--
    st.subheader("Fake Review Classifier")
    url = st.text_area("Enter Url: ")
    if st.button("Check"):
        subprocess.call(f" python review_crawler.py {url} ", shell=True)
        df = pd.read_csv('reviews1.csv')
        reviews = df['body'].to_list()
        while len(reviews) > 0:
            for review in reviews:
                text_classification(review)
                reviews.remove(review)
        


            

#RUN MAIN
main()