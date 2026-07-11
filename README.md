# 🍜 Recipe Preparation Agent

**AICTE 2026 — IBM SkillsBuild University Engagement**
**Problem Statement No. 16 — Recipe Preparation Agent**

A RAG-based AI system that helps users (students, hostlers, and everyday home
cooks) cook meals using only the ingredients they have on hand. Built on
**IBM watsonx Orchestrate** (IBM Cloud Lite services), with a curated
pan-Asian recipe knowledge base.

---

## 🎯 Problem Statement

> A Recipe Preparation Agent helps users cook meals using only the
> ingredients they have on hand. By inputting available groceries, users
> receive tailored recipe suggestions using a RAG-based AI system. The agent
> retrieves relevant recipes and generates step-by-step instructions adapted
> to ingredient limitations. It offers substitutions, cooking tips, and
> dietary adjustments based on user preferences or restrictions.

---

## 🏗️ Architecture

```
User Query (ingredients, diet preference, cuisine)
        │
        ▼
┌───────────────────────────┐
│  IBM watsonx Orchestrate   │   ← Core AI Agent (production)
│  - RAG Knowledge Base      │
│  - Behavior/Prompt config  │
│  - ReAct agent style       │
└───────────────────────────┘
        │
        ▼
Structured Recipe Response
(Name | Cuisine | Diet Type | Ingredients | Steps | Substitutions | Tips)
```

This repository contains:
1. `Pan_Asian_Recipe_Knowledge_Base.docx` — the knowledge source uploaded to
   watsonx Orchestrate
2. `app.py` — a **Streamlit demo frontend** that mirrors the same retrieval
   logic locally, for an interactive shareable web demo
3. `recipes.json` — structured recipe data (30 recipes, 5 cuisines)

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

## 🚀 Running the Demo Locally

### Prerequisites
- Python 3.9+

### Steps
```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/recipe-preparation-agent.git
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

1. IBM Cloud → watsonx Orchestrate (Lite plan, Dallas region)
2. Agent created from scratch with ReAct agent style
3. Knowledge base uploaded (`Pan_Asian_Recipe_Knowledge_Base.docx`)
4. Behavior prompt configured for diet-aware, ingredient-matched retrieval
5. Deployed to Live environment

Screenshots of the working agent are included in the project PPT submission.

---

## 🌟 Features

- **Diet-aware retrieval** — filters recipes by Vegetarian / Non-Vegetarian / Eggetarian
- **Ingredient matching** — suggests recipes based on what's actually on hand
- **Substitution guidance** — offers alternatives for hard-to-find ingredients
- **Hostel-friendly mode** — prioritizes minimal-equipment recipes
- **Serving size adjustment** — scales recipes to the number of servings needed

---

## 🔮 Future Scope

- Multi-modal input: photo-based ingredient recognition using Visual LLMs
- Grocery ordering API integration (Blinkit/Instacart) for missing ingredients
- Persistent user memory (allergies, dietary restrictions) via vector database
- Multi-agent architecture (Inventory Inspector, Chef Agent, Nutritionist Agent)
- Expiry-date tracking for food waste reduction

---

## 🛠️ Tech Stack

- **IBM watsonx Orchestrate** (IBM Cloud Lite) — core RAG agent
- **Python / Streamlit** — demo frontend
- **GPT-OSS 120B** — underlying model (via watsonx Orchestrate)

---

## 👤 Author

Built as part of the AICTE-2026 IBM SkillsBuild University Engagement program
(Edunet Foundation), Problem Statement No. 16.
