# analyzer.py
from transformers import pipeline

def generate_key_findings(description: str, clean_text: str) -> str:
    """
    Uses an LLM to generate key security findings based on a file's
    description and cleansed text content.
    """
    print("Generating key findings with LLM...")
    try:
        # We use a text-generation model to act as our security analyst
        # distilgpt2 is a good starting point. For higher quality, you could
        # explore models like 'mistralai/Mistral-7B-v0.1' if you have the resources.
        analyzer = pipeline("text-generation", model="distilgpt2")

        # Create a detailed prompt for the AI
        prompt = f"""
        Analyze the following document for potential security insights.
        
        Document Description: {description}
        
        Document Content: {clean_text[:1000]}
        
        Based on the description and content, list 3 to 4 key findings or security implications in bullet points:
        -
        """

        output = analyzer(prompt, max_length=200, num_return_sequences=1)
        # Clean up the output to only get the generated bullet points
        findings = output[0]['generated_text'].split('-')[-1].strip()
        
        # Prepend a dash to the first finding if it's missing
        if not findings.startswith('-'):
            findings = "- " + findings
        
        return findings

    except Exception as e:
        print(f"An error occurred in the analyzer: {e}")
        return "ERROR: Key findings could not be generated."
