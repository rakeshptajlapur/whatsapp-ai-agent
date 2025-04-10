from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from twilio.rest import Client
import json
from datetime import datetime, timedelta
from django.utils import timezone
from openai import OpenAI
from .models import ChatMessage, TrainingContent
from .training.agency_rules import AGENCY_RULES
import os


client_twilio = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
client_openai = OpenAI(api_key=settings.OPENAI_API_KEY)



def get_chat_history(sender, limit=10):
    messages = ChatMessage.objects.filter(sender=sender).order_by('-timestamp')[:limit]
    history = []
    for msg in messages:
        history.extend([
            {"role": "user", "content": msg.message},
            {"role": "assistant", "content": msg.response}
        ])
    return history[::-1]  # Reverse to get chronological order

def get_system_prompt():
    """Generate system prompt from active training content"""
    training_content = TrainingContent.objects.filter(is_active=True)
    
    prompt_sections = []
    
    # Add business rules
    rules = training_content.filter(content_type='rules')
    if (rules.exists()):
        prompt_sections.append("BUSINESS RULES:")
        for rule in rules:
            prompt_sections.append(rule.content)
    
    # Add FAQs
    faqs = training_content.filter(content_type='faq')
    if (faqs.exists()):
        prompt_sections.append("FREQUENTLY ASKED QUESTIONS:")
        for faq in faqs:
            prompt_sections.append(faq.content)
    
    # Add other sections...
    
    return "\n\n".join(prompt_sections)

def get_ai_response(message, sender):
    try:
        # Check for hosting-related queries first
        if any(word in message.lower() for word in ['hosting', 'domain', 'ssl', 'cpanel']):
            return "For hosting and domain related queries, please visit codesiddhi.space or use the live chat on our official website. 🌐"

        chat_history = get_chat_history(sender)
        
        system_prompt = f"""You are CodeBot, a friendly AI support assistant for Codesiddhi Technologies LLP. 🤖

{get_system_prompt()}

PERSONALITY & COMMUNICATION STYLE:
- Be warm, friendly, and conversational like a helpful team member 😊
- Start responses with friendly greetings or acknowledgments
- Show enthusiasm for helping the customer
- Use natural language and gentle tone
- Add relevant emojis but don't overdo it
- Keep responses under 100 words
- Always reference our policies/services but explain them in a friendly way
- When saying no, be empathetic and offer alternatives
- End messages with encouraging or supportive notes
- Remember past conversations to build rapport

EXAMPLES:
❌ "Our basic plan costs $99."
✅ "I'd be happy to tell you about our basic plan! It's $99, and you'll get great features like... 😊"

❌ "We don't do Shopify work."
✅ "While we don't work with Shopify (we want to be upfront about that!), we'd love to help you build an amazing custom WordPress store instead! 🛍️"

Remember: Be professional but friendly, like a helpful colleague they can trust! 🤝"""

        # Format messages with history
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add chat history if available
        if chat_history:
            messages.extend(chat_history)
            
        # Add current message
        messages.append({"role": "user", "content": message})

        # Get OpenAI response
        response = client_openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=200,  # Increased token limit
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        
        # Save conversation
        ChatMessage.objects.create(
            sender=sender,
            message=message,
            response=ai_response
        )
        
        return ai_response
            
    except Exception as e:
        print(f"OpenAI Error: {str(e)}")
        return "I'm having a brief technical hiccup. Please try again or reach out to our team at support@codesiddhi.com 🙏"

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        try:
            # Log incoming request data
            print("Incoming webhook data:", request.POST)
            
            incoming_msg = request.POST.get('Body', '')
            sender = request.POST.get('From', '')

            if not sender or not incoming_msg:
                print("Error: Missing sender or message")
                return HttpResponse('Missing parameters', status=400)

            if not sender.startswith('whatsapp:'):
                sender = f'whatsapp:{sender}'

            print(f"Processing message from {sender}: {incoming_msg}")
            
            # Get AI response
            ai_response = get_ai_response(incoming_msg, sender)
            if not ai_response:
                print("Error: No response from AI")
                return HttpResponse('AI response error', status=500)
                
            # Send WhatsApp response
            try:
                response = client_twilio.messages.create(
                    from_=settings.WHATSAPP_NUMBER,
                    body=ai_response,
                    to=sender
                )
                print(f"Twilio response sent: {response.sid}")
                return HttpResponse('OK')
            except Exception as twilio_error:
                print(f"Twilio Error: {str(twilio_error)}")
                return HttpResponse(f'Twilio error: {str(twilio_error)}', status=500)
                
        except Exception as e:
            print(f"Webhook Error: {str(e)}")
            return HttpResponse(f'Server error: {str(e)}', status=500)
    
    return HttpResponse('Method not allowed', status=405)

def test_message(request):
    try:
        # Test with template
        message = client_twilio.messages.create(
            from_=settings.WHATSAPP_NUMBER,
            content_sid='HX53e3f15f94e0242740f1f8daa9c5b56f',
            to='whatsapp:+918970175205'
        )
        return HttpResponse(f'Template message sent! SID: {message.sid}')
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}', status=500)

@csrf_exempt
def test_openai(request):
    try:
        test_response = get_ai_response("Tell me about your services", "test_sender")
        return HttpResponse(f"OpenAI Test Response: {test_response}")
    except Exception as e:
        return HttpResponse(f"OpenAI Test Failed: {str(e)}", status=500)

def debug_info(request):
    try:
        chat_count = ChatMessage.objects.count()
        last_message = ChatMessage.objects.last()
        return JsonResponse({
            'environment': 'render' if os.getenv('RENDER') else 'local',
            'database_connected': True,
            'message_count': chat_count,
            'last_message_time': str(last_message.timestamp) if last_message else None,
            'twilio_configured': bool(settings.TWILIO_ACCOUNT_SID),
            'openai_configured': bool(settings.OPENAI_API_KEY)
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'status': 'database_not_connected'
        }, status=500)
