# main.py
import os
import pandas as pd
from parsers import document_parser, image_parser, pdf_parser
from cleansers import text_cleanser
from analyzer import generate_key_findings

def process_file(file_path: str) -> dict:
    """
    [span_1](start_span)Orchestrates the entire file processing pipeline: parse, cleanse, and analyze.[span_1](end_span)
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return {}

    print(f"\n--- Starting processing for: {os.path.basename(file_path)} ---")
    file_name = os.path.basename(file_path)
    file_type = os.path.splitext(file_name)[1].lower()
    
    parser_output = {}

    # Step 1: Route to the correct parser based on file type
    if file_type in ['.pptx', '.xlsx']:
        parser_output = document_parser.parse_document(file_path)
    elif file_type in ['.png', '.jpg', '.jpeg']:
        parser_output = image_parser.parse_image(file_path)
    elif file_type == '.pdf':
        parser_output = pdf_parser.parse_pdf(file_path)
    else:
        print(f"Unsupported file type: {file_type}. Skipping.")
        return {}

    description = parser_output.get("description", "No description available.")
    raw_text = parser_output.get("raw_text", "")
    
    # Step 2: Cleanse the extracted text for PII
    clean_text = text_cleanser.cleanse_text(raw_text)
    
    # Step 3: Analyze the results to generate key findings
    key_findings = generate_key_findings(description, clean_text)

    # Step 4: Assemble the final, presentation-ready output
    final_output = {
        "File Name": file_name,
        "File Type": file_type,
        "File Description": description,
        "Key Findings": key_findings
    }
    
    print(f"--- Processing for {file_path} complete. ---")
    return final_output

# --- Main Execution Block ---
if __name__ == "__main__":
    test_files_dir = "test_files/"
    all_results = []

    if not os.path.isdir(test_files_dir):
        print(f"Error: Test directory '{test_files_dir}' not found.")
    else:
        # Process all supported files in the test directory
        for filename in sorted(os.listdir(test_files_dir)):
            file_path = os.path.join(test_files_dir, filename)
            if os.path.isfile(file_path):
                result = process_file(file_path)
                if result:
                    all_results.append(result)

    # Display the final results in a clean table format using pandas
    if all_results:
        print("\n\n--- ✅ FINAL PROJECT RESULTS ---")
        df = pd.DataFrame(all_results)
        # Set pandas display options to show full content
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', -1)
        print(df.to_string())
    else:
        print("\nNo files were processed or found in the test directory.")
