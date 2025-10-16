#!/usr/bin/env python3
"""
BOOST EMPLOIE - Outil automatisé de recherche et candidature d'emploi
Interface élégante et moderne en ligne de commande (Version ultra-compatible)
DEV BY SNIFFWEB
"""

import os
import sys
import time
from colorama import init, Fore, Back, Style

# Initialiser colorama pour Windows
init(autoreset=True)

# Ajouter le répertoire courant au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from config import COLORS
    from pole_emploi_scraper import PoleEmploiScraper
    from selenium_handler import SeleniumHandler
except ImportError as e:
    print(f"Erreur d'import: {e}")
    print("Veuillez installer les dependances avec: pip install -r requirements.txt")
    sys.exit(1)


class BoostEmploi:
    """Classe principale pour l'outil BOOST EMPLOIE"""
    
    def __init__(self):
        self.jobs = []
        self.personal_info = {}
        self.cv_path = None
        self.cover_letter_path = None
        
        # Configuration des couleurs élégantes
        self.colors = {
            'title': Fore.CYAN + Style.BRIGHT,
            'subtitle': Fore.MAGENTA + Style.BRIGHT,
            'menu_option': Fore.GREEN + Style.BRIGHT,
            'menu_number': Fore.YELLOW + Style.BRIGHT,
            'quit_option': Fore.RED + Style.BRIGHT,
            'success': Fore.GREEN + Style.BRIGHT,
            'error': Fore.RED + Style.BRIGHT,
            'warning': Fore.YELLOW + Style.BRIGHT,
            'info': Fore.BLUE + Style.BRIGHT,
            'input': Fore.CYAN,
            'reset': Style.RESET_ALL,
            'bold': Style.BRIGHT
        }
    
    def clear_screen(self):
        """Efface l'écran"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_title(self):
        """Affiche le titre principal élégant"""
        self.clear_screen()
        
        # Titre principal simple
        title = """
================================================================================
                            BOOST EMPLOIE
================================================================================
                                DEV BY SNIFFWEB
================================================================================
"""
        
        print(self.colors['title'] + title + self.colors['reset'])
        
        # Sous-titre
        print(f"{self.colors['subtitle']}{'=' * 80}{self.colors['reset']}")
        print(f"{self.colors['subtitle']}{'VOTRE PARTENAIRE INTELLIGENT POUR TROUVER L\'EMPLOI DE VOS REVES':^80}{self.colors['reset']}")
        print(f"{self.colors['subtitle']}{'=' * 80}{self.colors['reset']}")
        print()
    
    def print_menu(self):
        """Affiche le menu principal élégant"""
        print(f"{self.colors['bold']}{'MENU PRINCIPAL':^80}{self.colors['reset']}")
        print(f"{self.colors['info']}{'=' * 80}{self.colors['reset']}")
        print()
        
        # Options du menu avec design élégant
        options = [
            ("1", "Rechercher des offres d'emploi", "Trouvez les meilleures opportunites"),
            ("2", "Ajouter mon CV et ma lettre de motivation", "Configurez vos documents"),
            ("3", "Postuler a une offre d'emploi", "Candidature automatique"),
            ("4", "Quitter", "Fermer l'application")
        ]
        
        for num, title, desc in options:
            if num == "4":
                color = self.colors['quit_option']
            else:
                color = self.colors['menu_option']
            
            print(f"  {self.colors['menu_number']}[{num}]{self.colors['reset']} {color}{title:<50}{self.colors['reset']}")
            print(f"      {self.colors['info']}{desc}{self.colors['reset']}")
            print()
        
        print(f"{self.colors['info']}{'=' * 80}{self.colors['reset']}")
    
    def get_user_choice(self):
        """Récupère le choix de l'utilisateur"""
        while True:
            try:
                choice = input(f"{self.colors['input']}Votre choix (1-4): {self.colors['reset']}").strip()
                
                if choice in ['1', '2', '3', '4']:
                    return int(choice)
                else:
                    print(f"{self.colors['error']}Choix invalide ! Veuillez entrer un nombre entre 1 et 4.{self.colors['reset']}")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print(f"\n{self.colors['warning']}Operation annulee par l'utilisateur.{self.colors['reset']}")
                return 4
            except:
                print(f"{self.colors['error']}Erreur de saisie ! Veuillez reessayer.{self.colors['reset']}")
                time.sleep(1)
    
    def search_jobs(self):
        """Fonction de recherche d'offres d'emploi"""
        self.clear_screen()
        print(f"{self.colors['title']}{'RECHERCHE D\'OFFRES D\'EMPLOI':^80}{self.colors['reset']}")
        print(f"{self.colors['info']}{'=' * 80}{self.colors['reset']}")
        print()
        
        try:
            # Collecte des informations de recherche
            print(f"{self.colors['info']}Veuillez renseigner vos criteres de recherche :{self.colors['reset']}")
            print()
            
            keywords = input(f"{self.colors['input']}Mots-cles (ex: developpeur Python, comptable): {self.colors['reset']}").strip()
            location = input(f"{self.colors['input']}Localisation (ex: Paris, Lyon, 75): {self.colors['reset']}").strip()
            
            print(f"\n{self.colors['info']}Types de contrats disponibles :{self.colors['reset']}")
            contract_types = ['CDI', 'CDD', 'INTERIM', 'STAGE', 'ALTERNANCE', 'FREELANCE', 'TOUS']
            for i, contract in enumerate(contract_types, 1):
                print(f"  {self.colors['menu_number']}[{i}]{self.colors['reset']} {self.colors['menu_option']}{contract}{self.colors['reset']}")
            
            contract_choice = input(f"\n{self.colors['input']}Type de contrat (1-7, ou nom): {self.colors['reset']}").strip()
            
            if contract_choice.isdigit() and 1 <= int(contract_choice) <= 7:
                contract_type = contract_types[int(contract_choice) - 1]
            else:
                contract_type = contract_choice.upper() if contract_choice.upper() in contract_types else 'TOUS'
            
            max_results = input(f"{self.colors['input']}Nombre max de resultats (defaut: 20): {self.colors['reset']}").strip()
            max_results = int(max_results) if max_results.isdigit() else 20
            
            # Lancement de la recherche
            print(f"\n{self.colors['info']}Lancement de la recherche...{self.colors['reset']}")
            print(f"{self.colors['info']}Veuillez patienter, cela peut prendre quelques instants...{self.colors['reset']}")
            print()
            
            try:
                scraper = PoleEmploiScraper()
                self.jobs = scraper.search_jobs(
                    keywords=keywords,
                    location=location,
                    contract_type=contract_type,
                    max_results=max_results
                )
            except Exception as scrape_error:
                print(f"{self.colors['error']}Erreur lors du scraping: {str(scrape_error)}{self.colors['reset']}")
                print(f"{self.colors['info']}Verifiez votre connexion Internet et reessayez.{self.colors['reset']}")
                self.jobs = []
            
            if self.jobs:
                print(f"\n{self.colors['success']}RECHERCHE TERMINEE AVEC SUCCES !{self.colors['reset']}")
                print(f"{self.colors['success']}{len(self.jobs)} offres trouvees{self.colors['reset']}")
                self.show_jobs_summary()
            else:
                print(f"\n{self.colors['warning']}Aucune offre trouvee avec ces criteres{self.colors['reset']}")
            
            input(f"\n{self.colors['info']}Appuyez sur Entree pour continuer...{self.colors['reset']}")
            
        except Exception as e:
            print(f"\n{self.colors['error']}Erreur lors de la recherche : {str(e)}{self.colors['reset']}")
            input(f"\n{self.colors['info']}Appuyez sur Entree pour continuer...{self.colors['reset']}")
    
    def add_documents(self):
        """Fonction pour ajouter CV et lettre de motivation"""
        self.clear_screen()
        print(f"{self.colors['title']}{'CONFIGURATION DES DOCUMENTS':^80}{self.colors['reset']}")
        print(f"{self.colors['info']}{'=' * 80}{self.colors['reset']}")
        print()
        
        try:
            print(f"{self.colors['info']}Placez vos documents dans le dossier 'documents_exemple/' puis renseignez les chemins :{self.colors['reset']}")
            print()
            
            # CV
            print(f"{self.colors['info']}Configuration du CV :{self.colors['reset']}")
            cv_path = input(f"{self.colors['input']}Chemin vers votre CV (PDF recommande): {self.colors['reset']}").strip()
            
            if os.path.exists(cv_path):
                self.cv_path = cv_path
                print(f"{self.colors['success']}CV configure avec succes : {os.path.basename(cv_path)}{self.colors['reset']}")
            else:
                print(f"{self.colors['error']}Fichier CV non trouve : {cv_path}{self.colors['reset']}")
            
            print()
            
            # Lettre de motivation
            print(f"{self.colors['info']}Configuration de la lettre de motivation :{self.colors['reset']}")
            cover_letter_path = input(f"{self.colors['input']}Chemin vers votre lettre de motivation (PDF recommande): {self.colors['reset']}").strip()
            
            if os.path.exists(cover_letter_path):
                self.cover_letter_path = cover_letter_path
                print(f"{self.colors['success']}Lettre de motivation configuree avec succes : {os.path.basename(cover_letter_path)}{self.colors['reset']}")
            else:
                print(f"{self.colors['error']}Fichier lettre de motivation non trouve : {cover_letter_path}{self.colors['reset']}")
            
            if self.cv_path and self.cover_letter_path:
                print(f"\n{self.colors['success']}CONFIGURATION TERMINEE !{self.colors['reset']}")
                print(f"{self.colors['success']}Vos documents sont prets pour les candidatures{self.colors['reset']}")
            else:
                print(f"\n{self.colors['warning']}Configuration incomplete{self.colors['reset']}")
            
            input(f"\n{self.colors['info']}Appuyez sur Entree pour continuer...{self.colors['reset']}")
            
        except Exception as e:
            print(f"\n{self.colors['error']}Erreur lors de la configuration : {str(e)}{self.colors['reset']}")
            input(f"\n{self.colors['info']}Appuyez sur Entree pour continuer...{self.colors['reset']}")
    
    def apply_to_job(self):
        """Fonction pour postuler à une offre"""
        self.clear_screen()
        print(f"{self.colors['title']}{'CANDIDATURE AUTOMATIQUE':^80}{self.colors['reset']}")
        print(f"{self.colors['info']}{'=' * 80}{self.colors['reset']}")
        print()
        
        # Vérifications préalables
        if not self.jobs:
            print(f"{self.colors['error']}Aucune offre disponible{self.colors['reset']}")
            print(f"{self.colors['info']}Veuillez d'abord effectuer une recherche d'offres{self.colors['reset']}")
            input(f"\n{self.colors['info']}Appuyez sur Entree pour continuer...{self.colors['reset']}")
            return
        
        if not self.cv_path or not self.cover_letter_path:
            print(f"{self.colors['error']}Documents non configures{self.colors['reset']}")
            print(f"{self.colors['info']}Veuillez d'abord configurer votre CV et lettre de motivation{self.colors['reset']}")
            input(f"\n{self.colors['info']}Appuyez sur Entree pour continuer...{self.colors['reset']}")
            return
        
        try:
            # Affichage des offres disponibles
            print(f"{self.colors['info']}Offres disponibles pour candidature :{self.colors['reset']}")
            print()
            
            for i, job in enumerate(self.jobs, 1):
                print(f"  {self.colors['menu_number']}[{i}]{self.colors['reset']} {self.colors['menu_option']}{job['title'][:50]}...{self.colors['reset']}")
                print(f"      {self.colors['info']}Entreprise: {job['company']} | Localisation: {job['location']} | Contrat: {job['contract_type']}{self.colors['reset']}")
                print()
            
            # Sélection de l'offre
            job_index = input(f"{self.colors['input']}Numero de l'offre (1-{len(self.jobs)}): {self.colors['reset']}").strip()
            
            if not job_index.isdigit() or not (1 <= int(job_index) <= len(self.jobs)):
                print(f"{self.colors['error']}Numero invalide !{self.colors['reset']}")
                input(f"\n{self.colors['info']}Appuyez sur Entree pour continuer...{self.colors['reset']}")
                return
            
            selected_job = self.jobs[int(job_index) - 1]
            
            # Confirmation
            print(f"\n{self.colors['info']}Offre selectionnee :{self.colors['reset']}")
            print(f"  {self.colors['bold']}Titre :{self.colors['reset']} {selected_job['title']}")
            print(f"  {self.colors['bold']}Entreprise :{self.colors['reset']} {selected_job['company']}")
            print(f"  {self.colors['bold']}Localisation :{self.colors['reset']} {selected_job['location']}")
            print(f"  {self.colors['bold']}URL :{self.colors['reset']} {selected_job['url']}")
            
            confirm = input(f"\n{self.colors['warning']}Etes-vous sur de vouloir postuler ? (oui/non): {self.colors['reset']}").strip().lower()
            
            if confirm in ['oui', 'o', 'yes', 'y']:
                print(f"\n{self.colors['info']}Lancement de la candidature automatique...{self.colors['reset']}")
                print(f"{self.colors['info']}Veuillez patienter, le navigateur va s'ouvrir...{self.colors['reset']}")
                
                # Candidature automatique
                try:
                    with SeleniumHandler(headless=False) as handler:
                        handler.set_documents(self.cv_path, self.cover_letter_path)
                        success = handler.apply_to_job(selected_job['url'], self.personal_info)
                        
                        if success:
                            print(f"\n{self.colors['success']}CANDIDATURE ENVOYEE AVEC SUCCES !{self.colors['reset']}")
                            print(f"{self.colors['success']}Votre candidature a ete transmise a l'entreprise{self.colors['reset']}")
                        else:
                            print(f"\n{self.colors['error']}Echec de l'envoi de la candidature{self.colors['reset']}")
                            print(f"{self.colors['info']}Verifiez vos documents et informations{self.colors['reset']}")
                except Exception as selenium_error:
                    print(f"\n{self.colors['error']}Erreur Selenium: {str(selenium_error)}{self.colors['reset']}")
                    print(f"{self.colors['info']}Verifiez que Chrome est installe et reessayez.{self.colors['reset']}")
            else:
                print(f"\n{self.colors['info']}Candidature annulee{self.colors['reset']}")
            
            input(f"\n{self.colors['info']}Appuyez sur Entree pour continuer...{self.colors['reset']}")
            
        except Exception as e:
            print(f"\n{self.colors['error']}Erreur lors de la candidature : {str(e)}{self.colors['reset']}")
            input(f"\n{self.colors['info']}Appuyez sur Entree pour continuer...{self.colors['reset']}")
    
    def show_jobs_summary(self):
        """Affiche un résumé des offres trouvées"""
        if not self.jobs:
            return
        
        print(f"\n{self.colors['info']}RESUME DES RESULTATS :{self.colors['reset']}")
        print(f"{self.colors['info']}{'=' * 50}{self.colors['reset']}")
        
        # Statistiques par entreprise
        companies = {}
        for job in self.jobs:
            company = job['company']
            companies[company] = companies.get(company, 0) + 1
        
        print(f"  {self.colors['bold']}Total d'offres :{self.colors['reset']} {len(self.jobs)}")
        print(f"  {self.colors['bold']}Entreprises :{self.colors['reset']} {len(companies)}")
        
        # Top 3 des entreprises
        top_companies = sorted(companies.items(), key=lambda x: x[1], reverse=True)[:3]
        if top_companies:
            print(f"\n  {self.colors['bold']}Top entreprises :{self.colors['reset']}")
            for company, count in top_companies:
                print(f"    • {self.colors['menu_option']}{company}{self.colors['reset']} : {count} offre(s)")
    
    def run(self):
        """Fonction principale qui lance l'application"""
        while True:
            try:
                self.print_title()
                self.print_menu()
                
                choice = self.get_user_choice()
                
                if choice == 1:
                    self.search_jobs()
                elif choice == 2:
                    self.add_documents()
                elif choice == 3:
                    self.apply_to_job()
                elif choice == 4:
                    self.clear_screen()
                    print(f"{self.colors['title']}{'MERCI D\'AVOIR UTILISE BOOST EMPLOIE !':^80}{self.colors['reset']}")
                    print(f"{self.colors['info']}{'=' * 80}{self.colors['reset']}")
                    print()
                    print(f"{self.colors['success']}Bonne chance dans vos recherches d'emploi !{self.colors['reset']}")
                    print(f"{self.colors['success']}Que vos candidatures soient couronnees de succes !{self.colors['reset']}")
                    print()
                    print(f"{self.colors['subtitle']}Developpe avec amour par SNIFFWEB{self.colors['reset']}")
                    print()
                    time.sleep(3)
                    break
                    
            except KeyboardInterrupt:
                print(f"\n{self.colors['warning']}Application fermee par l'utilisateur.{self.colors['reset']}")
                break
            except Exception as e:
                print(f"\n{self.colors['error']}Erreur inattendue : {str(e)}{self.colors['reset']}")
                input(f"\n{self.colors['info']}Appuyez sur Entree pour continuer...{self.colors['reset']}")


def main():
    """Point d'entrée principal"""
    try:
        print("Initialisation de BOOST EMPLOIE...")
        app = BoostEmploi()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication fermee par l'utilisateur.")
        sys.exit(0)
    except Exception as e:
        print(f"Erreur critique : {str(e)}")
        print("Veuillez verifier votre installation et reessayer.")
        input("Appuyez sur Entree pour fermer...")
        sys.exit(1)


if __name__ == "__main__":
    main()
