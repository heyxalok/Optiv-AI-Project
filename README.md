# Automating File Cleansing and Analysis Leveraging AI

This project is a comprehensive Python-based prototype designed to solve the challenges outlined in the Optiv Cyber Simulation Exercise. The system automates the process of cleansing sensitive information from diverse file formats and leverages multiple state-of-the-art AI models to generate actionable security insights.

## 🎯 Project Goal

The goal of this project is to design and prototype an automated solution for Optiv's security consultants. [cite_start]The system will cleanse diverse client files (like images, PowerPoints, and Excel sheets) by removing sensitive information, pre-process them into a consistent format, and analyze the data to generate meaningful security insights[cite: 5].

## ✨ Key Features

* **Multi-Modal File Processing:** Ingests and analyzes a wide range of file types, including `.png`, `.jpg`, scanned `.pdf`, `.pptx`, and `.xlsx`.
* **Advanced Logo Cleansing:** Utilizes OpenCV's inpainting technique to seamlessly remove and "heal" areas where known client logos are detected.
* **AI-Powered PII Redaction:** Employs a hybrid approach using SpaCy's Named Entity Recognition (NER) to intelligently find and mask names, combined with regex for contact details (emails, phone numbers).
* **State-of-the-Art Analysis Engine:** Leverages a powerful Large Language Model (Mistral-7B) to act as an AI cybersecurity consultant, interpreting the cleansed data to produce high-quality, context-aware security findings.
* **Automated Description Generation:** Uses a suite of AI models (BLIP for images, DistilBART for documents) to generate contextual, human-readable descriptions for all processed files.

## ⚙️ Architecture

Below is the functional design diagram illustrating the project's architecture and data flow.

*[Insert Your Functional Design Diagram Image Here]*

## 🛠️ Tech Stack

* **Core:** Python 3.10+
* **AI / ML:** PyTorch, Hugging Face Transformers, SpaCy, OpenCV
* **Core Models:** `mistralai/Mistral-7B-Instruct-v0.2`, `Salesforce/blip-image-captioning-base`, `stepfun-ai/GOT-OCR-2.0-hf`, `sshleifer/distilbart-cnn-12-6`
* **Data Handling & Parsing:** Pandas, OpenPyXL, python-pptx, pdf2image

## 🚀 Setup & Usage (Google Colab)

This project is designed to run in a Google Colab environment with a GPU.

### 1. Environment Setup
* Create a new Colab notebook and set the runtime to **T4 GPU** (`Runtime` -> `Change runtime type`).

### 2. Project & Data Setup
* Clone this repository or upload it as a ZIP file.
* Create a folder named `logo_templates/` and add your logo image files (e.g., `optiv_logo.png`).
* Add the documents you want to analyze to the `test_files/` folder.

### 3. Install Dependencies
* Run the following command in a cell to install all necessary packages.
    ```python
    !apt-get update
    !apt-get install -y tesseract-ocr poppler-utils

    !pip install --quiet \
        "numpy==1.26.4" \
        "transformers" \
        "torch" \
        "accelerate" \
        "bitsandbytes" \
        "pillow" \
        "requests" \
        "opencv-python-headless" \
        "spacy==3.7.2" \
        "pdf2image" \
        "openpyxl" \
        "python-pptx" \
        "pandas"

    !python -m spacy download en_core_web_sm
    ```

### 4. Hugging Face Authentication
* The Mistral-7B model requires authentication. Run the following cell and paste your Hugging Face access token when prompted.
    ```python
    from huggingface_hub import login
    login()
    ```

### 5. Running the Pipeline
* Execute the main script to process all files in the `test_files` directory.
    ```python
    !python main.py
    ```
* The script will print a final, formatted table with the analysis results for each file.
