!apt-get install tesseract-ocr
!pip install pytesseract
!pip install transformers torch pillow requests accelerate language-tool-python
import pytesseract
from PIL import Image
import requests
from io import BytesIO
import torch
import language_tool_python
from transformers import (
    AutoProcessor,
    AutoModelForCausalLM,
    AutoModelForImageTextToText,
)

def polish_text(text):
    """Corrects grammar and style of a given text."""
    try:
        tool = language_tool_python.LanguageTool('en-US')
        corrected_text = tool.correct(text)
        return corrected_text
    except Exception as e:
        print(f"Error during text polishing: {e}")
        return text

def get_image_details_combined(image_source, task_complexity="simple"):
    """
    Analyzes an image to provide a detailed description and OCR based on task complexity,
    then polishes the final output for grammar and style.

    Args:
        image_source (str): A URL or local file path to the image.
        task_complexity (str): "simple" for plain text or "complex" for structured documents.

    Returns:
        dict: A dictionary with the detailed description and recognized text.
    """
    try:
        if image_source.startswith('http'):
            response = requests.get(image_source)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content)).convert("RGB")
        else:
            image = Image.open(image_source).convert("RGB")

        device = "cuda" if torch.cuda.is_available() else "cpu"

        # --- Part 1: Detailed Image Description (common for all tasks) ---
        print("Generating detailed image description...")
        description_processor = AutoProcessor.from_pretrained("microsoft/git-base-coco")
        description_model = AutoModelForCausalLM.from_pretrained("microsoft/git-base-coco").to(device)
        pixel_values = description_processor(images=image, return_tensors="pt").to(device).pixel_values
        generated_ids = description_model.generate(pixel_values=pixel_values, max_length=100, num_beams=5)
        raw_description = description_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        # --- Part 2: Dynamic OCR based on Complexity ---
        recognized_text = ""
        if task_complexity == "simple":
            print("Using simple OCR (pytesseract) for plain text...")
            recognized_text = pytesseract.image_to_string(image).strip()
        elif task_complexity == "complex":
            print("Using advanced OCR model (GOT-OCR2.0) for complex documents...")
            got_processor = AutoProcessor.from_pretrained("stepfun-ai/GOT-OCR-2.0-hf")
            got_model = AutoModelForImageTextToText.from_pretrained("stepfun-ai/GOT-OCR-2.0-hf", device_map="auto")

            inputs = got_processor(image, return_tensors="pt").to(device)

            with torch.no_grad():
                generated_ids = got_model.generate(
                    **inputs,
                    do_sample=False,
                    tokenizer=got_processor.tokenizer,
                    stop_strings="<|im_end|>",
                    max_new_tokens=4096,
                )

            recognized_text = got_processor.decode(generated_ids[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()

        # --- Part 3: Combine and format the final output ---
        if recognized_text:
            combined_text = f"{raw_description.capitalize()}. The image also contains the following text: \"{recognized_text}\"."
        else:
            combined_text = f"{raw_description.capitalize()}. No readable text was found in the image."

        final_polished_description = polish_text(combined_text)

        # --- Part 4: Dynamic Key Findings ---
        if recognized_text:
            key_findings_list = [f"- The image contains readable text.",
                                 f"- The text extracted by OCR is: {recognized_text}"]
            key_findings = "\n".join(key_findings_list)
        else:
            key_findings = "- No key text was found in the image."

        return {
            "file_description": final_polished_description,
            "key_findings": key_findings
        }

    except Exception as e:
        return {
            "file_description": f"An error occurred: {e}",
            "key_findings": "An error occurred during key findings extraction."
        }

# --- Example Usage ---
# Use the file you uploaded with a complex task
file_path = "https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcRq6dPp2BaPMzrInsQlEehkgjAYSjOTiDZ9vqVceSvScOAEV6ldynOyDa6Ng8nU1O1LXw4qkYWCOqQRZ8eP8E6h_n5rAmKSN1XH1uYXTBHt977UwSc"

print("## File Description\n")
results = get_image_details_combined(file_path, task_complexity="complex")
print(results["file_description"])

print("\n## Key Findings\n")
print(results["key_findings"])
