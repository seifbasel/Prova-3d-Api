# import joblib
# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.stem import SnowballStemmer
# nltk.download('punkt')
# nltk.download('stopwords')

# # Preprocessing function
# def preprocess_text(text):
#     if isinstance(text, str):
#         text = text.lower()
#         tokens = word_tokenize(text)
#         stop_words = set(stopwords.words('english'))
#         filtered_tokens = [word for word in tokens if word not in stop_words]
#         stemmer = SnowballStemmer(language='english')
#         stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]
#         processed_text = ' '.join(stemmed_tokens)
#         return processed_text
#     else:
#         return ""

# # Load the trained SVM model and TF-IDF vectorizer
# svm_model = joblib.load('back_api/sentement_models/svm_model.pkl')
# tfidf_vectorizer = joblib.load('back_api/sentement_models/tfidf_vectorizer.pkl')

# # Function to predict sentiment of input text
# def predict_sentiment(text):
#     # Preprocess the input text
#     processed_text = preprocess_text(text)
#     # Transform the text using the trained TF-IDF vectorizer
#     text_tfidf = tfidf_vectorizer.transform([processed_text])
#     # Predict the sentiment using the trained SVM model
#     prediction = svm_model.predict(text_tfidf)
#     return 1 if prediction[0] == 1 else 0  # 1 for Positive, 0 for Negative


# import nltk

# # Define the directory to download the NLTK data
# nltk_data_dir = 'virtual_fitting_env/virtual_fitting_project/back_api/nltk_data'

# # Ensure the directory exists
# import os
# os.makedirs(nltk_data_dir, exist_ok=True)

# # Download the necessary NLTK data
# nltk.download('punkt', download_dir=nltk_data_dir)
# nltk.download('stopwords', download_dir=nltk_data_dir)


import joblib
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer

# Set the NLTK data path to the pre-downloaded directory
nltk.data.path.append('virtual_fitting_env/virtual_fitting_project/back_api/nltk_data')

# Preprocessing function
def preprocess_text(text):
    if isinstance(text, str):
        text = text.lower()
        tokens = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word not in stop_words]
        stemmer = SnowballStemmer(language='english')
        stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]
        processed_text = ' '.join(stemmed_tokens)
        return processed_text
    else:
        return ""

# Load the trained SVM model and TF-IDF vectorizer
svm_model = joblib.load('back_api/sentement_models/svm_model.pkl')
tfidf_vectorizer = joblib.load('back_api/sentement_models/tfidf_vectorizer.pkl')

# Function to predict sentiment of input text
def predict_sentiment(text):
    # Preprocess the input text
    processed_text = preprocess_text(text)
    # Transform the text using the trained TF-IDF vectorizer
    text_tfidf = tfidf_vectorizer.transform([processed_text])
    # Predict the sentiment using the trained SVM model
    prediction = svm_model.predict(text_tfidf)
    return 1 if prediction[0] == 1 else 0  # 1 for Positive, 0 for Negative
