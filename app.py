import os
from datetime import datetime
import streamlit as st
from utils import get_stock_data, get_price_history, extract_pdf_text, calculate_dcf
from prompts import equity_prompt, pdf_report_prompt, comparison_prompt
from ai import get_ai_analysis
from report_generator import create_pdf_report

st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
        color: white;
    }
    .stTextInput>div>div>input {
        background-color: #1E222A;
        color: white;
    }
    .stNumberInput input {
        background-color: #1E222A;
        color: white;
    }
    .stButton>button {
        background-color: #FF9900;
        color: black;
        border-radius: 6px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

def save_report(ticker, report_text):
    folder_name = "saved_reports"

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{ticker.upper()}_report_{timestamp}.txt"
    file_path = os.path.join(folder_name, file_name)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(report_text)

    return file_path

st.set_page_config(
    page_title="AI Equity Research Copilot",
    layout="wide"
)

st.title("AI Equity Research Copilot")
st.info("Analyze companies, generate AI research reports, perform valuations, and compare stocks — all in one place.")
st.caption("AI-powered equity research, valuation, financial insights, and company comparison.")


section = st.sidebar.radio(
    "Navigation",
    [
        "Stock Analysis",
        "Annual Report PDF",
        "DCF Calculator",
        "Company Comparison"
    ]
)

if section == "Stock Analysis":
    st.markdown("## 📊 Stock Analysis")

    ticker = st.text_input("Enter Stock Ticker", placeholder="Example: AAPL, MSFT, TSLA")

    if st.button("Analyze Stock"):
        if not ticker:
            st.warning("Please enter a stock ticker.")
        else:
            with st.spinner("Fetching stock data..."):
                data = get_stock_data(ticker)

            st.subheader("Key Metrics")

            col1, col2, col3 = st.columns(3)

            col1.metric("Price", data["Current Price"])
            col2.metric("P/E Ratio", data["P/E Ratio"])
            col3.metric("Market Cap", data["Market Cap"])

            col1.metric("Revenue Growth", data["Revenue Growth"])
            col2.metric("Profit Margin", data["Profit Margin"])
            col3.metric("Debt to Equity", data["Debt to Equity"])

            st.subheader("Stock Price Chart")
            price_history = get_price_history(ticker)
            st.line_chart(price_history["Close"])

            prompt = equity_prompt(data)

            with st.spinner("Generating AI analysis..."):
                analysis = get_ai_analysis(prompt)

            st.subheader("AI Equity Research Report")
            st.markdown(analysis)

            st.download_button(
                label="Download Report",
                data=analysis,
                file_name=f"{ticker.upper()}_equity_report.txt",
                mime="text/plain"
            )
    
            pdf_file = create_pdf_report(
                f"{ticker.upper()} Equity Research Report",
                analysis
            )
            
            st.download_button(
                label="Download PDF Report",
                data=pdf_file,
                file_name=f"{ticker.upper()}_equity_report.pdf",
                mime="application/pdf"
            )
    
            if st.button("Save Report"):
                saved_path = save_report(ticker, analysis)
                st.success(f"Report saved to: {saved_path}")



if section == "Annual Report PDF":
    st.header("Analyze Annual Report PDF")

    uploaded_file = st.file_uploader("Upload annual report PDF", type=["pdf"])

    if uploaded_file is not None:
        with st.spinner("Reading PDF..."):
            pdf_text = extract_pdf_text(uploaded_file)

        st.success("PDF text extracted successfully.")

        if st.button("Analyze PDF"):
            prompt = pdf_report_prompt(pdf_text)

            with st.spinner("Analyzing annual report..."):
                pdf_analysis = get_ai_analysis(prompt)

            st.subheader("Annual Report Analysis")
            st.markdown(pdf_analysis)




if section == "DCF Calculator":
    st.markdown("## 📉 DCF Calculator")

    free_cash_flow = st.number_input("Free Cash Flow", value=1000000000.0)
    growth_rate = st.number_input("Growth Rate (%)", value=5.0) / 100
    discount_rate = st.number_input("Discount Rate (%)", value=10.0) / 100
    terminal_growth_rate = st.number_input("Terminal Growth Rate (%)", value=2.5) / 100
    shares_outstanding = st.number_input("Shares Outstanding", value=1000000000.0)

    if st.button("Calculate DCF"):
        dcf_result = calculate_dcf(
            free_cash_flow,
            growth_rate,
            discount_rate,
            terminal_growth_rate,
            shares_outstanding
        )

        st.subheader("DCF Result")
        st.metric("Enterprise Value", f"${dcf_result['Enterprise Value']:,.0f}")
        st.metric("Fair Value Per Share", f"${dcf_result['Fair Value Per Share']:,.2f}")




if section == "Company Comparison":
     st.markdown("## ⚔️ Company Comparison")

     ticker1 = st.text_input("First Company Ticker", placeholder="Example: AAPL")
     ticker2 = st.text_input("Second Company Ticker", placeholder="Example: MSFT")

     if st.button("Compare Companies"):
        if ticker1 and ticker2:
            data1 = get_stock_data(ticker1)
            data2 = get_stock_data(ticker2)

            comparison = {
                "Metric": [
                    "Company Name",
                    "Sector",
                    "Current Price",
                    "Market Cap",
                    "P/E Ratio",
                    "Forward P/E",
                    "Profit Margin",
                    "Revenue Growth",
                    "Debt to Equity",
                ],
                ticker1.upper(): [
                    data1["Company Name"],
                    data1["Sector"],
                    data1["Current Price"],
                    data1["Market Cap"],
                    data1["P/E Ratio"],
                    data1["Forward P/E"],
                    data1["Profit Margin"],
                    data1["Revenue Growth"],
                    data1["Debt to Equity"],
                ],
                ticker2.upper(): [
                    data2["Company Name"],
                    data2["Sector"],
                    data2["Current Price"],
                    data2["Market Cap"],
                    data2["P/E Ratio"],
                    data2["Forward P/E"],
                    data2["Profit Margin"],
                    data2["Revenue Growth"],
                    data2["Debt to Equity"],
                ],
            }

            st.subheader("Company Comparison")
            st.table(comparison)

            with st.spinner("Generating AI comparison..."):
                comp_prompt = comparison_prompt(data1, data2)
                comp_analysis = get_ai_analysis(comp_prompt)

            st.subheader("AI Comparison Insight")
            st.markdown(comp_analysis)
        else:
            st.warning("Please enter both tickers.")
