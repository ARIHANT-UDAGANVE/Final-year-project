import streamlit as st
import pandas as pd
from bson.objectid import ObjectId
import matplotlib.pyplot as plt
import seaborn as sns

# Mapping categories to departments
DEPARTMENT_MAPPING = {
    "Operations Department": [
        "Punctuality Issues",
        "Ticketing Problems",
        "Seat and Berth Allocation",
        "Infrastructure Problems",
    ],
    "Customer Service Department": [
        "Onboard Services",
        "Behavior of Staff",
        "Catering and Food Quality",
        "Cleanliness and Hygiene",
    ],
    "Safety and Logistics Department": [
        "Safety Concerns",
        "Luggage Handling and Storage",
    ],
}


def plot_chart(chart_type, df):
    if chart_type == "Bar Chart: Pending Complaints by Category":
        # Bar Chart
        st.subheader("Pending Complaints by Category")
        pending_df = df[df["status"] == "Pending"]
        if not pending_df.empty:
            category_counts = pending_df["category"].value_counts()
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x=category_counts.index, y=category_counts.values, palette="coolwarm", ax=ax)
            plt.xticks(rotation=45)
            ax.set_title("Number of Pending Complaints by Category", fontsize=16)
            ax.set_xlabel("Category", fontsize=12)
            ax.set_ylabel("Count", fontsize=12)
            st.pyplot(fig)
        else:
            st.write("No pending complaints to display.")

    elif chart_type == "Pie Chart: Pending Complaints Distribution":
        # Pie Chart
        st.subheader("Pending Complaints Distribution by Category")
        pending_df = df[df["status"] == "Pending"]
        if not pending_df.empty:
            category_counts = pending_df["category"].value_counts()
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
            ax.set_title("Pending Complaints Distribution")
            st.pyplot(fig)
        else:
            st.write("No pending complaints to display.")

    elif chart_type == "Line Chart: Complaints Over Time":
        # Line Chart
        st.subheader("Complaints Trend Over Time")
        if not df.empty:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            trend_data = df.groupby(df["timestamp"].dt.date).size()
            fig, ax = plt.subplots(figsize=(10, 6))
            trend_data.plot(kind="line", ax=ax, marker='o', color='b')
            ax.set_title("Number of Complaints Over Time", fontsize=16)
            ax.set_xlabel("Date", fontsize=12)
            ax.set_ylabel("Number of Complaints", fontsize=12)
            st.pyplot(fig)
        else:
            st.write("No complaints data available.")

    elif chart_type == "Stacked Bar Chart: Complaints by Category and Status":
        # Stacked Bar Chart
        st.subheader("Complaints by Category and Status")
        if not df.empty:
            category_status = df.groupby(["category", "status"]).size().unstack(fill_value=0)
            fig, ax = plt.subplots(figsize=(12, 6))
            category_status.plot(kind="bar", stacked=True, ax=ax, colormap="viridis")
            ax.set_title("Complaints by Category and Status", fontsize=16)
            ax.set_xlabel("Category", fontsize=12)
            ax.set_ylabel("Number of Complaints", fontsize=12)
            st.pyplot(fig)
        else:
            st.write("No complaints data available.")

    elif chart_type == "Heatmap: Complaints by Category and Priority":
        # Heatmap
        st.subheader("Complaints Heatmap by Category and Priority")
        if not df.empty:
            heatmap_data = df.pivot_table(index="category", columns="priority", values="complaint_id", aggfunc="count", fill_value=0)
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlGnBu", ax=ax)
            ax.set_title("Heatmap of Complaints by Category and Priority", fontsize=16)
            st.pyplot(fig)
        else:
            st.write("No complaints data available.")

def forward_complaints_to_departments(complaints_collection):
    # Retrieve all complaints with status 'Pending'
    pending_complaints = list(complaints_collection.find({"status": "Pending"}))

    if not pending_complaints:
        st.info("No pending complaints to forward.")
        return

    # Forward complaints to respective departments
    for complaint in pending_complaints:
        category = complaint["category"]
        for department, categories in DEPARTMENT_MAPPING.items():
            if category in categories:
                # Update complaint with department information
                complaints_collection.update_one(
                    {"_id": complaint["_id"]},
                    {"$set": {"department": department, "status": "In Progress"}},
                )
                break  # Stop searching once a department is found

    st.success("All pending complaints have been forwarded to respective departments.")

def admin_dashboard(complaints_collection):
    st.title("Admin Dashboard")

    # Retrieve complaints from the database
    complaints = list(complaints_collection.find())

    if complaints:
        df = pd.DataFrame(complaints)
        df["complaint_id"] = df["complaint_id"].astype(str)

        # Filter complaints by status or category
        status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Resolved", "In Progress"])
        category_filter = st.selectbox("Filter by Category", ["All"] + list(df["category"].unique()))

        if status_filter != "All":
            df = df[df["status"] == status_filter]
        
        if category_filter != "All":
            df = df[df["category"] == category_filter]

        # Display the filtered complaints
        st.dataframe(df[["complaint_id", "username", "complaint", "category", "status"]])

        # Update Complaint Status
        selected_complaint_id = st.selectbox("Select Complaint ID:", df["complaint_id"].tolist())
        new_status = st.selectbox("Select New Status", ["Pending", "Resolved", "In Progress"])

        if st.button("Update Status"):
            result = complaints_collection.update_one(
                {"complaint_id": selected_complaint_id},
                {"$set": {"status": new_status}}
            )
            if result.matched_count > 0:
                st.success(f"Complaint {selected_complaint_id} updated to {new_status}.")
            else:
                st.error("Complaint ID not found.")

        # Forward complaint to department
        if st.button("Forward Complaints to the Dedpartment"):
            forward_complaints_to_departments(complaints_collection)

        if not df.empty:
        # Dropdown for chart selection
            chart_options = [
                "Bar Chart: Pending Complaints by Category",
                "Pie Chart: Pending Complaints Distribution",
                "Line Chart: Complaints Over Time",
                "Stacked Bar Chart: Complaints by Category and Status",
                "Heatmap: Complaints by Category and Priority"
            ]
            selected_chart = st.selectbox("Select a Chart to Display:", chart_options)
            
            
            plot_chart(selected_chart, df)
            
    else:
        st.info("No complaints found.")

    if st.button('Logout'):
        st.session_state.username = None

def department_admin_dashboard(complaints_collection, department_name):
    st.title(f"{department_name} Department Dashboard")

    # Retrieve complaints assigned to the department
    complaints = list(complaints_collection.find({"assigned_department": department_name}))

    if complaints:
        df = pd.DataFrame(complaints)
        df["complaint_id"] = df["complaint_id"].astype(str)

        # Display complaints
        st.dataframe(df[["complaint_id", "username", "complaint", "category", "status"]])

        # Update Complaint Status
        selected_complaint_id = st.selectbox("Select Complaint ID:", df["complaint_id"].tolist())
        new_status = st.selectbox("Select New Status", ["Pending", "Resolved", "In Progress"])

        if st.button("Update Status"):
            result = complaints_collection.update_one(
                {"complaint_id": selected_complaint_id},
                {"$set": {"status": new_status}}
            )
            if result.matched_count > 0:
                st.success(f"Complaint {selected_complaint_id} updated to {new_status}.")
            else:
                st.error("Complaint ID not found.")
    else:
        st.info(f"No complaints assigned to {department_name}.")

