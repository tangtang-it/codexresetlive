from classifier import classify_tweet

CASES = [
    ("completed", "Reset all propagated. Enjoy.", "confirmed_reset", True),
    ("future", "Global reset landing by EOD PST time. Enjoy", "pending_reset", False),
    ("banked", "Loading a banked reset in everyone’s paid accounts.", "banked_reset", False),
    ("personal", "My personal quota reset after five hours.", "chatter", False),
    ("ordinary", "I demand a reset", "chatter", False),
    ("slogan", "Day 20/ Rest and reset", "chatter", False),
    ("banked-chatter", "I demand a banked reset", "chatter", False),
]

for name, text, category, is_reset in CASES:
    actual = classify_tweet(name, text)
    assert actual["category"] == category, (name, actual)
    assert actual["is_reset"] is is_reset, (name, actual)

# A banked credit is not an automatic public reset, but it is a completed
# source-linked reset benefit and must remain available to user-facing views.
banked = classify_tweet("banked-benefit", "Day 28/ Banked 2/2")
assert banked["category"] == "banked_reset", banked
assert banked["is_reset"] is False, banked

print("publication contract fixtures passed: " + str(len(CASES)))