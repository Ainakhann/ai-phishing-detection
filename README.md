<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" />
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" />
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" />
  
  <h1>🛡️ DarkByte — AI Phishing Detection System</h1>
  <p><strong>A Real-Time, Rule-Based Threat Analysis Engine for URLs and Emails</strong></p>
  <p><em>Developed for B.Tech Minor Project · Team DarkByte · K.R. Mangalam University · CSE Department</em></p>
</div>

---

## 📖 Overview

The **DarkByte AI Phishing Detection System** is a lightweight, high-performance web application designed to defend against cyber threats in real-time. By leveraging an intelligent, rule-based feature extraction engine, the system analyzes suspicious URLs and email content to determine their legitimacy, providing users with a comprehensive **Verdict**, **Confidence Score**, and **Detailed Flag Report**.

Features a stunning **Dark Cyberpunk UI** and offers dual-deployment options: a dedicated **Streamlit app** or a **Flask + HTML API architecture**.

---

## ✨ Key Features

- **🌐 Comprehensive URL Analysis:** Detects unusually long URLs, IP address usage, malicious TLDs (e.g., `.tk`, `.ml`), missing HTTPS, multi-subdomains, and embedded phishing keywords.
- **📧 Deep Email Scanning:** Identifies generic greetings, urgency tactics, lottery/scam language, embedded malicious links, and personal data extraction attempts.
- **⚡ Real-Time Scoring Engine:** Multi-factor risk scoring system assigns a 0–100% confidence rating based on localized feature weights.
- **🎨 State-of-the-Art UI:** Includes animated confidence metering, scan-line effects, and a responsive dark-mode cyber design.
- **🔌 Developer-Ready API:** Comes with a ready-to-use Flask `/predict` endpoint that returns structured JSON payloads for frontend integration.

---

## 📁 Project Architecture

```text
Phising_Detector/
├── detector.py         ← Core Detection Engine (Shared Logic)
├── streamlit_app.py    ← Modern Streamlit Frontend Interface
├── app.py              ← API Backend (Flask Framework)
├── index.html          ← Vanilla HTML/JS Frontend (Connects to Flask)
├── requirements.txt    ← Project Dependencies
└── README.md           ← Project Documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python 3.8+ installed on your system.

### 2. Installation
Clone the repository and install the required dependencies:
```bash
git clone https://github.com/hunny0025/Phising_Detector.git
cd Phising_Detector
pip install -r requirements.txt
```

---

### 3. Running the Application (Two Options)

#### ▶ Option A: Streamlit Unified App (Recommended)
This launches the application using the dynamic Streamlit interface.
```bash
streamlit run streamlit_app.py
```
*Access the app at: **http://localhost:8501***

#### ▶ Option B: Flask API + HTML Frontend
Launch the Flask server, which serves both the API endpoints and the `index.html` frontend.
```bash
python app.py
```
*Access the app at: **http://127.0.0.1:5000***

---

## 🔌 API Documentation

For developers looking to integrate the engine into other services, DarkByte provides a REST API via Flask.

**Endpoint:** `POST /predict`

### Example Request (URL)
```json
{
  "type": "url",
  "content": "http://secure-login.bank-verify.tk/@account/update"
}
```

### Example Request (Email)
```json
{
  "type": "email",
  "content": "Dear Customer, URGENT: Your account has been suspended. Click here to verify your credit card details immediately."
}
```

### Example Response
```json
{
  "verdict": "Phishing",
  "confidence": 100,
  "reason": "Urgency/manipulation phrases: 'urgent'; Requesting sensitive info: 'credit card'",
  "flags": [
    "Urgency/manipulation phrases: 'urgent'",
    "Generic/impersonal greeting detected",
    "Requesting sensitive info: credit card"
  ]
}
```

---

## 🧠 Threat Scoring Logic (`detector.py`)

The application processes text sequentially and aggregates risk scores:

| Trigger Feature | Assigned Risk Score |
| :--- | :--- |
| **URL Flags** | |
| Target IP instead of Domain | +25 Points |
| Critical Phishing Keywords | +8 Points (capped at 30) |
| Known Dangerous TLD | +20 Points |
| Uses `@` symbol trick | +20 Points |
| **Email Flags** | |
| Posing as Lottery/Prize | +25 Points |
| Severe Threat Language | +20 Points |
| Multi-embedded URLs | +20 Points |
| Requests Sensitive Data | +12 Points per occurrence |

**Verdict Thresholds:**  
`[Url ≥ 40 Points]` ➔ ⚠️ Phishing  
`[Email ≥ 35 Points]` ➔ ⚠️ Phishing

---

## ⚠️ Disclaimer
This tool was developed strictly for educational and academic purposes as part of a B.Tech Minor Project by Team DarkByte (K.R. Mangalam University). It is not intended as a substitute for enterprise-grade security appliances, and its creators assume no liability for missed threats in production environments.
