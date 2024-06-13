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
    if {clean_string(match['category'])} in ["finale", "quart de finale", "demi-finale", "Huitièmes de finale"]:
        summary = (
            f"Lors de la {clean_string(match['category'])} qui s'est déroulée le {clean_string(match['date'])} à {clean_string(match['hour'])}, "
            f"l'équipe {clean_string(match['team1'])} a affronté l'équipe {clean_string(match['team2'])}. Dans cette rencontre, "
            f"l'équipe {clean_string(match['team1'])} a eu une possession de {clean_string(match['possession team1'])}, tandis que l'équipe {clean_string(match['team2'])} "
            f"a possédé le ballon pendant {clean_string(match['possession team2'])} du temps. Le match s'est soldé sur un score de {match['number of goals team1']} - {match['number of goals team2']}, "
            f"avec {clean_string(match['team1'])} et {clean_string(match['team2'])} marquant chacun {match['number of goals team1']} but(s). Les tentatives totales d'attaque "
            f"de {clean_string(match['team1'])} étaient de {match['total attempts team1']}, tandis que {clean_string(match['team2'])} en a réalisé {match['total attempts team2']}. "
            f"Les deux équipes ont concédé {match['conceded team1']} but(s) chacune. {clean_string(match['team1'])} a réussi {match['goal inside the penalty area team1']} buts à l'intérieur de la surface de réparation, "
            f"et {clean_string(match['team2'])} en a marqué {match['goal inside the penalty area team2']}. {clean_string(match['team1'])} a également réalisé {match['goal outside the penalty area team1']} but(s) en dehors de la surface de réparation, "
            f"tandis que {clean_string(match['team2'])} n'a pas marqué à l'extérieur de la surface. De plus, {clean_string(match['team1'])} a effectué {match['passes team1']} passes, dont {match['passes completed team1']} ont été complétées. "
            f"Quant à {clean_string(match['team2'])}, elles ont réalisé {match['passes team2']} passes, avec {match['passes completed team2']} complétées avec succès. "
            f"Au total, {clean_string(match['team1'])} a appliqué {match['defensive pressures applied team1']} pressions défensives, tandis que {clean_string(match['team2'])} en a appliqué {match['defensive pressures applied team2']}."
        )
    else:
        summary = (
            f"Dans le {clean_string(match['category'])}, le {clean_string(match['date'])} à {clean_string(match['hour'])}, "
            f"l'équipe {clean_string(match['team1'])} a affronté l'équipe {clean_string(match['team2'])}. Dans cette rencontre, "
            f"l'équipe {clean_string(match['team1'])} a eu une possession de {clean_string(match['possession team1'])}, tandis que l'équipe {clean_string(match['team2'])} "
            f"a possédé le ballon pendant {clean_string(match['possession team2'])} du temps. Le match s'est soldé sur un score de {match['number of goals team1']} - {match['number of goals team2']}, "
            f"avec {clean_string(match['team1'])} et {clean_string(match['team2'])} marquant chacun {match['number of goals team1']} but(s). Les tentatives totales d'attaque "
            f"de {clean_string(match['team1'])} étaient de {match['total attempts team1']}, tandis que {clean_string(match['team2'])} en a réalisé {match['total attempts team2']}. "
            f"Les deux équipes ont concédé {match['conceded team1']} but(s) chacune. {clean_string(match['team1'])} a réussi {match['goal inside the penalty area team1']} buts à l'intérieur de la surface de réparation, "
            f"et {clean_string(match['team2'])} en a marqué {match['goal inside the penalty area team2']}. {clean_string(match['team1'])} a également réalisé {match['goal outside the penalty area team1']} but(s) en dehors de la surface de réparation, "
            f"tandis que {clean_string(match['team2'])} n'a pas marqué à l'extérieur de la surface. De plus, {clean_string(match['team1'])} a effectué {match['passes team1']} passes, dont {match['passes completed team1']} ont été complétées. "
            f"Quant à {clean_string(match['team2'])}, elles ont réalisé {match['passes team2']} passes, avec {match['passes completed team2']} complétées avec succès. "
            f"Au total, {clean_string(match['team1'])} a appliqué {match['defensive pressures applied team1']} pressions défensives, tandis que {clean_string(match['team2'])} en a appliqué {match['defensive pressures applied team2']}."
        )
    return summary

def add_context_to_matches(matches):
    context_only_matches = []
    for match in matches:
        context_only_matches.append({"contexte": summarize_match(match)})
    return context_only_matches

# Path to the input JSON file
input_file_path = 'wc22.json'

# Path to the output JSON file
output_file_path = 'wc20222_context.json'

# Load JSON data from the file
with open(input_file_path, 'r') as file:
    matches = json.load(file)

# Add context to each match and keep only the context
context_only_matches = add_context_to_matches(matches)

# Save the updated matches back to a new file
with open(output_file_path, 'w') as file:
    json.dump(context_only_matches, file, indent=4)

print(f"Updated matches with only context have been saved to {output_file_path}")
