import streamlit as st

from pipeline.classify import classify_trip
from pipeline.moderation import moderate_inputs
from pipeline.research import research_trip
from pipeline.plan import plan_itinerary
from pipeline.dining import suggest_dining
from pipeline.budget import allocate_budget
from pipeline.evaluate import evaluate_trip

st.set_page_config(page_title="AI Travel Planner", layout="wide")

st.title("🌍 AI Travel Planner 🌍")
st.markdown("Plan your dream trip with AI-powered recommendations.")


def run_pipeline(destination, dates, budget, interests, status):
    """Chain all 7 pipeline steps. Returns (results_dict, error_list).
    `status` is an st.status container for live progress updates."""
    budget = int(budget)

    # Step 1: Classify
    status.update(label="Classifying your trip...", state="running")
    status.write("🏷️ Analyzing destination and interests to determine trip type...")
    classification = classify_trip(destination, dates, budget, interests)
    status.write(f"✅ Classified as **{classification['trip_type'].title()}** trip")

    # Step 2: Moderate
    status.update(label="Checking inputs...", state="running")
    status.write("🛡️ Validating your trip details...")
    moderated = moderate_inputs(destination, dates, budget, interests)
    if not moderated["is_valid"]:
        status.update(label="Validation failed", state="error")
        return None, moderated["errors"]
    status.write("✅ All inputs look good")

    # Step 3: Research
    status.update(label=f"Researching {destination}...", state="running")
    status.write(f"🔍 Gathering info on neighborhoods, weather, customs, and safety...")
    trip_researched = research_trip(
        destination, dates, interests, budget,
        trip_type=classification["trip_type"],
    )
    status.write(f"✅ Research complete — {trip_researched['num_of_days']}-day trip planned")

    # Step 4: Plan itinerary
    status.update(label="Planning your itinerary...", state="running")
    status.write("📅 Building a day-by-day itinerary with activities and timings...")
    itinerary = plan_itinerary(
        destination,
        trip_type=classification["trip_type"],
        num_days=trip_researched["num_of_days"],
        interests=interests,
        research=trip_researched,
    )
    status.write(f"✅ Itinerary ready — {len(itinerary['days'])} days of activities")

    # Step 5: Dining
    status.update(label="Finding dining spots...", state="running")
    status.write("🍽️ Curating restaurant and dining recommendations...")
    dining = suggest_dining(
        destination,
        trip_type=classification["trip_type"],
        budget=budget,
        itinerary=itinerary,
    )
    status.write("✅ Dining suggestions locked in")

    # Step 6: Budget
    status.update(label="Allocating budget...", state="running")
    status.write("💰 Estimating costs for accommodation, food, activities, and transport...")
    budget_alloc = allocate_budget(
        destination,
        total_budget=budget,
        num_days=trip_researched["num_of_days"],
        itinerary=itinerary,
        dining=dining,
    )
    within = "within" if budget_alloc.get("is_within_budget") else "over"
    status.write(f"✅ Budget breakdown complete — estimated total is {within} budget")

    # Step 7: Evaluate
    status.update(label="Evaluating trip quality...", state="running")
    status.write("✅ Running quality checks on pace, geography, and budget accuracy...")
    user_dream_trip = {
        "destination": destination,
        "dates": dates,
        "budget": budget,
        "interests": interests,
    }
    evaluation = evaluate_trip(
        user_dream_trip,
        classification["reasoning"],
        itinerary,
        dining,
        budget_alloc,
    )
    status.write(f"✅ Evaluation complete — score: {evaluation['overall_score']}/10")

    status.update(label="Trip planned successfully!", state="complete")

    results = {
        "classification": classification,
        "research": trip_researched,
        "itinerary": itinerary,
        "dining": dining,
        "budget": budget_alloc,
        "evaluation": evaluation,
    }
    return results, []


# --- Input Form ---
with st.form("trip_form"):
    col1, col2 = st.columns(2)
    with col1:
        destination = st.text_input("Destination", placeholder="e.g. Tokyo, Japan")
        budget = st.number_input("Budget (USD)", min_value=100, value=2000, step=100)
    with col2:
        dates = st.text_input("Dates", placeholder="e.g. June 1–8, 2025")
        interests = st.text_input("Interests", placeholder="e.g. food, history, art")

    submitted = st.form_submit_button("🚀 Plan My Trip")

# --- Session State ---
if "results" not in st.session_state:
    st.session_state.results = None
if "moderation_errors" not in st.session_state:
    st.session_state.moderation_errors = None
if "api_error" not in st.session_state:
    st.session_state.api_error = None

# --- Run Pipeline on Submit ---
if submitted:
    if not destination.strip() or not dates.strip() or not interests.strip():
        st.warning("Please fill in all fields.")
    else:
        st.session_state.results = None
        st.session_state.moderation_errors = None
        st.session_state.api_error = None
        with st.status("Planning your trip...", expanded=True) as status:
            try:
                results, errors = run_pipeline(destination, dates, budget, interests, status)
                if errors:
                    st.session_state.moderation_errors = errors
                else:
                    st.session_state.results = results
            except Exception as e:
                status.update(label="Something went wrong", state="error")
                st.session_state.api_error = str(e)

# --- Display Errors ---
if st.session_state.moderation_errors:
    for err in st.session_state.moderation_errors:
        st.warning(err)

if st.session_state.api_error:
    st.error(f"Pipeline error: {st.session_state.api_error}")

# --- Display Results ---
if st.session_state.results:
    res = st.session_state.results

    # ── Classification ──
    st.header("🏷️ Trip Classification")
    st.metric("Trip Type", res["classification"]["trip_type"].title())
    st.info(res["classification"]["reasoning"])

    st.divider()

    # ── Research ──
    st.header("🔍 Destination Research")
    research = res["research"]
    r1, r2 = st.columns(2)
    r1.metric("Duration", f"{research['num_of_days']} days")
    r2.metric("Weather", research.get("weather", "N/A"))

    with st.expander("🏘️ Neighborhoods"):
        for n in research.get("neighborhoods", []):
            st.write(f"- {n}")

    with st.expander("🎯 Attractions"):
        for a in research.get("attractions", []):
            st.write(f"- {a}")

    with st.expander("🎎 Customs"):
        for c in research.get("customs", []):
            st.write(f"- {c}")

    with st.expander("🚌 Transportation"):
        for t in research.get("transportation", []):
            st.write(f"- {t}")

    with st.expander("🛡️ Safety"):
        st.write(research.get("safety", "No safety info available."))

    st.divider()

    # ── Itinerary ──
    st.header("📅 Itinerary")
    itinerary_days = res["itinerary"]["days"]
    day_tabs = st.tabs([f"Day {d['day']}" for d in itinerary_days])
    for tab, day in zip(day_tabs, itinerary_days):
        with tab:
            cols = st.columns(3)
            for col, period in zip(cols, ["morning", "afternoon", "evening"]):
                with col:
                    info = day.get(period, {})
                    st.subheader(period.title())
                    st.write(f"**{info.get('activity', 'Free time')}**")
                    st.write(f"🕐 {info.get('time', '')}")
                    st.write(info.get("description", ""))
                    if info.get("reasoning"):
                        st.caption(f"💡 {info['reasoning']}")
            if day.get("travel_time"):
                st.caption(f"🚗 Travel time: {day['travel_time']}")

    st.divider()

    # ── Dining ──
    st.header("🍽️ Dining Suggestions")
    dining_days = res["dining"]["days"]
    dining_tabs = st.tabs([f"Day {d['day']}" for d in dining_days])
    for tab, day in zip(dining_tabs, dining_days):
        with tab:
            cols = st.columns(3)
            for col, meal in zip(cols, ["breakfast", "lunch", "dinner"]):
                with col:
                    info = day.get(meal, {})
                    st.subheader(meal.title())
                    st.write(f"**{info.get('name', 'TBD')}**")
                    st.write(f"📍 {info.get('location', '')}")
                    st.write(info.get("description", ""))
                    st.write(f"💰 {info.get('price_range', '')}")
            if day.get("local_experience"):
                st.success(f"🌟 {day['local_experience']}")

    st.divider()

    # ── Budget ──
    st.header("💰 Budget Breakdown")
    budget_data = res["budget"]
    if budget_data.get("is_within_budget"):
        st.success(
            f"✅ Your trip fits within your ${budget_data['user_budget']} budget! "
            f"Estimated total: ${budget_data['total_estimated']}"
        )
    else:
        st.error(
            f"⚠️ Estimated cost ${budget_data['total_estimated']} exceeds "
            f"your ${budget_data['user_budget']} budget."
        )

    b1, b2, b3, b4, b5 = st.columns(5)
    b1.metric("Accommodation/Night", f"${budget_data.get('accommodation_per_night', 0)}")
    b2.metric("Daily Food", f"${budget_data.get('daily_food_budget', 0)}")
    b3.metric("Activities/Day", f"${budget_data.get('activity_costs_per_day', 0)}")
    b4.metric("Transportation", f"${budget_data.get('transportation', 0)}")
    b5.metric("Miscellaneous", f"${budget_data.get('miscellaneous', 0)}")

    for w in budget_data.get("warnings", []):
        st.warning(w)

    st.divider()

    # ── Evaluation ──
    st.header("✅ Trip Evaluation")
    evaluation = res["evaluation"]
    st.metric("Overall Score", f"{evaluation['overall_score']} / 10")
    st.info(evaluation.get("overall_feedback", ""))

    checks = evaluation.get("checks", {})
    for check_name, check_data in checks.items():
        label = check_name.replace("_", " ").title()
        status = "✅ Passed" if check_data.get("passed") else "❌ Failed"
        with st.expander(f"{status} — {label}"):
            st.write(check_data.get("reasoning", ""))
            if check_data.get("suggestion"):
                st.write(f"💡 **Suggestion:** {check_data['suggestion']}")

    refinements = evaluation.get("refinements", [])
    if refinements:
        st.subheader("Suggested Refinements")
        for r in refinements:
            st.write(f"- {r}")