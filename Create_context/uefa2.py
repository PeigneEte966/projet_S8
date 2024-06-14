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
    f"Dans le {clean_string(match['RoundName'])}, {clean_string(match['HomeTeamName'])} a affronté "
    f"{clean_string(match['AwayTeamName'])} le {clean_string(match['DateandTimeCET'])}. Le match était arbitré par {clean_string(match['RefereeWebName'])} avec comme arbitre assistant "
    f"{clean_string(match['AssistantRefereeWebName'])}. Le score final était de {match['ScoreHome']} - {match['ScoreAway']}. "
    f"Le match a duré {match['MatchMinute']} minutes avec {match['InjuryTime']} minutes supplémentaires de temps additionnel. "
    f"L'humidité était de {match['Humidity']} %, la température était de {match['Temperature']} °C, et la vitesse du vent était de {match['WindSpeed']} km/h."
)

    return summary

def add_context_to_matches(matches):
    context_only_matches = []
    for match in matches:
        context_only_matches.append({"contexte": summarize_match(match)})
    return context_only_matches

# Path to the input JSON file
input_file_path = 'uefaEuro2020.json'

# Path to the output JSON file
output_file_path = 'UEFAcontext2020-fr.json'

# Load JSON data from the file
with open(input_file_path, 'r') as file:
    matches = json.load(file)

# Add context to each match and keep only the context
context_only_matches = add_context_to_matches(matches)

# Save the updated matches back to a new file
with open(output_file_path, 'w') as file:
    json.dump(context_only_matches, file, indent=4)

print(f"Updated matches with only context have been saved to {output_file_path}")
