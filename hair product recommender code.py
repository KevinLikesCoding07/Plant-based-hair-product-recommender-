import streamlit as st
import pandas as pd
import time
import random


st.set_page_config(
    page_title="Élixir Botanique | Luxury Hair Suite",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
    <style>
    /* Global Dark Theme */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: #f8fafc !important;
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.025em;
    }
    
    p, span, label {
        color: #cbd5e1 !important;
    }
    
    /* Containers & Cards */
    div[data-testid="stVerticalBlock"] > div[style*="border"], 
    div[data-testid="stExpander"] {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        border-radius: 16px !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    
    /* Primary Gradient Button */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: white;
        border-radius: 12px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #047857 0%, #059669 100%);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.5);
        transform: translateY(-1px);
    }

    /* Secondary Buttons */
    div.stButton > button[kind="secondary"] {
        background-color: #334155 !important;
        color: #f8fafc !important;
        border: 1px solid #475569 !important;
    }

    /* Metric Cards Styling */
    [data-testid="stMetric"] {
        background-color: #1e293b;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #334155;
    }
    [data-testid="stMetricValue"] {
        color: #10b981 !important;
        font-size: 2.2rem !important;
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
        border-right: 1px solid #334155;
    }
    
    /* Alert / Info boxes */
    .stAlert {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        color: #f8fafc !important;
        border-radius: 12px;
    }
    </style>
""", unsafe_allow_html=True)


def init_session_state():
    if "quiz_history" not in st.session_state:
        st.session_state["quiz_history"] = []
    if "current_scores" not in st.session_state:
        st.session_state["current_scores"] = None
    if "wishlist" not in st.session_state:
        st.session_state["wishlist"] = []
    if "last_result" not in st.session_state:
        st.session_state["last_result"] = None
    if "diy_creations" not in st.session_state:
        st.session_state["diy_creations"] = []

init_session_state()


PRODUCT_BRANDS = {
    "Murumuru Butter": "Dr Adorable Inc",
    "Ouai Wave spray": "OUAI",
    "Tea Tree oil": "Nexon Botanics",
    "Coconut Oil": "Viva Naturals Organic Extra Virgin",
    "Shea Butter": "Cantu",
    "Aloe Vera": "Parachute",
    "Surface Awaken Shampoo & Conditioner": "Surface Hair Care",
    "Argan Oil": "Cliganic"
}

PRODUCT_EXPLAINERS = {
    "Murumuru Butter": "Rich in fatty acids; locks in moisture for curly/coily hair without heavy residue.",
    "Ouai Wave spray": "Plant proteins add striking texture, volume, and definition to wavy hair patterns.",
    "Tea Tree oil": "Clarifying agent that balances natural sebum production; ideal for oily scalps.",
    "Coconut Oil": "Penetrates the hair shaft deeply for intensive hydration on dry scalps.",
    "Shea Butter": "Creates a protective barrier on high-porosity cuticles to lock in hydration.",
    "Aloe Vera": "Lightweight hydration that moisturizes strands cleanly without feeling greasy.",
    "Surface Awaken Shampoo & Conditioner": "Botanical extracts stimulate follicles safely without harsh chemical additives.",
    "Argan Oil": "Tames flyaways and delivers brilliant gloss to straight hair."
}

def reset_app():
    st.session_state["current_scores"] = None
    st.session_state["last_result"] = None

def get_recommendation(hair, scalp, thickness, porosity, sensitivities):
    scores = {prod: 0 for prod in PRODUCT_BRANDS.keys()}
    veto = -1000
    if "Nuts / Tree Nuts" in sensitivities: scores["Shea Butter"] = veto
    if "Heavy Oils / Coconut" in sensitivities: scores["Coconut Oil"] = veto
    if "Strong Essential Oils" in sensitivities: scores["Tea Tree oil"] = veto
    
    if hair in ["Curly", "Coily"]: scores["Murumuru Butter"] += 2
    if hair == "Wavy": scores["Ouai Wave spray"] += 3
    if hair == "Straight": scores["Argan Oil"] += 3
    if scalp == "Oily": scores["Tea Tree oil"] += 4
    if scalp == "Dry": scores["Coconut Oil"] += 3
    if thickness == "Thin": scores["Surface Awaken Shampoo & Conditioner"] += 3
    if porosity == "High": scores["Shea Butter"] += 3
    if porosity == "Low": scores["Aloe Vera"] += 4

    best_product = max(scores, key=scores.get)
    if scores[best_product] <= 0:
        best_product = "Aloe Vera"
    best_brand = PRODUCT_BRANDS.get(best_product, "Élixir Labs")
    return best_product, best_brand, scores

def get_persona(hair, porosity):
    if hair == "Straight": return "✨ The Sleek & Glossy Icon"
    if hair == "Wavy": return "🌊 The Beachside Wave Master"
    if hair == "Curly": return "🌀 The Spirited Coil & Curl Royalty"
    if hair == "Coily": return "👑 The Crown Coily Sovereign"
    return "🌿 The Botanical Alchemist"


def show_recommender():
    col1, col2 = st.columns([5, 1])
    with col1:
        st.title("🌿 Élixir Botanique")
        st.markdown("### Tailored Hair Diagnostic Suite")
        st.write("Complete your botanical profile below to unlock a bespoke formulation and custom persona badge.")
    with col2:
        st.image("https://img.icons8.com/?size=100&id=118515&format=png&color=10B981", width=70)

    st.markdown("---")
    
    with st.container():
        st.subheader("I. Hair Structure")
        user_hair = st.pills("Hair Pattern:", ["Straight", "Wavy", "Curly", "Coily"], key="h_type")
        user_porosity = st.pills("Cuticle Porosity:", ["Low", "Medium", "High"], key="h_porosity")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("II. Scalp & Density")
        user_scalp = st.pills("Scalp Condition:", ["Oily", "Balanced", "Dry", "Combination"], key="s_type")
        user_thickness = st.pills("Strand Thickness:", ["Thin", "Fine", "Medium", "Thick"], key="h_thick")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("III. Safety Vetoes (Optional)")
        user_sensitivities = st.multiselect(
            "Select ingredients to filter out:",
            ["Nuts / Tree Nuts", "Heavy Oils / Coconut", "Strong Essential Oils"],
            key="sens"
        )

    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        find_btn = st.button("✨ Run Diagnostic Suite", type="primary")

    if find_btn:
        if not user_hair or not user_scalp or not user_thickness or not user_porosity:
            st.warning("⚠️ **Incomplete Profile:** Please select an option for all diagnostic categories.")
            return

        with st.spinner("Synthesizing organic data signatures..."):
            time.sleep(1.5)

        final_product, final_brand, scores = get_recommendation(user_hair, user_scalp, user_thickness, user_porosity, user_sensitivities)
        persona = get_persona(user_hair, user_porosity)
        
        st.session_state["current_scores"] = scores
        st.session_state["last_result"] = {"product": final_product, "brand": final_brand, "hair": user_hair, "persona": persona}
        st.session_state["quiz_history"].append({
            "Hair": user_hair, "Scalp": user_scalp, 
            "Thickness": user_thickness, "Porosity": user_porosity,
            "Recommendation": f"{final_brand} {final_product}"
        })
        
        st.balloons()
        st.success("Diagnostic Successful.")

        st.info(f"🏆 **Assigned Persona:** {persona}")

        max_possible_score = 10
        user_score = max(scores[final_product], 1)
        match_percentage = min(int((user_score / max_possible_score) * 100), 100)
        
        mc1, mc2 = st.columns(2)
        with mc1:
            st.metric(label="Compatibility Index", value=f"{match_percentage}%", delta="Optimized fit")
        with mc2:
            st.metric(label="Premier Brand", value=final_brand)
            
        with st.container():
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.subheader(final_product)
                st.caption(f"Manufactured by {final_brand}")
                st.write(f"💡 **Why this works:** {PRODUCT_EXPLAINERS.get(final_product, '')}")
            with col_b:
                st.write("")
                search_query = f"{final_brand} {final_product}".replace(" ", "+")
                st.link_button("Acquire Online ↗", f"https://www.google.com/search?q={search_query}")
                
                if st.button("❤️ Save to Vault", key="save_res"):
                    item_str = f"{final_brand} - {final_product}"
                    if item_str not in st.session_state["wishlist"]:
                        st.session_state["wishlist"].append(item_str)
                        st.toast("Secured in Vault!")

        st.markdown("<br>", unsafe_allow_html=True)
        col_act1, col_act2 = st.columns(2)
        with col_act1:
            scorecard_text = f"Élixir Botanique Diagnostic Profile:\n{user_hair}, {user_thickness}, {user_porosity}\nPersona: {persona}\n\nOptimal Match:\n{final_brand} {final_product}"
            st.download_button("📥 Download Diagnostic Certificate", scorecard_text, f"Certificate_{user_hair}.txt", use_container_width=True)
        with col_act2:
            st.button("Reset Diagnostic", on_click=reset_app, type="secondary", use_container_width=True)

    if st.session_state["quiz_history"]:
        st.markdown("---")
        with st.expander("📊 Diagnostic Archives"):
            df = pd.DataFrame(st.session_state["quiz_history"])
            st.dataframe(df, use_container_width=True, hide_index=True)
            if st.button("Clear Archives"):
                st.session_state["quiz_history"] = []
                st.rerun()


def show_diy_lab():
    st.title("🧪 Custom Formulation Lab")
    st.markdown("### Build Your Bespoke Organic Hair Mask")
    st.write("Hand-select carrier oils, nourishing butters, and active botanical infusions to synthesize a custom treatment.")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        mask_name = st.text_input("Formula Title:", value="Midnight Elixir")
        base_oil = st.selectbox("Carrier Oil:", ["Jojoba Oil", "Sweet Almond Oil", "Grapeseed Oil", "Argan Oil"])
        butter_choice = st.selectbox("Structural Butter/Gel:", ["Shea Butter", "Murumuru Butter", "Aloe Vera Gel", "Coconut Oil"])
        boost_add = st.selectbox("Active Botanical Infusion:", ["Tea Tree Drop (Clarifying)", "Lavender Extract (Aromatherapy)", "Vitamin E Complex (Repair)"])
        
    with col2:
        st.markdown("### 🔬 Laboratory Preview")
        with st.container():
            st.markdown(f"**Formula:** {mask_name}")
            st.markdown(f"- 🌿 **Base:** {base_oil} (30ml)")
            st.markdown(f"- 🥑 **Structure:** {butter_choice} (15g)")
            st.markdown(f"- ✨ **Infusion:** {boost_add} (5 drops)")
            
            hydration_score = random.randint(90, 99)
            st.metric(label="Bio-Compatibility Score", value=f"{hydration_score}%", delta="Pure botanical grade")
            
            if st.button("Save Formula to Vault"):
                formula_desc = f"{mask_name} ({base_oil} + {butter_choice})"
                if formula_desc not in st.session_state["diy_creations"]:
                    st.session_state["diy_creations"].append(formula_desc)
                    st.success(f"Formula '{mask_name}' synthesized and stored successfully!")
                else:
                    st.info("Formula already exists in vault.")

    if st.session_state["diy_creations"]:
        st.markdown("---")
        st.subheader("🧪 Saved Bespoke Formulas")
        for fml in st.session_state["diy_creations"]:
            st.caption(f"• 🔒 {fml}")


def show_custom_routine():
    st.title("🛁 Wash-Day Protocol")
    st.markdown("### Structured Maintenance Schedule")
    st.markdown("---")
    
    if st.session_state["last_result"]:
        res = st.session_state["last_result"]
        st.success(f"Protocol synchronized for: **{res['brand']} {res['product']}** ({res['hair']} Hair)")
        
        steps = [
            ("Phase I: Pre-Treatment & Detangling", "Delicately detangle dry strands (coily/curly) or damp strands (wavy/straight) prior to cleansing."),
            ("Phase II: Targeted Cleansing", f"Apply **{res['brand']} {res['product']}**. Massage thoroughly into roots for 3 minutes. Rinse with lukewarm water."),
            ("Phase III: Hydration Seal", "Distribute conditioning agents evenly from mid-shaft to ends. Allow 5 minutes of penetration before cool rinsing."),
            ("Phase IV: Micro-Fiber Drying", "Press gently with a microfiber towel. Apply prescribed stylers to damp cuticles.")
        ]
        
        for i, (title, desc) in enumerate(steps):
            with st.container():
                c1, c2 = st.columns([1, 6])
                with c1:
                    st.markdown(f"<h2 style='color:#10b981; text-align:center;'>0{i+1}</h2>", unsafe_allow_html=True)
                with c2:
                    st.subheader(title)
                    st.write(desc)
    else:
        st.warning("⚠️ Please execute the diagnostic suite first to generate your custom timeline.")


def show_glossary():
    st.title("📚 Botanical Lexicon")
    st.markdown("### Structural Hair Science & Scalp Anatomy")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["Hair Properties", "Scalp Classifications"])
    with tab1:
        st.markdown("### Hair Attributes")
        data = {
            "Porosity": "The cuticular layer's capacity to absorb and hold moisture. High porosity features wide-open cuticles; low porosity features tight overlapping scales.",
            "Density": "Total follicular count per square inch across the scalp.",
            "Elasticity": "The measure of structural stretch before fiber breakage occurs."
        }
        for term, definition in data.items():
            with st.expander(f"Define: {term}"):
                st.write(definition)
                
    with tab2:
        st.markdown("### Scalp Conditions")
        scalps = {
            "Oily": "Excessive sebum secretion requiring balancing clarifying agents.",
            "Dry": "Deficient natural lipid production leading to micro-flaking and tightness.",
            "Balanced": "Optimal homeostatic sebum levels.",
            "Combination": "Variable sebum activity (sebum-dense crown, dry perimeter)."
        }
        for term, definition in scalps.items():
             with st.expander(f"Condition: {term}"):
                st.write(definition)


def hair_graph():
    st.title("📈 Bio-Scoring Analytics")
    st.markdown("### Comprehensive Algorithm Scoring Breakdown")
    st.markdown("---")
    if st.session_state.get("current_scores"):
        st.subheader("Compatibility Weight Distribution:")
        chart_df = pd.DataFrame(
            list(st.session_state["current_scores"].items()), 
            columns=["Product", "Score"]
        )
        chart_df = chart_df.sort_values(by="Score", ascending=False)
        st.bar_chart(data=chart_df, x="Product", y="Score", color="#10b981")
    else:
        st.info("👋 Run a diagnostic quiz to render your scoring analytics chart.")


with st.sidebar:
    st.image("https://img.icons8.com/?size=100&id=23233&format=png&color=10B981", width=45)
    st.title("Élixir Suite")
    
    st.markdown("---")
    st.subheader("🔒 Saved Vault")
    if st.session_state["wishlist"]:
        for item in st.session_state["wishlist"]:
            st.caption(f"• {item}")
        if st.button("Purge Vault", key="clr_wsh"):
            st.session_state["wishlist"] = []
            st.rerun()
    else:
        st.info("Vault is currently empty.")
        
    st.markdown("---")
    st.subheader("Navigation")
    pages_mapping = {
        "Diagnostic Suite": show_recommender,
        "🧪 Formulation Lab": show_diy_lab,
        "Wash-Day Protocol": show_custom_routine,
        "Lexicon": show_glossary,
        "Analytics": hair_graph,
    }
    selected_page = st.selectbox("Select Module", options=list(pages_mapping.keys()), label_visibility="collapsed")
    
    st.markdown("---")
    with st.expander("⚠️ Clinical Disclaimer"):
        st.caption("Formulations are for educational and cosmetic evaluation purposes. Perform individual patch tests prior to topical application.")


pages_mapping[selected_page]()


st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b;'>Élixir Botanique &copy; 2026 | Luxury Hair Science Suite</p>", unsafe_allow_html=True)
