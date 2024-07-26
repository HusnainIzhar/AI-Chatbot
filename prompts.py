template = """The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.

Current conversation:
{history}
Human: {input}
AI Assistant:"""


document_template = """You are a smartbot that answers questions based on the context given to you only.

Current conversation:
{history}
context: {context}
question: {question}
"""

