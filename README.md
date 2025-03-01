# Krush33: Plant Disease Detection and Agricultural Support System

Krush33 is a comprehensive agricultural technology platform that combines multiple key features to support farmers.

## Disease Detection System

- Uses a CNN (Convolutional Neural Network) architecture for plant disease detection
- Allows users to upload images through drag-and-drop, file selection, or direct camera capture
- The disease detection model has over 52 million trainable parameters and processes images of size 224x224 pixels
- Provides disease descriptions and prevention measures in multiple languages

## Soil Type Analysis

- Implements a separate CNN model for soil classification
- Can identify 5 different soil types: Black, Cinder, Laterite, Peat, and Yellow soil
- Uses a smaller architecture (~229K parameters) with multiple convolution and pooling layers

## Weather Forecasting

- Provides weather forecasts for 7-14 days
- Uses geolocation to automatically detect user location
- Displays key metrics like temperature, humidity, wind speed, and precipitation chances

## Marketplace Integration

- Recommends products based on detected plant diseases
- Provides direct links to purchase agricultural supplies
- Shows relevant preventive products for identified issues

## Multilingual Support

- Supports multiple Indian languages including Hindi (hi), Tamil (ta), Telugu (te), Marathi (mr), Bengali (bn), Oriya (or) and many more.
- Includes text-to-speech functionality for accessibility
- Maintains consistent translations across the platform
