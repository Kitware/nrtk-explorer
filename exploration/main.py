#!/usr/bin/python

import numpy as np
import io
import os
import sys
import base64
import json
import timm
import torch

from PIL import Image as ImageModule
from PIL.Image import Image
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def load_image_as_tensor(path):
    img = ImageModule.open(path)
    img = img.resize((224, 224))
    img = img.convert("RGB")
    img = torch.as_tensor(np.array(img, dtype=np.float32)).transpose(2,0)[None]
    return img

def generate_pca_values(path):
    img = load_image_as_tensor(path)

    m = timm.create_model('resnet50d', pretrained=True)

    for param in m.parameters():
        param.requires_grad = False

    fs = m.forward_features(img)

    _, nx, ny, nz = fs.shape
    img_in = fs.reshape(_*nx,ny*nz)

    pca = PCA(n_components=3)
    x = pca.fit(img_in)
    print(x.singular_values_)

    return x.singular_values_

current_dataset = "/tmp/OIRDS_v1_0/oirds_test.json"

with open(current_dataset) as f:
    dataset = json.load(f)

images = dataset["images"][:10]

X = [ ]
for image_metadata in images:
   X.extend(generate_pca_values("/tmp/OIRDS_v1_0/" + image_metadata["file_name"]))

X = np.array(X).reshape(10,3)
print(X)
print(X.shape)

ax = plt.figure().add_subplot(projection='3d')

# Plot the training points
ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=[0]* 10, edgecolor="k")

plt.show()
