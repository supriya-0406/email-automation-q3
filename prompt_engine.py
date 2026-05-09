# prompt_engine.py — Email follow-up generator with graceful fallback
import os
import re

# Try to load OpenAI (optional)
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Load API key (optional)
API_KEY = os.getenv("OPENAI_API_KEY")
USE_OPENAI = OPENAI_AVAILABLE and API_KEY and len(API_KEY) > 10

SYSTEM_PROMPT = """
You are a sales operations assistant for a B2B SaaS company.
Your task: Draft a personalized 3-sentence follow-up email based on meeting notes.

Rules:
1. Tone: Professional but warm, concise (max 3 sentences)
2. Must include: 
   - Reference to last discussion topic
   - Specific next step with timeline
   - Clear call-to-action
3. Personalize using company/role context if provided
4. Output format: Plain text email body ONLY (no subject line, no JSON)
"""

def _generate_template_fallback(meeting_notes: str, lead_name: str, company: str) -> str:
    """
    Template-based fallback — guarantees execution without API keys.
    Uses keyword extraction for basic personalization.
    """
    # Extract topic from notes (simple heuristic)
    topic = "our platform"
    notes_lower = meeting_notes.lower()
    if "analytics" in notes_lower: topic = "the analytics module"
    elif "pricing" in notes_lower or "budget" in notes_lower: topic = "pricing options"
    elif "demo" in notes_lower: topic = "the product demo"
    elif "integration" in notes_lower: topic = "integration capabilities"
    elif "security" in notes_lower: topic = "security features"
    
    # Extract next step (simple heuristic)
    next_step = "schedule a follow-up call"
    if "demo" in notes_lower: next_step = "schedule the technical demo"
    elif "case study" in notes_lower or "deck" in notes_lower: next_step = "send the case study and pricing deck"
    elif "proposal" in notes_lower: next_step = "send the formal proposal"
    
    return (
        f"Hi {lead_name}, great discussing {topic} for {company} yesterday. "
        f"As next steps, I'll {next_step} by EOD tomorrow. "
        f"Could we schedule a 15-min sync next Tuesday to align on rollout? Best, [Your Name]"
    )

def _generate_with_openai(meeting_notes: str, lead_name: str, company: str) -> str:
    """
    OpenAI-powered generation — used when API key is available and quota permits.
    """
    if not USE_OPENAI:
        raise RuntimeError("OpenAI not available or API key not set")
    
    client = OpenAI(api_key=API_KEY)
    user_prompt = f"""
    Lead: {lead_name} at {company}
    Meeting Notes: {meeting_notes}
    
    Draft the follow-up email (3 sentences max, professional tone):
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

def generate_follow_up(meeting_notes: str, lead_name: str = "there", company: str = "") -> str:
    """
    Main entry point: tries OpenAI first, falls back to template if:
    - No API key
    - API unavailable
    - Quota exceeded
    - Any other error
    """
    if USE_OPENAI:
        try:
            return _generate_with_openai(meeting_notes, lead_name, company)
        except Exception as e:
            error_msg = str(e).lower()
            # Log specific errors for debugging
            if "quota" in error_msg or "insufficient_quota" in error_msg:
                print(f"⚠️  OpenAI quota exceeded — using template fallback")
            elif "api key" in error_msg or "authentication" in error_msg:
                print(f"⚠️  OpenAI auth error — using template fallback")
            else:
                print(f"⚠️  OpenAI error ({type(e).__name__}) — using template fallback")
            # Fall through to template
    else:
        print("ℹ️  OpenAI not configured — using template fallback")
    
    return _generate_template_fallback(meeting_notes, lead_name, company)

if __name__ == "__main__":
    # Test with sample data
    notes = "Discussed Q2 expansion plans. They need analytics module. Budget approved. Next: send case study + schedule demo."
    draft = generate_follow_up(notes, lead_name="Raj", company="Acme Corp")
    print("📧 Generated Email Draft:\n", draft)
