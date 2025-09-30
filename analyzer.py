# analyzer.py
import torch
from transformers import pipeline, BitsAndBytesConfig

def generate_key_findings(description: str, clean_text: str) -> str:
    """
    Uses a powerful LLM (Mistral-7B) to generate key security findings based on a
    [span_0](start_span)file's description and cleansed text content.[span_0](end_span)
    """
    print("Generating key findings with Mistral-7B LLM...")
    try:
        # Configuration for running a large model efficiently
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16
        )

        # Initialize the text-generation pipeline with the powerful Mistral model
        analyzer = pipeline(
            "text-generation",
            model="mistralai/Mistral-7B-Instruct-v0.2",
            model_kwargs={"quantization_config": quantization_config}
        )

        # Craft a detailed prompt to guide the AI's analysis
        prompt = f"""
        [INST]
        As a cybersecurity consultant, your task is to analyze the following document summary and provide key findings.
        
        Document Description: "{description}"
        
        Document Content Snippet: "{clean_text[:1500]}"
        
        Based on this information, identify 3-4 key security implications, vulnerabilities, or operational risks. Present your findings as a concise, professional bulleted list.
        [/INST]
        -
        """

        output = analyzer(prompt, max_new_tokens=150, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
        
        # Process the output to get a clean, bulleted list
        findings = output[0]['generated_text'].split('[/INST]')[-1].strip()
        
        # Ensure it starts with a bullet point
        if not findings.startswith('-'):
            findings = "- " + findings
        
        return findings

    except Exception as e:
        print(f"An error occurred in the analyzer: {e}")
        return "ERROR: Key findings could not be generated due to a model or system error."
