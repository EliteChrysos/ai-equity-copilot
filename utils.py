import yfinance as yf
from PyPDF2 import PdfReader

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    data = {
        "Ticker": ticker.upper(),
        "Company Name": info.get("longName"),
        "Sector": info.get("sector"),
        "Industry": info.get("industry"),
        "Current Price": info.get("currentPrice"),
        "Market Cap": info.get("marketCap"),
        "P/E Ratio": info.get("trailingPE"),
        "Forward P/E": info.get("forwardPE"),
        "Profit Margin": info.get("profitMargins"),
        "Revenue Growth": info.get("revenueGrowth"),
        "Debt to Equity": info.get("debtToEquity"),
    }

    return data

def get_price_history(ticker, period="6mo"):
    stock = yf.Ticker(ticker)
    history = stock.history(period=period)

    return history

def extract_pdf_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text

def calculate_dcf(
    free_cash_flow,
    growth_rate,
    discount_rate,
    terminal_growth_rate,
    shares_outstanding,
    years=5
):
    projected_cash_flows = []

    for year in range(1, years + 1):
        future_cash_flow = free_cash_flow * ((1 + growth_rate) ** year)
        discounted_cash_flow = future_cash_flow / ((1 + discount_rate) ** year)
        projected_cash_flows.append(discounted_cash_flow)

    terminal_value = (
        projected_cash_flows[-1] * (1 + terminal_growth_rate)
    ) / (discount_rate - terminal_growth_rate)

    discounted_terminal_value = terminal_value / ((1 + discount_rate) ** years)

    enterprise_value = sum(projected_cash_flows) + discounted_terminal_value

    fair_value_per_share = enterprise_value / shares_outstanding

    return {
        "Enterprise Value": enterprise_value,
        "Fair Value Per Share": fair_value_per_share,
        "Discounted Cash Flows": projected_cash_flows,
    }


def get_stock_news(ticker):
    stock = yf.Ticker(ticker)
    news = stock.news

    articles = []

    for item in news[:5]:
        content = item.get("content", {})

        title = content.get("title")
        publisher = content.get("provider", {}).get("displayName")
        link = content.get("canonicalUrl", {}).get("url")

        if title:
            articles.append({
                "Title": title,
                "Publisher": publisher,
                "Link": link
            })

    return articles