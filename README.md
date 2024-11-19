## ABA Framework Generator and Relation Based Argumentation Classification Model

### ABA Generator
This repository contains the code in regards to the the creation of an online application for an ABA Generator using Object Oriented Programming with all functionnalities in regards to :
- Definition of literals and creation of the basic ABA framework
- Conversion to non-circular and atomic ABA framework
- Creation of arguments and attacks
- Handling of preferences to compute normal and reverse attacks

We built a UI using streamlit with documentation on how to use the generator which we deployed on [Render](https://aba-generator-yyux.onrender.com)

![Image](https://i.ibb.co/fGjgy4Q/image.png)

### Relation Based Argumentation Classification
We build a dataset of arguments with the corresponding attack or support relatiosn by scrapping data from Kialo.<br/>
After building the dataset we thus proceeded to implement an approach that would enable us to perform binary classification on pairs of textual arguments. To do so we tested four approaches based on those shown during the lecture and approaches to text classification in literature regarding Natural Language Processing such as:
- A classical approach using featurizers like TF-IDF and CountVectorizer followed by classification using Logistic Regression

![Results](https://i.ibb.co/WvSwttB/image.png)

- An approach using reccurent neural network in particular with LSTM

![Results](https://i.ibb.co/DfNv87p/image.png)

- Using transformers models such as BERT and GPT

![Results](https://i.ibb.co/ZBVJTVR/image.png)

- Fine tuning a LLaMa3.1-8b model for argument classification

![Results](https://i.ibb.co/vYMYcZ3/image.png)

We also studied how our model performances in regards to identifying indirect relations between arguments