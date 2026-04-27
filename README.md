# ✉️ Tophawks Q3: AI Email Follow-up Automation

Generates personalized sales follow-ups from meeting notes. **Runs instantly without API keys** using template fallback; switches to OpenAI when configured.

## ✨ Features
- ✅ **Graceful fallback**: Works without OpenAI API key or quota
- ✅ **Production-ready**: Clean separation of template vs. LLM logic
- ✅ **Error handling**: Catches quota, auth, and network errors gracefully
- ✅ **Personalization**: Keyword-based topic extraction for template mode

## 🚀 How to Run

### Option 1: Without API Key (Template Fallback — Recommended for Demo)
```bash
pip install -r requirements.txt
python app.py
