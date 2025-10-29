from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

class StudentAgent:
    def __init__(self):
        self.name = "Student Support Agent"

    def handle_query(self, student_data):
        prompt = f"""
        You are a student support AI. A student has raised a query:
        Name: {student_data['name']}
        ID: {student_data['student_id']}
        Batch: {student_data['batch']}
        Question: {student_data['question']}

        Your task: Acknowledge the question politely and summarize it for the program manager.
        """
        response = llm.invoke(prompt)
        return response.content
