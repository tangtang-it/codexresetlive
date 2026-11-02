from classifier import classify_tweet

CASES = [
    ("completed", "Reset all propagated. Enjoy.", "confirmed_reset", True),
    ("future", "Global reset landing by EOD PST time. Enjoy", "pending_reset", False),
    ("banked", "Loading a banked reset in everyone’s paid accounts.", "banked_reset", False),
    ("personal", "My personal quota reset after five hours.", "chatter", False),
    ("ordinary", "I demand a reset", "chatter", False),
    ("slogan", "Day 20/ Rest and reset", "chatter", False),
]

for name, text, category, is_reset in CASES:
    actual = classify_tweet(name, text)
    assert actual["category"] == category, (name, actual)
    assert actual["is_reset"] is is_reset, (name, actual)

print("publication contract fixtures passed: " + str(len(CASES)))