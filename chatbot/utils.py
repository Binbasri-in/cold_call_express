from django.conf import settings
import logging
import requests
import json

logger = logging.getLogger(__name__)

cloudflare_url = settings.CLOUDFLARE_URL

def generate_bot_response(campaign, user_message, conversation_history, language='en'):
    try:
        conversation_context = "\n".join([f"{'Human' if not msg.is_bot else 'AI'}: {msg.content}" for msg in conversation_history])
        prompt = f"""
        You are an AI assistant for a cold-calling campaign. Use the following information to guide your responses:

        Campaign: {campaign.name}
        Company Details: {campaign.company_details}
        Product/Service: {campaign.product_service}
        Marketing Keywords: {campaign.marketing_keywords}

        Always be polite and professional. If asked about personal information or topics unrelated to the campaign, politely redirect the conversation back to the product or service.

        Previous conversation:
        {conversation_context}

        Human: {user_message}
        AI:"""
        try:
            data = {'prompt': prompt, 'max_tokens': 100, 'temperature': 0.3}
            response = requests.post(cloudflare_url, headers={'Authorization': f"Bearer {settings.CLOUDFLARE_API_TOKEN}"},
                                    data=json.dumps(data)).json()
            print(response["result"]["response"])
            bot_response = response["result"]["response"]
        except Exception as e:
            logger.error(f"Error generating bot response from Cloudflare: {str(e)}")
            bot_response = "I'm sorry, but I'm currently unable to generate a response."
            
        if language != 'en':
            bot_response = translate_text(bot_response, language)
        return bot_response
    except Exception as e:
        # Instead of print, use Django's logging mechanism
        logger.error(f"Error generating bot response: {str(e)}")
        raise  # Re-raise the exception to be handled by the caller

def translate_text(text, target_language):
    # Implement translation logic here (e.g., using Google Translate API)
    # For now, we'll return the original text
    return text