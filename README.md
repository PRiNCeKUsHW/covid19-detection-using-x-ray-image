# Covid-19 Detection Using Chest X-Ray Images

A deep learning project that classifies **chest X-ray images as Covid-19 positive or normal** using a Convolutional Neural Network (CNN) built in Keras. The trained model is served through a Flask web app where a user fills in their details, uploads an X-ray and gets a result.

## Features

- Custom CNN trained on chest X-ray images (224 x 224 RGB input)
- Data augmentation during training (shear, zoom, horizontal flip)
- Flask web app with a patient form (name, age, gender, mobile, email, address) and X-ray upload
- Image preprocessing with OpenCV (resize and normalize) before prediction
- Result page showing a positive or negative result, with a "Check Again" button
- Sends an email alert with the patient's details when a result is positive

## Tech Stack

- **Deep learning:** TensorFlow / Keras
- **Image processing:** OpenCV, Pillow
- **Web app:** Flask, Flask-WTF, Bootstrap-Flask (Bootstrap 5)
- **Notebook:** Jupyter

## Model Architecture

```
Input (224, 224, 3)
→ Conv2D(32) → Conv2D(64) → MaxPool → Dropout(0.25)
→ Conv2D(64) → MaxPool → Dropout(0.25)
→ Conv2D(128) → MaxPool → Dropout(0.25)
→ Flatten → Dense(64) → Dropout(0.5)
→ Dense(1, sigmoid)
```

- Loss: binary cross-entropy
- Optimizer: Adam
- The trained weights are saved as `covid.h5`.

## Getting Started

### 1. Clone and install

```bash
git clone https://github.com/PRiNCeKUsHW/covid19-detection-using-x-ray-image.git
cd covid19-detection-using-x-ray-image
python -m venv venv
venv\Scripts\activate          # macOS/Linux: source venv/bin/activate
pip install flask bootstrap-flask flask-wtf email-validator tensorflow opencv-python pillow
```

### 2. Add email credentials

The app imports email settings from a `pas.py` file that is not committed. Create it in the project root:

```python
# pas.py
own_email = "your-email@gmail.com"
own_password = "your-gmail-app-password"
```

### 3. Create the uploads folder and run

```bash
mkdir uploads
python main.py
```

Open http://127.0.0.1:5000, go to the check page, fill in the form and upload a JPEG X-ray.

## Retraining the Model

Open `covid19.ipynb`. It expects the dataset in this layout:

```
CovidDataset/Data/
├── train/   # one subfolder per class
└── test/
```

Run all cells to train the model and save a new `covid.h5`.

## Project Structure

```
covid19-detection-using-x-ray-image/
├── covid19.ipynb    # Model building and training
├── covid.h5         # Trained model
├── main.py          # Flask app: form, upload, prediction, email alert
├── templates/       # base, index, test (form), result
└── static/          # CSS and images
```

## Disclaimer

This is an educational project. It is **not** a medical diagnostic tool and must not be used for real diagnosis.

## Team

Made by Abhisheak Mishra, Anuj Kumar Kushwaha and Prabhat Mogha.
