# WhatsApp AI Support Agent V1

AI-powered WhatsApp support agent using OpenAI GPT and Twilio WhatsApp Business API.

## Features
- 🤖 AI-powered responses using OpenAI GPT-3.5
- 💬 WhatsApp integration via Twilio
- 📝 Chat history tracking
- 🎯 Context-aware responses
- 🏢 Business rules integration
- ⚡ Quick hosting query redirection

## Project Structure
```
whatsapp_agent/
├── bot/
│   ├── training/
│   │   └── agency_rules.py    # Business rules and policies
│   ├── admin.py              # Django admin configuration
│   ├── models.py            # Database models
│   ├── urls.py             # URL routing
│   └── views.py           # Core logic and API endpoints
├── whatsapp_agent/
│   └── settings.py       # Project settings
└── manage.py
```

## Setup

1. Clone repository
```bash
git clone https://github.com/rakeshptajlapur/whatsapp-ai-agent.git
cd whatsapp-ai-agent
```

2. Create and activate virtual environment
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
```bash
cp .env.example .env
# Update .env with your credentials
```

5. Run migrations
```bash
python manage.py migrate
```

6. Start development server
```bash
python manage.py runserver 8080
```

## Environment Variables
Required variables in `.env`:
```bash
DJANGO_SECRET_KEY=your_secret_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
OPENAI_API_KEY=your_openai_key
WHATSAPP_NUMBER=whatsapp:+1234567890
DEBUG=True
```

## API Endpoints
- `/bot/webhook/` - Twilio WhatsApp webhook
- `/bot/test-openai/` - Test OpenAI integration

## Business Rules
The AI agent follows business rules defined in `bot/training/agency_rules.py`:
- Company achievements and stats
- Service offerings and limitations
- Pricing and packages
- Project workflow and milestones
- Payment terms and policies
- Communication channels
- Support protocols

## Testing
1. Test OpenAI integration:
```bash
curl http://localhost:8080/bot/test-openai/
```

2. Test WhatsApp webhook:
- Set up Twilio webhook URL to `your-domain/bot/webhook/`
- Send a message to your WhatsApp business number
- Check Django admin for message logs

## Future Versions
- V2: Ticketing system integration
- V3: Project board access

## Error Handling
- Graceful handling of API failures
- Chat history persistence
- Automatic hosting query redirection
- Comprehensive error logging

## License
MIT License

## Authors
- Rakesh Kumar T (@rakeshptajlapur)
- rakesh@codesiddhi.com