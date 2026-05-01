# 🚀 AI Equity Research Copilot

👉 **Live Demo:** https://ai-equity-copilot-pkj9gg4vwbl222pj9kwmyx.streamlit.app/

AI Equity Research Copilot is an end-to-end **investment analysis platform** that combines financial data, valuation models, and large language models to help users analyze stocks faster and more intelligently.

Built with Python and Streamlit, this tool simulates a lightweight equity research workflow—making it useful for **investors, students, and aspiring analysts**.

---

## 📌 Why This Project?

Traditional equity research is:
- Time-consuming  
- Data-heavy  
- Requires multiple tools  

This app brings everything into **one unified interface**, allowing users to:
- Analyze companies instantly  
- Generate AI-powered research reports  
- Perform valuation (DCF)  
- Compare companies  
- Track portfolios  
- Understand market sentiment  

---

## 🧠 Key Features

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
- 🤖 AI-generated equity research report:
  - Business summary
  - Financial insights
  - Valuation view
  - Risks
  - Investment recommendation

---

### 📄 Annual Report (PDF) Analysis

Upload a company’s annual report and extract:

- Business summary  
- Revenue & profitability insights  
- Balance sheet analysis  
- Management discussion highlights  
- Key risks  
- AI-generated investment view  

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
- 🤖 AI-generated insights:
  - Key differences  
  - Strength analysis  
  - Final investment view  

---

### 📈 Portfolio Tracker

Track your holdings easily:

- Input stocks + number of shares  
- View:
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

## 🛠️ Tech Stack

- Python  
- Streamlit  
- yfinance  
- pandas  
- matplotlib  
- PyPDF2  
- ReportLab  
- Anthropic Claude API  
- python-dotenv  

---

## 📂 Project Structure

```text
ai-equity-copilot/
│
├── app.py                 # Main Streamlit application
├── utils.py               # Financial data, DCF, PDF, and news logic
├── prompts.py             # AI prompt templates
├── ai.py                  # LLM integration (Claude)
├── report_generator.py    # PDF report generation
├── requirements.txt       # Dependencies
├── .gitignore             # Ignored files
└── README.md              # Documentation
