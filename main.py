# main.py
import os
from parsers import document_parser, image_parser, pdf_parser
from cleansers import text_cleanser
from analyzer import generate_key_findings

def process_file(file_path: str) -> dict:
    """
    Orchestrates the entire file processing pipeline:
    1. Parse the file to get description and raw text.
    2. Cleanse the raw text to remove PII.
    3. Analyze the results to generate key findings.
    """
    print(f"--- Starting processing for: {file_path} ---")
    file_name = os.path.basename(file_path)
    file_type = os.path.splitext(file_name)[1]
    
    parser_output = {}

    if file_type in ['.pptx', '.xlsx']:
        parser_output = document_parser.parse_document(file_path)
    elif file_type in ['.png', '.jpg', '.jpeg']:
        parser_output = image_parser.parse_image(file_path)
    elif file_type == '.pdf':
        parser_output = pdf_parser.parse_pdf(file_path)
    else:
        print("Unsupported file type.")
        return {}

    raw_text = parser_output.get("raw_text", "")
    description = parser_output.get("description", "No description available.")

    clean_text = text_cleanser.cleanse_text(raw_text)
    
    key_findings = generate_key_findings(description, clean_text)

    final_output = {
        "File Name": file_name,
        "File Type": file_type,
        "File Description": description,
        "Key Findings": key_findings
    }
    
    print(f"--- Processing for {file_path} complete. ---")
    return final_output

# --- Main Execution ---
if __name__ == "__main__":
    # Create a list of test files
    test_files_dir = "test_files/"
    test_files = [os.path.join(test_files_dir, f) for f in os.listdir(test_files_dir)]

    # Process all files in the test directory
    for file in test_files:
        if os.path.isfile(file): # Ensure it's a file
            result = process_file(file)
            # You can now print the result in a nice format
            if result:
                print("\n--- FINAL OUTPUT ---")
                for key, value in result.items():
                    print(f"{key}: {value}")
                print("--------------------\n")
