from keras.models import Sequential
from keras.layers import Dense, LSTM



model = Sequential()
model.add(Embedding(MAX_WORDS, EMBEDDING_DIM, input_length=X.shape[1]))
model.add(SpatialDropout1D(0.2))
model.add(LSTM(50))
model.add(Dense(32, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(X_train, Y_train, epochs=10, batch_size=50,validation_split=0.1)