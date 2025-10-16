"""
Module d'automatisation avec Selenium pour les candidatures automatiques
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from config import SELENIUM_WAIT_TIME, PAGE_LOAD_TIMEOUT, COLORS


class SeleniumHandler:
    """Classe pour gérer l'automatisation des candidatures avec Selenium"""
    
    def __init__(self, headless=False):
        """
        Initialise le gestionnaire Selenium
        
        Args:
            headless (bool): Mode headless pour le navigateur
        """
        self.driver = None
        self.wait = None
        self.headless = headless
        self.cv_path = None
        self.cover_letter_path = None
        
    def setup_driver(self):
        """Configure et initialise le driver Chrome"""
        try:
            print(f"{COLORS['INFO']}🚀 Configuration du navigateur Chrome...{COLORS['END']}")
            
            # Options Chrome
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument("--headless")
            
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            
            # Désactiver les notifications et popups
            prefs = {
                "profile.default_content_setting_values.notifications": 2,
                "profile.default_content_settings.popups": 0,
                "profile.managed_default_content_settings.images": 2
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            # Installer automatiquement le driver Chrome
            service = Service(ChromeDriverManager().install())
            
            # Créer le driver
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
            
            # Configurer l'attente implicite
            self.wait = WebDriverWait(self.driver, SELENIUM_WAIT_TIME)
            
            print(f"{COLORS['SUCCESS']}✅ Navigateur Chrome configuré avec succès{COLORS['END']}")
            return True
            
        except Exception as e:
            print(f"{COLORS['ERROR']}❌ Erreur lors de la configuration du navigateur: {str(e)}{COLORS['END']}")
            return False
    
    def set_documents(self, cv_path, cover_letter_path):
        """
        Définit les chemins vers le CV et la lettre de motivation
        
        Args:
            cv_path (str): Chemin vers le fichier CV
            cover_letter_path (str): Chemin vers le fichier de lettre de motivation
        """
        if os.path.exists(cv_path):
            self.cv_path = cv_path
            print(f"{COLORS['SUCCESS']}✅ CV trouvé: {cv_path}{COLORS['END']}")
        else:
            print(f"{COLORS['ERROR']}❌ CV non trouvé: {cv_path}{COLORS['END']}")
            
        if os.path.exists(cover_letter_path):
            self.cover_letter_path = cover_letter_path
            print(f"{COLORS['SUCCESS']}✅ Lettre de motivation trouvée: {cover_letter_path}{COLORS['END']}")
        else:
            print(f"{COLORS['ERROR']}❌ Lettre de motivation non trouvée: {cover_letter_path}{COLORS['END']}")
    
    def apply_to_job(self, job_url, personal_info=None):
        """
        Postule automatiquement à une offre d'emploi
        
        Args:
            job_url (str): URL de l'offre d'emploi
            personal_info (dict): Informations personnelles (nom, email, téléphone, etc.)
            
        Returns:
            bool: True si la candidature a été envoyée avec succès
        """
        if not self.driver:
            print(f"{COLORS['ERROR']}❌ Navigateur non initialisé{COLORS['END']}")
            return False
        
        try:
            print(f"{COLORS['INFO']}📝 Début de la candidature pour: {job_url}{COLORS['END']}")
            
            # Naviguer vers l'offre
            self.driver.get(job_url)
            time.sleep(3)
            
            # Vérifier si on est sur la bonne page
            if not self._verify_job_page():
                print(f"{COLORS['ERROR']}❌ Page d'offre non reconnue{COLORS['END']}")
                return False
            
            # Chercher le bouton de candidature
            apply_button = self._find_apply_button()
            if not apply_button:
                print(f"{COLORS['ERROR']}❌ Bouton de candidature non trouvé{COLORS['END']}")
                return False
            
            # Cliquer sur le bouton de candidature
            print(f"{COLORS['INFO']}🔘 Clic sur le bouton de candidature...{COLORS['END']}")
            self.driver.execute_script("arguments[0].click();", apply_button)
            time.sleep(3)
            
            # Remplir le formulaire de candidature
            success = self._fill_application_form(personal_info)
            
            if success:
                print(f"{COLORS['SUCCESS']}🎉 Candidature envoyée avec succès!{COLORS['END']}")
            else:
                print(f"{COLORS['ERROR']}❌ Échec de l'envoi de la candidature{COLORS['END']}")
            
            return success
            
        except Exception as e:
            print(f"{COLORS['ERROR']}❌ Erreur lors de la candidature: {str(e)}{COLORS['END']}")
            return False
    
    def _verify_job_page(self):
        """Vérifie si on est sur une page d'offre d'emploi valide"""
        try:
            # Vérifier la présence d'éléments typiques d'une offre
            indicators = [
                "offre", "emploi", "job", "poste", "recrutement",
                "candidature", "apply", "postuler"
            ]
            
            page_text = self.driver.page_source.lower()
            return any(indicator in page_text for indicator in indicators)
            
        except Exception:
            return False
    
    def _find_apply_button(self):
        """Trouve le bouton de candidature sur la page"""
        # Sélecteurs possibles pour le bouton de candidature
        button_selectors = [
            "//button[contains(text(), 'Postuler')]",
            "//button[contains(text(), 'Candidater')]",
            "//button[contains(text(), 'Apply')]",
            "//a[contains(text(), 'Postuler')]",
            "//a[contains(text(), 'Candidater')]",
            "//input[@value='Postuler']",
            "//input[@value='Candidater']",
            "//button[contains(@class, 'postuler')]",
            "//button[contains(@class, 'candidater')]",
            "//button[contains(@class, 'apply')]",
            "//a[contains(@class, 'postuler')]",
            "//a[contains(@class, 'candidater')]"
        ]
        
        for selector in button_selectors:
            try:
                button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                if button and button.is_displayed():
                    return button
            except TimeoutException:
                continue
        
        # Essayer de trouver par ID ou classe CSS
        css_selectors = [
            "#postuler", "#candidater", "#apply",
            ".postuler", ".candidater", ".apply",
            "[data-testid='postuler']", "[data-testid='candidater']"
        ]
        
        for selector in css_selectors:
            try:
                button = self.driver.find_element(By.CSS_SELECTOR, selector)
                if button and button.is_displayed():
                    return button
            except NoSuchElementException:
                continue
        
        return None
    
    def _fill_application_form(self, personal_info):
        """Remplit le formulaire de candidature"""
        try:
            print(f"{COLORS['INFO']}📋 Remplissage du formulaire de candidature...{COLORS['END']}")
            
            # Attendre que le formulaire soit chargé
            time.sleep(3)
            
            # Remplir les informations personnelles si fournies
            if personal_info:
                self._fill_personal_info(personal_info)
            
            # Uploader le CV
            if self.cv_path:
                self._upload_cv()
            
            # Uploader la lettre de motivation
            if self.cover_letter_path:
                self._upload_cover_letter()
            
            # Remplir d'autres champs si nécessaire
            self._fill_additional_fields()
            
            # Soumettre le formulaire
            return self._submit_form()
            
        except Exception as e:
            print(f"{COLORS['ERROR']}❌ Erreur lors du remplissage du formulaire: {str(e)}{COLORS['END']}")
            return False
    
    def _fill_personal_info(self, personal_info):
        """Remplit les informations personnelles"""
        field_mappings = {
            'nom': ['nom', 'name', 'lastname', 'nom_famille'],
            'prenom': ['prenom', 'firstname', 'prenom'],
            'email': ['email', 'mail', 'courriel', 'adresse_email'],
            'telephone': ['telephone', 'phone', 'tel', 'mobile'],
            'adresse': ['adresse', 'address', 'rue'],
            'ville': ['ville', 'city', 'commune'],
            'code_postal': ['code_postal', 'postal_code', 'cp', 'zip']
        }
        
        for field_type, possible_names in field_mappings.items():
            if field_type in personal_info:
                value = personal_info[field_type]
                self._fill_field_by_name(possible_names, value)
    
    def _fill_field_by_name(self, field_names, value):
        """Remplit un champ par son nom"""
        for name in field_names:
            try:
                # Essayer par ID
                field = self.driver.find_element(By.ID, name)
                field.clear()
                field.send_keys(value)
                return
            except NoSuchElementException:
                pass
            
            try:
                # Essayer par name
                field = self.driver.find_element(By.NAME, name)
                field.clear()
                field.send_keys(value)
                return
            except NoSuchElementException:
                pass
            
            try:
                # Essayer par placeholder
                field = self.driver.find_element(By.XPATH, f"//input[@placeholder='{name}']")
                field.clear()
                field.send_keys(value)
                return
            except NoSuchElementException:
                pass
    
    def _upload_cv(self):
        """Upload le CV"""
        try:
            print(f"{COLORS['INFO']}📄 Upload du CV...{COLORS['END']}")
            
            # Sélecteurs pour les champs de fichier CV
            cv_selectors = [
                "input[type='file'][name*='cv']",
                "input[type='file'][name*='resume']",
                "input[type='file'][name*='curriculum']",
                "input[type='file'][id*='cv']",
                "input[type='file'][id*='resume']",
                "//input[@type='file' and contains(@name, 'cv')]",
                "//input[@type='file' and contains(@name, 'resume')]"
            ]
            
            for selector in cv_selectors:
                try:
                    if selector.startswith("//"):
                        file_input = self.driver.find_element(By.XPATH, selector)
                    else:
                        file_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if file_input:
                        file_input.send_keys(os.path.abspath(self.cv_path))
                        print(f"{COLORS['SUCCESS']}✅ CV uploadé avec succès{COLORS['END']}")
                        return True
                except NoSuchElementException:
                    continue
            
            print(f"{COLORS['WARNING']}⚠️ Champ d'upload CV non trouvé{COLORS['END']}")
            return False
            
        except Exception as e:
            print(f"{COLORS['ERROR']}❌ Erreur lors de l'upload du CV: {str(e)}{COLORS['END']}")
            return False
    
    def _upload_cover_letter(self):
        """Upload la lettre de motivation"""
        try:
            print(f"{COLORS['INFO']}📝 Upload de la lettre de motivation...{COLORS['END']}")
            
            # Sélecteurs pour les champs de fichier lettre de motivation
            letter_selectors = [
                "input[type='file'][name*='lettre']",
                "input[type='file'][name*='motivation']",
                "input[type='file'][name*='cover']",
                "input[type='file'][id*='lettre']",
                "input[type='file'][id*='motivation']",
                "//input[@type='file' and contains(@name, 'lettre')]",
                "//input[@type='file' and contains(@name, 'motivation')]"
            ]
            
            for selector in letter_selectors:
                try:
                    if selector.startswith("//"):
                        file_input = self.driver.find_element(By.XPATH, selector)
                    else:
                        file_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if file_input:
                        file_input.send_keys(os.path.abspath(self.cover_letter_path))
                        print(f"{COLORS['SUCCESS']}✅ Lettre de motivation uploadée avec succès{COLORS['END']}")
                        return True
                except NoSuchElementException:
                    continue
            
            print(f"{COLORS['WARNING']}⚠️ Champ d'upload lettre de motivation non trouvé{COLORS['END']}")
            return False
            
        except Exception as e:
            print(f"{COLORS['ERROR']}❌ Erreur lors de l'upload de la lettre de motivation: {str(e)}{COLORS['END']}")
            return False
    
    def _fill_additional_fields(self):
        """Remplit d'autres champs du formulaire si nécessaire"""
        try:
            # Chercher des champs texte vides et essayer de les remplir
            text_fields = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text'], textarea")
            
            for field in text_fields:
                try:
                    if not field.get_attribute('value') and field.is_displayed():
                        # Essayer de deviner le type de champ par son nom/id/placeholder
                        field_id = field.get_attribute('id', '').lower()
                        field_name = field.get_attribute('name', '').lower()
                        placeholder = field.get_attribute('placeholder', '').lower()
                        
                        # Valeurs par défaut selon le type de champ
                        if any(keyword in field_id + field_name + placeholder for keyword in ['message', 'comment', 'motivation']):
                            field.send_keys("Je suis très intéressé(e) par ce poste et souhaite vous faire parvenir ma candidature.")
                        elif any(keyword in field_id + field_name + placeholder for keyword in ['experience', 'competence']):
                            field.send_keys("Voir CV joint")
                except Exception:
                    continue
                    
        except Exception as e:
            print(f"{COLORS['WARNING']}⚠️ Erreur lors du remplissage des champs supplémentaires: {str(e)}{COLORS['END']}")
    
    def _submit_form(self):
        """Soumet le formulaire de candidature"""
        try:
            print(f"{COLORS['INFO']}🚀 Soumission du formulaire...{COLORS['END']}")
            
            # Sélecteurs pour le bouton de soumission
            submit_selectors = [
                "//button[contains(text(), 'Envoyer')]",
                "//button[contains(text(), 'Soumettre')]",
                "//button[contains(text(), 'Submit')]",
                "//button[contains(text(), 'Postuler')]",
                "//input[@type='submit']",
                "//button[@type='submit']",
                "button[type='submit']",
                "input[type='submit']",
                ".submit", ".envoyer", ".postuler"
            ]
            
            for selector in submit_selectors:
                try:
                    if selector.startswith("//"):
                        submit_button = self.driver.find_element(By.XPATH, selector)
                    else:
                        submit_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                    if submit_button and submit_button.is_displayed():
                        self.driver.execute_script("arguments[0].click();", submit_button)
                        time.sleep(5)  # Attendre la soumission
                        
                        # Vérifier si la soumission a réussi
                        if self._verify_submission_success():
                            return True
                        
                except NoSuchElementException:
                    continue
            
            print(f"{COLORS['WARNING']}⚠️ Bouton de soumission non trouvé{COLORS['END']}")
            return False
            
        except Exception as e:
            print(f"{COLORS['ERROR']}❌ Erreur lors de la soumission: {str(e)}{COLORS['END']}")
            return False
    
    def _verify_submission_success(self):
        """Vérifie si la soumission a réussi"""
        try:
            # Chercher des indicateurs de succès
            success_indicators = [
                "candidature envoyée", "merci", "confirmation",
                "success", "envoyé", "réussi"
            ]
            
            page_text = self.driver.page_source.lower()
            return any(indicator in page_text for indicator in success_indicators)
            
        except Exception:
            return False
    
    def close(self):
        """Ferme le navigateur"""
        if self.driver:
            try:
                self.driver.quit()
                print(f"{COLORS['SUCCESS']}✅ Navigateur fermé{COLORS['END']}")
            except Exception as e:
                print(f"{COLORS['WARNING']}⚠️ Erreur lors de la fermeture du navigateur: {str(e)}{COLORS['END']}")
    
    def __enter__(self):
        """Context manager entry"""
        if self.setup_driver():
            return self
        else:
            raise Exception("Impossible d'initialiser le navigateur")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
