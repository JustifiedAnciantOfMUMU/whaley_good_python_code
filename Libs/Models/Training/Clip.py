import torch
from transformers import CLIPProcessor, CLIPModel, CLIPTextClassificationHead
from PIL import Image
import os

# Data directory containing your images
train_dir = "/path/to/your/image/directory"

device = "cuda" if torch.cuda.is_available() else "cpu"

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch16").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16").to(device)

# Define a function to determine the class based on the last digit
def classify_by_last_digit(filename):
    last_digit = int(filename[-5])  # Assuming the filename format is "image_#.jpg"
    if last_digit == 1:
        return 'positive'
    else:
        return 'negative'

# Load pre-trained CLIP model and processor
device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch16").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16").to(device)

# Define two class descriptions corresponding to "positive" and "negative" classes
class_descriptions = ["An image with an even last digit.", "An image with an odd last digit."]

# Create a binary classification head for CLIP
classification_head = CLIPTextClassificationHead(512, num_labels=2).to(device)

# Define optimizer and training loop
optimizer = torch.optim.Adam(classification_head.parameters(), lr=1e-5)

# List all image files in the directory
image_files = [f for f in os.listdir(train_dir) if f.endswith(".jpg")]

# Perform classification for each image based on last digit
for image_file in image_files:
    image_path = os.path.join(train_dir, image_file)
    image = Image.open(image_path)

    # Determine the class based on the last digit of the file name
    class_label = classify_by_last_digit(image_file)

    # Preprocess the image and text description
    inputs = processor(text=class_descriptions, images=image, return_tensors="pt", padding=True)

    # Move inputs to the appropriate device
    inputs = {key: val.to(device) for key, val in inputs.items()}

    # Perform Classification
    with torch.no_grad():
        outputs = model(**inputs)

    logits_per_image = outputs.logits_per_image
    logits_per_text = outputs.logits_per_text
    loss = classification_head(logits_per_image, logits_per_text, torch.tensor([0 if class_label == "positive" else 1]).to(device))

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()