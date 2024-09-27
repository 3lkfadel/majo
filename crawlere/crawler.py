import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

# Fonction pour récupérer les liens et titres d'une page
def scrape_page(url):
    try:
        # Envoyer une requête à la page
        response = requests.get(url)
        response.raise_for_status()  # Vérifier s'il y a des erreurs HTTP
        
        # Parser le contenu HTML avec BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Trouver tous les liens et titres
        data = []
        for link in soup.find_all('a'):
            title = link.get_text(strip=True)
            href = link.get('href')
            
            # Si le lien est valide
            if href:
                # Transformer les liens relatifs en liens absolus
                full_url = urljoin(url, href)
                if full_url.startswith('http'):
                    data.append({"title": title, "link": full_url})
        
        return data
    except requests.RequestException as e:
        print(f"Erreur lors du scraping de {url}: {e}")
        return []

# Fonction principale du crawler
def crawl(start_url, depth=2, output_file='scraped_data.json'):
    visited = set()  # Pour éviter de visiter les mêmes pages plusieurs fois
    results = []

    # Fonction récursive pour explorer les liens
    def explore(url, current_depth):
        if current_depth > depth or url in visited:
            return
        
        print(f"Scraping {url}...")
        visited.add(url)

        # Scraper la page actuelle
        page_data = scrape_page(url)
        results.extend(page_data)

        # Sauvegarder les résultats actuels à chaque étape
        save_results(results, output_file)

        # Explorer chaque lien trouvé
        for item in page_data:
            explore(item['link'], current_depth + 1)

    # Démarrer le crawling à partir de l'URL donnée
    explore(start_url, 0)

    print("Scraping terminé ! Les données sont sauvegardées dans le fichier.")

# Fonction pour sauvegarder les résultats dans un fichier JSON
def save_results(data, output_file):
    try:
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde dans {output_file}: {e}")

# Exécuter le crawler
if __name__ == "__main__":
    start_url = input("Entrez l'URL de départ : ")
    crawl(start_url)
