"""
Recipe Preparation Agent - RAG-based Frontend Demo
AICTE 2026 - Problem Statement No. 16
IBM watsonx Orchestrate + Streamlit

Design: "Night Market" theme — warm charred background, chili-red /
mango-yellow / jade-green accents, recipe results styled as food-stall
order tickets with diet-type color badges.
"""

import streamlit as st
import streamlit.components.v1 as components
import json

# ---------------------------------------------------------------
# Custom hero illustration (original SVG artwork — no external
# images, so no copyright/hotlink concerns for GitHub submission)
# ---------------------------------------------------------------
HERO_SVG = """
<div style="text-align:center; margin-bottom: 6px;">
<svg width="100%" height="170" viewBox="0 0 800 170" xmlns="http://www.w3.org/2000/svg">
  <path d="M330 70 Q315 40 335 18 Q350 2 336 -18" stroke="#B7A697" stroke-width="3"
        fill="none" opacity="0.45" stroke-linecap="round"/>
  <path d="M400 65 Q385 35 405 12 Q420 -4 406 -26" stroke="#B7A697" stroke-width="3"
        fill="none" opacity="0.6" stroke-linecap="round"/>
  <path d="M470 70 Q455 40 475 18 Q490 2 476 -18" stroke="#B7A697" stroke-width="3"
        fill="none" opacity="0.45" stroke-linecap="round"/>

  <path d="M230 108 Q400 190 570 108" stroke="#3E322A" stroke-width="7" fill="none" stroke-linecap="round"/>
  <ellipse cx="400" cy="112" rx="172" ry="22" fill="#241D19" stroke="#3E322A" stroke-width="3"/>

  <rect x="176" y="100" width="46" height="9" rx="4.5" fill="#3E322A"/>
  <rect x="578" y="100" width="46" height="9" rx="4.5" fill="#3E322A"/>

  <circle cx="330" cy="92" r="13" fill="#E8491D"/>
  <circle cx="368" cy="80" r="9"  fill="#F2A93B"/>
  <circle cx="404" cy="94" r="12" fill="#6FA287"/>
  <circle cx="440" cy="82" r="8"  fill="#F2A93B"/>
  <circle cx="472" cy="96" r="10" fill="#E8491D"/>
  <path d="M300 96 q8 -10 16 0" stroke="#F7EEE3" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.7"/>
  <path d="M495 92 q8 -10 16 0" stroke="#F7EEE3" stroke-width="3" fill="none" stroke-linecap="round" opacity="0.7"/>

  <line x1="520" y1="60" x2="600" y2="130" stroke="#F2A93B" stroke-width="5" stroke-linecap="round"/>
  <line x1="535" y1="55" x2="615" y2="125" stroke="#F2A93B" stroke-width="5" stroke-linecap="round"/>
</svg>
</div>
"""

# ---------------------------------------------------------------
# Page config
# ---------------------------------------------------------------
st.set_page_config(
    page_title="Recipe Preparation Agent",
    page_icon="🍜",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------
# Theme — "Night Market"
# ---------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;0,9..144,700;0,9..144,900;1,9..144,600&family=Work+Sans:wght@400;500;600;700&display=swap');

:root {
    --bg: #1B1512;
    --bg-card: #241D19;
    --bg-card-2: #2C231E;
    --chili: #E8491D;
    --mango: #F2A93B;
    --jade: #6FA287;
    --text: #F7EEE3;
    --muted: #B7A697;
    --border: #3E322A;
}

html, body, [class*="css"]  { font-family: 'Work Sans', sans-serif; }

.stApp {
    background: radial-gradient(circle at 15% 0%, #2A2019 0%, #1B1512 45%), var(--bg);
    color: var(--text);
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2.2rem; max-width: 760px; }

/* ---------- Hero ---------- */
.hero-eyebrow {
    display: inline-block;
    font-family: 'Work Sans', sans-serif;
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--mango);
    background: rgba(242, 169, 59, 0.1);
    border: 1px solid rgba(242, 169, 59, 0.35);
    padding: 5px 14px;
    border-radius: 999px;
    margin-bottom: 18px;
}
.hero-title {
    font-family: 'Fraunces', serif;
    font-weight: 900;
    font-size: 3rem;
    line-height: 1.05;
    color: var(--text);
    margin: 0 0 10px 0;
}
.hero-title em {
    font-style: italic;
    font-weight: 600;
    color: var(--chili);
}
.hero-sub {
    font-family: 'Work Sans', sans-serif;
    color: var(--muted);
    font-size: 1.02rem;
    max-width: 520px;
    margin-bottom: 28px;
}

/* ---------- Input "wok" card ---------- */
.wok-card {
    background: linear-gradient(155deg, var(--bg-card) 0%, var(--bg-card-2) 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 28px 26px 8px 26px;
    margin-bottom: 28px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.35);
}
.section-label {
    font-family: 'Fraunces', serif;
    font-weight: 700;
    font-size: 1.3rem;
    color: var(--text);
    margin-bottom: 4px;
}

/* Streamlit widget restyling */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: #1E1713 !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--chili) !important;
    box-shadow: 0 0 0 1px var(--chili) !important;
}
div[data-baseweb="select"] > div {
    background: #1E1713 !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
}
.stCheckbox label p { color: var(--muted) !important; }

.stButton > button {
    background: linear-gradient(135deg, var(--chili) 0%, #C93A15 100%) !important;
    color: #FFF6EE !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Work Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1.02rem !important;
    padding: 0.7rem 1rem !important;
    width: 100%;
    box-shadow: 0 8px 20px rgba(232, 73, 29, 0.35) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 26px rgba(232, 73, 29, 0.45) !important;
}

[data-testid="stExpander"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
}

/* ---------- Recipe "ticket" card ---------- */
.ticket {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 22px 24px 20px 24px;
    margin-bottom: 22px;
    position: relative;
    border-top: 3px dashed var(--border);
}
.ticket-name {
    font-family: 'Fraunces', serif;
    font-weight: 700;
    font-size: 1.5rem;
    color: var(--text);
    margin-bottom: 8px;
}
.badge-row { margin-bottom: 14px; display: flex; flex-wrap: wrap; gap: 8px; }
.badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 999px;
    letter-spacing: 0.02em;
}
.badge-veg { background: rgba(111,162,135,0.15); color: var(--jade); border: 1px solid rgba(111,162,135,0.4); }
.badge-nonveg { background: rgba(232,73,29,0.15); color: var(--chili); border: 1px solid rgba(232,73,29,0.4); }
.badge-egg { background: rgba(242,169,59,0.15); color: var(--mango); border: 1px solid rgba(242,169,59,0.4); }
.badge-cuisine { background: rgba(247,238,227,0.08); color: var(--muted); border: 1px solid var(--border); }
.dot { width: 7px; height: 7px; border-radius: 50%; display: inline-block; }
.dot-veg { background: var(--jade); }
.dot-nonveg { background: var(--chili); }
.dot-egg { background: var(--mango); }

.meta-row {
    display: flex; gap: 18px; flex-wrap: wrap;
    font-size: 0.85rem; color: var(--muted);
    border-bottom: 1px solid var(--border);
    padding-bottom: 14px; margin-bottom: 16px;
}
.meta-item { display: flex; align-items: center; gap: 6px; }

.ing-title, .step-title, .sub-title {
    font-family: 'Work Sans', sans-serif;
    font-weight: 700;
    font-size: 0.78rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--mango);
    margin: 14px 0 8px 0;
}
.ing-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 4px; }
.ing-chip {
    background: #1E1713;
    border: 1px solid var(--border);
    color: var(--text);
    font-size: 0.85rem;
    padding: 5px 12px;
    border-radius: 10px;
}
.step-list { list-style: none; padding: 0; margin: 0; counter-reset: step; }
.step-list li {
    counter-increment: step;
    position: relative;
    padding-left: 34px;
    margin-bottom: 10px;
    font-size: 0.92rem;
    color: var(--text);
    line-height: 1.5;
}
.step-list li::before {
    content: counter(step);
    position: absolute;
    left: 0; top: 0;
    width: 22px; height: 22px;
    background: var(--chili);
    color: #FFF6EE;
    font-size: 0.72rem;
    font-weight: 700;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
}
.sub-box {
    background: rgba(111,162,135,0.08);
    border: 1px solid rgba(111,162,135,0.25);
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 0.85rem;
    color: var(--text);
    margin-bottom: 4px;
}
.sub-box div { margin-bottom: 4px; }
.tip-line {
    margin-top: 16px;
    font-style: italic;
    color: var(--mango);
    font-size: 0.88rem;
    border-left: 2px solid var(--mango);
    padding-left: 12px;
}

.footer-note {
    text-align: center;
    color: var(--muted);
    font-size: 0.8rem;
    margin-top: 30px;
    padding-top: 18px;
    border-top: 1px solid var(--border);
}

@media (max-width: 640px) {
    .hero-title { font-size: 2.1rem; }
    .meta-row { flex-direction: column; gap: 6px; }
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------
# Load knowledge base
# ---------------------------------------------------------------
@st.cache_data
def load_recipes():
    with open("recipes.json", "r", encoding="utf-8") as f:
        return json.load(f)

recipes = load_recipes()

# ---------------------------------------------------------------
# Retrieval logic (simple RAG-style scoring)
# ---------------------------------------------------------------
def score_recipe(recipe, user_ingredients, diet_pref, cuisine_pref, equipment_hint):
    score = 0
    ing_text = " ".join(recipe["ingredients"]).lower()

    for ing in user_ingredients:
        ing = ing.strip().lower()
        if ing and ing in ing_text:
            score += 3

    if diet_pref != "Any":
        if recipe["diet"] == diet_pref:
            score += 5
        else:
            score -= 100

    if cuisine_pref != "Any" and recipe["cuisine"] == cuisine_pref:
        score += 2

    if equipment_hint:
        eq = recipe["equipment"].lower()
        if "pan" in eq or "none" in eq:
            score += 2

    return score


def retrieve_best_recipes(user_ingredients, diet_pref, cuisine_pref, equipment_hint, top_n=3):
    scored = [
        (score_recipe(r, user_ingredients, diet_pref, cuisine_pref, equipment_hint), r)
        for r in recipes
    ]
    scored.sort(key=lambda x: x[0], reverse=True)
    results = [r for s, r in scored if s > 0]
    return results[:top_n] if results else [scored[0][1]]


DIET_BADGE = {
    "Vegetarian": ("badge-veg", "dot-veg", "Vegetarian"),
    "Non-Vegetarian": ("badge-nonveg", "dot-nonveg", "Non-Vegetarian"),
    "Eggetarian": ("badge-egg", "dot-egg", "Eggetarian"),
}


def render_recipe_card(recipe, servings_override=None):
    servings = servings_override or recipe["servings"]
    diet_class, dot_class, diet_label = DIET_BADGE.get(
        recipe["diet"], ("badge-cuisine", "dot-veg", recipe["diet"])
    )

    ingredients_html = "".join(
        f'<span class="ing-chip">{ing}</span>' for ing in recipe["ingredients"]
    )
    steps_html = "".join(f"<li>{step}</li>" for step in recipe["steps"])

    subs_html = ""
    if recipe.get("substitutions"):
        subs_items = "".join(f"<div>🔄 {s}</div>" for s in recipe["substitutions"])
        subs_html = (
            '<div class="sub-title">Substitutions</div>'
            f'<div class="sub-box">{subs_items}</div>'
        )

    html = (
        '<div class="ticket">'
        f'<div class="ticket-name">{recipe["name"]}</div>'
        '<div class="badge-row">'
        f'<span class="badge {diet_class}"><span class="dot {dot_class}"></span>{diet_label}</span>'
        f'<span class="badge badge-cuisine">{recipe["cuisine"]}</span>'
        '</div>'
        '<div class="meta-row">'
        f'<span class="meta-item">🍽️ Serves {servings}</span>'
        f'<span class="meta-item">⏱️ {recipe["prepTime"]}</span>'
        f'<span class="meta-item">🔧 {recipe["equipment"]}</span>'
        '</div>'
        '<div class="ing-title">Ingredients</div>'
        f'<div class="ing-chips">{ingredients_html}</div>'
        '<div class="step-title">Steps</div>'
        f'<ul class="step-list">{steps_html}</ul>'
        f'{subs_html}'
        f'<div class="tip-line">💡 {recipe["tips"]}</div>'
        '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def render_read_aloud_button(recipe, key_suffix):
    """Hands-free 'Read Steps Aloud' using the browser's built-in
    Web Speech API — no external TTS service, works offline once loaded."""
    spoken_text = f"{recipe['name']}. Ingredients: " + ", ".join(recipe["ingredients"])
    spoken_text += ". Steps: " + " ".join(
        f"Step {i+1}. {s}" for i, s in enumerate(recipe["steps"])
    )
    text_json = json.dumps(spoken_text)
    btn_id = f"tts-{key_suffix}"

    html = f"""
    <div style="font-family:'Work Sans',sans-serif;">
      <button id="{btn_id}" style="
          background: linear-gradient(135deg, #6FA287 0%, #4F7D63 100%);
          color: #F7EEE3; border: none; border-radius: 10px;
          padding: 9px 16px; font-size: 0.88rem; font-weight: 600;
          cursor: pointer; width: 100%;">
        🔊 Read Steps Aloud
      </button>
    </div>
    <script>
      const btn = document.getElementById("{btn_id}");
      const text = {text_json};
      let speaking = false;
      btn.onclick = () => {{
        if (speaking) {{
          window.speechSynthesis.cancel();
          speaking = false;
          btn.innerText = "🔊 Read Steps Aloud";
          return;
        }}
        const utter = new SpeechSynthesisUtterance(text);
        utter.rate = 0.95;
        utter.onend = () => {{
          speaking = false;
          btn.innerText = "🔊 Read Steps Aloud";
        }};
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(utter);
        speaking = true;
        btn.innerText = "⏸ Stop Reading";
      }};
    </script>
    """
    components.html(html, height=54)


# ---------------------------------------------------------------
# Hero
# ---------------------------------------------------------------
st.markdown(HERO_SVG, unsafe_allow_html=True)

st.markdown("""
<div class="hero-eyebrow">🍜 AICTE 2026 · Problem Statement No. 16</div>
<div class="hero-title">What's in your <em>pantry</em><br>tonight?</div>
<div class="hero-sub">
    Tell your Recipe Preparation Agent what you've got — it'll pull a
    ready-to-cook pan-Asian dish from a 30-recipe knowledge base, with
    substitutions for whatever you're missing.
</div>
""", unsafe_allow_html=True)

with st.expander("ℹ️  About this project"):
    st.markdown(
        """
        This is the **frontend demo** for a Recipe Preparation Agent built for
        the AICTE-IBM SkillsBuild University Engagement program.

        - **Core agent** is built and deployed on **IBM watsonx Orchestrate**
          (IBM Cloud Lite services) with a RAG knowledge base of 30 pan-Asian recipes.
        - This Streamlit app mirrors the **same retrieval logic** locally,
          for an interactive, shareable web demo.
        - Covers **Thai, Chinese/Indo-Chinese, Japanese, Korean, and
          Vietnamese** cuisines, tagged by diet type, with substitutions for
          hostel/home cooking.
        """
    )

# ---------------------------------------------------------------
# Input card
# ---------------------------------------------------------------
st.markdown('<div class="wok-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">🧂 What have you got?</div>', unsafe_allow_html=True)

ingredients_input = st.text_input(
    "Ingredients",
    placeholder="e.g. paneer, capsicum, onion",
    label_visibility="collapsed",
)

col1, col2 = st.columns(2)
with col1:
    diet_pref = st.selectbox("Diet Preference", ["Any", "Vegetarian", "Non-Vegetarian", "Eggetarian"])
with col2:
    cuisine_pref = st.selectbox(
        "Cuisine Preference",
        ["Any", "Thai", "Chinese", "Indo-Chinese", "Japanese", "Korean", "Vietnamese"]
    )

col3, col4 = st.columns(2)
with col3:
    equipment_hint = st.checkbox("🏠 Hostel-friendly (limited equipment)")
with col4:
    servings_override = st.number_input("Servings needed", min_value=1, max_value=10, value=1)

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
search_clicked = st.button("🔍  Find My Recipe")
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------
# Results
# ---------------------------------------------------------------
if search_clicked:
    if not ingredients_input.strip():
        st.warning("Enter at least one ingredient to get started.")
    else:
        user_ingredients = [i.strip() for i in ingredients_input.split(",") if i.strip()]
        results = retrieve_best_recipes(
            user_ingredients, diet_pref, cuisine_pref, equipment_hint, top_n=3
        )
        st.markdown(
            f'<div class="section-label" style="margin-bottom:14px;">'
            f'🍳 {len(results)} recipe{"s" if len(results) > 1 else ""} for you</div>',
            unsafe_allow_html=True,
        )
        for idx, r in enumerate(results):
            render_recipe_card(r, servings_override)
            render_read_aloud_button(r, key_suffix=f"{r['name']}-{idx}")

st.markdown(
    '<div class="footer-note">Built with Streamlit • Powered by IBM watsonx '
    'Orchestrate (RAG) • Curated for students, hostlers & home cooks</div>',
    unsafe_allow_html=True,
)
