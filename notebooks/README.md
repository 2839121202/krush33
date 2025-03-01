# Notebooks

This directory contains Jupyter notebooks that demonstrate the CNN Model

## Disease Architecture

| Layer (type)  | Output Shape       | Params     |
| ------------- | ------------------ | ---------- |
| Conv2d-1      | [-1, 32, 224, 224] | 896        |
| ReLU-1        | [-1, 32, 224, 224] | 0          |
| BatchNorm2d-1 | [-1, 32, 224, 224] | 64         |
| Conv2d-2      | [-1, 32, 224, 224] | 9,248      |
| ReLU-2        | [-1, 32, 224, 224] | 0          |
| BatchNorm2d-2 | [-1, 32, 224, 224] | 64         |
| MaxPool2d-1   | [-1, 32, 112, 112] | 0          |
| Conv2d-3      | [-1, 64, 112, 112] | 18,496     |
| ReLU-3        | [-1, 64, 112, 112] | 0          |
| BatchNorm2d-3 | [-1, 64, 112, 112] | 128        |
| Conv2d-4      | [-1, 64, 112, 112] | 36,928     |
| ReLU-4        | [-1, 64, 112, 112] | 0          |
| BatchNorm2d-4 | [-1, 64, 112, 112] | 128        |
| MaxPool2d-2   | [-1, 64, 56, 56]   | 0          |
| Conv2d-5      | [-1, 128, 56, 56]  | 73,856     |
| ReLU-5        | [-1, 128, 56, 56]  | 0          |
| BatchNorm2d-5 | [-1, 128, 56, 56]  | 256        |
| Conv2d-6      | [-1, 128, 56, 56]  | 147,584    |
| ReLU-6        | [-1, 128, 56, 56]  | 0          |
| BatchNorm2d-6 | [-1, 128, 56, 56]  | 256        |
| MaxPool2d-3   | [-1, 128, 28, 28]  | 0          |
| Conv2d-7      | [-1, 256, 28, 28]  | 295,168    |
| ReLU-7        | [-1, 256, 28, 28]  | 0          |
| BatchNorm2d-7 | [-1, 256, 28, 28]  | 512        |
| Conv2d-8      | [-1, 256, 28, 28]  | 590,080    |
| ReLU-8        | [-1, 256, 28, 28]  | 0          |
| BatchNorm2d-8 | [-1, 256, 28, 28]  | 512        |
| MaxPool2d-4   | [-1, 256, 14, 14]  | 0          |
| Dropout-1     | [-1, 50176]        | 0          |
| Linear-1      | [-1, 1024]         | 51,381,248 |
| ReLU-9        | [-1, 1024]         | 0          |
| Dropout-2     | [-1, 1024]         | 0          |
| Linear-2      | [-1, K]            | 1025\*K    |

================================================================
Total params: 52,556,424 + 1025*K
Trainable params: 52,556,424 + 1025*K
Non-trainable params: 0

---

Input size (MB): 0.57
Forward/backward pass size (MB): 116.44
Parameters size (MB): 200.52
Estimated total size (MB): 317.53

## Soil Type Architecture

| Layer (type)   | Output Shape         | Params  |
| -------------- | -------------------- | ------- |
| Conv2D-1       | [None, 218, 218, 16] | 448     |
| MaxPooling2D-1 | [None, 109, 109, 16] | 0       |
| Conv2D-2       | [None, 107, 107, 32] | 4,640   |
| MaxPooling2D-2 | [None, 53, 53, 32]   | 0       |
| Conv2D-3       | [None, 51, 51, 64]   | 18,496  |
| MaxPooling2D-3 | [None, 25, 25, 64]   | 0       |
| Conv2D-4       | [None, 23, 23, 64]   | 36,928  |
| MaxPooling2D-4 | [None, 11, 11, 64]   | 0       |
| Conv2D-5       | [None, 9, 9, 64]     | 36,928  |
| MaxPooling2D-5 | [None, 4, 4, 64]     | 0       |
| Flatten        | [None, 1024]         | 0       |
| Dense-1        | [None, 128]          | 131,200 |
| Dense-2        | [None, 5]            | 645     |

================================================================
Total params: 229,285
Trainable params: 229,285
Non-trainable params: 0

---

Input size (MB): 0.58
Forward/backward pass size (MB): 14.21
Parameters size (MB): 0.87
Estimated total size (MB): 15.66
