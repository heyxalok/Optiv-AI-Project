# main.py
from parsers import document_parser, image_parser
from cleansers import text_cleanser

def process_file(file_path):
    print(f"--- Starting processing for {file_path} ---")

    if file_path.endswith('.pptx') or file_path.endswith('.xlsx'):
        raw_text = document_parser.parse_document(file_path)
        # [span_0](start_span)This task is to pre-process diverse file formats into a consistent, usable structure[span_0](end_span)

    elif file_path.endswith('.png') or file_path.endswith('.jpeg'):
        raw_text, image_desc = image_parser.parse_image(file_path)
        # [span_1](start_span)This task involves text extraction from images[span_1](end_span)

    else:
        print("Unsupported file type.")
        return

    # [span_2](start_span)The cleanse_text function will eventually remove PII[span_2](end_span)
    clean_text = text_cleanser.cleanser_text(raw_text)

    # In Phase 2, this is where you will add your analysis step
    print("--- Analysis Step (Coming in Phase 2) ---")

    print(f"--- Processing for {file_path} complete ---\n")

# --- Main Execution ---
if __name__ == "__main__":
    test_pptx = "test_files/sample.pptx" # Make sure you have a sample file here
    test_png = "test_files/sample.png"   # And here

    process_file(test_pptx)
    process_file(test_png)
