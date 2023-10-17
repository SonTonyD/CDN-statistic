import os
import re

# Liste des URL à traiter
liste_urls = [
    "https://bu.univ-lyon3.fr",
    "https://www.bl.uk",
    "ug.edu.gh"
]

# Chemin vers le fichier de format de timing
timing_format_file = "timing-format.txt"

# Nombre de fois que chaque URL doit être testée
nombre_tests = 2

# Dictionnaire pour stocker les temps pour chaque URL
temps_par_url = {url: {"time_namelookup": [], "time_appconnect": [], "time_starttransfer": [], "speed_download": []} for url in liste_urls}

# Boucle à travers chaque URL
for url in liste_urls:
    for _ in range(nombre_tests):
        # Construction de la commande curl
        commande_curl = f"curl -w @{timing_format_file} -o /dev/null -s {url}"

        # Exécution de la commande curl en utilisant os.popen()
        try:
            result = os.popen(commande_curl).read()
            for line in result.split("\n"):
                match = re.search(r"(time_\w+): (\d+\.\d+)", line)
                if match:
                    key, value = match.groups()
                    temps_par_url[url][key].append(float(value))
        except Exception as e:
            print(f"Erreur lors de l'exécution de curl pour l'URL {url}. Erreur: {e}")

# Calcul des moyennes pour chaque URL
for url, timings in temps_par_url.items():
    print(f"URL: {url}")
    for key, values in timings.items():
        moyenne = sum(values) / len(timings.items())
        print(f"{key}: {moyenne:.6f}")
    print()
