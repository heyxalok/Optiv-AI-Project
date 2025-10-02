# analyzer.py
import torch
from transformers import pipeline, BitsAndBytesConfig

def generate_final_description(analyzer_pipeline, initial_description: str, clean_text: str) -> str:
    """Uses an LLM to create a refined description from an initial visual summary and OCR text."""
    print("Generating final, enhanced description with LLM...")
    try:
        # We only need a short snippet of text for context
        text_snippet = clean_text[:500]

        prompt = f"""
        [INST]
        Synthesize the following information into a single, concise, and descriptive paragraph of about 2-3 sentences.
        
        Initial Visual Description: "{initial_description}"
        
        Text Content Found in the Document: "{text_snippet}"
        
        Based on both, what is this document and what is it about?
        [/INST]
        """

        output = analyzer_pipeline(prompt, max_new_tokens=100, do_sample=False)
        final_desc = output[0]['generated_text'].split('[/INST]')[-1].strip()
        return final_desc

    except Exception as e:
        print(f"An error occurred during description enhancement: {e}")
        return initial_description # Fallback to the initial visual description on error

def generate_key_findings(analyzer_pipeline, final_description: str, clean_text: str) -> str:
    """Uses a pre-loaded LLM pipeline to generate key security findings."""
    print("Generating key findings with LLM...")
    try:
        prompt = f"""
        [INST]
        As a cybersecurity consultant, analyze the following document summary and provide key findings.
        
        Document Description: "{final_description}"
        
        Document Content Snippet: "{clean_text[:1500]}"
        
        Based on this information, identify 3-4 key security implications, vulnerabilities, or operational risks. Present your findings as a concise, professional bulleted list.
        [/INST]
        -
        """

        output = analyzer_pipeline(prompt, max_new_tokens=200, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
        
        findings = output[0]['generated_text'].split('[/INST]')[-1].strip()
        
        if not findings.startswith('-'):
            findings = "- " + findings
        
        return findings

    except Exception as e:
        print(f"An error occurred in the analyzer: {e}")
        return "ERROR: Key findings could not be generated."