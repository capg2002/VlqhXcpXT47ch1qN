import torch

from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from torchvision.models import resnet18, ResNet18_Weights

weights = 

image = Image.open("images/testing/flip/0002_000000012.jpg").convert("RGB")

transform = T.Compose([
    T.Resize((224,224)),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225])
])

tensor = transform(image)

input_tensor = tensor.unsqueeze(0)