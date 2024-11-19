import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, log_loss, accuracy_score
import matplotlib.pyplot as plt
import joblib

# Charger les données
data = pd.read_csv('combined_arguments.csv', sep=',')

print("Colonnes du DataFrame:")
print(data.columns)
print("\nPremières lignes du DataFrame:")
print(data.head())

# Préparer les données
X = data['Argument1'] + ' ' + data['Argument2']  # Combiner les deux arguments
y = (data['Relation'] == 'Support').astype(int)  # Encoder 'Support' comme 1, 'Attack' comme 0

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectoriser le texte
vectorizer = TfidfVectorizer(max_features=5000)
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# Créer et entraîner le modèle
model = LogisticRegression(random_state=42, max_iter=1000)
model.fit(X_train_vectorized, y_train)

# Évaluer le modèle
y_pred = model.predict(X_test_vectorized)
y_pred_proba = model.predict_proba(X_test_vectorized)

# Calculer loss et accuracy
loss = log_loss(y_test, y_pred_proba)
accuracy = accuracy_score(y_test, y_pred)

print("\nRapport de classification:")
print(classification_report(y_test, y_pred, target_names=['Attack', 'Support']))
print(f"\nLoss: {loss}")
print(f"Accuracy: {accuracy}")

# Afficher la matrice de confusion
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Matrice de confusion')
plt.colorbar()
tick_marks = np.arange(2)
plt.xticks(tick_marks, ['Attack', 'Support'], rotation=45)
plt.yticks(tick_marks, ['Attack', 'Support'])
plt.tight_layout()
plt.ylabel('Vraie classe')
plt.xlabel('Classe prédite')
plt.savefig('confusion_matrix.png')

# Enregistrer le modèle
joblib.dump(model, 'logistic_regression_model.joblib')
joblib.dump(vectorizer, 'tfidf_vectorizer.joblib')

# Enregistrer les métriques
with open('model_metrics.txt', 'w') as f:
    f.write(f"Loss: {loss}\n")
    f.write(f"Accuracy: {accuracy}\n")

# Fonction pour faire des prédictions sur de nouvelles paires d'arguments
def predict_relation(arg1, arg2):
    combined_arg = arg1 + ' ' + arg2
    vectorized_arg = vectorizer.transform([combined_arg])
    prediction = model.predict(vectorized_arg)[0]
    return "Support" if prediction == 1 else "Attack"

# Exemple d'utilisation
print("\nExemple de prédiction:")
print(predict_relation("This policy will reduce crime rates.", "The policy focuses on rehabilitation programs."))

print("\nModèle et métriques enregistrés avec succès.")
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import log_loss, accuracy_score
import matplotlib.pyplot as plt
import joblib

# Charger les données
data = pd.read_csv('combined_arguments.csv', sep=',')

print("Colonnes du DataFrame:")
print(data.columns)
print("\nPremières lignes du DataFrame:")
print(data.head())

# Préparer les données
X = data['Argument1'] + ' ' + data['Argument2']
y = (data['Relation'] == 'Support').astype(int)

# Diviser les données
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectoriser le texte
vectorizer = TfidfVectorizer(max_features=10000)
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# Initialiser le modèle
model = SGDClassifier(loss='log_loss', random_state=42, max_iter=1, tol=None)

# Listes pour stocker les métriques
train_losses = []
val_losses = []
train_accuracies = []
val_accuracies = []

# Entraînement itératif
n_epochs = 100
for epoch in range(n_epochs):
    model.partial_fit(X_train_vectorized, y_train, classes=np.unique(y))
    
    # Calculer les métriques d'entraînement
    train_pred = model.predict(X_train_vectorized)
    train_pred_proba = model.predict_proba(X_train_vectorized)
    train_loss = log_loss(y_train, train_pred_proba)
    train_accuracy = accuracy_score(y_train, train_pred)
    
    # Calculer les métriques de validation
    val_pred = model.predict(X_test_vectorized)
    val_pred_proba = model.predict_proba(X_test_vectorized)
    val_loss = log_loss(y_test, val_pred_proba)
    val_accuracy = accuracy_score(y_test, val_pred)
    
    # Stocker les métriques
    train_losses.append(train_loss)
    val_losses.append(val_loss)
    train_accuracies.append(train_accuracy)
    val_accuracies.append(val_accuracy)

# Créer les graphiques
plt.figure(figsize=(12, 5))

# Graphique de la loss
plt.subplot(1, 2, 1)
plt.plot(train_losses, label='Train Loss')
plt.plot(val_losses, label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

# Graphique de l'accuracy
plt.subplot(1, 2, 2)
plt.plot(train_accuracies, label='Train Accuracy')
plt.plot(val_accuracies, label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.tight_layout()
plt.savefig('trainingLogisticRegression_history.png')
print("Graphiques d'entraînement sauvegardés dans 'training_history.png'")

# Enregistrer le modèle final
joblib.dump(model, 'logistic_regression_model.joblib')
joblib.dump(vectorizer, 'tfidf_vectorizer.joblib')

# Fonction pour faire des prédictions
def predict_relation(arg1, arg2):
    combined_arg = arg1 + ' ' + arg2
    vectorized_arg = vectorizer.transform([combined_arg])
    prediction = model.predict(vectorized_arg)[0]
    return "Support" if prediction == 1 else "Attack"

print("\nModèle enregistré avec succès.")

