from agents.students_agent import StudentAgent
from agents.manager_agent import ManagerAgent

# Initialize agents
student_agent = StudentAgent()
manager_agent = ManagerAgent()

# Step 1: Create a sample student query
student_question = {
    "student_id": "S123",
    "name": "Rahul Sharma",
    "batch": "DS2025",
    "question": "I didn’t understand logistic regression. Can someone explain it?"
}

print("🚀 Agentic AI Support Ticket System\n")

# Step 2: Student agent processes the query
summary = student_agent.handle_query(student_question)
print("🧠 Student Agent Summary:\n", summary)

# Step 3: Manager agent receives and assigns ticket
response = manager_agent.assign_ticket(summary)
print("\n👨‍💼 Manager Agent Response:\n", response)
