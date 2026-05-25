🛡️ SMS Spam Classifier
An AI-powered SMS spam detection web app built with Streamlit, scikit-learn, and NLTK. Paste any SMS message and instantly know whether it's spam or safe — with confidence scores.

📸 Demo

Paste a message → Click Analyze Message → Get instant spam/ham verdict with confidence percentage.

🌐 Live Demo

GitHub Repository: https://github.com/kajal9873/Image-Caption-Generator

Deploy on Streamlit Cloud: https://sms-spam-classifier-6gdd2kkgaud6jvzrqyqghz.streamlit.app/

🚀 Features

🔍 Real-time spam detection using a trained Naive Bayes model
📊 Confidence score for both spam and legitimate (ham) predictions
🧹 Full NLP preprocessing pipeline (lowercasing, tokenization, stopword removal, stemming)
📈 Message stats — word count and character count
🎨 Sleek dark-themed UI with smooth animations


🧠 How It Works

Input: User pastes an SMS message into the text box
Preprocessing:

Convert to lowercase
Tokenize using NLTK
Remove stopwords and punctuation
Apply Porter Stemming


Vectorization: TF-IDF vectorizer transforms the cleaned text into numerical features
Prediction: Multinomial Naive Bayes model predicts spam (1) or ham (0)
Output: Result displayed with confidence scores and message statistics


📁 Project Structure
sms-spam-classifier/
├── app.py               # Streamlit web application
├── model.pkl            # Trained Multinomial Naive Bayes model
├── vectorizer.pkl       # Fitted TF-IDF vectorizer
├── spam.csv             # Dataset (5,572 SMS messages)
└── sms-spam-detection.ipynb  # Training notebook (EDA + model building)

📊 Dataset
LabelCountHam (legitimate)4,825Spam747Total5,572
Source: UCI SMS Spam Collection Dataset

🛠️ Tech Stack
ComponentLibrary / ToolWeb AppStreamlitML Modelscikit-learn (MultinomialNB)VectorizerTF-IDF (scikit-learn)NLPNLTK (tokenization, stopwords, stemming)DatapandasLanguagePython 3

⚙️ Installation & Setup
1. Clone the repository
bashgit clone https://github.com/your-username/sms-spam-classifier.git
cd sms-spam-classifier
2. Install dependencies
bashpip install streamlit scikit-learn nltk pandas
3. Download NLTK data (auto-handled by the app, but you can do it manually)
pythonimport nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
4. Run the app
bashstreamlit run app.py
The app will open at http://localhost:8501

🧪 Try It Out
Paste messages like these to test:
Spam example:
Congratulations! You've won a FREE iPhone. Click now to claim your prize!
Ham example:
Hey, are you coming to dinner tonight?

📓 Training Notebook
The sms-spam-detection.ipynb notebook covers:

Exploratory Data Analysis (EDA)
Text preprocessing pipeline
TF-IDF vectorization
Model training and evaluation
Saving the model and vectorizer as .pkl files


📄 License
This project is open source and available under the MIT License.

🙌 Acknowledgements

UCI Machine Learning Repository — for the SMS Spam Collection dataset
NLTK — for natural language processing tools
Streamlit — for the easy-to-build web app framework
