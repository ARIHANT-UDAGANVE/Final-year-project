import streamlit as st
import google.generativeai as genai

# Set up the API key for Google Gemini
genai.configure(api_key="AIzaSyB7azxaXQ5ATN9dgdKuNLcRDYgCkUF9Mx0")

def chatbot_page():
    st.title("Railway AI Helper")
    st.write("Ask me railway-related questions!")

    # Input box for user query
    user_query = st.text_input("Enter your question here:")

    if st.button("Ask"):
        if user_query.strip():
            try:
                # Use the Google Gemini chat model to generate the response
                obj = genai.GenerativeModel(
                    #prompt=f"You are a helpful assistant for railway-related queries. Answer the following question: {user_query}",
                    model_name="gemini-1.5-flash-8b",  # Use your appropriate model
                    #temperature=0.7,
                    #max_output_tokens=150
                )
                
                response = obj.generate_content(f"If a user asks about how to use the app, guide them as follows: Start by instructing them to go to the login page. If they already have credentials, they should log in using their username and password; otherwise, they need to choose the *Sign Up* option and create an account. Once logged in, advise them to switch to the *User Page* tab, where they can enter their complaint. Inform them that the app will automatically direct the complaint to the necessary category, generate a unique Complaint ID, and display its status. If the user requires further assistance at any point, suggest switching to the *AI Helper* tab for additional support.:{user_query}")

                # Display the response from the model
                st.success("Answer:")
                st.write(response.text)  # Assuming the response contains a 'text' field
                print(response)

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please type a question.")
