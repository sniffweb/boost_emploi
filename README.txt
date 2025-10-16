================================================================================
                            BOOST EMPLOIE
                         DEV BY SNIFFWEB
================================================================================

DESCRIPTION:
BOOST EMPLOIE est un outil automatisé élégant qui vous permet de rechercher 
des offres d'emploi sur Pôle Emploi et de postuler automatiquement avec 
votre CV et votre lettre de motivation.

FONCTIONNALITES:
- Recherche d'offres d'emploi avec mots-clés et localisation
- Filtrage par type de contrat (CDI, CDD, Interim, Stage, Alternance, etc.)
- Configuration de CV et lettre de motivation
- Candidature automatique via navigateur automatisé
- Interface élégante et colorée en ligne de commande

LANCEMENT RAPIDE:
1. Double-cliquez sur "DEMARRER.bat" (le plus simple)
2. Ou double-cliquez sur "LANCER_BOOST_EMPLOIE.bat"

INSTALLATION:
1. Double-cliquez sur "INSTALLER.bat" pour installer les dépendances
2. Ou tapez: python verifier_installation.py

TEST:
Double-cliquez sur "TESTER.bat" pour vérifier l'installation

ETAPES D'UTILISATION:

1. PREPARATION:
   - Placez votre CV.pdf dans le dossier "documents_exemple/"
   - Placez votre lettre_motivation.pdf dans le dossier "documents_exemple/"

2. PREMIERE UTILISATION:
   - Lancez l'application avec DEMARRER.bat
   - Choisissez l'option "2" pour configurer vos documents
   - Entrez les chemins vers votre CV et lettre de motivation

3. RECHERCHE D'OFFRES:
   - Choisissez l'option "1" dans le menu
   - Entrez vos mots-clés (ex: "développeur Python")
   - Spécifiez votre localisation (ex: "Paris")
   - Sélectionnez le type de contrat
   - Attendez les résultats

4. CANDIDATURE:
   - Choisissez l'option "3" dans le menu
   - Sélectionnez une offre dans la liste
   - Confirmez votre candidature
   - Le navigateur s'ouvre automatiquement
   - La candidature est envoyée automatiquement

MENU PRINCIPAL:
[1] Rechercher des offres d'emploi
[2] Ajouter mon CV et ma lettre de motivation
[3] Postuler à une offre d'emploi
[4] Quitter

TYPES DE CONTRATS SUPPORTES:
- CDI (Contrat à durée indéterminée)
- CDD (Contrat à durée déterminée)
- INTERIM (Mission d'intérim)
- STAGE (Stage)
- ALTERNANCE (Contrat d'alternance)
- FREELANCE (Freelance)
- TOUS (Tous les types)

PREREQUIS:
- Python 3.7+ installé
- Google Chrome installé
- Connexion Internet
- CV et lettre de motivation au format PDF

STRUCTURE DU PROJET:
boost-emploi/
├── boost_emploi_clean.py        # Script principal
├── DEMARRER.bat                 # Lanceur rapide
├── LANCER_BOOST_EMPLOIE.bat     # Lanceur complet
├── INSTALLER.bat                # Installation automatique
├── TESTER.bat                   # Test de l'installation
├── verifier_installation.py     # Script de vérification
├── pole_emploi_scraper.py       # Module de scraping
├── selenium_handler.py          # Module d'automatisation
├── config.py                    # Configuration
├── requirements.txt             # Dépendances
├── documents_exemple/           # Dossier pour vos documents
├── GUIDE_UTILISATION.txt        # Guide détaillé
└── README.txt                   # Ce fichier

DEPANNAGE:

Problème: Chrome non détecté
Solution: Installez Google Chrome

Problème: Erreur de scraping
Solution: Vérifiez votre connexion Internet

Problème: Candidature échouée
Solution: Vérifiez vos documents et informations

Problème: Erreurs d'installation
Solution: Lancez INSTALLER.bat

AVERTISSEMENTS:
- Utilisez cet outil de manière responsable
- Respectez les conditions d'utilisation de Pôle Emploi
- Vérifiez vos candidatures avant envoi
- Ne surchargez pas les serveurs

CONSEILS:
- Utilisez des mots-clés spécifiques pour de meilleurs résultats
- Vérifiez vos documents avant de les configurer
- Testez d'abord avec une offre qui vous intéresse moins
- Gardez vos informations personnelles à jour

SUPPORT:
En cas de problème:
1. Consultez ce README
2. Lancez TESTER.bat pour diagnostiquer
3. Vérifiez vos documents et informations
4. Vérifiez votre connexion Internet
5. Vérifiez l'installation de Chrome

BONNE CHANCE DANS VOS RECHERCHES D'EMPLOI !

================================================================================
                                DEV BY SNIFFWEB
================================================================================
