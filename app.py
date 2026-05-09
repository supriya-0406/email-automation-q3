# app.py — Main entry point for Q3 email automation
from prompt_engine import generate_follow_up

def main():
    print("🎯 Tophawks Q3: AI Email Follow-up Generator")
    print("=" * 60)
    
    # Load sample meeting notes
    with open("sample_data/meeting_notes.txt", "r") as f:
        notes = f.read().strip()
    
    print(f"📝 Input Meeting Notes:\n{notes}\n")
    
    # Generate email draft
    draft = generate_follow_up(
        meeting_notes=notes,
        lead_name="Raj Patel",
        company="Acme Corp"
    )
    
    print(f"✉️  Generated Follow-up Email:\n{draft}\n")
    print("=" * 60)
    print("✅ Done. In production: draft → Gmail/CRM draft folder via API")

if __name__ == "__main__":
    main()
