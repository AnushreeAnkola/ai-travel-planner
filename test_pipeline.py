from pipeline.classify import classify_trip
from pipeline.moderation import moderate_inputs
from pipeline.research import research_trip
from pipeline.plan import plan_itinerary
from pipeline.dining import suggest_dining
from pipeline.budget import allocate_budget
from pipeline.evaluate import evaluate_trip

user_dream_trip = {
    'destination': "Tokyo",
    'dates': "June 1-7th 2026",
    'budget':2000,
    'interests':"food, temple, anime"
}



classification = classify_trip(
    destination=user_dream_trip['destination'],
    dates=user_dream_trip['dates'],
    budget=user_dream_trip['budget'],
    interests=user_dream_trip['interests']
)

moderated = moderate_inputs(
    destination=user_dream_trip['destination'],
    dates=user_dream_trip['dates'],
    budget=user_dream_trip['budget'],
    interests=user_dream_trip['interests']
)

if not moderated["is_valid"]:
    print("Invalid inputs:", moderated["errors"])
    exit()

trip_researched = research_trip(
    destination=user_dream_trip['destination'],
    dates=user_dream_trip['dates'],
    budget=user_dream_trip['budget'],
    interests=user_dream_trip['interests'],
    trip_type = classification['trip_type']
)


itinery_plan = plan_itinerary(
    destination=user_dream_trip['destination'],
    trip_type=classification['trip_type'],
    num_days=trip_researched['num_of_days'],
    interests=user_dream_trip['interests'],
    research=trip_researched
)

dining_suggestions = suggest_dining(
    destination=user_dream_trip['destination'],
    trip_type=classification['trip_type'],
    budget=user_dream_trip['budget'],
    itinerary=itinery_plan
)

budget_allocation = allocate_budget(
    destination=user_dream_trip['destination'],
    total_budget=user_dream_trip['budget'],
    num_days=trip_researched['num_of_days'],
    itinerary=itinery_plan,
    dining=dining_suggestions
)

evaluate = evaluate_trip(user_dream_trip, classification['reasoning'], 
                              itinery_plan, dining_suggestions, budget_allocation)
print("FINAL")
print(evaluate)
