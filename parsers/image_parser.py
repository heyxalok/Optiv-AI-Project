# parsers/image_parser.py
import os
import cv2
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import torch
from transformers import (
    BlipProcessor, BlipForConditionalGeneration,
    AutoProcessor, AutoModelForImageTextToText
)
from cleansers.logo_cleanser import mask_logo

def parse_image(image_source: Image.Image or str) -> dict:
    """Cleanses an image of all known logos, then extracts a description and raw text."""
    try:
        if isinstance(image_source, str):
            if image_source.startswith('http'):
                response = requests.get(image_source)
                response.raise_for_status()
                image_pil = Image.open(BytesIO(response.content)).convert("RGB")
            else:
                image_pil = Image.open(image_source).convert("RGB")
        elif isinstance(image_source, Image.Image):
            image_pil = image_source.convert("RGB")
        else:
            raise TypeError("image_source must be a file path, URL, or PIL Image.")

        # --- Step 1: Cleanse All Logos ---
        print("Performing logo cleansing...")
        # Convert PIL Image to OpenCV format (CORRECTED TYPO)
        image_cv = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
        
        cleansed_image_cv = image_cv 
        template_folder = "logo_templates/"
        if os.path.isdir(template_folder):
            for template_file in os.listdir(template_folder):
                template_path = os.path.join(template_folder, template_file)
                template_cv = cv2.imread(template_path)
                if template_cv is not None:
                    cleansed_image_cv = mask_logo(cleansed_image_cv, template_cv)
        
        # Convert the cleansed OpenCV image back to PIL format (CORRECTED TYPO)
        cleansed_image_pil = Image.fromarray(cv2.cvtColor(cleansed_image_cv, cv2.COLOR_BGR2RGB))
        
        device = "cuda" if torch.cuda.is_available() else "cpu"

        # --- Step 2: Generate Description from the CLEANSED image ---
        print("Generating image description with BLIP...")
        blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)
        inputs = blip_processor(images=cleansed_image_pil, return_tensors="pt").to(device)
        generated_ids = blip_model.generate(**inputs, max_new_tokens=50)
        raw_description = blip_processor.decode(generated_ids[0], skip_special_tokens=True).strip()

        # --- Step 3: Extract Text from the CLEANSED image ---
        print("Extracting text with GOT-OCR...")
        ocr_processor = AutoProcessor.from_pretrained("stepfun-ai/GOT-OCR-2.0-hf")
        ocr_model = AutoModelForImageTextToText.from_pretrained("stepfun-ai/GOT-OCR-2.0-hf", device_map="auto")
        inputs = ocr_processor(cleansed_image_pil, return_tensors="pt").to(device)
        with torch.no_grad():
            generated_ids = ocr_model.generate(**inputs, do_sample=False, tokenizer=ocr_processor.tokenizer, stop_strings="<|im_end|>")
        raw_text = ocr_processor.decode(generated_ids[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()

        # --- Step 4: Clean up GPU memory ---
        print("Cleaning up image parser models from GPU memory...")
        del blip_model, ocr_model
        import gc
        gc.collect()
        torch.cuda.empty_cache()

        return {"description": raw_description, "raw_text": raw_text}

    except Exception as e:
        print(f"An error occurred in image parser: {e}")
        return {"description": f"ERROR: Image processing failed. Details: {e}", "raw_text": ""}