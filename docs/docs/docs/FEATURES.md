# Features and Implementation Status

Status key: **Implemented** / **Partial** / **Unverified** (not yet checked in the real app). Verification steps are in [TESTING.md](TESTING.md).

| Feature | Behavior | Status |
|---|---|---|
| Voice-first home | Prominent Tap to Speak control and a typing box | Implemented |
| Tamil, English, Tanglish | Language detection and replies in all three | Implemented |
| Personalization | Remembers user-approved preferences | Unverified |
| Reminders | Add, edit and delete medicine and appointment reminders | Implemented |
| Family contacts | Trusted caregiver and doctor details | Implemented |
| SOS | User-started call links for 112, 108 and a family contact | Unverified |
| Relaxation music | Calming audio by category, generated in the browser | Implemented |
| Medicine scanner | Label analysis (see the note below) | Unverified |

## Safety notes
- **SOS is user-initiated.** The app shows `tel:` call links that the user taps. It does not call, message or predict emergencies by itself.
- **Medicine scanner:** with a Gemini key it analyses the photo. Without a key it returns built-in demo medicine information, so the result is not read from the photo. It always advises confirming with a doctor or pharmacist.
- **Demo data:** the sample profile (Kalyani Ramanathan, family and doctor) is fictional. No real personal, medical or contact data is included.
- **Offline use:** without an API key or internet, THUNAI falls back to built-in rules.
- **Consent:** personal preferences are saved only when the user approves them.

Project limits (not a diagnostic or emergency service) are in [PROBLEM_AND_SOLUTION.md](PROBLEM_AND_SOLUTION.md).
