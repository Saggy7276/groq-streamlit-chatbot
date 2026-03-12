# 🤖 Groq Chatbot using Streamlit

A simple **multi-turn AI chatbot** built with **Streamlit** and the **Groq API**.  
The app allows users to interact with Groq language models, select models dynamically, and adjust generation parameters.

---

## 🚀 Features

- Multi-turn conversation support
- Dynamic **Groq model selection**
- Adjustable system prompt
- Temperature and Top-P controls
- Token limit configuration
- Persistent chat history
- Clean Streamlit chat interface
- API key managed securely with `.env`

---

## 📂 Project Structure


streamlit-groq-chatbot/
│
├── app.py # Main Streamlit chatbot application
├── requirements.txt # Python dependencies
├── .gitignore # Files ignored by Git
└── README.md # Project documentation


---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Saggy7276/streamlit-groq-chatbot.git
cd streamlit-groq-chatbot
2. Create a virtual environment
Windows
python -m venv venv
venv\Scripts\activate
Mac / Linux
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
🔑 Environment Variables

Create a .env file in the project root:

GROQ_API_KEY=your_groq_api_key_here

You can obtain an API key from the Groq Console.

▶️ Run the Application

Start the Streamlit app:

streamlit run app.py

Then open your browser and go to:

http://localhost:8501
⚙️ Configuration Options

The sidebar allows you to configure:

Setting	Description
API Key	Your Groq API key
Model	Select a Groq language model
System Prompt	Define assistant behavior
Temperature	Controls randomness
Top-P	Controls sampling diversity
Max Tokens	Limits response length
💾 Chat History

Chat messages are stored locally in:

chat_logs.json

This file keeps previous conversations between sessions.

📦 Dependencies

The project uses the following Python packages:

streamlit

groq

requests

python-dotenv

Install them using:

pip install -r requirements.txt
🔒 Security Notes

Never commit your .env file to GitHub

Keep your API keys private

.env is excluded using .gitignore

🔮 Future Improvements

Possible enhancements:

Streaming responses

Conversation export

Authentication system

Deployment to Streamlit Cloud

Model comparison

📜 License

This project is released under the MIT License.

👨‍💻 Author

Sagar
