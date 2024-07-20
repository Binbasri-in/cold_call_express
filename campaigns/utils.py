from django.conf import settings
import logging
import requests
import json

logger = logging.getLogger(__name__)

cloudflare_url = settings.CLOUDFLARE_URL

def generate_text(company_details, product_service, marketing_keywords, language='en'):
    try:
        try:
            prompt = f"""
            Generate only text in a telephony way for a cold call. imagine that you are calling a potential customer regarding the following details:
            Company Details: {company_details}
            Product/Service: {product_service}
            Marketing Keywords: {marketing_keywords}
            
            your name is Sara, now you are calling him, what would you say? (make sure to make your pitch concise, and end it with a question) make sure your response is very short
            Sara:
            """
            data = {'prompt': prompt, 'max_tokens': 100}
            response = requests.post(cloudflare_url, headers={'Authorization': f"Bearer {settings.CLOUDFLARE_API_TOKEN}"},
                                    data=json.dumps(data)).json()
            
            print(response)
            response = response["result"]["response"]
            response.replace("\n", " ").strip()
        except Exception as e:
            logger.error(f"Error generating bot response from Cloudflare: {str(e)}")
            print(e)
            response = "I'm sorry, but I'm currently unable to generate a response."
            
        if language != 'en':
            response = translate_text(response, language)
        return response
    except Exception as e:
        # Instead of print, use Django's logging mechanism
        logger.error(f"Error generating bot response: {str(e)}")
        print(e)
        raise  # Re-raise the exception to be handled by the caller

def translate_text(text, target_language):
    # Implement translation logic here (e.g., using Google Translate API)
    # For now, we'll return the original text
    return text