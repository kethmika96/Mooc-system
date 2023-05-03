import torch
import json

import numpy as np

from torchvision import transforms
from torchvision.models.resnet import resnet50


class Ratings:
    def __init__(self, model_path="./models/model_best.pth", id2label="./models/id2label.json",
                 label2id="./models/label2id.json") -> None:

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self.load_model(model_path)

        with open(id2label, 'r') as idlabel:
            _id2label = json.load(idlabel)

        self.id2label = {}
        for key, value in _id2label.items():
            self.id2label[int(key)] = value

        with open(label2id, 'r') as labelid:
            _label2id = json.load(labelid)

        self.label2id = {}
        for key, value in _label2id.items():
            self.label2id[key] = int(value)

        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize((224, 224)),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])

    def load_model(self, path):
        model = resnet50()
        done = False
        in_features = model.fc.in_features

        fc_layers = []
        while not done:
            if (in_features / 16) < 3:
                fc_layers.append(torch.nn.Linear(in_features=in_features, out_features=3, bias=True))
                print("Finishing up...")
                break
            else:
                out_features = int(in_features / 16)
                print(in_features, out_features)
                fc_layers.append(torch.nn.Linear(in_features=in_features, out_features=out_features, bias=True))
                in_features = out_features

        model.fc = torch.nn.Sequential(*fc_layers)

        model.load_state_dict(
            torch.load(path, map_location=torch.device('cuda' if torch.cuda.is_available() else 'cpu')))

        return model

    def classify_facial_expression(self, images):
        if isinstance(images, np.ndarray):
            if images.ndim == 4:
                transformed = []
                for image in images:
                    transformed.append(self.transform(image).unsqueeze(dim=0).to(self.device))

                images = torch.cat(transformed)
            else:
                images = self.transform(images).unsqueeze(dim=0).to(self.device)

        elif isinstance(images, list):
            transformed = []
            for image in images:
                transformed.append(self.transform(image).unsqueeze(dim=0).to(self.device))

            images = torch.cat(transformed)

        if images.ndim == 3:
            images = images.unsqueeze(dim=0)

        preds = torch.softmax(self.model(images), dim=1)

        if preds.ndim == 2:
            class_ids = torch.argmax(preds, dim=1)
            classes = []
            confs = []
            for i, class_id in enumerate(class_ids):
                classes.append(self.id2label[class_id.item()])
                confs.append(torch.max(preds).item())

            return classes, confs

        else:
            class_id = torch.argmax(preds)
            return self.id2label[class_id.item()], [torch.max(preds).item()]

    def __call__(self, images):
        return self.classify_facial_expression(images)