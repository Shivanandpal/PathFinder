import streamlit as st
from backend.utils.matcher import load_roles, match_role, get_missing_skills

# Load data
roles_data = load_roles()

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to right, #ff0099, #493240);
}
[data-testid="stSidebar"] {
    background-color: #ff000050;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
st.set_page_config(page_title="AI Career Guide", layout="centered")

st.title("🚀 AI Career Guidance System")
st.write("Get career path, skills, projects & resources")

# Input
degree = st.selectbox("🎓 Degree", ["BSc IT", "BTech", "BCom", "Other"])
skills = st.text_input("💡 Enter skills (comma separated)")
year = st.selectbox("📅 Year", ["1st", "2nd", "3rd", "4th"])

if st.button("🔍 Analyze"):

    if not skills:
        st.warning("Please enter skills")
    else:
        role, score = match_role(skills, roles_data)

        if role:
            data = roles_data[role]

            missing_skills = get_missing_skills(skills, data["skills_required"])
            readiness = int((score / len(data["skills_required"])) * 100)

            # Output
            st.success(f"🎯 Target Role: {role}")
            st.info(f"📊 Readiness: {readiness}%")

            st.subheader("📉 Skill Gap")
            for skill in missing_skills:
                st.write(f"- {skill}")

            st.subheader("🪜 Next Steps")
            st.write("1. Learn missing skills")
            st.write("2. Build projects below")
            st.write("3. Apply for internships")

            # Projects
            st.subheader("🧠 Projects")
            for project in data["projects"]:
                st.markdown(f"**{project['level']} - {project['name']}**")
                for f in project["features"]:
                    st.write(f"• {f}")

            # Resources
            st.subheader("🎓 Learning Resources")

            st.write("🆓 Free:")
            for link in data["resources"]["free"]:
                st.write(link)

            st.write("💰 Paid:")
            for link in data["resources"]["paid"]:
                st.write(link)

        else:
            st.error("No matching role found. Try adding more skills.")