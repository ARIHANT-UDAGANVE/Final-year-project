from transformers import pipeline
import streamlit as st
import uuid
from datetime import datetime

# Initialize the pipelines
category_analyzer = pipeline("zero-shot-classification")
sentiment_analyzer = pipeline("sentiment-analysis")

# List of predefined complaint categories
CATEGORIES = [
    "Punctuality Issues", "Cleanliness and Hygiene", "Ticketing Problems",
    "Safety Concerns", "Catering and Food Quality", "Seat and Berth Allocation",
    "Onboard Services", "Behavior of Staff", "Infrastructure Problems",
    "Luggage Handling and Storage"
]

# Priority assignment logic
urgent_keywords = ["urgent", "safety", "immediate", "critical","emergency"]

def assign_priority(complaint_text):
    sentiment = sentiment_analyzer(complaint_text)[0]
    sentiment_score = 10 if sentiment["label"] == "NEGATIVE" else 5
    keyword_score = 10 if any(word in complaint_text.lower() for word in urgent_keywords) else 0
    priority_score = (sentiment_score * 0.6) + (keyword_score * 0.4)

    if priority_score >= 8:
        return "High"
    elif priority_score >= 5:
        return "Medium"
    return "Low"


def auto_assign_category(complaint_text):
    result = category_analyzer(complaint_text, CATEGORIES)
    return result["labels"][0]  # The category with the highest confidence


def user_page(users_collection, complaints_collection):
    st.title(f"Hi, {st.session_state.username}!")

    # Input: Complaint Text
    complaint_text = st.text_area("Enter your complaint:")
    if st.button("File Complaint"):
        if complaint_text:
            # Automatically assign category
            category = auto_assign_category(complaint_text)

            # Automatically assign priority
            priority = assign_priority(complaint_text)

            # Generate unique complaint ID
            complaint_id = f"C{uuid.uuid4().hex[:6].upper()}"

            # Insert the complaint into the database
            complaints_collection.insert_one({
                "complaint_id": complaint_id,
                "username": st.session_state.username,
                "complaint": complaint_text,
                "category": category,
                "priority": priority,
                "status": "Pending",
                "timestamp": datetime.utcnow()
            })

            st.success(f"Complaint filed successfully!")
            st.balloons()
            st.info(f"Category: {category}")
            st.info(f"Priority: {priority}")
        else:
            st.error("Please enter a complaint.")

    # Display user's complaints
    st.subheader("Your Complaints")
    complaints = list(complaints_collection.find({"username": st.session_state.username}))
    if complaints:
        st.table([
            {
                "ID": c["complaint_id"],
                "Category": c["category"],
                "Priority": c["priority"],
                "Status": c["status"]
            }
            for c in complaints
        ])
    else:
        st.write("No complaints filed yet.")

    # Logout Button
    if st.button("Logout"):
        st.session_state.username = None
