# Study Buddy

A modern, LLM-powered quiz and study system that leverages advanced system design patterns for maintainability, extensibility, and robustness.

## 🚀 Features
- **LLM-Powered Quiz Generation:** Uses large language models to generate multiple-choice and fill-in-the-blank questions on any topic and difficulty.
- **System Design Patterns:** Incorporates Factory, Strategy, and Template Method patterns for clean, modular, and extensible code.
- **Beautiful Streamlit UI:** Interactive, user-friendly web interface for quiz taking and results review.
- **Session Management:** Uses Streamlit session state for persistent, multi-step workflows.
- **Result Export:** Download quiz results as CSV files.

## 🏗️ System Design
- **Factory Pattern:** Centralized question creation logic for different question types.
- **Strategy Pattern:** Pluggable evaluation and UI logic for each question type.
- **Template Method Pattern:** Modular quiz workflow steps (generate, attempt, evaluate).
- **Separation of Concerns:** Business logic, UI, and LLM integration are cleanly separated.

## 🛠️ Tech Stack
- **Python 3.12**
- **Streamlit** (frontend/UI)
- **LangChain** (LLM integration)
- **Pydantic** (data validation)
- **Kubernetes** (container orchestration)
- **GCP VM** (cloud hosting)
- **Jenkins** (CI pipeline)
- **ArgoCD** (CD pipeline)

## ⚡ Setup
1. **Clone the repo:**
   ```sh
   git clone https://github.com/yourusername/study_buddy.git
   cd study_buddy
   ```
2. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set up environment variables:**
   - Copy `.env.example` to `.env` and fill in your API keys and settings.

5. **Run the app locally:**
   ```sh
   streamlit run app.py
   ```

## ☸️ Deployment
- **Kubernetes:**
  - Deploy the app using the provided `Dockerfile` and Kubernetes manifests (`manifests/`).
- **GCP VM:**
  - Host your Kubernetes cluster or Jenkins/ArgoCD runners on Google Cloud Platform VMs.
- **Jenkins (CI):**
  - Automated testing, linting, and build pipeline.
- **ArgoCD (CD):**
  - GitOps-based continuous deployment to Kubernetes.

## 📁 Project Structure
```
src/
  models/           # Pydantic models
  generator/        # LLM question factory
  strategy/         # Evaluation and UI strategies
  utils/            # QuizManager and helpers
  prompts/          # Prompt templates
  common/           # Logging, exceptions, constants
  config/           # Settings
app.py              # Streamlit entry point
manifests/          # Kubernetes manifests
Dockerfile          # Container build
.pre-commit-config.yaml
```

## 🤝 Contributing
Pull requests are welcome! Please lint and format your code with pre-commit before submitting.

## 📜 License
MIT License
