import streamlit as st
import pandas as pd
import time  
def show_recommender():
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("🌱 Plant-Based Hair Product Recommender")
        st.write("Find the right product for you")

with col2:
    st.image("https://content.latest-hairstyles.com/wp-content/uploads/experts-favorite-hair-products-1200x900.jpg", use_container_width=True)

if "quiz_history" not in st.session_state:
    st.session_state["quiz_history"] = []

with st.container(border=True):
    user_hair = st.pills(
        "Enter your hair type:",
        ["Straight", "Wavy", "Curly", "Coily"]
    )

    user_scalp = st.pills(
        "Enter scalp type:",
        ["Oily", "Balanced", "Dry", "Combination"]
    )

    user_thickness = st.pills(
        "Enter Hair Thickness:",
        ["Thin", "Fine", "Medium", "Thick"]
    )

    user_porosity = st.pills(
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

PRODUCT_EXPLAINERS = {
    "Murumuru Butter": "Murumuru Butter is excellent for curly and coily hair. It also locks in moisture, making it useful for curly and coily hair because they tend to dry easily.",
    "Ouai Wave spray": "Ouai wave spray is really good for wavy hair because it uses plant proteins to give your wavy hair more texture, volume, and definition.",
    "Tea Tree oil": "Tea tree oil is like a clarifying agent, which balances sebum and helps with an oily scalp.",
    "Coconut Oil": "Coconut oil penetrates your scalp and locks in moisture,  which is perfect for a dry scalp.",
    "Shea Butter": "Shea butter is good for high porosity hair because it acts like a protective barrier with an open  cuticle, which locks in moisture.",
    "Aloe Vera": "Aloe vera is a lightweight, hydration product that hydrates your hair without making it greasy.",
    "Surface Awaken Shampoo & Conditioner": "Surface Awaken Shampoo & Conditioner uses natural, botanical ingredients that stimulate your scalp and this product doesn't have any chemicals that will damage your hair",
    "Argan Oil": "Argan oil is a lightweight, frizz control product that moisturizes your hair and scalp, and it is amazing for straight hair and straight hair patterns that can get frizzy", 
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
    
    if user_hair is None or user_scalp is None or user_thickness is None or user_porosity is None:
        st.error("⚠️ **Missing information:** Please select an option for ALL 4 questions before running the recommendation engine!")
    else:
        with st.spinner("Analyzing your hair details....."):
            time.sleep(2.5)
        st.success("We found your perfect product")

        final_product, final_brand, scores = get_recommendation(user_hair, user_scalp, user_thickness, user_porosity)
        st.session_state["current_scores"] = scores
        st.session_state["quiz_history"].append({
            "Hair Type": user_hair,
            "Scalp Type": user_scalp,
            "Thickness": user_thickness,
            "Porosity": user_porosity,
            "Recommended Product": f"{final_brand} {final_product}"
        })
        st.balloons()
        
        max_possible_score = 7
        user_score = scores[final_product]
        match_percentage = min(int((user_score / max_possible_score) * 100), 100)
        
        st.subheader("Your Custom Match:")
        
       
        col_metric1, col_metric2 = st.columns(2)
        with col_metric1:
            st.metric(label="Match Compatibility", value=f"{match_percentage}%", delta="Most compatible Product for you")
        with col_metric2:
            st.metric(label="Recommended Brand", value=final_brand)
            
        search_query = f"{final_brand} {final_product}".replace(" ", "+")
        google_url = f"https://www.google.com/search?q={search_query}"
        match_explainer = PRODUCT_EXPLAINERS.get(final_product, "This product is a perfect match for your hair details!")
        st.info(f"💡 **Why this works:** {match_explainer}")
        
        google_button_html = f'<a href="{google_url}" target="_blank" style="text-decoration: none;"><div style="background-color: #add8e6; color: black; padding: 15px 20px; text-align: center; border-radius: 5px; font-weight: bold; margin-top: 10px;">Find {final_brand} {final_product} on Google</div></a>'
        st.markdown(google_button_html, unsafe_allow_html=True)
        
        scorecard_text = f"""
        Plant-based hair product recommender
        ------------------------------------
        YOUR PROFILE:
        - Hair type: {user_hair}
        - Scalp type: {user_scalp}
        - Hair Thickness: {user_thickness}
        - Hair porosity: {user_porosity}
        --------------------------------
        YOUR MATCH:
        Product: {final_product}
        Brand: {final_brand}
        --------------------
        WHY THIS WORKS
        {match_explainer}
        -----------------
        Generated by Plant-Based Hair Product Recommender
        Disclaimer: This tool is just for educational purposes. It's best to always test a product before using to make sure there is no sensitivity or allergic reactions.
        """
        st.download_button(
            label="📥 Download My Hair Scorecard",
            data=scorecard_text,
            file_name=f"Hair_Scorecard_{user_hair}.txt",
            mime="text/plain",
            use_container_width=True
        )

if st.button("reset quiz", type="secondary"):
   st.session_state["current_scores"] = None
   st.rerun()
def show_rating():
    st.markdown("---")
    st.write("Rate your recommended product")
    rating = st.slider("How accurate does this recommended product feel for your hair?", 1, 5, 4)
    feedback_notes = st.text_input("Any specific ingredients, brands you wish we included or did you wish the product had different results?")
    if st.button("Submit Feedback"):
     st.success(f"Thank you for your {rating}-star review! Your suggestion for '{feedback_notes}' has been sent.")
     st.markdown("---")
     
if st.session_state["quiz_history"]:
   st.markdown("---")
   st.subheader(" Session Comparison Matrix")
   st.write("Your tested hair profiles are shown below. Click any column header to sort, or hover to expand columns:")
   df = pd.DataFrame(st.session_state["quiz_history"])
   st.dataframe(df, use_container_width=True)

if st.button("Clear Quiz History", type="secondary"):
   st.session_state["quiz_history"] = []
   st.rerun()
def show_glossary
st.subheader("Don't understand any of these terms?, check out this educational resource")

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
def show_routine():
st.subheader("Hair care routine for each type of hair")

with st.expander("Straight hair routine"):
     st.write("""
     * Wash your hair 2-3 times a week.
     * Use a sulfate-free shampoo and use a conditioner to make sure hair doesn't fall flat and look frizzy.
     * Use a brush to detangle.
     * Use a natural hair oil once a week to maintain a healthy scalp.
     """)
with st.expander("Wavy hair routine"):
     st.write("""
     * Avoid using too much shampoo; only use it 2-3 times a week.
     * Avoid brushing your hair while it is dry, as this can damage hair and cause frizz. Only brush when wet.
     * Use a lightweight conditioner every time you use shampoo.
     * Use a lightweight hair oil once a week for scalp health.
     """)
with st.expander("Curly hair routine"):
     st.write("""
     *Avoid brushing your hair dry; do it while it is wet.
     * Use richer products.
     * Use a sulfate-free shampoo and cleansing conditioner.
     * Sleep with a silk bonnet to avoid frizz.
     """)
with st.expander("Coily hair routine"):
     st.write("""
     * Use sulfate-free shampoo and a rich conditioner once a week
     * Sleep with a bonnet to protect hair
     * Use light oils for a healthy scalp
     """)
st.info("⚠️ **DISCLAIMER:** This tool is just for educational purposes. It's best to always test a product before using to make sure there is no sensitivity or allergic reactions.")

if st.session_state.get("current_scores") is not None:
    st.markdown("### How your hair was scored:")
    
    chart_df = pd.DataFrame(
        list(st.session_state["current_scores"].items()), 
        columns=["Product", "Score"]
    )
    
    st.bar_chart(data=chart_df, x="Product", y="Score", color="#FFD700")
    st.write("Thank you for doing this test!")

pages = {
    "Find my perfect product quiz": [
        st.Page(show_recommender, title="Product recommender"),
    ],

    "Rating my product": [
        st.Page(show_rating, title="Product feedback"),
    ],

    "Information": [
        st.Page(show_glossary, title="Hair terms"),
        st.Page(show_routine, title="Hair routines"),
        ],
}

pg = st.navigation(pages)
pg.run()
