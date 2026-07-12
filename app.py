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
import requests

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
.badge-online { background: rgba(90,150,220,0.15); color: #7EB3F0; border: 1px solid rgba(90,150,220,0.4); }
.badge-kb { background: rgba(111,162,135,0.1); color: var(--jade); border: 1px solid rgba(111,162,135,0.3); }
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
.ing-chip-have {
    background: rgba(111,162,135,0.14);
    border: 1px solid rgba(111,162,135,0.45);
    color: var(--jade);
    font-weight: 600;
}
.ing-chip-staple {
    background: rgba(242,169,59,0.1);
    border: 1px solid rgba(242,169,59,0.35);
    color: var(--mango);
}
.coverage-tag {
    display: block;
    font-size: 0.78rem;
    color: var(--muted);
    margin-bottom: 8px;
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


def ingredient_match_count(recipe, user_ingredients):
    ing_text = " ".join(recipe["ingredients"]).lower()
    return sum(
        1 for ing in user_ingredients
        if ing.strip() and ing.strip().lower() in ing_text
    )


def retrieve_best_recipes(user_ingredients, diet_pref, cuisine_pref, equipment_hint, top_n=3):
    scored = [
        (score_recipe(r, user_ingredients, diet_pref, cuisine_pref, equipment_hint), r)
        for r in recipes
    ]
    scored.sort(key=lambda x: x[0], reverse=True)
    results = [r for s, r in scored if s > 0]
    top_recipe = results[0] if results else scored[0][1]

    # Confidence = fraction of the user's ingredients actually present in
    # the best local match. Coincidental single-ingredient overlaps (e.g.
    # "onion" or "tomato" showing up in an unrelated dish) shouldn't count
    # as a genuine match — we want most of what the user has to be covered.
    matched = ingredient_match_count(top_recipe, user_ingredients)
    match_ratio = matched / len(user_ingredients) if user_ingredients else 0

    final_results = results[:top_n] if results else [scored[0][1]]
    return final_results, match_ratio


# Items assumed present in almost every kitchen — these should never count
# as "missing" just because the user didn't explicitly list them.
PANTRY_STAPLES = [
    "salt", "oil", "water", "sugar", "black pepper", "pepper", "ghee",
    "cooking oil", "vegetable oil", "butter", "vinegar",
]


def missing_ingredient_count(recipe, user_ingredients):
    """How many ingredients in this recipe the user would still need to buy
    (i.e. not something they listed, and not a common pantry staple)."""
    normalized_user = [normalize_for_search(u) for u in user_ingredients if u.strip()]
    missing = 0
    for ing in recipe["ingredients"]:
        ing_lower = ing.lower()
        user_has = any(u in ing_lower for u in normalized_user)
        is_staple = any(s in ing_lower for s in PANTRY_STAPLES)
        if not user_has and not is_staple:
            missing += 1
    return missing


def retrieve_zero_shopping(user_ingredients, diet_pref, cuisine_pref, top_n=3):
    """Scan the whole knowledge base and rank by fewest missing ingredients,
    instead of the usual overlap-score retrieval — used when the user
    explicitly doesn't want to buy anything extra."""
    candidates = []
    for r in recipes:
        if diet_pref != "Any" and r["diet"] != diet_pref:
            continue
        if cuisine_pref != "Any" and r["cuisine"] != cuisine_pref:
            continue
        candidates.append((missing_ingredient_count(r, user_ingredients), r))
    candidates.sort(key=lambda x: x[0])
    zero_matches = [r for m, r in candidates if m == 0]
    closest = [r for m, r in candidates[:top_n]]
    return zero_matches, closest


DIET_BADGE = {
    "Vegetarian": ("badge-veg", "dot-veg", "Vegetarian"),
    "Non-Vegetarian": ("badge-nonveg", "dot-nonveg", "Non-Vegetarian"),
    "Eggetarian": ("badge-egg", "dot-egg", "Eggetarian"),
}


# Common Hinglish/Hindi ingredient names -> English, since TheMealDB only
# recognizes English ingredient names (e.g. "aloo" must become "potato").
HINGLISH_TO_ENGLISH = {
    "aloo": "potato", "alu": "potato", "pyaz": "onion", "pyaaz": "onion",
    "tamatar": "tomato", "adrak": "ginger", "lehsun": "garlic", "lasun": "garlic",
    "hari mirch": "chilli", "mirch": "chilli", "dhaniya": "coriander",
    "jeera": "cumin", "haldi": "turmeric", "chawal": "rice", "dahi": "yogurt",
    "atta": "flour", "besan": "gram flour", "gobi": "cauliflower",
    "bhindi": "okra", "baingan": "eggplant", "matar": "peas", "palak": "spinach",
    "murgi": "chicken", "murga": "chicken", "anda": "egg", "ande": "egg",
    "machli": "fish", "doodh": "milk", "makhan": "butter", "shimla mirch": "pepper",
    "nimbu": "lemon", "chini": "sugar", "namak": "salt", "tel": "oil",
    "ghee": "ghee", "gud": "jaggery", "kaddu": "pumpkin", "shakarkandi": "sweet potato",
    "mooli": "radish", "gajar": "carrot", "kheera": "cucumber", "lauki": "bottle gourd",
    "rajma": "kidney beans", "chana": "chickpeas", "dal": "lentils", "moong": "lentils",
    "kaju": "cashew", "badam": "almond", "kishmish": "raisin", "til": "sesame",
    "imli": "tamarind", "elaichi": "cardamom", "dalchini": "cinnamon", "laung": "clove",
}


def normalize_for_search(ingredient):
    key = ingredient.strip().lower()
    return HINGLISH_TO_ENGLISH.get(key, key)


# ---------------------------------------------------------------
# Online fallback — when the local knowledge base has no strong
# ingredient match, search a live recipe database (TheMealDB, free
# public API, no key required) so the user still gets a usable recipe.
# Returns (results, debug_reason) — debug_reason explains a failure
# so it's diagnosable instead of silently swallowed.
# ---------------------------------------------------------------
@st.cache_data(show_spinner=False, ttl=3600)
def search_online_recipes(user_ingredients_tuple, diet_pref):
    base = "https://www.themealdb.com/api/json/v1/1"
    user_ingredients = list(user_ingredients_tuple)

    def fetch_details(meals):
        detailed = []
        for m in meals[:3]:
            try:
                d = requests.get(f"{base}/lookup.php?i={m['idMeal']}", timeout=8)
                d.raise_for_status()
                full = (d.json() or {}).get("meals") or []
                if full:
                    detailed.append(full[0])
            except (requests.RequestException, ValueError):
                continue
        return detailed

    tried = []
    try:
        if diet_pref == "Vegetarian":
            resp = requests.get(f"{base}/filter.php?c=Vegetarian", timeout=8)
            resp.raise_for_status()
            meals = (resp.json() or {}).get("meals") or []
            tried.append("category=Vegetarian")
            if meals:
                return fetch_details(meals), None

        for raw_ing in user_ingredients:
            ing = normalize_for_search(raw_ing)
            resp = requests.get(f"{base}/filter.php?i={ing}", timeout=8)
            resp.raise_for_status()
            meals = (resp.json() or {}).get("meals") or []
            tried.append(f"ingredient={ing}")
            if meals:
                return fetch_details(meals), None

        if user_ingredients:
            keyword = normalize_for_search(user_ingredients[0])
            resp = requests.get(f"{base}/search.php?s={keyword}", timeout=8)
            resp.raise_for_status()
            meals = (resp.json() or {}).get("meals") or []
            tried.append(f"name-search={keyword}")
            if meals:
                return meals[:3], None

        return [], f"No results for any of: {', '.join(tried) or 'nothing tried'}"
    except requests.RequestException as e:
        return [], f"Network/request error: {type(e).__name__}: {e}"
    except ValueError as e:
        return [], f"Response parsing error: {e}"


def normalize_online_meal(meal, diet_pref):
    ingredients = []
    for i in range(1, 21):
        ing = (meal.get(f"strIngredient{i}") or "").strip()
        measure = (meal.get(f"strMeasure{i}") or "").strip()
        if ing:
            ingredients.append(f"{measure} {ing}".strip())

    raw_instructions = meal.get("strInstructions") or ""
    steps = [s.strip() for s in raw_instructions.replace("\r\n", "\n").split("\n") if s.strip()]
    if not steps:
        steps = [raw_instructions.strip() or "Instructions unavailable."]

    return {
        "name": meal.get("strMeal", "Untitled Recipe"),
        "cuisine": meal.get("strArea", "International"),
        "diet": diet_pref if diet_pref != "Any" else "Unspecified",
        "servings": 2,
        "prepTime": "Varies",
        "equipment": "Standard kitchen",
        "ingredients": ingredients,
        "steps": steps,
        "substitutions": [],
        "tips": "Sourced live from TheMealDB — an online recipe database, used when the "
                "local knowledge base doesn't have a close match for your ingredients.",
        "source": "online",
    }



def render_recipe_card(recipe, servings_override=None, user_ingredients=None):
    servings = servings_override or recipe["servings"]
    diet_class, dot_class, diet_label = DIET_BADGE.get(
        recipe["diet"], ("badge-cuisine", "dot-veg", recipe["diet"])
    )

    user_ingredients = user_ingredients or []
    normalized_user = [normalize_for_search(u) for u in user_ingredients if u.strip()]

    have_count = 0
    staple_count = 0
    chip_parts = []
    for ing in recipe["ingredients"]:
        ing_lower = ing.lower()
        user_has_it = any(u in ing_lower for u in normalized_user)
        is_staple = any(s in ing_lower for s in PANTRY_STAPLES)

        if user_has_it:
            have_count += 1
            chip_parts.append(f'<span class="ing-chip ing-chip-have">✓ {ing}</span>')
        elif is_staple:
            staple_count += 1
            chip_parts.append(f'<span class="ing-chip ing-chip-staple">🧂 {ing}</span>')
        else:
            chip_parts.append(f'<span class="ing-chip">{ing}</span>')
    ingredients_html = "".join(chip_parts)

    coverage_html = ""
    if normalized_user:
        total = len(recipe["ingredients"])
        to_buy = total - have_count - staple_count
        coverage_html = (
            f'<span class="coverage-tag">✓ {have_count} you already have &nbsp;·&nbsp; '
            f'🧂 {staple_count} common pantry staples &nbsp;·&nbsp; '
            f'🛒 {to_buy} to buy</span>'
        )

    steps_html = "".join(f"<li>{step}</li>" for step in recipe["steps"])

    subs_html = ""
    if recipe.get("substitutions"):
        subs_items = "".join(f"<div>🔄 {s}</div>" for s in recipe["substitutions"])
        subs_html = (
            '<div class="sub-title">Substitutions</div>'
            f'<div class="sub-box">{subs_items}</div>'
        )

    is_online = recipe.get("source") == "online"
    source_badge = (
        '<span class="badge badge-online">🌐 Found Online</span>'
        if is_online
        else '<span class="badge badge-kb">📗 Knowledge Base</span>'
    )

    html = (
        '<div class="ticket">'
        f'<div class="ticket-name">{recipe["name"]}</div>'
        '<div class="badge-row">'
        f'<span class="badge {diet_class}"><span class="dot {dot_class}"></span>{diet_label}</span>'
        f'<span class="badge badge-cuisine">{recipe["cuisine"]}</span>'
        f'{source_badge}'
        '</div>'
        '<div class="meta-row">'
        f'<span class="meta-item">🍽️ Serves {servings}</span>'
        f'<span class="meta-item">⏱️ {recipe["prepTime"]}</span>'
        f'<span class="meta-item">🔧 {recipe["equipment"]}</span>'
        '</div>'
        '<div class="ing-title">Ingredients</div>'
        f'{coverage_html}'
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

zero_shopping = st.checkbox(
    "🙅 Don't want to buy anything — only show recipes I can fully make right now"
)

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
search_clicked = st.button("🔍  Find My Recipe")
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------
# Results
# ---------------------------------------------------------------
if search_clicked:
    if not ingredients_input.strip():
        st.warning("Enter at least one ingredient to get started.")
    elif zero_shopping:
        # ---- Zero-shopping mode: only recipes fully makeable right now ----
        user_ingredients = [i.strip() for i in ingredients_input.split(",") if i.strip()]
        zero_matches, closest = retrieve_zero_shopping(user_ingredients, diet_pref, cuisine_pref)

        if zero_matches:
            st.success(
                f"🎉 {len(zero_matches)} recipe{'s' if len(zero_matches) > 1 else ''} "
                f"you can make right now — zero shopping needed!"
            )
            for idx, r in enumerate(zero_matches[:3]):
                r["source"] = "kb"
                render_recipe_card(r, servings_override, user_ingredients)
                render_read_aloud_button(r, key_suffix=f"zero-{idx}")
        else:
            st.warning(
                "No recipe in the knowledge base can be made with zero shopping from "
                "just these ingredients. Here are the closest options — each shows "
                "exactly how many extra items you'd need."
            )
            for idx, r in enumerate(closest):
                r["source"] = "kb"
                render_recipe_card(r, servings_override, user_ingredients)
                render_read_aloud_button(r, key_suffix=f"closest-{idx}")
    else:
        user_ingredients = [i.strip() for i in ingredients_input.split(",") if i.strip()]
        results, match_ratio = retrieve_best_recipes(
            user_ingredients, diet_pref, cuisine_pref, equipment_hint, top_n=3
        )
        for r in results:
            r["source"] = "kb"

        # Require most (75%+) of the user's ingredients to genuinely appear
        # in the top local match before trusting the knowledge base alone.
        match_found = match_ratio >= 0.75

        if match_found:
            st.markdown(
                f'<div class="section-label" style="margin-bottom:14px;">'
                f'🍳 {len(results)} recipe{"s" if len(results) > 1 else ""} for you</div>',
                unsafe_allow_html=True,
            )
            for idx, r in enumerate(results):
                render_recipe_card(r, servings_override, user_ingredients)
                render_read_aloud_button(r, key_suffix=f"kb-{idx}")
        else:
            st.info(
                "🔎 These ingredients don't closely match anything in the "
                "pan-Asian knowledge base — searching online for more options..."
            )
            with st.spinner("Searching TheMealDB..."):
                online_meals, debug_reason = search_online_recipes(
                    tuple(user_ingredients), diet_pref
                )

            if online_meals:
                normalized = [normalize_online_meal(m, diet_pref) for m in online_meals]
                st.markdown(
                    f'<div class="section-label" style="margin-bottom:14px;">'
                    f'🌐 {len(normalized)} recipe{"s" if len(normalized) > 1 else ""} found online</div>',
                    unsafe_allow_html=True,
                )
                for idx, r in enumerate(normalized):
                    render_recipe_card(r, servings_override, user_ingredients)
                    render_read_aloud_button(r, key_suffix=f"online-{idx}")

                st.caption(
                    "💡 Closest match from our curated knowledge base is shown below too."
                )
                render_recipe_card(results[0], servings_override, user_ingredients)
                render_read_aloud_button(results[0], key_suffix="kb-fallback")
            else:
                st.warning(
                    "Couldn't find an online match either. "
                    "Here's the closest recipe from our knowledge base:"
                )
                if debug_reason:
                    with st.expander("🛠️ Why did online search fail? (debug info)"):
                        st.code(debug_reason)
                render_recipe_card(results[0], servings_override, user_ingredients)
                render_read_aloud_button(results[0], key_suffix="kb-fallback-only")


st.markdown(
    '<div class="footer-note">Built with Streamlit • Powered by IBM watsonx '
    'Orchestrate (RAG) • Curated for students, hostlers & home cooks</div>',
    unsafe_allow_html=True,
)
