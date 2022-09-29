from model import ResNet
from PIL import Image
import torch
import torch.nn.functional as F
import torchvision.transforms.functional as TF
import boto3

IMG_EXTENSIONS = [
    '.jpg', '.JPG', '.jpeg', '.JPEG',
    '.png', '.PNG', '.ppm', '.PPM', '.bmp', '.BMP']

def import_model(bucket, key, filename="model.pth"):
    s3 = boto3.client('s3',endpoint_url='https://minio.lab.sspcloud.fr/')
    s3.download_file(Bucket=bucket, Key=key, Filename=filename)

    

def load_model(device, path="model.pth"):
    model = ResNet(pretrained=False)
    model = model.to(device)
    model.load_state_dict(torch.load(path, map_location=device))
    model.eval()
    return model

def load_image(file):
    img = Image.open(file).convert("RGB")
    return img

def predict(img, model, device):
    img = TF.to_tensor(img)
    img = TF.normalize(img, [0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    img = img.to(device)
    img = img.unsqueeze(0)
    preds = model(img)
    preds = F.softmax(preds, dim=1)
    if float(preds[0][0]) < float(preds[0][1]):
        results = "Pizza with probability: {:.2f}".format(float(preds[0][1]))
    else:
        results = "Not Pizza with probability: {:.2f}".format(float(preds[0][0]))
    return results

def load_device():
    if torch.cuda.is_available():
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')
    return device

def is_image_file(filename):
  return any(filename.endswith(extension) for extension in IMG_EXTENSIONS)
