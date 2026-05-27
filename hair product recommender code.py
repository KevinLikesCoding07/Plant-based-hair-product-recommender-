import streamlit as st
col1, col2 = st.columns([2, 1])

with col1:
    st.title("🌱 Plant-Based Hair Product Recommender")
    st.write("Find the right product for you")

with col2:

    st.image("https://content.latest-hairstyles.com/wp-content/uploads/experts-favorite-hair-products-1200x900.jpg", use_container_width=True)



with st.container(border=True):
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
    
    if hair in ["Curly", "Coily"]:
        scores["Murumuru Butter"] += 1
    if hair == "Wavy":
        scores["Ouai Wave spray"] += 3
    if scalp == "Oily":
        scores["Tea Tree oil"] += 5
    if scalp == "Dry":
        scores["Coconut Oil"] += 4
    if porosity == "High":
        scores["Shea Butter"] += 2
    if porosity == "Low":
        scores["Aloe Vera"] += 6
    if thickness == "Thin":
        scores["Surface Awaken Shampoo & Conditioner"] += 4
    if hair == "Straight":
        scores["Argan Oil"] += 7
       
    best_match = max(scores, key=scores.get)
    return best_match
    best_brand = PRODUCT_BRANDS.get(best_product, "Generic Brand")
    
    return best_product, best_brand
st.markdown("---")


if st.button("Find my perfect product", type="primary"):
final_product, final_brand =  final_recommendation = get_recommendation(user_hair, user_scalp, user_thickness, user_porosity)
    
    # Fun effect!
    st.balloons()
    
    st.subheader("Your Custom Match:")
    st.success(f"Based on your hair profile, the best product for you is: **{final_recommendation}**")


st.info(" **DISCLAIMER:** This tool is just for educational purposes. It's best to always test a product before using to make sure there is no sensitivity or allergic reactions.")

st.write("Thank you for doing this test!")
