from prompt_engine import generate_draft

def main():
    print("🎯 Tophawks Q3: Email Follow-up Generator")
    print("="*50)
    with open("sample_data/meeting_notes.txt", "r") as f:
        notes = f.read().strip()
    print(f"📝 Meeting Notes:\n{notes}\n")
    draft = generate_draft(notes, lead_name="Raj Patel", company="Acme Corp")
    print(f"✉️  Generated Draft:\n{draft}\n")
    print("="*50)

if __name__ == "__main__":
    main()