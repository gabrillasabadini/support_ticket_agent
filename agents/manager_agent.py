from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

class ManagerAgent:
    def __init__(self):
        self.name = "Program Manager Agent"

    def assign_ticket(self, student_summary):
        prompt = f"""
        You are a program manager AI. You receive the following student query summary:
        {student_summary}

        Your task: Generate a professional response confirming the ticket is assigned and
        specify what action will be taken next.
        """
        response = llm.invoke(prompt)
        return response.content
