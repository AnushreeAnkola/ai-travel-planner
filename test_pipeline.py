from pipeline.classify import classify_trip
from pipeline.moderation import moderate_inputs
from pipeline.research import research_trip
from pipeline.plan import plan_itinerary
from pipeline.dining import suggest_dining
from pipeline.budget import allocate_budget


destination = "Tokyo"
dates = "June 1-7th 2026"
budget=2000
interests="food, temple, anime"


classification = classify_trip(
    destination=destination,
    dates=dates,
    budget=budget,
    interests=interests
)

moderated = moderate_inputs(
    destination=destination,
    dates=dates,
    budget=budget,
    interests=interests
)

if not moderated["is_valid"]:
    print("Invalid inputs:", moderated["errors"])
    exit()

trip_researched = research_trip(
    destination=destination,
    dates=dates,
    budget=budget,
    interests=interests,
    trip_type = classification['trip_type']
)


itinery_plan = plan_itinerary(
    destination=destination,
    trip_type=classification['trip_type'],
    num_days=trip_researched['num_of_days'],
    interests=interests,
    research=trip_researched
)

dining_suggestions = suggest_dining(
    destination=destination,
    trip_type=classification['trip_type'],
    budget=budget,
    itinerary=itinery_plan
)

budget_allocation = allocate_budget(
    destination=destination,
    total_budget=budget,
    num_days=trip_researched['num_of_days'],
    itinerary=itinery_plan,
    dining=dining_suggestions
)

print("FINAL")
print(budget_allocation)
