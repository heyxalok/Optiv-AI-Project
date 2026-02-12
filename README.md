# Automating File Cleansing and Security Analysis Leveraging AI

AI-powered system that automatically sanitizes sensitive data from multi-format enterprise documents and generates cybersecurity risk insights using Computer Vision, NLP, and Large Language Models.

---

## Why

Organizations frequently handle large volumes of heterogeneous files such as PDFs, images, spreadsheets, and presentations that often contain sensitive information like personally identifiable information (PII), confidential text, or proprietary branding. Manual sanitization is slow, error-prone, and not scalable.

This project automates document cleansing and performs AI-driven security pre-assessment. It detects and removes sensitive data across multiple file formats and generates structured cybersecurity insights, helping security teams reduce manual effort and prevent unintended data exposure before document sharing or analysis.

---

## What It Does

- Processes `.png`, `.jpg`, scanned `.pdf`, `.pptx`, and `.xlsx` files  
- Detects and removes logos using OpenCV inpainting  
- Redacts sensitive information (names, emails, phone numbers) using NLP + regex  
- Generates contextual descriptions using image captioning and document summarization models  
- Produces AI-driven cybersecurity findings using a Large Language Model  
- Outputs structured, consultant-style security analysis  

---

## How to Run (Google Colab)

This project is designed to run in a **GPU-enabled Google Colab environment**.

### Step 1 — Setup Environment

- Open a new Colab notebook  
- Set runtime to **T4 GPU**  
  `Runtime → Change runtime type → T4 GPU`

---

### Step 2 — Project Setup

- Upload or clone this repository  
- Create a folder named `logo_templates/` and add logo images (e.g., `optiv_logo.png`)  
- Add files to be analyzed inside `test_files/`  

---

### Step 3 — Install Dependencies

Run:

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

---

### Step 4 — Hugging Face Authentication

```python
from huggingface_hub import login
login()
```

Paste your Hugging Face token when prompted.

---

### Step 5 — Run the Pipeline

```python
!python main.py
```

The system processes all files inside `test_files/` and outputs structured cybersecurity findings.

---

### Sample Output

Example AI-generated security finding:

```
--- ✅ FINAL PROJECT RESULTS ---

File Name: File_001.png  
File Type: .png  

File Description:  
This document appears to be an electrical engineering report, as indicated by the acronym "IDF" and the reference to "ELECTRICAL" in its text. The initial visual description suggests an action taking place in an electrical system, possibly the activation of a circuit or device, such as a switch or relay, by pressing a button on a wall.  

Key Findings:

1. **Potential for Electrical System Manipulation:**  
The document's content suggesting an electrical system and the absence of any context regarding who has access to this system could indicate a potential risk of unauthorized access and manipulation of electrical systems. This could lead to various issues, such as power outages, short circuits, or even damage to critical infrastructure.  

2. **Lack of Authentication and Authorization:**  
The document does not provide any information about the authentication or authorization methods used to access the electrical system. This could mean that anyone with access to the IDF system could potentially activate circuits or devices without proper authorization, increasing the risk of unintended consequences or malicious activities.  

3. **Inadequate Document Control:**  
The document's content being available to an external entity, such as a cybersecurity consultant, raises concerns about inadequate document control within the organization. This could lead to sensitive information being leaked or misused.
```


---

## Tech Stack

**Core:** Python  

**AI / ML:** PyTorch, Hugging Face Transformers, SpaCy, OpenCV  

**Models Used:**
- `mistralai/Mistral-7B-Instruct-v0.2`
- `Salesforce/blip-image-captioning-base`
- `stepfun-ai/GOT-OCR-2.0-hf`
- `sshleifer/distilbart-cnn-12-6`

**Data Processing:** Pandas, OpenPyXL, python-pptx, pdf2image, OCR (Tesseract)

---

## Impact

- Automated sensitive data sanitization across multiple enterprise file formats  
- Reduced manual document inspection and preprocessing effort  
- Enabled AI-driven cybersecurity pre-assessment before document sharing  
- Detects PII exposure and proprietary information risks automatically  
- Modular, scalable pipeline for enterprise document security workflows  

---

## Architecture Overview

- Documents are ingested and categorized by file type  
- Sensitive data is detected using Computer Vision + NLP techniques  
- Logos and PII are removed/redacted from files  
- AI model generates structured cybersecurity risk findings  
- Sanitized output and analysis results are produced  

![WhatsApp Image 2026-02-12 at 7 06 04 PM](https://github.com/user-attachments/assets/6842f797-a4c7-4586-a196-08870796952d)


---

## Future Improvements

- Add web interface for file upload and visualization  
- Improve contextual PII detection accuracy  
- Enable real-time processing pipeline  
- Add automated risk scoring system  
- Optimize performance for large-scale batch processing  

---

## Author

Developed as part of an AI-driven cybersecurity automation prototype focused on document sanitization and intelligent risk analysis.
