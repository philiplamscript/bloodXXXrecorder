# Standard Library
import json
import uuid

# Logic ported from your Function.py
def parse_votes(votes_str):
    """Converts a string of player numbers into a dictionary of voters."""
    record_dict = {}
    # Wrap with delimiters for easy lookahead/lookbehind
    s = f"&{votes_str}&"
    for i in range(1, len(s) - 1):
        target = s[i]
        if target != "&":
            # Handle the +10 case logic from your original script
            if (target == s[i+1]) and (target == s[i-1]):
                record_dict[f"1{target}"] = True
                record_dict[f"{target}"] = True
            elif target != s[i+1]:
                if target == s[i-1]:
                    record_dict[f"1{target}"] = True
                else:
                    record_dict[f"{target}"] = True
    return record_dict

def process_vote_record(day, way, voters, note):
    """Processes a single nomination record into a displayable format."""
    # Split 'way' into from/to (e.g. '1 5')
    parts = way.split()
    from_p = parts[0] if len(parts) > 0 else "?"
    to_p = parts[-1] if len(parts) > 1 else "?"
    
    vote_map = parse_votes(voters)
    
    return {
        "id": str(uuid.uuid4()),
        "Day": day,
        "from": from_p,
        "to": to_p,
        "vote_count": len(vote_map),
        "voters": list(vote_map.keys()),
        "Note": note
    }

# This backend is designed to be called by the React Frontend
# In a real environment, you would use FastAPI or Flask here.
print("Backend logic initialized. Ready to process game states.")