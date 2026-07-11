
# 🔬 AI Medicine & Pesticide Verifier

A Streamlit web application that uses Google Gemini AI (`gemini-3.5-flash`) to extract pesticide or medicine names from uploaded images and verifies their approval status (Approved/Banned) against a local dataset.

## 📋 Prerequisites

Before you begin, ensure you have the following:
* **Python 3.9 or higher** installed on your machine.
* A **Google Gemini API Key**. You can generate one for free from [Google AI Studio](https://aistudio.google.com/).

---

## 🛠️ Local Development Setup

Follow these steps to download and run the project on your local machine.

### 1. Clone the Repository
Open your terminal and clone the project directly from GitHub:
```bash
# clone repository
git clone https://github.com/aungkoman/pesticides.git
# go to project
cd pesticides

```

### 2. Create a Virtual Environment (Recommended)

It is best practice to use a virtual environment to manage dependencies and avoid conflicts.

```bash
# Create the virtual environment named .venv
python -m venv .venv

# Activate the virtual environment on Windows:
.venv\Scripts\activate

# Activate the virtual environment on Mac/Linux:
source .venv/bin/activate

```

### 3. Install Dependencies

Install the required Python packages using the provided `requirements.txt` file.

```bash
pip install -r requirements.txt

```

### 4. Configure Your API Key

This project uses Streamlit's secrets manager to securely handle API keys. **Do not** write your API key directly into the code.

1. Create a hidden folder named `.streamlit` in the root directory of the project.
2. Inside that folder, create a file named `secrets.toml`.
3. Add your Gemini API key to the file like this:

**`.streamlit/secrets.toml`**

```toml
GEMINI_API_KEY = "your_actual_api_key_here"

```

*(Note: The `.streamlit` folder is typically ignored by Git, ensuring your key remains safe and private).*

---

## 🚀 Running the App

Once your environment is set up and your API key is configured, start the Streamlit server:

```bash
streamlit run app.py

```

The app will automatically open in your default web browser at `http://localhost:8501`.

---

## 📁 Project Structure

* `app.py`: Main Streamlit application script.
* `final.csv`: Dataset containing pesticide/medicine statuses.
* `requirements.txt`: List of required Python dependencies.


```text
Pesticides/
│
├── app.py                # Main Streamlit application script
├── final.csv             # Dataset containing pesticide/medicine statuses
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
│
├── .streamlit/           # Streamlit configuration folder (DO NOT COMMIT to Git)
│   └── secrets.toml      # Local secrets (API Key)
│
└── .gitignore            # Git ignore file (should include .streamlit/)

```
