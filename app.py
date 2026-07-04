import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import pickle

    # Load model and scaler
model = pickle.load(open("models/placement_model.pkl", "rb"))
scaler = pickle.load(open("models/scaler.pkl", "rb"))

st.set_page_config(
        page_title="PlacementPro AI",
        page_icon="🎓",
        layout="centered"
    )

st.title("🎓 PlacementPro AI")
st.write("Predict placement probability and get personalized career guidance.")

    # User Inputs
cgpa = st.slider("CGPA", 0.0, 10.0, 7.0)
internship = st.selectbox("Internship", ["No", "Yes"])
projects = st.number_input("Projects", 0)
workshops = st.number_input("Workshops", 0)
aptitude = st.number_input("Aptitude Score", 0)
softskills = st.number_input("Soft Skills Score", 0)
training = st.selectbox("Placement Training", ["No", "Yes"])

    # Convert categorical values
internship = 1 if internship == "Yes" else 0
training = 1 if training == "Yes" else 0

columns = [
        "CGPA",
        "Internships",
        "Projects",
        "Workshops/Certifications",
        "AptitudeTestScore",
        "SoftSkillsRating",
        "PlacementTraining"
    ]

    # Reusable Prediction Function
def get_prediction(cgpa, internship, projects, workshops,aptitude, softskills, training):

        input_data = pd.DataFrame(
            [[
                cgpa,
                internship,
                projects,
                workshops,
                aptitude,
                softskills,
                training
            ]],
            columns=columns
        )

        scaled = scaler.transform(input_data)

        probability = model.predict_proba(scaled)[0][1]

        return probability

    # Prediction
if st.button("🚀 Analyze Risk"):

        prob = get_prediction(
        cgpa,
        internship,
        projects,
        workshops,
        aptitude,
        softskills,
        training
        )

        percentage = prob * 100

        st.subheader("📊 Analysis Result")

        st.metric(
            "Placement Probability",
            f"{percentage:.2f}%"
        )
        st.progress(int(percentage))

        # Risk Level
        if percentage >= 70:
            st.success("✅ High Chance of Placement")

        elif percentage >= 40:
            st.warning("⚠️ Moderate Chance of Placement")

        else:
            st.error("❌ Low Chance of Placement")

        # Strength Analysis
        st.subheader("💪 Strength Analysis")

        strengths = []

        if cgpa >= 8:
            strengths.append("Strong Academic Performance")
            
        if workshops >= 2:
            strengths.append("Active in Certifications and Workshops")

        if internship == 1:
            strengths.append("Industry Exposure Through Internship")

        if projects >= 3:
            strengths.append("Good Project Portfolio")

        if aptitude >= 70:
            strengths.append("Strong Aptitude Skills")

        if softskills >= 80:
            strengths.append("Excellent Communication Skills")

        if strengths:
            for strength in strengths:
                st.write("✅", strength)
        else:
            st.write("No major strengths identified yet.")

        # Career Advisor
        st.subheader("🎯 Career Advisor")

        suggestions = []

        if cgpa < 7:
            suggestions.append("Improve CGPA above 7")

        if internship == 0:
            suggestions.append("Complete at least one internship")

        if projects < 3:
            suggestions.append("Build more real-world projects")

        if workshops < 2:
            suggestions.append("Attend certifications/workshops")

        if aptitude < 70:
            suggestions.append("Improve aptitude preparation")

        if softskills < 70:
            suggestions.append("Improve communication and soft skills")

        if training == 0:
            suggestions.append("Join placement training sessions")

        if suggestions:
            for item in suggestions:
                st.write("•", item)
        else:
            st.success(
                "Excellent profile! Keep maintaining your performance."
            )
        # -----------------------------
        # What-If Simulator
        # -----------------------------
        st.subheader("🔮 What-If Simulator")

        st.write("See how improving different areas can increase your placement probability.")

        scenarios = []

            # Scenario 1 - Improve CGPA
        improved_prob = get_prediction(
                max(cgpa, 8.5),
                internship,
                projects,
                workshops,
                aptitude,
                softskills,
                training
            )

        scenarios.append((
            "📈 Improve CGPA to 8.5",
            improved_prob
        ))

            # Scenario 2 - Complete Internship
        improved_prob = get_prediction(
                cgpa,
                1,
                projects,
                workshops,
                aptitude,
                softskills,
                training
            )

        scenarios.append((
                "💼 Complete One Internship",
                improved_prob
        ))

            # Scenario 3 - Build More Projects
        improved_prob = get_prediction(
                cgpa,
                internship,
                max(projects, 4),
                workshops,
                aptitude,
                softskills,
                training
        )

        scenarios.append((
                "📚 Build 4 Projects",
                improved_prob
        ))

            # Scenario 4 - Improve Aptitude
        improved_prob = get_prediction(
                cgpa,
                internship,
                projects,
                workshops,
                max(aptitude, 85),
                softskills,
                training
        )

        scenarios.append((
                "🧠 Improve Aptitude to 85",
                improved_prob
        ))

            # Display Results
        for title, new_prob in scenarios:

            new_percentage = new_prob * 100
            increase = new_percentage - percentage

            st.write("---")
            st.write(f"### {title}")
            st.metric(
                "New Placement Probability",
                f"{new_percentage:.2f}%",
                delta=f"{increase:.2f}%"
            )
        
        # ----------------------------------
        # Feature Importance
        # ----------------------------------

        st.subheader("📊 Feature Importance")

        importances = model.feature_importances_

        feature_names = columns

        importance_df = pd.DataFrame({
            "Feature": feature_names,
            "Importance": importances
        })

        importance_df = importance_df.sort_values(
            by="Importance",
            ascending=False
        )

        fig, ax = plt.subplots(figsize=(8,4))

        ax.barh(
            importance_df["Feature"],
            importance_df["Importance"]
        )

        ax.set_xlabel("Importance Score")
        ax.set_ylabel("Features")
        ax.set_title("Random Forest Feature Importance")

        ax.invert_yaxis()

        st.pyplot(fig)


