import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, Dropout, Bidirectional, Concatenate
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.regularizers import l2
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt

# Charger les données
data = pd.read_csv('combined_arguments.csv', sep=',')

# Vérifier les colonnes et les premières lignes
print("Colonnes du DataFrame:")
print(data.columns)
print("\nPremières lignes du DataFrame:")
print(data.head())

# Paramètres
max_words = 10000
max_len = 100
embedding_dim = 100
batch_size = 128

# Vérifier le contenu des colonnes Argument1 et Argument2
print("\nExemple d'Argument1:")
print(data['Argument1'].iloc[0])
print("\nExemple d'Argument2:")
print(data['Argument2'].iloc[0])

# Créer le tokenizer
tokenizer = Tokenizer(num_words=max_words)
all_texts = data['Argument1'].tolist() + data['Argument2'].tolist()
tokenizer.fit_on_texts(all_texts)

# Tokeniser les arguments
arg1_seq = tokenizer.texts_to_sequences(data['Argument1'])
arg2_seq = tokenizer.texts_to_sequences(data['Argument2'])

print("\nExemple de séquence tokenisée pour Argument1:")
print(arg1_seq[0])
print("\nExemple de séquence tokenisée pour Argument2:")
print(arg2_seq[0])

# Padding
arg1_pad = pad_sequences(arg1_seq, maxlen=max_len, padding='post')
arg2_pad = pad_sequences(arg2_seq, maxlen=max_len, padding='post')

print("\nForme de arg1_pad:", arg1_pad.shape)
print("Forme de arg2_pad:", arg2_pad.shape)

# Encoder les labels
labels = [1 if r == 'Support' else 0 for r in data['Relation']]

print("\nExemple de labels:")
print(labels[:10])

# Diviser les données
X1_train, X1_test, X2_train, X2_test, y_train, y_test = train_test_split(
    arg1_pad, arg2_pad, labels, test_size=0.2, random_state=42)
X1_train = np.array(X1_train, dtype=np.float32)
X2_train = np.array(X2_train, dtype=np.float32)
y_train = np.array(y_train, dtype=np.float32)

print("\nForme de X1_train:", X1_train.shape)
print("Forme de X2_train:", X2_train.shape)
print("Forme de y_train:", len(y_train))

input_1 = Input(shape=(max_len,))
input_2 = Input(shape=(max_len,))

embedding = Embedding(max_words, embedding_dim)
x1 = embedding(input_1)
x2 = embedding(input_2)

lstm = Bidirectional(LSTM(16, return_sequences=True, kernel_regularizer=l2(0.01)))
x1 = lstm(x1)
x2 = lstm(x2)
x1 = Dropout(0.3)(x1)  # Ajout de dropout
x2 = Dropout(0.3)(x2)  # Ajout de dropout

lstm2 = Bidirectional(LSTM(8, kernel_regularizer=l2(0.01))) 
x1 = lstm2(x1)
x2 = lstm2(x2)
x1 = Dropout(0.3)(x1)  # Ajout de dropout
x2 = Dropout(0.3)(x2)  # Ajout de dropout

x = Concatenate()([x1, x2])
x = Dense(32, activation='relu', kernel_regularizer=l2(0.01))(x)  
x = Dropout(0.5)(x)
output = Dense(1, activation='sigmoid')(x)

model = Model(inputs=[input_1, input_2], outputs=output)

# Compiler le modèle
model.compile(optimizer=Adam(learning_rate=0.0005), loss='binary_crossentropy', metrics=['accuracy'])

# Callbacks
checkpoint = ModelCheckpoint('best_model.h5', monitor='val_accuracy', save_best_only=True, mode='max', verbose=1)
early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True) 

# Entraîner le modèle
history = model.fit(
    [X1_train, X2_train], y_train,
    batch_size=256,  
    epochs=50,  
    validation_split=0.2,
    callbacks=[checkpoint, early_stopping]
)
# Charger le meilleur modèle
model = tf.keras.models.load_model('best_model.h5')

# Évaluer le modèle
y_pred = model.predict([X1_test, X2_test])
y_pred_classes = (y_pred > 0.5).astype(int)
print("\nRapport de classification:")
print(classification_report(y_test, y_pred_classes))

# Créer des figures pour accuracy et loss et les enregistrer sans afficher
plt.figure(figsize=(12, 5))

# Graphique de l'accuracy
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

# Graphique de la loss
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.savefig('training_historyLSTM.png')
print("\nGraphique d'historique d'entraînement sauvegardé dans 'training_history.png'")

# Fonction pour faire des prédictions sur de nouvelles paires d'arguments
def predict_relation(arg1, arg2):
    arg1_seq = tokenizer.texts_to_sequences([arg1])
    arg2_seq = tokenizer.texts_to_sequences([arg2])
    arg1_pad = pad_sequences(arg1_seq, maxlen=max_len, padding='post')
    arg2_pad = pad_sequences(arg2_seq, maxlen=max_len, padding='post')
    prediction = model.predict([arg1_pad, arg2_pad])[0][0]
    return "Support" if prediction > 0.5 else "Attack"

