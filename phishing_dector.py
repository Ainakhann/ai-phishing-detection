# phishing_detector.py

def load_keywords():
    with open("security_rules/phishing_keywords.txt", "r") as file:
        return [line.strip().lower() for line in file]

def check_phishing(message, keywords):
    message = message.lower()
    for word in keywords:
        if word in message:
            return "⚠️ Phishing Detected"
    return "✅ Safe Message"

# Load security rules
phishing_keywords = load_keywords()

# User input
msg = input("Enter email/message: ")

# Security check
result = check_phishing(msg, phishing_keywords)
print("Security Status:", result)
