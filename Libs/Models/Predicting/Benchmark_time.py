from keras.models import load_model


# Load the model from a custom folder path
model_path = r"C:\Users\Jon\Documents\UNI\Thesis\code\Libs\Models\Trained_models\230817_resnet50"
loaded_model = load_model(model_path)
loaded_model.summary()