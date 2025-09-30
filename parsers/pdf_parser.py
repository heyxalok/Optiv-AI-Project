# parsers/pdf_parser.py
from pdf2image import convert_from_path
# Assumes the perfected image_parser.py is in the same directory
from parsers.image_parser import parse_image

def parse_pdf(file_path: str) -> dict:
    """
    Parses a PDF file by converting its pages to images and using the image_parser module.
    """
    print(f"Parsing PDF file: {file_path}")
    try:
        images = convert_from_path(file_path)

        if not images:
            return {"description": "ERROR: PDF is empty or could not be read.", "raw_text": ""}

        print("Generating description from the first page...")
        first_page_data = parse_image(images[0])
        description = first_page_data.get("description", "No description generated.")

        all_pages_text = []
        print(f"Extracting text from {len(images)} pages...")
        for i, page_image in enumerate(images):
            print(f"Processing page {i+1}...")
            if i == 0:
                page_text = first_page_data.get("raw_text", "")
            else:
                page_data = parse_image(page_image)
                page_text = page_data.get("raw_text", "")
            all_pages_text.append(page_text)

        full_raw_text = "\n\n--- Page Break ---\n\n".join(all_pages_text)
        
        print("PDF parsing successful.")
        return {
            "description": description.strip(),
            "raw_text": full_raw_text.strip()
        }

    except Exception as e:
        print(f"An error occurred in PDF parser: {e}")
        return {
            "description": f"ERROR: PDF processing failed. Details: {e}",
            "raw_text": ""
        }

