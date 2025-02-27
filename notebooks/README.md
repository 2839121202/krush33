# Notebooks

This directory contains Jupyter notebooks that demonstrate the CNN Model

## Architecture

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
