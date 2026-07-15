# 🍜 Recipe Preparation Agent

**AICTE 2026 — IBM SkillsBuild University Engagement**
**Problem Statement No. 16 — Recipe Preparation Agent**

🔗 **Live Demo:** [recipe-preparation-agent.streamlit.app](https://recipe-preparation-agent-5ehuam9lmnoodywtappfhkc.streamlit.app)

A hybrid **RAG-based AI cooking assistant** that helps students, hostlers, and
everyday home cooks turn whatever groceries they have on hand into a
practical, ready-to-cook meal — with a guaranteed answer even when a recipe
can't be found locally or online.

Built on **IBM watsonx Orchestrate** (IBM Cloud Lite services), with a
curated pan-Asian recipe knowledge base and a companion Streamlit web app.

---

## 🎯 Problem Statement

> A Recipe Preparation Agent helps users cook meals using only the
> ingredients they have on hand. By inputting available groceries, users
> receive tailored recipe suggestions using a RAG-based AI system. The agent
> retrieves relevant recipes and generates step-by-step instructions adapted
> to ingredient limitations. It offers substitutions, cooking tips, and
> dietary adjustments based on user preferences or restrictions. Designed to
> reduce food waste and save time, it turns pantry items into practical meal
> solutions.

---

## 🏗️ Architecture

```
                         User Query
        ("I have paneer, capsicum, onion — veg recipe?")
                             │
              ┌──────────────┴──────────────┐
              ▼                              ▼
 ┌────────────────────────┐      ┌───────────────────────────┐
 │ IBM watsonx Orchestrate │      │   Streamlit Frontend       │
 │  - RAG Knowledge Base   │      │  - Mirrors retrieval logic │
 │  - Behavior/Prompt cfg  │      │  - Audio + visual polish   │
 │  - ReAct agent style    │      └──────────────┬──────────────┘
 └────────────┬─────────────┘                    │
              ▼                                   ▼
     Structured Recipe                   3-Tier Fallback Chain
   Response (KB-grounded)      1) Local knowledge base (30 recipes)
                                2) Online search (TheMealDB API)
                                3) Auto-generated recipe (guaranteed
                                   zero-shopping result)
```

This repository contains:
1. `Pan_Asian_Recipe_Knowledge_Base.docx` — the knowledge source uploaded to
   watsonx Orchestrate
2. `app.py` — the **Streamlit companion app**, including the hybrid
   retrieval logic, online fallback, and auto-generated recipe engine
3. `recipes.json` — structured recipe data (30 recipes, 5 cuisines)
4. `requirements.txt` — Python dependencies

---

## 📊 Knowledge Base

| Cuisine | Recipes | Veg | Non-Veg/Egg |
|---|---|---|---|
| Thai | 8 | 6 | 2 |
| Chinese / Indo-Chinese | 8 | 5 | 3 |
| Japanese | 5 | 4 | 1 |
| Korean | 5 | 3 | 2 |
| Vietnamese | 4 | 3 | 1 |
| **Total** | **30** | **21** | **9** |

Each recipe includes: diet type, servings, prep time, equipment needed,
ingredients with quantities, step-by-step instructions, substitutions for
hard-to-find items, and practical cooking tips.

---

## 🌟 Key Features

### 🔗 Hybrid 3-Tier Retrieval
The agent never returns a dead end:
1. **Local knowledge base** — matches ingredients against the curated
   30-recipe dataset, requiring 75%+ genuine ingredient overlap before
   trusting a match.
2. **Online search fallback** — if the local knowledge base has no strong
   match, the app queries **TheMealDB** (a free public recipe API),
   including a **Hinglish → English ingredient translator** (e.g. *aloo* →
   *potato*, *pyaz* → *onion*) so Hindi/English mixed input still works.
3. **Auto-generated recipe** — if neither source has a match, the app
   builds a simple stir-fry/dish from exactly the ingredients provided, so
   the user always gets a usable result.

### 🙅 Zero-Shopping Mode
An optional filter that scans the entire knowledge base (and, if needed,
the web) for a recipe requiring **zero additional purchases** — ideal for
"I really don't want to buy anything" moments.

### 🧂 Transparent Ingredient Tagging
Every ingredient on a recipe card is tagged:
- ✅ **Have** — something the user already listed
- 🧂 **Pantry Staple** — oil, salt, sugar, water, etc. — assumed available,
  never falsely marked "missing"
- 🛒 **To Buy** — genuinely needs purchasing

### 🔊 Hands-Free Audio
A **"Read Steps Aloud"** button uses the browser's built-in Web Speech API
to read out the full recipe — no paid text-to-speech service required.

### 🎨 Custom "Night Market" UI
A warm, food-stall-inspired visual theme with an original SVG wok
illustration (no external/copyrighted images), diet-color-coded badges, and
ingredient chips styled as order tickets.

### 🥗 Diet-Aware by Design
Every recipe is explicitly tagged **Vegetarian / Non-Vegetarian /
Eggetarian** and filterable end-to-end, including in the online-search and
auto-generated fallback tiers.

---

## 🚀 Running the Demo Locally

### Prerequisites
- Python 3.9+

### Steps
```bash
# 1. Clone the repository
git clone https://github.com/himani-aiml/recipe-preparation-agent.git
cd recipe-preparation-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## ☁️ IBM Cloud Deployment (Core Agent)

The production agent is built and deployed on **IBM watsonx Orchestrate**:

1. IBM Cloud → watsonx Orchestrate (Lite/Trial plan, Dallas region)
2. Agent created from scratch with **ReAct** agent style
3. Knowledge base uploaded (`Pan_Asian_Recipe_Knowledge_Base.docx`)
4. Behavior prompt configured for diet-aware, ingredient-matched retrieval
   with substitution guidance
5. Deployed to the **Live** environment

Screenshots of the working agent (build, testing, and deployment) are
included in the project PPT submission.

---

## 🔮 Future Scope

- **Multi-modal input** — photo-based ingredient recognition using Visual LLMs
- **Grocery ordering API integration** (Blinkit/Instacart) for missing items
- **Persistent user memory** (allergies, dietary restrictions) via vector database
- **Multi-agent architecture** (Inventory Inspector, Chef Agent, Nutritionist Agent)
- **Expiry-date tracking** to further reduce food waste
- **Nutrition & macro tracking** synced to fitness goals

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Core Agent | IBM watsonx Orchestrate (IBM Cloud Lite) |
| Model | GPT-OSS 120B |
| Retrieval | Retrieval-Augmented Generation (RAG) |
| Frontend | Python + Streamlit |
| Online Fallback | TheMealDB API (free, public) |
| Audio | Web Speech API (browser-native) |
| Hosting | Streamlit Community Cloud + GitHub |

---

## 👤 Author

Built as part of the AICTE-2026 IBM SkillsBuild University Engagement
program (Edunet Foundation), Problem Statement No. 16.
