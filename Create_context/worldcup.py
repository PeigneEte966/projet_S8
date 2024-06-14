import json
from unidecode import unidecode
import re

def clean_string(s):
    # Replace specific problematic sequences
    cleaned = s.replace('\u00c3\u00a9', 'e').replace('\u00c2\u00a0', ' ').replace('\u00c3\u00a0', 'à').replace('\u00c3\u00a1', 'a').replace('\u00c3\u00ad', 'i').replace('\u00b0', 'e').replace('\u00c3\u2021', 'C')
    # Remove extra spaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def summarize_match(match):
    summary = (
        f"Lors de la Coupe du Monde {match['year']} en {clean_string(match['country'])}, la finale s'est déroulée à {clean_string(match['city'])} le {clean_string(match['dayofweek'])} "
        f"{clean_string(match['date'])}. L'équipe {clean_string(match['home_team'])} a affronté l'équipe {clean_string(match['away_team'])}. "
        f"Le score final était de {match['home_score']} - {match['away_score']}, avec la victoire de {clean_string(match['winning_team'])}. "
        f"Le match, tenu au stade de {clean_string(match['city'])}, a marqué la victoire de {clean_string(match['winning_team'])} sur {clean_string(match['losing_team'])}, scellant le tournoi avec un résultat de {match['home_score']} - {match['away_score']}. "
        f"Cette finale mémorable s'est déroulée au mois de {clean_string(match['month'])} {match['year']}."
    )
    return summary

def add_context_to_matches(matches):
    context_only_matches = []
    for match in matches:
        context_only_matches.append({"contexte": summarize_match(match)})
    return context_only_matches

# Path to the input JSON file
input_file_path = 'worldcup.json'

# Path to the output JSON file
output_file_path = 'worldcup_context.json'

# Load JSON data from the file
with open(input_file_path, 'r') as file:
    matches = json.load(file)

# Add context to each match and keep only the context
context_only_matches = add_context_to_matches(matches)

# Save the updated matches back to a new file
with open(output_file_path, 'w') as file:
    json.dump(context_only_matches, file, indent=4)

print(f"Updated matches with only context have been saved to {output_file_path}")
