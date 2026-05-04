from typing import TypedDict, List, Dict, Any, Optional

from langgraph.graph import StateGraph, END

from utils import get_stock_data, calculate_dcf
from ai import get_ai_analysis

#defines shared memory across all steps
class InvestmentAgentState(TypedDict):
    ticker: str
    peer_tickers: List[str]
    vector_store: Any
    dcf_inputs: Dict[str, float]

    task_plan: str
    company_data: Dict[str, Any]
    peer_data: List[Dict[str, Any]]
    document_context: str
    retrieved_sources: List[Dict[str, Any]]
    peer_analysis: str
    dcf_result: Dict[str, Any]
    risk_analysis: str
    final_memo: str

#creates the plan of execution
def understand_task_node(state: InvestmentAgentState):
    ticker = state["ticker"]
    peer_tickers = state.get("peer_tickers", [])

    task_plan = f"""
Investment research workflow for {ticker.upper()}.

Planned steps:
1. Retrieve relevant uploaded financial document context if available.
2. Fetch market and financial data for {ticker.upper()}.
3. Fetch peer data for comparison: {peer_tickers if peer_tickers else "No peers provided"}.
4. Run DCF valuation using user assumptions.
5. Analyze risks from financial data and documents.
6. Generate final investment memo.
"""

    return {"task_plan": task_plan}


def retrieve_documents_node(state: InvestmentAgentState):
    vector_store = state.get("vector_store")
    ticker = state["ticker"]

    if vector_store is None:
        return {
            "document_context": "No uploaded documents were available for retrieval.",
            "retrieved_sources": []
        }

    query = (
        f"{ticker} business overview revenue profitability debt risks "
        f"management discussion investment outlook"
    )

    # build query about company, searched vectorDB, retrieves top5 chunk
    docs = vector_store.similarity_search(query, k=5)

    context_parts = []
    sources = []

    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "Uploaded document")
        page = doc.metadata.get("page", "N/A")

        context_parts.append(
            f"""
[Source {i}: {source}, page {page}]
{doc.page_content}
"""
        )

        sources.append({
            "Source": source,
            "Page": page,
            "Preview": doc.page_content[:400]
        })

    return {
        "document_context": "\n\n".join(context_parts),
        "retrieved_sources": sources
    }


def fetch_financial_data_node(state: InvestmentAgentState):
    ticker = state["ticker"]
    peer_tickers = state.get("peer_tickers", [])

    company_data = get_stock_data(ticker)

    peer_data = []
    for peer in peer_tickers:
        if peer.strip():
            peer_data.append(get_stock_data(peer.strip()))

    return {
        "company_data": company_data,
        "peer_data": peer_data
    }


def peer_comparison_node(state: InvestmentAgentState):
    company_data = state["company_data"]
    peer_data = state.get("peer_data", [])

    if not peer_data:
        return {
            "peer_analysis": "No peer companies were provided, so peer comparison was skipped."
        }

    prompt = f"""
You are an equity research analyst.

Compare the target company with its peers.

Target Company:
{company_data}

Peer Companies:
{peer_data}

Analyze:
1. Relative valuation
2. Profitability
3. Growth
4. Balance sheet risk
5. Which company appears stronger and why

Be concise and analytical.
"""

    peer_analysis = get_ai_analysis(prompt)

    return {"peer_analysis": peer_analysis}


def dcf_node(state: InvestmentAgentState):
    dcf_inputs = state.get("dcf_inputs", {})

    required_fields = [
        "free_cash_flow",
        "growth_rate",
        "discount_rate",
        "terminal_growth_rate",
        "shares_outstanding"
    ]

    if not all(field in dcf_inputs for field in required_fields):
        return {"dcf_result": {}}

    dcf_result = calculate_dcf(
        free_cash_flow=dcf_inputs["free_cash_flow"],
        growth_rate=dcf_inputs["growth_rate"],
        discount_rate=dcf_inputs["discount_rate"],
        terminal_growth_rate=dcf_inputs["terminal_growth_rate"],
        shares_outstanding=dcf_inputs["shares_outstanding"]
    )

    return {"dcf_result": dcf_result}


def risk_analysis_node(state: InvestmentAgentState):
    company_data = state["company_data"]
    document_context = state.get("document_context", "")

    prompt = f"""
You are an equity research analyst.

Analyze the key investment risks for this company.

Company Data:
{company_data}

Retrieved Document Context:
{document_context}

Give:
1. Business risks
2. Financial risks
3. Valuation risks
4. Risks mentioned in uploaded documents, if available

If uploaded documents are used, cite them using [filename, page number].
Do not invent facts.
"""

    risk_analysis = get_ai_analysis(prompt)

    return {"risk_analysis": risk_analysis}

# final report generator
def final_memo_node(state: InvestmentAgentState):
    ticker = state["ticker"]
    company_data = state["company_data"]
    document_context = state.get("document_context", "")
    peer_analysis = state.get("peer_analysis", "")
    dcf_result = state.get("dcf_result", {})
    risk_analysis = state.get("risk_analysis", "")

    prompt = f"""
You are an equity research analyst.

Create a final investment memo for {ticker.upper()}.

Use the information below.

Company Data:
{company_data}

Retrieved Document Context:
{document_context}

Peer Analysis:
{peer_analysis}

DCF Result:
{dcf_result}

Risk Analysis:
{risk_analysis}

Format the memo as:

# Investment Memo: {ticker.upper()}

## 1. Executive Summary
## 2. Business Overview
## 3. Financial Snapshot
## 4. Valuation View
## 5. Peer Comparison
## 6. Key Risks
## 7. Investment Recommendation

Rules:
- Be analytical and concise.
- Use Buy / Hold / Sell recommendation.
- Cite uploaded document sources when using document context.
- Do not invent missing numbers.
- Clearly state when information is unavailable.
"""

    final_memo = get_ai_analysis(prompt)

    return {"final_memo": final_memo}


def build_investment_agent():
    graph = StateGraph(InvestmentAgentState)

    graph.add_node("understand_task", understand_task_node)
    graph.add_node("retrieve_documents", retrieve_documents_node)
    graph.add_node("fetch_financial_data", fetch_financial_data_node)
    graph.add_node("peer_comparison", peer_comparison_node)
    graph.add_node("dcf", dcf_node)
    graph.add_node("risk_analysis", risk_analysis_node)
    graph.add_node("final_memo", final_memo_node)

    graph.set_entry_point("understand_task")

    graph.add_edge("understand_task", "retrieve_documents")
    graph.add_edge("retrieve_documents", "fetch_financial_data")
    graph.add_edge("fetch_financial_data", "peer_comparison")
    graph.add_edge("peer_comparison", "dcf")
    graph.add_edge("dcf", "risk_analysis")
    graph.add_edge("risk_analysis", "final_memo")
    graph.add_edge("final_memo", END)

    return graph.compile()
# this is pipeline DAG

# run the agent
def run_investment_agent(
    ticker,
    peer_tickers=None,
    vector_store=None,
    dcf_inputs=None
):
    # build graph
    agent = build_investment_agent()

    initial_state = {
        "ticker": ticker,
        "peer_tickers": peer_tickers or [],
        "vector_store": vector_store,
        "dcf_inputs": dcf_inputs or {},
        "task_plan": "",
        "company_data": {},
        "peer_data": [],
        "document_context": "",
        "retrieved_sources": [],
        "peer_analysis": "",
        "dcf_result": {},
        "risk_analysis": "",
        "final_memo": ""
    }

    final_state = agent.invoke(initial_state)

    return final_state