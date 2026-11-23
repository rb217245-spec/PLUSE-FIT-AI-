# Pulse Fit Plus AI

A premium dark-themed Streamlit wellness demo with:
- Dashboard
- Built-in AI-style workout planner (no API key)
- Nutrition assistant
- Progress charts and activity logging
- Topic-based chatbot
- Demo login/signup

## Run in VS Code

1. Extract the ZIP and open the `Pulse_Fit_Plus_AI` folder in VS Code.
2. Open the VS Code terminal in that folder.
3. (Optional) Create and activate a virtual environment:

   Windows:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

4. Install packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Start the app:
   ```bash
   streamlit run app.py
   ```

6. Streamlit will open the app in your browser. If it does not, open the local URL printed in the terminal (usually http://localhost:8501).

## Important notes

- The built-in assistant is rule-based demo logic; it does not call Gemini, ChatGPT, or another external AI service.
- Login/signup is for demonstration only. It does not securely store accounts or passwords.
- Activity and chat data are stored in Streamlit session state and may reset when the session restarts.
- Wellness suggestions are general information, not medical advice.
