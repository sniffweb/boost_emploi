"""
Module de scraping pour les offres d'emploi de Pôle Emploi
"""

import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urljoin, urlparse, parse_qs
from config import (
    POLE_EMPLOI_SEARCH_URL, 
    DEFAULT_HEADERS, 
    REQUEST_DELAY,
    COLORS
)


class PoleEmploiScraper:
    """Classe pour scraper les offres d'emploi sur Pôle Emploi"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        self.base_url = "https://candidat.pole-emploi.fr"
        
    def search_jobs(self, keywords="", location="", contract_type="TOUS", max_results=50):
        """
        Recherche des offres d'emploi sur Pôle Emploi
        
        Args:
            keywords (str): Mots-clés de recherche
            location (str): Localisation (ville, département, région)
            contract_type (str): Type de contrat
            max_results (int): Nombre maximum de résultats à retourner
            
        Returns:
            list: Liste des offres d'emploi trouvées
        """
        print(f"{COLORS['INFO']}🔍 Recherche d'offres d'emploi en cours...{COLORS['END']}")
        print(f"   Mots-clés: {keywords}")
        print(f"   Localisation: {location}")
        print(f"   Type de contrat: {contract_type}")
        
        jobs = []
        page = 1
        max_pages = 10  # Limiter le nombre de pages à scraper
        
        try:
            while len(jobs) < max_results and page <= max_pages:
                print(f"{COLORS['INFO']}   📄 Scraping page {page}...{COLORS['END']}")
                
                # Construire les paramètres de recherche
                params = self._build_search_params(keywords, location, contract_type, page)
                
                # Effectuer la requête
                response = self._make_request(POLE_EMPLOI_SEARCH_URL, params)
                
                if not response:
                    break
                    
                # Parser les résultats
                page_jobs = self._parse_job_listings(response.text)
                
                if not page_jobs:
                    print(f"{COLORS['WARNING']}   ⚠️ Aucune offre trouvée sur la page {page}{COLORS['END']}")
                    break
                    
                jobs.extend(page_jobs)
                print(f"{COLORS['SUCCESS']}   ✅ {len(page_jobs)} offres trouvées sur la page {page}{COLORS['END']}")
                
                page += 1
                time.sleep(REQUEST_DELAY)
                
            # Limiter les résultats au maximum demandé
            jobs = jobs[:max_results]
            
            print(f"{COLORS['SUCCESS']}🎉 Recherche terminée: {len(jobs)} offres trouvées{COLORS['END']}")
            
        except Exception as e:
            print(f"{COLORS['ERROR']}❌ Erreur lors de la recherche: {str(e)}{COLORS['END']}")
            
        return jobs
    
    def _build_search_params(self, keywords, location, contract_type, page):
        """Construit les paramètres de recherche pour l'URL"""
        params = {
            'motsCles': keywords,
            'lieux': location,
            'page': str(page),
            'offresPartenaires': 'true',
            'rayon': '10',
            'tri': '0',
            'minCreationDate': '',
            'maxCreationDate': '',
            'typeContrat': contract_type if contract_type != 'TOUS' else '',
            'natureContrat': '',
            'salaireMin': '',
            'salaireMax': '',
            'experience': '',
            'qualification': '',
            'secteurActivite': '',
            'typeConvention': '',
            'nomEntreprise': '',
            'lieuTravail': '',
            'filtresRecherche': '',
            'origineOffre': 'PE',
            'origineOffre': 'PARTENAIRES'
        }
        
        # Nettoyer les paramètres vides
        return {k: v for k, v in params.items() if v}
    
    def _make_request(self, url, params=None):
        """Effectue une requête HTTP avec gestion d'erreurs"""
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"{COLORS['ERROR']}❌ Erreur de requête: {str(e)}{COLORS['END']}")
            return None
    
    def _parse_job_listings(self, html_content):
        """Parse le contenu HTML pour extraire les offres d'emploi"""
        soup = BeautifulSoup(html_content, 'html.parser')
        jobs = []
        
        # Sélecteurs pour les offres d'emploi sur Pôle Emploi
        job_selectors = [
            'article[data-testid="offre-emploi"]',
            '.titreMedia',
            '.result',
            '.job-result',
            '[data-testid="job-offer"]'
        ]
        
        job_elements = []
        for selector in job_selectors:
            job_elements = soup.select(selector)
            if job_elements:
                break
        
        if not job_elements:
            # Essayer de trouver les offres avec d'autres sélecteurs
            job_elements = soup.find_all(['article', 'div'], class_=re.compile(r'(offre|job|result|emploi)'))
        
        for element in job_elements:
            job_data = self._extract_job_data(element)
            if job_data:
                jobs.append(job_data)
        
        return jobs
    
    def _extract_job_data(self, element):
        """Extrait les données d'une offre d'emploi"""
        try:
            # Titre de l'offre
            title_selectors = [
                'h3 a', 'h2 a', '.titreMedia a', 'a[data-testid="offre-lien"]',
                'a.titreOffre', '.title a', 'h3', 'h2'
            ]
            
            title_element = None
            title = "Titre non trouvé"
            job_url = ""
            
            for selector in title_selectors:
                title_element = element.select_one(selector)
                if title_element:
                    title = title_element.get_text(strip=True)
                    # Essayer d'extraire l'URL
                    if title_element.name == 'a':
                        href = title_element.get('href', '')
                        if href:
                            job_url = urljoin(self.base_url, href)
                    else:
                        # Chercher un lien à proximité
                        link = element.find('a', href=True)
                        if link:
                            job_url = urljoin(self.base_url, link['href'])
                    break
            
            # Entreprise
            company_selectors = [
                '.entreprise', '.company', '.employeur', '.societe',
                '[data-testid="entreprise"]', '.nomEntreprise'
            ]
            
            company = "Entreprise non spécifiée"
            for selector in company_selectors:
                company_element = element.select_one(selector)
                if company_element:
                    company = company_element.get_text(strip=True)
                    break
            
            # Localisation
            location_selectors = [
                '.lieu', '.location', '.ville', '.adresse',
                '[data-testid="lieu"]', '.localisation'
            ]
            
            location = "Localisation non spécifiée"
            for selector in location_selectors:
                location_element = element.select_one(selector)
                if location_element:
                    location = location_element.get_text(strip=True)
                    break
            
            # Type de contrat
            contract_selectors = [
                '.typeContrat', '.contract', '.contrat', '.type',
                '[data-testid="type-contrat"]', '.natureContrat'
            ]
            
            contract_type = "Type non spécifié"
            for selector in contract_selectors:
                contract_element = element.select_one(selector)
                if contract_element:
                    contract_type = contract_element.get_text(strip=True)
                    break
            
            # Date de publication
            date_selectors = [
                '.date', '.publication', '.creation', '.datePublication',
                '[data-testid="date"]', '.dateOffre'
            ]
            
            date = "Date non spécifiée"
            for selector in date_selectors:
                date_element = element.select_one(selector)
                if date_element:
                    date = date_element.get_text(strip=True)
                    break
            
            # Description (tronquée)
            description_selectors = [
                '.description', '.resume', '.extrait', '.summary',
                '[data-testid="description"]', '.texteOffre'
            ]
            
            description = ""
            for selector in description_selectors:
                desc_element = element.select_one(selector)
                if desc_element:
                    description = desc_element.get_text(strip=True)[:200] + "..."
                    break
            
            return {
                'title': title,
                'company': company,
                'location': location,
                'contract_type': contract_type,
                'date': date,
                'description': description,
                'url': job_url,
                'source': 'Pôle Emploi'
            }
            
        except Exception as e:
            print(f"{COLORS['WARNING']}⚠️ Erreur lors de l'extraction des données: {str(e)}{COLORS['END']}")
            return None
    
    def get_job_details(self, job_url):
        """
        Récupère les détails complets d'une offre d'emploi
        
        Args:
            job_url (str): URL de l'offre d'emploi
            
        Returns:
            dict: Détails complets de l'offre
        """
        try:
            response = self._make_request(job_url)
            if not response:
                return None
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extraire les détails complets
            details = {
                'full_description': '',
                'requirements': '',
                'benefits': '',
                'salary': '',
                'contact_info': ''
            }
            
            # Description complète
            desc_selectors = [
                '.descriptionOffre', '.description', '.contenuOffre',
                '[data-testid="description-complete"]', '.texteComplet'
            ]
            
            for selector in desc_selectors:
                desc_element = soup.select_one(selector)
                if desc_element:
                    details['full_description'] = desc_element.get_text(strip=True)
                    break
            
            # Salaire
            salary_selectors = [
                '.salaire', '.remuneration', '.salary', '.salaireOffre'
            ]
            
            for selector in salary_selectors:
                salary_element = soup.select_one(selector)
                if salary_element:
                    details['salary'] = salary_element.get_text(strip=True)
                    break
            
            return details
            
        except Exception as e:
            print(f"{COLORS['ERROR']}❌ Erreur lors de la récupération des détails: {str(e)}{COLORS['END']}")
            return None
    
    def filter_jobs(self, jobs, filters):
        """
        Filtre les offres d'emploi selon les critères spécifiés
        
        Args:
            jobs (list): Liste des offres d'emploi
            filters (dict): Critères de filtrage
            
        Returns:
            list: Offres filtrées
        """
        filtered_jobs = jobs.copy()
        
        # Filtrage par mots-clés
        if filters.get('keywords'):
            keywords = filters['keywords'].lower()
            filtered_jobs = [
                job for job in filtered_jobs
                if keywords in job['title'].lower() or 
                   keywords in job['description'].lower() or
                   keywords in job['company'].lower()
            ]
        
        # Filtrage par type de contrat
        if filters.get('contract_type') and filters['contract_type'] != 'TOUS':
            contract = filters['contract_type'].lower()
            filtered_jobs = [
                job for job in filtered_jobs
                if contract in job['contract_type'].lower()
            ]
        
        # Filtrage par localisation
        if filters.get('location'):
            location = filters['location'].lower()
            filtered_jobs = [
                job for job in filtered_jobs
                if location in job['location'].lower()
            ]
        
        return filtered_jobs
