"""
detector.py — Shared phishing detection logic
Used by both app.py (Flask) and streamlit_app.py (Streamlit)
Team DarkByte | K.R. Mangalam University | B.Tech Minor Project
"""

import re

# ──────────────────────────────────────────────
#  URL ANALYSIS
# ──────────────────────────────────────────────

URL_PHISHING_KEYWORDS = [
    "login", "verify", "secure", "account", "update", "confirm",
    "bank", "paypal", "ebay", "amazon", "signin", "password",
    "credential", "validation", "suspended", "billing", "payment",
    "free", "prize", "winner", "lucky", "click", "urgent",
]

IP_PATTERN = re.compile(r"https?://(\d{1,3}\.){3}\d{1,3}")


def analyze_url(url: str) -> dict:
    score = 0
    reasons = []
    url_lower = url.lower()

    if len(url) > 75:
        score += 20
        reasons.append("Unusually long URL")
    elif len(url) > 54:
        score += 10
        reasons.append("Above-average URL length")

    if "@" in url:
        score += 20
        reasons.append("Contains '@' symbol (common phishing trick)")

    domain_part = url.split("/")[2] if "/" in url else url
    if domain_part.count("-") >= 3:
        score += 15
        reasons.append("Multiple hyphens in domain")
    elif domain_part.count("-") >= 1:
        score += 5

    if not url_lower.startswith("https://"):
        score += 15
        reasons.append("URL does not use HTTPS")

    matched_keywords = [kw for kw in URL_PHISHING_KEYWORDS if kw in url_lower]
    if matched_keywords:
        score += min(len(matched_keywords) * 8, 30)
        reasons.append(f"Suspicious keywords: {', '.join(matched_keywords[:4])}")

    dot_count = url_lower.count(".")
    if dot_count >= 4:
        score += 15
        reasons.append(f"Excessive subdomains ({dot_count} dots)")
    elif dot_count >= 3:
        score += 7

    if IP_PATTERN.match(url_lower):
        score += 25
        reasons.append("IP address used instead of a domain name")

    suspicious_tlds = [".tk", ".ml", ".ga", ".cf", ".gq", ".xyz", ".pw", ".top"]
    if any(url_lower.endswith(t) or (t + "/") in url_lower for t in suspicious_tlds):
        score += 20
        reasons.append("High-risk top-level domain (TLD) detected")

    path = "/" + "/".join(url.split("/")[3:]) if "/" in url else ""
    if "//" in path:
        score += 10
        reasons.append("Suspicious double slashes in URL path")

    shorteners = ["bit.ly", "tinyurl", "goo.gl", "t.co", "ow.ly", "short.link"]
    if any(s in url_lower for s in shorteners):
        score += 20
        reasons.append("URL shortener service detected")

    confidence = min(score, 100)
    verdict = "Phishing" if confidence >= 40 else "Legitimate"
    if not reasons:
        reasons.append("No strong phishing indicators found")
    reason_text = "; ".join(reasons[:3])
    if verdict == "Legitimate":
        reason_text = "URL appears safe — " + reason_text
    return {"verdict": verdict, "confidence": confidence, "reason": reason_text, "flags": reasons}


# ──────────────────────────────────────────────
#  EMAIL ANALYSIS
# ──────────────────────────────────────────────

EMAIL_URGENT_KEYWORDS = [
    "urgent", "immediately", "verify now", "act now",
    "click here", "winner", "won", "prize", "limited time",
    "account suspended", "account blocked", "unusual activity",
    "confirm your", "update your", "verify your", "congratulations",
    "free gift", "no cost", "risk free", "100% free", "guaranteed",
    "dear customer", "dear user", "dear account holder",
    "your account will be", "will be terminated", "will be suspended",
    "click the link", "click below", "log in now", "sign in now",
    "we have noticed", "suspicious activity", "unauthorized access",
]


def analyze_email(content: str) -> dict:
    score = 0
    reasons = []
    content_lower = content.lower()

    matched_urgent = [kw for kw in EMAIL_URGENT_KEYWORDS if kw in content_lower]
    if matched_urgent:
        score += min(len(matched_urgent) * 7, 40)
        reasons.append(f"Urgency/manipulation phrases: '{', '.join(matched_urgent[:3])}'")

    url_pattern = re.findall(r"http[s]?://\S+", content)
    if len(url_pattern) >= 3:
        score += 20
        reasons.append(f"Multiple links embedded ({len(url_pattern)} found)")
    elif len(url_pattern) >= 1:
        score += 8
        reasons.append(f"Link embedded in email ({len(url_pattern)} found)")

    for link in url_pattern:
        if IP_PATTERN.match(link.lower()):
            score += 20
            reasons.append("Embedded link uses raw IP address")
            break
        if any(t in link.lower() for t in [".tk", ".ml", ".ga", ".cf", ".xyz", ".pw"]):
            score += 15
            reasons.append("Embedded link has high-risk TLD")
            break

    generic_greetings = ["dear customer", "dear user", "dear valued", "dear account", "hello user"]
    if any(g in content_lower for g in generic_greetings):
        score += 15
        reasons.append("Generic/impersonal greeting detected")

    personal_info_keywords = ["password", "ssn", "social security", "credit card",
                               "bank account", "pin number", "cvv", "date of birth"]
    matched_personal = [k for k in personal_info_keywords if k in content_lower]
    if matched_personal:
        score += min(len(matched_personal) * 12, 25)
        reasons.append(f"Requesting sensitive info: {', '.join(matched_personal[:2])}")

    obfuscation_words = re.findall(r"[a-z]*[0-9]+[a-z]+|[a-z]+[0-9]+[a-z]*", content_lower)
    if len(obfuscation_words) >= 2:
        score += 10
        reasons.append("Letter-number substitution (obfuscation) detected")

    caps_phrases = re.findall(r"\b[A-Z]{4,}\b", content)
    if len(caps_phrases) >= 3:
        score += 10
        reasons.append(f"Excessive capitalization ({len(caps_phrases)} instances)")

    prize_patterns = ["you have been selected", "you are a winner", "claim your prize",
                       "you won", "cash prize", "gift card"]
    if any(p in content_lower for p in prize_patterns):
        score += 25
        reasons.append("Lottery/prize scam language detected")

    threat_keywords = ["legal action", "arrest", "prosecute", "report to authorities",
                        "fine", "penalty", "court", "your account will be deleted"]
    if any(t in content_lower for t in threat_keywords):
        score += 20
        reasons.append("Threatening language detected")

    word_count = len(content.split())
    if word_count < 30 and len(url_pattern) >= 1:
        score += 15
        reasons.append("Suspiciously brief email with embedded link")

    confidence = min(score, 100)
    verdict = "Phishing" if confidence >= 35 else "Legitimate"
    if not reasons:
        reasons.append("No strong phishing indicators found in email content")
    reason_text = "; ".join(reasons[:3])
    if verdict == "Legitimate":
        reason_text = "Email appears safe — " + reason_text
    return {"verdict": verdict, "confidence": confidence, "reason": reason_text, "flags": reasons}
