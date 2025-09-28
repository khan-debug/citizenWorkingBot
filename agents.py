import vertexai
from vertexai.generative_models import GenerativeModel
import os

# Set up authentication using service account key
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service-account-key.json'

# Initialize Vertex AI with project ID and location
vertexai.init(project="ultimate-realm-473419-c7", location="us-central1") 

def explain_in_plain_language(text_to_explain: str) -> str:
    """
    Uses a generative AI model to rephrase technical text into simple language.
    This is the core of the Explanation Agent.
    """
    try:
        # Using Gemini Pro, which is widely available.
        model = GenerativeModel("gemini-pro") 

        # This prompt is crucial. It tells the AI how to behave.
        prompt = f"""
        You are a helpful assistant for the citizens of Pakistan.
        Your task is to explain things in a very simple, clear, and encouraging way.
        Do not be technical. Use simple English.
        
        Please rephrase the following information for a citizen:

        "{text_to_explain}"
        """

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Fallback explanation if AI model is not available
        return create_fallback_explanation(text_to_explain, str(e))


def create_fallback_explanation(text_to_explain: str, error_message: str) -> str:
    """
    Creates a simple explanation when the AI model is not available.
    This is a fallback function for testing purposes.
    """
    # Simple rule-based explanation for common scenarios
    if "INELIGIBLE" in text_to_explain and "INCOME_EXCEEDS_LIMIT" in text_to_explain:
        return """
        Hello! I'm here to help explain this information in simple terms.
        
        Unfortunately, you are not eligible for the Ehsaas Education Grant because your monthly income 
        is higher than what the program allows. The program is designed to help families with lower incomes.
        
        Don't worry! There might be other programs that could help you. You can check with your local 
        government office for other assistance programs that might be suitable for your situation.
        
        Note: This explanation was generated using basic rules because the AI service is currently 
        not available. Please contact your local government office for more detailed information.
        """
    else:
        return f"""
        Hello! I'm here to help explain this information in simple terms.
        
        The information you received contains some technical details that I would normally explain 
        in simple language, but I'm currently unable to access the AI service that helps me do this.
        
        Here's what I can tell you: {text_to_explain}
        
        For a clearer explanation, please contact your local government office or visit their website.
        They will be able to help you understand this information better.
        
        Note: The AI service is currently unavailable due to: {error_message}
        """


# --- This is a test block to see the agent in action ---
if __name__ == '__main__':
    # This is a sample technical output from a future agent.
    sample_technical_data = """
    {
        "status": "INELIGIBLE",
        "scheme": "Ehsaas Education Grant",
        "reason_code": "INCOME_EXCEEDS_LIMIT",
        "details": "User's monthly income of 35000 is greater than the allowed maximum of 30000."
    }
    """
    
    print("--- Sending technical data to Explanation Agent ---")
    print(sample_technical_data)
    
    explanation = explain_in_plain_language(sample_technical_data)
    
    print("\n--- Plain Language Explanation from Agent ---")
    print(explanation)