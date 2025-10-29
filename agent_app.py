import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import pandas as pd

# --- Load environment variables ---
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- File setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
CSV_PATH = os.path.join(DATA_DIR, "support_tickets.csv")

# --- Gemini model ---
model = genai.GenerativeModel("gemini-2.0-flash")

# --- Helper functions ---
def generate_summary(student_data):
    prompt = f"""
    A student has submitted a question:
    Name: {student_data['name']}
    ID: {student_data['student_id']}
    Batch: {student_data['batch']}
    Question: {student_data['question']}

    Summarize this in a short, clear paragraph for the program manager.
    """
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_manager_response(summary):
    prompt = f"""
    You are a program manager. Here is the student's query summary:
    {summary}

    Write a short, professional response acknowledging the student's concern 
    and assuring that support will be provided.
    """
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_student_email(name, question, manager_response):
    prompt = f"""
    Compose an email to student {name} who asked:
    "{question}"

    The manager responded:
    "{manager_response}"

    Write a polite, empathetic, and encouraging email in a professional tone 
    from the program support team. Sign off as "Program Support Team".
    """
    response = model.generate_content(prompt)
    return response.text.strip()

def save_ticket(student_id, name, batch, question, summary, manager_response, student_email):
    """Save ticket to CSV."""
    if not os.path.exists(CSV_PATH):
        df = pd.DataFrame(columns=[
            "Student ID", "Name", "Batch", "Question", "Summary",
            "Manager Response", "Generated Email"
        ])
    else:
        df = pd.read_csv(CSV_PATH)

    new_row = {
        "Student ID": student_id,
        "Name": name,
        "Batch": batch,
        "Question": question,
        "Summary": summary,
        "Manager Response": manager_response,
        "Generated Email": student_email
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(CSV_PATH, index=False)

# --- Streamlit UI ---
st.set_page_config(page_title="AI Student Support Ticket System", page_icon="🎓", layout="centered")
st.title("🎓 Agentic AI Student Support System with Email Generator")

st.markdown("""
This system uses **Gemini AI** to automatically handle student queries, 
summarize them, generate manager responses, and craft personalized follow-up emails.  
""")

# --- Form ---
student_id = st.text_input("Student ID")
name = st.text_input("Student Name")
batch = st.text_input("Batch")
question = st.text_area("Student Question")

# Use session_state to persist data between reruns
if "summary" not in st.session_state:
    st.session_state.summary = ""
    st.session_state.manager_response = ""
    st.session_state.student_email = ""

# --- Generate Button ---
if st.button("🚀 Generate Ticket & Email"):
    if not all([student_id, name, batch, question]):
        st.warning("⚠️ Please fill in all fields.")
    else:
        student_data = {
            "student_id": student_id,
            "name": name,
            "batch": batch,
            "question": question
        }

        with st.spinner("Processing with Gemini AI..."):
            summary = generate_summary(student_data)
            manager_response = generate_manager_response(summary)
            student_email = generate_student_email(name, question, manager_response)

        st.session_state.summary = summary
        st.session_state.manager_response = manager_response
        st.session_state.student_email = student_email

        st.success("✅ Ticket processed successfully!")

# --- Display results if available ---
if st.session_state.summary:
    st.subheader("🧠 Summary for Manager")
    st.write(st.session_state.summary)

    st.subheader("👨‍💼 Manager's Response")
    st.write(st.session_state.manager_response)

    st.subheader("📧 Generated Email to Student")
    st.code(st.session_state.student_email, language="markdown")

    if st.button("💾 Save Ticket"):
        save_ticket(
            student_id, name, batch, question,
            st.session_state.summary,
            st.session_state.manager_response,
            st.session_state.student_email
        )
        st.success(f"✅ Ticket saved successfully at `{CSV_PATH}`")

        with st.expander("📄 View Saved Tickets"):
            df = pd.read_csv(CSV_PATH)
            st.dataframe(df)
