# Projet Informatique ICy S8 - Galactik Footbot

## Description
Dans le cadre de notre projet sur la création d'un ChatBot munie d’une IA, nous avons choisi le thème du football et notamment celui des rencontres internationales masculines (Championnat d’Europe et Coupe du Monde principalement). Avec la venue de l’Euro 2024, qui se déroulera en Allemagne, un ChatBot capable d’informer les utilisateurs sur les rencontres passées et de potentiellement donner un avis sur les rencontres futures serait intéressant à développer. C’est pourquoi, nous avons pris la décision de développer un ChatBot (Galactik FootBot) capable de donner diverses informations à propos de ces 2 compétitions. Nous avons donc récupéré les datasets des résultats des matchs de 1930 à 2022 pour la Coupe du Monde et de 1960 à 2020 pour le Championnat d’Europe. 

<br>

## Fonction de création de contexte
Ce projet comprend plusieurs scripts Python qui permettent de récupérer des données à partir de pages web, de nettoyer et de transformer ces données, puis de les sauvegarder dans un format structuré (JSON).

### Scripts inclus dans le dossier *Create_context*:

1. *extraireWiki.py* :
   - Ce script récupère une page Wikipedia spécifiée par l'URL qu'on fournit, extrait les titres de section, les sous-titres et le contenu des paragraphes, puis sauvegarde les données dans un fichier JSON structuré.
   - Utilise les modules `requests`, `BeautifulSoup` et `re` pour le web scraping et le nettoyage des données.

2. *uefa1-fr.py* - *uefa2.py* - *worldcup.py* - *worldcup22.py* :
   - Ces script prennent en entrée un fichier JSON contenant des données en français sur les matches de football de l'Euro de 1960 à 2016 (*uefa1-fr.py*), de l'Euro 2020 (*uefa2.py*), de la coupe du monde de 1930 à 2018 (*worldcup.py*), de la coupe du monde 2022 (*worldcup22.py*) et génère un nouveau fichier JSON où chaque match est représenté par une seule clé `"contexte"` contenant un résumé du match.
   - Les données sont nettoyées en utilisant la fonction `clean_string()`, et des informations supplémentaires comme le vainqueur du match sont ajoutées à chaque résumé.

### Utilisation :
1. *extraireWiki.py* :
   - Modifier la variable `url` pour définir l'URL de la page Wikipedia à analyser.
   - Exécuter le script pour récupérer, analyser et sauvegarder les données.
   - Les données sont sauvegardées dans un fichier JSON nommé de votre choix.

2. *uefa1-fr.py* - *uefa2.py* - *worldcup.py* - *worldcup22.py* :
   - Modifier `input_file_path` pour spécifier le chemin du fichier JSON d'entrée contenant les données des matches.
   - Spécifier `output_file_path` pour le chemin où le fichier JSON mis à jour, contenant uniquement les résumés de contexte, doit être sauvegardé.
   - Exécuter le script pour ajouter le contexte à chaque match et sauvegarder les données dans le fichier spécifié.

### Dépendances
- `requests`, `BeautifulSoup`, `re` pour *extraireWiki.py*
- `json`, `re` pour *uefa1-fr.py*, *uefa2.py*, *worldcup.py*, *worldcup22.py*

### Notes :
- Assurez-vous d'avoir les bibliothèques Python nécessaires installées avant d'exécuter les scripts.
- Plusieurs scripts Python d'extraction sont nécessaires car les données récupérées varient. Par exemple, le dataset couvrant les Coupes du Monde de 1930 à 2018 n'incluait pas celui de 2022. Il a donc fallu trouver un dataset spécifique pour la Coupe du Monde 2022, qui ne contient pas forcément les mêmes détails d'informations que le précédent.
- Chaque script d'extraction est différent en raison de la formulation du contexte et des clés correspondantes, qui dépendent du fichier JSON récupéré et à traiter.


## Modèle IA



## Interface Graphique
Les technologies utilisées pour l'interface graphique sont les suivantes : React, Vite.js et TailwindCss.

### Utilisation
1. Lancez l'application :
   ```bash
   npm run dev
   ```
2. Ouvrez votre navigateur et accédez à `http://localhost:3000`
