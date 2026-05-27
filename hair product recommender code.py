import streamlit as st
import pandas as pd

col1, col2 = st.columns([2, 1])

with col1:
    st.title("🌱 Plant-Based Hair Product Recommender")
    st.write("Find the right product for you")

with col2:
    st.image("https://content.latest-hairstyles.com/wp-content/uploads/experts-favorite-hair-products-1200x900.jpg", use_container_width=True)
if "quiz_history" not in st.session_state:
    st.session_state["quiz_history"] = []
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

PRODUCT_BRANDS = {
    "Murumuru Butter": "Dr Adorable Inc",
    "Ouai Wave spray": "OUAI",
    "Tea Tree oil": "Nexon Botanics",
    "Coconut Oil": " Viva Naturals Organic Extra Virgin",
    "Shea Butter": "Cantue",
    "Aloe Vera": "Parachute",
    "Surface Awaken Shampoo & Conditioner": "Surface Hair Care",
    "Argan Oil": "Cliganic "
}

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
       
    best_product = max(scores, key=scores.get)
    best_brand = PRODUCT_BRANDS.get(best_product, "Generic Brand")
    
    return best_product, best_brand, scores

st.markdown("---")

if st.button("Find my perfect product", type="primary"):
    final_product, final_brand, scores = get_recommendation(user_hair, user_scalp, user_thickness, user_porosity)
    
    st.balloons()
    
    st.subheader("Your Custom Match:")
    search_query = f"{final_brand} {final_product}".replace(" ", "+")
    google_url = f"https://www.google.com/search?q={search_query}"

    st.markdown(
       f"""
    <a href="{google_url}" target="_blank" style="text-decoration: none;">
            <div style="background-color: #add8e6; color: black; padding: 15px 20px; text-align: center; border-radius: 5px; font-weight: bold; margin-top: 10px;">
                 Find {final_brand} {final_product} on Google
            </div>
        </a>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.write("Rate your recommended product")
    rating = st.slider("How accurate does this recommended product feel for your hair?", 1, 2, 3, 4, 5)
    feedback_notes = st.text_input("Any specific ingredients, brands you wish we included or did you wish the product had different results?")
    if st.button("Submit Feedback"):
        st.success(f"Thank you for your {rating}-star review! Your suggestion for '{feedback_notes}' has been sent.")
    st.markdown("---")
    st.subheader("Don't understand any off these terms?, check out this educational resource")
    if st.session_state["quiz_history"]:
        st.markdown("---")
        st.subheader(" Session Comparison Matrix")
        st.write("Your tested hair profiles are shown below. Click any column header to sort, or hover to expand columns:")
        df = pd.DataFrame(st.session_state["quiz_history"])
    st.dataframe(df, use_container_width=True)
    if st.button("Clear Quiz History", type="secondary"):
        st.session_state["quiz_history"] = []
        st.rerun()
    
    with st.expander("What is Hair porosity"):
         st.write("""
         **Hair porosity refers to your hair's ability to absorb or retain moisture:
         * **High porosity:**The hair cuticles are open. This means the hair can absorb moisture quickly, but also lose it as quickly; it can't retain moisture. This requires heavy sealant products.
         * **Medium porosity:**This is the sweet spot for porosity because the cuticles are not too tight or open, and it absorbs and retains moisture pretty well.
         * **Low porosity:**The hair cuticles are tightly packed. This means it absorbs moisture, and it also retains it, and it doesn't allow it to leave. This is the healthiest porosity type.
         """)
    with  st.expander("What are the scalp types"):
          st.write("""
          **Your scalp condition changes how products interact with your hair follicles:
          * **Dry scalp:**This lacks natural sebum production, which can cause flakes and itchiness. The flakes can easily be mistaken for dandruff, but these flakes are white, and they are like snow; dandruff is yellow.
          * **Oily scalp:**This is when there's an overproduction of sebum, which can weigh your hair down and cause greasiness.
          * **Balanced scalp:**This is when there's the perfect amount of natural sebum production, and this is a healthy scalp.
          * **Combination scalp:**This means there's different sebum activity in different areas. Some areas may be dry and some may be oily.
          """)
         
    
    
st.info("⚠️ **DISCLAIMER:** This tool is just for educational purposes. It's best to always test a product before using to make sure there is no sensitivity or allergic reactions.")
if st.session_state["current_scores"] is not None:
    st.markdown("### How your hair was scored:")
    chart_data = pd.Series(st.session_state["current_scores"])
    st.bar_chart(chart_data)
st.write("Thank you for doing this test!")
