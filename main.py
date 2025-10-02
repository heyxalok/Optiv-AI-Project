# main.py
import os
import pandas as pd
import torch
from transformers import pipeline, BitsAndBytesConfig
from parsers import document_parser, image_parser, pdf_parser
from cleansers import text_cleanser
# Import both functions from the analyzer
from analyzer import generate_final_description, generate_key_findings

def process_file(file_path: str, analyzer_pipeline) -> dict:
    """Orchestrates the entire file processing pipeline."""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return {}
    
    print(f"\n--- Starting processing for: {os.path.basename(file_path)} ---")
    file_name = os.path.basename(file_path)
    file_type = os.path.splitext(file_name)[1].lower()
    
    parser_output = {}

    if file_type in ['.pptx', '.xlsx']:
        parser_output = document_parser.parse_document(file_path)
    elif file_type in ['.png', '.jpg', '.jpeg']:
        parser_output = image_parser.parse_image(file_path)
    elif file_type == '.pdf':
        parser_output = pdf_parser.parse_pdf(file_path)
    else:
        print(f"Unsupported file type: {file_type}. Skipping.")
        return {}

    initial_description = parser_output.get("description", "No description available.")
    raw_text = parser_output.get("raw_text", "")
    clean_text = text_cleanser.cleanse_text(raw_text)
    
    # --- Step 3 (NEW): Generate the enhanced "meta-description" ---
    final_description = generate_final_description(analyzer_pipeline, initial_description, clean_text)
    
    # --- Step 4: Analyze for key findings using the better description ---
    raw_findings = generate_key_findings(analyzer_pipeline, final_description, clean_text)
    key_findings = ' '.join(raw_findings.split())

    # Step 5: Assemble the final output
    final_output = {
        "File Name": file_name,
        "File Type": file_type,
        "File Description": final_description, # Use the new, high-quality description
        "Key Findings": key_findings
    }
    
    print(f"--- Processing for {file_path} complete. ---")
    return final_output

if __name__ == "__main__":
    print("--- Initializing and loading the Mistral-7B model... ---")
    quantization_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)
    analyzer_pipeline = pipeline(
        "text-generation",
        model="mistralai/Mistral-7B-Instruct-v0.2",
        model_kwargs={"quantization_config": quantization_config}
    )
    print("--- Model loaded successfully. Starting file processing. ---")
    
    test_files_dir = "test_files/"
    all_results = []

    if not os.path.isdir(test_files_dir):
        print(f"Error: Test directory '{test_files_dir}' not found.")
    else:
        for filename in sorted(os.listdir(test_files_dir)):
            file_path = os.path.join(test_files_dir, filename)
            if os.path.isfile(file_path):
                result = process_file(file_path, analyzer_pipeline) 
                if result:
                    all_results.append(result)

    if all_results:
        print("\n\n--- ✅ FINAL PROJECT RESULTS ---")
        df = pd.DataFrame(all_results)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_colwidth', None)
        print(df.to_string())
    else:
        print("\nNo files were processed.")