SYSTEM_PROMPT = """
You are a B2B sales assistant. Draft a personalized 3-sentence follow-up email.
Rules:
1. Tone: Professional, warm, concise
2. Must include: reference to last discussion, specific next step, clear CTA
3. Output: Plain text ONLY (no JSON, no subject line)
"""

def generate_draft(meeting_notes: str, lead_name: str, company: str) -> str:
    """Template fallback that guarantees execution without API keys"""
    topic = "our platform"
    if "analytics" in meeting_notes.lower(): topic = "the analytics module"
    elif "pricing" in meeting_notes.lower(): topic = "pricing options"
    elif "demo" in meeting_notes.lower(): topic = "the product demo"
    
    return (
        f"Hi {lead_name}, great discussing {topic} for {company} yesterday. "
        f"As a next step, I'll send the enterprise case study and implementation timeline by EOD tomorrow. "
        f"Could we schedule a 15-min sync next Tuesday to align on rollout? Best, [Your Name]"
    )

# To use real OpenAI: uncomment below & set OPENAI_API_KEY in your terminal
"""
import os
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def generate_draft(meeting_notes: str, lead_name: str, company: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Lead: {lead_name} @ {company}\nNotes: {meeting_notes}"}
        ], temperature=0.3
    )
    return response.choices[0].message.content.strip()
"""