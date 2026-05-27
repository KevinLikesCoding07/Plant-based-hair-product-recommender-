import streamlit as st

st.title("🌱 Plant-Based Hair Product Recommender")

# 1. Gather inputs using Streamlit selectboxes
user_hair = st.selectbox(
    "Enter your hair type:",
    ["Straight", "Wavy", "Curly", "Coily"]
)

user_scalp = st.selectbox(
    "Enter scalp type:",
    ["Oily", "Balanced", "Dry", "Combination"]
)

user_thickness = st.selectbox(
    "Enter Hair Thickness:",
    ["Thin", "Fine", "Medium", "Thick"]
)

user_porosity = st.selectbox(
    "Enter Hair porosity:",
    ["Low", "Medium", "High"]
)

def get_recommendation(hair, scalp, thickness, porosity):
    scores = {
        "Murumuru Butter": 0, 
        "Ouai Wave spray": 0, 
        "Tea Tree oil": 0, 
        "Coconut Oil": 0, 
        "Shea Butter": 0, 
        "Aloe Vera": 0, 
        "Surface Awaken Shampoo & Conditioner": 0, 
        "Argan Oil": 0
    }
    
    # Matches strings exactly as they appear in the dropdowns
    if hair in ["Curly", "Coily"]:
        scores["Murumuru Butter"] += 3
    if hair == "Wavy":
        scores["Ouai Wave spray"] += 3
    if scalp == "Oily":
        scores["Tea Tree oil"] += 5
    if scalp == "Dry":
        scores["Coconut Oil"] += 5
    if porosity == "High":
        scores["Shea Butter"] += 5
    if porosity == "Low":
        scores["Aloe Vera"] += 5
    if thickness == "Thin":
        scores["Surface Awaken Shampoo & Conditioner"] += 5
    if hair == "Straight":
        scores["Argan Oil"] += 5
       
    best_match = max(scores, key=scores.get)
    return best_match

st.markdown("---")

final_recommendation = get_recommendation(user_hair, user_scalp, user_thickness, user_porosity)

st.subheader("Your Custom Match:")
st.success(f"Based on your hair profile, the best product for you is: **{final_recommendation}**")

# 4. Disclaimers and Outros
st.info(" **DISCLAIMER:** This tool is just for educational purposes. It's best to always test a product before using to make sure there is no sensitivity or allergic reactions.")

st.write("Thank you for doing this test!")

