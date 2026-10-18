import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()


def format_docs(docs):
    """
    Converts retrieved documents into one context string.
    Also keeps page numbers for citation-like output.
    """

    formatted_text = ""

    for i, doc in enumerate(docs, start=1):
        page = doc.metadata.get("page", "unknown")
        source = doc.metadata.get("source", "unknown")

        formatted_text += f"\n\nSource {i}:\n"
        formatted_text += f"Page: {page}\n"
        formatted_text += f"File: {source}\n"
        formatted_text += f"Content:\n{doc.page_content}\n"

    return formatted_text


def get_llm():
    """
    Creates Gemini chat model.
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        temperature=0.2
    )

    return llm


def answer_question(question, retrieved_docs):
    """
    Takes user question + retrieved PDF chunks
    and asks LLM to generate final answer.
    """

    context = format_docs(retrieved_docs)

    prompt = ChatPromptTemplate.from_template(
        """
You are a helpful PDF assistant.

Use ONLY the given PDF context to answer the user's question.

Rules:
1. If the answer is not present in the context, say:
   "I could not find this information in the uploaded PDF."
2. Do not make up facts.
3. If code is present in the context, preserve the code formatting.
4. Give page/source references when possible.

PDF Context:
{context}

User Question:
{question}

Final Answer:
"""
    )

    llm = get_llm()

    chain = prompt | llm

    response = chain.invoke(
        {
            "context": context,
            "question": question
        }
    )

    return response.content