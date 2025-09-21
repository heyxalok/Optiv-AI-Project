# Automating File Cleansing and Analysis Leveraging AI

## 🎯 Project Goal

The goal of this project is to design and prototype an automated solution for Optiv's security consultants. The system will cleanse diverse client files (like images, PowerPoints, and Excel sheets) by removing sensitive information, pre-process them into a consistent format, and analyze the data to generate meaningful security insights.

---

## 🧑‍💻 Team & Roles

* **Architect:** @[heyxalok] - Manages the overall project structure, integrates all modules, and performs the final security analysis to generate `Key Findings`.
* **Image Parser:** @[ARYANNNN1234] - Responsible for processing image files (`.png`, `.jpeg`) to perform OCR and generate rich, contextual descriptions.
* **Document Parser:** @[Anamika's GitHub Username] - Responsible for processing text-based documents (`.pptx`, `.xlsx`) to extract all text content.
* **Text Cleanser:** @[ashishanilsikaria] - Responsible for taking raw text from the parsers and cleansing it of Personally Identifiable Information (PII).

---

## ✅ Phase 1 Sprint Goal (Deadline: Sunday, Sept 21st)

The objective of our first sprint is for each team member to create a basic, functional script for their assigned role.

* **Architect:** Create the GitHub repo, define the project's folder structure, and build the main application skeleton (`main.py`) that shows the overall logic flow.
* **Image Parser:** Create a script that can take an image as input and successfully perform both OCR and AI-driven image description.
* **Document Parser:** Create a script that can take a `.pptx` or `.xlsx` file as input and extract all text.
* **Text Cleanser:** Create a script that can take a string of text and remove basic PII like email addresses and phone numbers.
