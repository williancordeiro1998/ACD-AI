# 🛡️ ACD-AI: Autonomous Cyber Defense System

> An autonomous, AI-driven incident response platform that detects, analyzes, and mitigates cyber threats in real-time using Serverless Architecture and Google Gemini Pro.

![AWS](https://img.shields.io/badge/AWS-Serverless-orange?style=flat&logo=amazon-aws)
![AI](https://img.shields.io/badge/AI-Google%20Gemini%20Pro-blue?style=flat&logo=google)
![Python](https://img.shields.io/badge/Python-3.11-yellow?style=flat&logo=python)
![Status](https://img.shields.io/badge/Status-MVP%20Complete-green)

## 🚀 Overview

**ACD-AI** addresses the critical challenge of "alert fatigue" in modern Security Operations Centers (SOCs). Instead of relying solely on static rules or manual human analysis, this system ingests security logs, leverages Large Language Models (LLMs) to understand attack intent/context, and orchestrates automated response actions.

It demonstrates a modern **Cloud-Native** approach to security, combining **Event-Driven Architecture** with **Generative AI**.

## 📸 Live Evidence

### End-to-End Execution (AWS Console Proof)
The screenshot below demonstrates a successful full cycle execution:
1.  **Visual Workflow (Left):** AWS Step Functions successfully orchestrating the *ThreatDetector* and *DefenseExecutor* Lambdas.
2.  **Audit Log (Right):** The system output showing the AI correctly identifying the SQL Injection (`"malicious": true`) and the Defense Executor triggering a blocking action in Dry-Run mode (`"status": "BLOCKED"`).

![AWS Execution Proof](assets/aws-execution-proof.png)

## 🧠 Key Differentiators

* **Cognitive Threat Analysis:** Unlike traditional WAFs that use RegEx, ACD-AI understands context (e.g., obfuscated SQL payloads, semantic attacks).
* **Serverless Orchestration:** Fully decoupled architecture using **AWS Step Functions**, ensuring state management, retries, and audit trails.
* **Cost-Efficient Scaling:** Zero idle cost. Resources (Lambda, DynamoDB) scale down to zero when no threats are detected.
* **Safety First:** Implements a "Dry-Run" mode for the Defense Executor to prevent accidental self-blocking during testing.

## 🛠️ Technical Architecture

The system follows a strict microservices pattern orchestrated by a State Machine:

1.  **Ingress Layer (API Gateway + Lambda):**
    * Receives raw security logs (Webhooks/JSON).
    * Validates payload integrity and triggers the workflow.
2.  **Orchestrator (AWS Step Functions):**
    * Manages the lifecycle of the incident analysis.
    * Handles error handling and flow control.
3.  **Threat Detector Agent (Lambda + Google Gemini):**
    * Analyzes the log using a specialized security prompt.
    * Returns a classification (Malicious/Safe), confidence score, and reasoning.
4.  **Defense Executor (Lambda):**
    * Reads the AI verdict.
    * Executes mitigation actions (e.g., WAF IP Block, User Suspension).
    * *Currently operating in Dry-Run mode for demonstration.*

## 💻 Tech Stack

* **Cloud Provider:** AWS (US-East-1)
* **Infrastructure as Code:** Serverless Framework v3
* **Runtime:** Python 3.11
* **AI Model:** Google Gemini 2.0 Flash (via REST API)
* **Database:** DynamoDB (Audit Logs)
* **Observability:** Amazon CloudWatch

## 🚀 How to Run

### Prerequisites
* Node.js & NPM
* Serverless Framework (`npm install -g serverless`)
* Python 3.11
* AWS CLI configured
* Google AI Studio API Key

### Deployment

1.  **Clone the repository:**
    ```bash
    git clone [https://https://github.com/williancordeiro1998/acd-ai.git](https://https://github.com/williancordeiro1998/acd-ai.git)
    cd acd-ai
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    pip install -r requirements.txt
    ```

3.  **Deploy to AWS:**
    ```bash
    npx serverless deploy
    ```

## 📝 Author

Developed by **Willian Cordeiro**.
*Full-Stack Developer passionate about Cloud Security and AI Agents.*