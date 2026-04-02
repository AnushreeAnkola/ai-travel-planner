# 🌍 AI Travel Planner 🌍

An AI-powered travel planning app built with Streamlit and the Anthropic API. Enter a destination, dates, budget, and interests, The app runs a 7-step LLM pipeline to generate a complete trip plan with itinerary, dining, budget breakdown, and quality evaluation.

It follows concepts from the Deeplearning AI's course Building Systems with OpeAI API. 

🚀 **[Try the live app](https://ai-travel-planner-1.streamlit.app/)**


## How It Works

The app chains seven sequential LLM calls, each handling a specific aspect of trip planning:

```
Classify → Moderate → Research → Plan Itinerary → Suggest Dining → Allocate Budget → Evaluate
```

| Step | Module | What it does |
|------|--------|-------------|
| 1 | `pipeline/classify.py` | Determines the trip type (cultural, adventure, relaxation, etc.) based on destination and interests |
| 2 | `pipeline/moderation.py` | Validates inputs for safety and feasibility and stops the pipeline early if issues are found |
| 3 | `pipeline/research.py` | Gathers destination intel: neighborhoods, weather, customs, attractions, safety, transportation |
| 4 | `pipeline/plan.py` | Builds a day-by-day itinerary with morning, afternoon, and evening activities |
| 5 | `pipeline/dining.py` | Recommends breakfast, lunch, and dinner spots for each day with local experiences |
| 6 | `pipeline/budget.py` | Breaks down costs across accommodation, food, activities, transport, and miscellaneous |
| 7 | `pipeline/evaluate.py` | Scores the trip on geographic logic, pace, budget accuracy, rest periods, and trip-type match |

Each step passes its output forward to the next, so later steps build on earlier context. The UI shows real-time progress as each step completes.

## Project Structure

```
ai-travel-planner/
├── app.py                  # Streamlit UI
├── pipeline/
│   ├── __init__.py
│   ├── classify.py         # Trip type classification
│   ├── moderation.py       # Input validation and safety checks
│   ├── research.py         # Destination research
│   ├── plan.py             # Itinerary planning
│   ├── dining.py           # Restaurant and dining suggestions
│   ├── budget.py           # Budget allocation and cost estimation
│   └── evaluate.py         # Trip quality evaluation and scoring
├── test_pipeline.py        # End-to-end pipeline test
├── requirements.txt
└── README.md
```

## Setup

### Prerequisites

- Python 3.9+
- An [Anthropic API key](https://console.anthropic.com/)

### Installation

```bash
git clone https://github.com/your-username/ai-travel-planner.git
cd ai-travel-planner
pip install -r requirements.txt
```

### Environment

Set your Anthropic API key:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

Or create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=sk-ant-...
```

### Run

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Usage

1. **Fill in the form** — enter a destination, travel dates, budget (USD), and your interests.
2. **Click "Plan My Trip"** — the pipeline runs with live progress updates showing each step.
3. **Browse results** — six sections display classification, research, itinerary (tabbed by day), dining, budget breakdown, and an evaluation score.

### Example Input

| Field | Value |
|-------|-------|
| Destination | Tokyo, Japan |
| Dates | Dec 1–9, 2026 |
| Budget | $2,000 |
| Interests | food, anime, history |

## UI Sections

**Classification** —> Shows the detected trip type with reasoning.

**Research** —> Duration and weather at a glance, with expandable sections for neighborhoods, attractions, customs, transportation, and safety.

**Itinerary** —> One tab per day, three columns (morning / afternoon / evening) showing each activity's name, time, description, and reasoning.

**Dining** —> One tab per day, three columns (breakfast / lunch / dinner) with restaurant name, location, description, and price range. Local food experiences highlighted per day.

**Budget** —> Success/error banner based on whether the plan fits your budget, five metric cards for cost categories, and any warnings.

**Evaluation** —> Overall score out of 10, qualitative feedback, pass/fail checks on geographic logic, pacing, budget accuracy, rest periods, and trip-type alignment, plus suggested refinements.

## Pipeline Data Flow

```
User Input (destination, dates, budget, interests)
    │
    ├─→ classify_trip() ─→ trip_type, reasoning
    │
    ├─→ moderate_inputs() ─→ is_valid, errors
    │       └─ (stops here if invalid)
    │
    ├─→ research_trip(trip_type) ─→ neighborhoods, weather, customs, attractions, safety, num_of_days
    │
    ├─→ plan_itinerary(trip_type, num_days, research) ─→ days[{morning, afternoon, evening}]
    │
    ├─→ suggest_dining(trip_type, itinerary) ─→ days[{breakfast, lunch, dinner}]
    │
    ├─→ allocate_budget(num_days, itinerary, dining) ─→ cost breakdown, is_within_budget
    │
    └─→ evaluate_trip(all above) ─→ score, checks, feedback, refinements
```

## Testing

Run the end-to-end pipeline test:

```bash
python test_pipeline.py
```

This executes the full 7-step chain with sample inputs and prints each step's output.

## Troubleshooting

**"Unterminated string" or JSON parse errors** — The LLM occasionally returns malformed JSON. This is a transient issue. Re-run the pipeline by clicking "Plan My Trip" again. If it persists, check the pipeline modules for proper JSON parsing and consider adding retry logic.

**API key errors** — Make sure `ANTHROPIC_API_KEY` is set in your environment or `.env` file.

**Rate limits** — The pipeline makes 7 sequential API calls. If you hit rate limits, add a small delay between steps or check your Anthropic plan's limits.

