import json
import re

# Fonction pour nettoyer les chaînes de caractères
def clean_string(s):
    # Remplacer les séquences spécifiques problématiques
    cleaned = s.replace('\u00c3\u00a9', 'é').replace('\u00c2\u00a0', ' ').replace('\u00c3\u00a0', 'à').replace('\u00e9', 'é')
    # Supprimer les espaces supplémentaires
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

# Fonction pour déterminer le vainqueur du match
def determine_winner(home_goals, away_goals, home_team, away_team):
    if home_goals > away_goals:
        return home_team
    elif away_goals > home_goals:
        return away_team
    else:
        return "Match nul"

# Fonction pour résumer un match
def summarize_match(match):
    # Déterminer le vainqueur
    winner = determine_winner(match['HomeTeamGoals'], match['AwayTeamGoals'], clean_string(match['HomeTeamName']), clean_string(match['AwayTeamName']))
    # Définir le résultat en fonction du vainqueur
    if winner == "Match nul":
        result = "Le match s'est terminé par un match nul."
    else:
        result = f"Le vainqueur était {winner}."

    # Générer le résumé du match
    summary = (
        f"Le {clean_string(match['Date'])} à {clean_string(match['Time'])}, 
        {clean_string(match['HomeTeamName'])} "
        f"a joué contre {clean_string(match['AwayTeamName'])} 
        lors de {clean_string(match['Stage'])}. Le match a eu lieu au "
        f"{clean_string(match['Stadium'])} à {clean_string(match['City'])}, 
        avec une affluence de "
        f"{match['Attendance']} spectateurs. Le score final était de 
        {match['HomeTeamGoals']} - {match['AwayTeamGoals']}. {result}"
    )

    return summary

# Fonction pour ajouter le contexte à chaque match
def add_context_to_matches(matches):
    context_only_matches = []
    for match in matches:
        context_only_matches.append({"contexte": summarize_match(match)})
    return context_only_matches

# Chemin vers le fichier JSON d'entrée
input_file_path = 'uefaEuro.json'

# Chemin vers le fichier JSON de sortie
output_file_path = 'UEFAcontext-fr1.json'

# Charger les données JSON depuis le fichier
with open(input_file_path, 'r') as file:
    matches = json.load(file)

# Ajouter le contexte à chaque match et ne conserver que le contexte
context_only_matches = add_context_to_matches(matches)

# Sauvegarder les matches mis à jour dans un nouveau fichier
with open(output_file_path, 'w') as file:
    json.dump(context_only_matches, file, indent=4)

print(f"Les matches mis à jour contenant uniquement le contexte ont été enregistrés dans {output_file_path}")
