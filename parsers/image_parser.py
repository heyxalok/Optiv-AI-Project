import pytesseract
from PIL import Image
import requests
from io import BytesIO
import torch
from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration,
    AutoProcessor,
    AutoModelForImageTextToText,
)

def parse_image(image_source: str) -> dict:
    """
    Analyzes an image to extract a raw description and raw text content.

    This function acts as a pure parser, providing the raw data needed for the main
    pipeline's cleansing and analysis steps. It uses the BLIP model for high-quality
    image captioning and the GOT-OCR model for advanced text extraction.

    Args:
        image_source (str): A URL or a local file path to the image.

    Returns:
        A dictionary with two keys: 'description' (the image caption) and
        'raw_text' (the text extracted via OCR). Returns a structured error
        if processing fails.
    """
    try:
        # Step 1: Load the image from either a URL or a local path
        print(f"Processing image from: {image_source}")
        if image_source.startswith('http'):
            response = requests.get(image_source)
            response.raise_for_status()  # Raise an exception for bad status codes
            image = Image.open(BytesIO(response.content)).convert("RGB")
        else:
            image = Image.open(image_source).convert("RGB")

        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")

        # --- Part 1: Generate Raw Image Description with BLIP ---
        print("Generating image description with BLIP...")
        blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

        inputs = blip_processor(images=image, return_tensors="pt").to(device)
        generated_ids = blip_model.generate(**inputs, max_new_tokens=50)
        raw_description = blip_processor.decode(generated_ids[0], skip_special_tokens=True).strip()

        # --- Part 2: Extract Raw Text with Advanced OCR ---
        print("Extracting text with GOT-OCR...")
        ocr_processor = AutoProcessor.from_pretrained("stepfun-ai/GOT-OCR-2.0-hf")
        ocr_model = AutoModelForImageTextToText.from_pretrained("stepfun-ai/GOT-OCR-2.0-hf", device_map="auto")

        inputs = ocr_processor(image, return_tensors="pt").to(device)
        with torch.no_grad():
            generated_ids = ocr_model.generate(
                **inputs,
                do_sample=False,
                tokenizer=ocr_processor.tokenizer,
                stop_strings="<|im_end|>",
                max_new_tokens=4096,
            )
        raw_text = ocr_processor.decode(generated_ids[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()

        # --- Part 3: Return a dictionary with raw, separate data ---
        print("Image processing successful.")
        return {
            "description": raw_description,
            "raw_text": raw_text
        }

    except Exception as e:
        print(f"An error occurred in image parser: {e}")
        return {
            "description": f"ERROR: Image processing failed. Details: {e}",
            "raw_text": ""
        }
