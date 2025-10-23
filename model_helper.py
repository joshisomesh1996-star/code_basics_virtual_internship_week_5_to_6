import torch
from torch import nn
from torchvision import models, transforms
from PIL import Image

# Class labels
class_names = [
    'F_Banana', 'F_Lemon', 'F_Lulo', 'F_Mango',
    'F_Orange', 'F_Strawberry', 'F_Tamarillo', 'F_Tomato',
    'S_Banana', 'S_Lemon', 'S_Lulo', 'S_Mango',
    'S_Orange', 'S_Strawberry', 'S_Tamarillo', 'S_Tomato'
]

trained_model = None


# Define model architecture
class HarvestClassifierResNet(nn.Module):
    def __init__(self, num_classes=16, dropout_rate=0.5):
        super().__init__()
        self.model = models.resnet50(weights='DEFAULT')
        # Freeze all layers
        for param in self.model.parameters():
            param.requires_grad = False
        # Unfreeze final ResNet block for fine-tuning
        for param in self.model.layer4.parameters():
            param.requires_grad = True
        # Replace final fully connected layer
        self.model.fc = nn.Sequential(
            nn.Dropout(dropout_rate),
            nn.Linear(self.model.fc.in_features, num_classes)
        )

    def forward(self, x):
        return self.model(x)


def predict(image_path):
    """Run prediction on a single image and return freshness + fruit type."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    image = Image.open(image_path).convert("RGB")

    # Data preprocessing
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225]),
    ])

    image_tensor = transform(image).unsqueeze(0).to(device)

    global trained_model
    if trained_model is None:
        trained_model = HarvestClassifierResNet(num_classes=len(class_names))
        trained_model.load_state_dict(torch.load("model/saved_model.pth", map_location=device))
        trained_model.to(device)
        trained_model.eval()

    with torch.no_grad():
        outputs = trained_model(image_tensor)
        _, predicted_idx = torch.max(outputs, 1)
        label = class_names[predicted_idx.item()]

    # 🌿 Determine freshness and fruit name
    freshness = "Fresh" if label.startswith("F_") else "Spoiled"
    fruit_name = label.split("_")[1] if "_" in label else label

    return f"{fruit_name} ({freshness})"
