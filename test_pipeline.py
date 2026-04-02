from pipeline.classify import classify_trip
from pipeline.moderation import moderate_inputs
from pipeline.research import research_trip

result = classify_trip(
    destination="Tokyo",
    dates="June 1-7th 2026",
    budget=2000,
    interests="food, temple, anime"
)



moderated = moderate_inputs(
    destination="Tokyo",
    dates="June 1-7th 2026",
    budget=2000,
    interests="food, temple, anime"
)

research = research_trip(
    destination="Tokyo",
    dates="June 1-7th 2026",
    budget=2000,
    interests="food, temple, anime"
)


print("RESEARCH")
print(research)
