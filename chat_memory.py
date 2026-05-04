from ai import get_ai_analysis

#takes past msgs nd keeps only 8
def format_chat_history(messages, max_messages=8):
    recent_messages = messages[-max_messages:]
    # prevents prompt from getting too long

    formatted = ""
    # intializes string to store formatted history

    for message in recent_messages:
        role = message["role"]
        content = message["content"]

        formatted += f"{role.upper()}: {content}\n\n"

    return formatted


def answer_with_memory(user_question, chat_history, current_context=None):
    formatted_history = format_chat_history(chat_history)

    prompt = f"""
You are an AI equity research assistant.

You have access to the conversation history below. Use it to understand follow-up questions.

Conversation History:
{formatted_history}

Current Context:
{current_context if current_context else "No additional context provided."}

User's Latest Question:
{user_question}

Instructions:
- Answer as a finance and equity research assistant.
- Use the conversation history to resolve references like "it", "that company", "compare it", or "the previous stock".
- If the user asks for financial analysis, structure the answer clearly.
- If the user asks for a comparison but the second company is unclear, ask for the missing ticker/company.
- Do not pretend to have real-time data unless it is provided in the current context.
- Be concise but useful.

Answer:
"""

    return get_ai_analysis(prompt)