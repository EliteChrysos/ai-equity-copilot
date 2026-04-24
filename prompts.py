def equity_prompt(data):
    prompt = f"""
You are an equity research analyst.

Analyze this company using the data below:

Ticker: {data["Ticker"]}
Company Name: {data["Company Name"]}
Sector: {data["Sector"]}
Industry: {data["Industry"]}
Current Price: {data["Current Price"]}
Market Cap: {data["Market Cap"]}
P/E Ratio: {data["P/E Ratio"]}
Forward P/E: {data["Forward P/E"]}
Profit Margin: {data["Profit Margin"]}
Revenue Growth: {data["Revenue Growth"]}
Debt to Equity: {data["Debt to Equity"]}

Give the output in this format:

1. Business Summary
2. Key Financial Insights
3. Valuation View
4. Main Risks
5. Investment Recommendation: Buy / Hold / Sell

Important:
- Be concise.
- Use financial reasoning.
- Do not invent missing numbers.
- If data is missing, say it is unavailable.
"""
    return prompt

def pdf_report_prompt(text):
    return f"""
You are an equity research analyst.

Analyze the following annual report text.

Give the output in this format:

1. Business Summary
2. Revenue and Profitability Insights
3. Balance Sheet / Debt Insights
4. Management Discussion Highlights
5. Key Risks
6. Investment View

Important:
- Be concise.
- Use only the information in the report.
- Do not invent numbers.
- If something is unclear, say it is unclear.

Annual Report Text:
{text[:12000]}
"""


def comparison_prompt(data1, data2):
    return f"""
You are an equity research analyst.

Compare the following two companies:

Company 1:
Name: {data1["Company Name"]}
P/E Ratio: {data1["P/E Ratio"]}
Market Cap: {data1["Market Cap"]}
Revenue Growth: {data1["Revenue Growth"]}
Profit Margin: {data1["Profit Margin"]}
Debt to Equity: {data1["Debt to Equity"]}

Company 2:
Name: {data2["Company Name"]}
P/E Ratio: {data2["P/E Ratio"]}
Market Cap: {data2["Market Cap"]}
Revenue Growth: {data2["Revenue Growth"]}
Profit Margin: {data2["Profit Margin"]}
Debt to Equity: {data2["Debt to Equity"]}

Provide:

1. Key Differences
2. Which company is financially stronger
3. Valuation comparison
4. Final recommendation: which is a better investment and why

Be concise and analytical.
"""