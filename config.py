"""
Configuration pour l'outil de scraping Pôle Emploi
"""

# Configuration des URLs
POLE_EMPLOI_BASE_URL = "https://candidat.pole-emploi.fr"
POLE_EMPLOI_SEARCH_URL = "https://candidat.pole-emploi.fr/offres/recherche"

# Configuration des délais (en secondes)
REQUEST_DELAY = 2
SELENIUM_WAIT_TIME = 10
PAGE_LOAD_TIMEOUT = 30

# Configuration des headers pour les requêtes
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'fr-FR,fr;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Types de contrats disponibles
CONTRACT_TYPES = {
    'CDI': 'CDI',
    'CDD': 'CDD', 
    'INTERIM': 'Interim',
    'STAGE': 'Stage',
    'ALTERNANCE': 'Contrat d\'alternance',
    'FREELANCE': 'Freelance',
    'TOUS': 'Tous'
}

# Configuration des couleurs pour l'interface
COLORS = {
    'SUCCESS': '\033[92m',  # Vert
    'ERROR': '\033[91m',    # Rouge
    'WARNING': '\033[93m',  # Jaune
    'INFO': '\033[94m',     # Bleu
    'HEADER': '\033[95m',   # Magenta
    'BOLD': '\033[1m',      # Gras
    'UNDERLINE': '\033[4m', # Souligné
    'END': '\033[0m'        # Reset
}
