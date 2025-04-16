import streamlit as st

def safety_logistics_admin_page(complaints_collection):
    st.title("Safety and Logistics Department Admin Dashboard")

    # Fetch complaints assigned to the Safety and Logistics Department
    complaints = list(complaints_collection.find({
        "department": "Safety and Logistics Department",
        "status": {"$ne": "Resolved"}
    }))

    if complaints:
        for complaint in complaints:
            st.subheader(f"Complaint ID: {complaint['complaint_id']}")
            st.write(f"Category: {complaint['category']}")
            st.write(f"Complaint: {complaint['complaint']}")
            st.write(f"Priority: {complaint['priority']}")
            st.write(f"Status: {complaint['status']}")

            # Dropdown to update status
            new_status = st.selectbox(
                f"Update Status for Complaint ID {complaint['complaint_id']}",
                ["In Progress", "Pending", "Resolved"],
                key=f"status_{complaint['_id']}",
            )

            if st.button(f"Update Status for {complaint['complaint_id']}"):
                complaints_collection.update_one(
                    {"_id": complaint["_id"]},
                    {"$set": {"status": new_status}},
                )
                st.success(f"Status for Complaint ID {complaint['complaint_id']} updated to {new_status}")
    else:
        st.write("No complaints assigned to the Safety and Logistics Department.")
