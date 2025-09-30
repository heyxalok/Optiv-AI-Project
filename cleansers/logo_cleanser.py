# cleansers/logo_cleanser.py
import cv2
import numpy as np

def mask_logo(main_img: np.ndarray, template_logo: np.ndarray, threshold=0.8) -> np.ndarray:
    """
    Detects a logo in an image using template matching and masks it using inpainting.

    Args:
        main_img (np.ndarray): The main image in OpenCV format (BGR).
        template_logo (np.ndarray): The logo template in OpenCV format (BGR).
        threshold (float): Similarity threshold for a match (0.0 to 1.0).

    Returns:
        The image with the logo removed, in OpenCV format.
    """
    if main_img is None or template_logo is None:
        print("Error: Input image or template is invalid.")
        return main_img

    if template_logo.shape[0] > main_img.shape[0] or template_logo.shape[1] > main_img.shape[1]:
        print("Warning: Template is larger than the main image.")
        return main_img

    w, h = template_logo.shape[1], template_logo.shape[0]
    
    # Perform template matching
    result = cv2.matchTemplate(main_img, template_logo, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)

    if len(loc[0]) == 0:
        print("No logo detected based on the template.")
        return main_img

    # Create a black mask of the same size as the main image
    mask = np.zeros(main_img.shape[:2], dtype="uint8")

    # Mark all detected logo locations as white on the mask
    for pt in zip(*loc[::-1]):
        cv2.rectangle(mask, pt, (pt[0] + w, pt[1] + h), 255, -1)
    
    print(f"Found and marked {len(loc[0])} instances of the logo for removal.")

    # Perform inpainting to "heal" the image where the mask is white
    inpainted_image = cv2.inpaint(main_img, mask, 3, cv2.INPAINT_TELEA)

    return inpainted_image
