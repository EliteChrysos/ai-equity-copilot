# 🚀 AI Equity Research Copilot

👉 Live Demo: https://ai-equity-copilot-pkj9gg4vwbl222pj9kwmyx.streamlit.app/

AI Equity Research Copilot is an end-to-end investment analysis platform that combines financial data, document intelligence (RAG), valuation models, and large language models to help users analyze stocks faster and more intelligently.

Built with Python and Streamlit, this tool simulates a lightweight equity research workflow—making it useful for investors, students, and aspiring analysts.

---

## 📌 Why This Project?

Traditional equity research is:

- Time-consuming  
- Data-heavy  
- Requires multiple tools  

This app brings everything into one unified interface, allowing users to:

- Analyze companies instantly  
- Generate AI-powered research reports  
- Perform valuation (DCF)  
- Compare companies  
- Track portfolios  
- Understand market sentiment  
- Analyze financial documents using AI  
- Generate structured investment memos  

---

## 🧠 Key Features

---

### 📊 Stock Analysis

Enter a stock ticker and get:

- Company overview (sector, industry)  
- Key financial metrics:  
  - Price, Market Cap  
  - P/E & Forward P/E  
  - Profit Margin  
  - Revenue Growth  
  - Debt-to-Equity  
- Historical price chart  

🤖 AI-generated equity research report:
- Business summary  
- Financial insights  
- Valuation view  
- Risks  
- Investment recommendation  

---

### 📄 Financial Document Analysis (RAG)

Upload a company’s financial documents (PDFs, reports, notes) and extract:

- Business summary  
- Revenue & profitability insights  
- Balance sheet analysis  
- Management discussion highlights  
- Key risks  

⚙️ Behind the scenes:
- Document chunking  
- Embedding generation  
- Vector search (FAISS)  
- Semantic retrieval  
- Source-backed AI answers  

---

### 🤖 Agentic Investment Workflow (NEW)

Automatically generate a complete investment memo using a multi-step AI workflow:

- Retrieve relevant document context  
- Fetch financial data  
- Compare peer companies  
- Run DCF valuation  
- Analyze risks  
- Generate final investment memo  

📌 Output includes:
- Executive Summary  
- Business Overview  
- Financial Snapshot  
- Valuation View  
- Peer Comparison  
- Key Risks  
- Investment Recommendation  

---

### 💬 Research Chat with Memory (NEW)

Ask follow-up questions with context awareness:

Example:
User: Analyze TCS  
User: Compare it with Infosys  

✔ Understands references like “it”  
✔ Maintains session memory  
✔ Uses previous analysis context  

---

### 💰 DCF Valuation Calculator

Perform a basic Discounted Cash Flow analysis using:

- Free Cash Flow  
- Growth Rate  
- Discount Rate  
- Terminal Growth Rate  
- Shares Outstanding  

Outputs:

- Enterprise Value  
- Estimated Fair Value per Share  

---

### ⚖️ Company Comparison

Compare two companies side-by-side:

- Financial metrics comparison  
- Valuation comparison  
- Profitability & growth differences  

🤖 AI-generated insights:
- Key differences  
- Strength analysis  
- Final investment view  

---

### 📈 Portfolio Tracker

Track your holdings easily:

- Input stocks + number of shares  

View:
- Individual position value  
- Total portfolio value  

---

### 📰 News Sentiment Analysis

Analyze recent company news:

- Overall sentiment (Positive / Neutral / Negative)  
- Key themes  
- Market impact  
- Risks and concerns  
- Short investment takeaway  

---

### 📥 Report Download

Export AI-generated reports as:

- Text files  
- PDF documents  

Useful for:

- Saving research  
- Sharing insights  
- Building investment notes  

---

### 🧠 AI Response Evaluation (NEW)

Basic quality checks for AI responses:

- Ensures structured output  
- Validates presence of useful content  
- Supports citation-based answers (RAG)  

User feedback system:
- 👍 Good Answer  
- 👎 Needs Improvement  

---

## 🛠️ Tech Stack

- Python  
- Streamlit  
- yfinance  
- pandas  
- matplotlib  
- PyPDF2  
- ReportLab  
- python-dotenv  

### AI / GenAI:

- Anthropic Claude API  
- LangChain  
- LangGraph  
- FAISS (vector database)  
- FastEmbed  

---

## 📂 Project Structure

ai-equity-copilot/  
│  
├── app.py                 # Main Streamlit application  
├── utils.py               # Financial data, DCF, PDF, and news logic  
├── prompts.py             # AI prompt templates  
├── ai.py                  # LLM integration (Claude)  
├── rag.py                 # RAG pipeline (documents, embeddings, retrieval)  
├── chat_memory.py         # Multi-turn conversation memory  
├── agent_workflow.py      # LangGraph investment workflow  
├── evaluation.py          # Response quality checks  
├── report_generator.py    # PDF report generation  
├── requirements.txt       # Dependencies  
├── .gitignore             # Igned files  
└── README.md              # Documentation  

---

## ⚠️ Disclaimer

This project is for educational and demonstration purposes only.

The generated analysis should not be considered financial advice. Users should conduct their own research before making investment decisions.
