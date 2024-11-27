# manage application exit and command-line arguments
import sys
# Manages caching logic for HTTP responses
from CacheManager import CacheManager
# Manages Cookies
from CookiesManager import CookiesManager
# sending HTTP requests
import requests
# GUI components
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QLineEdit, QComboBox, QPushButton, QTextEdit, QInputDialog, QMessageBox,
    QDialog, QHBoxLayout, QLabel
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QColor, QIcon


# QMainWindow to build the main window
class CustomBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Navigateur personnalisé")
        self.setGeometry(100, 100, 1000, 700)

        # Create the main layout for CustomBrowser
        main_layout = QVBoxLayout(self)  # Set the layout for the main widget

        self.cache_manager = CacheManager()
        self.cookies_manager = CookiesManager()

        # Widget principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        # vertical layout (QVBoxLayout)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Input pour URL text field (QLineEdit)
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Entrez une URL")
        self.url_input.setStyleSheet("font-size: 14px; padding: 5px; border-radius: 5px;")
        self.layout.addWidget(self.url_input)

        # Liste déroulante (Dropdown QComboBox) pour la méthode HTTP (GET, POST...)
        self.method_select = QComboBox(self)
        self.method_select.setStyleSheet("font-size: 14px; padding: 5px; border-radius: 5px;")
        self.layout.addWidget(self.method_select)

        # Liste déroulante (Dropdown QComboBox) pour la version HTTP
        self.version_select = QComboBox(self)
        self.version_select.addItems(["HTTP/1.1", "HTTP/1.0", "Personnalisé"])  # Ajout "Personnalisé"
        self.version_select.setStyleSheet("font-size: 14px; padding: 5px; border-radius: 5px;")
        self.layout.addWidget(self.version_select)

        # Champ pour entrer les données POST/PUT (initialement masqué)
        self.body_input = QTextEdit(self)
        self.body_input.setPlaceholderText("Entrez le corps de la requête (JSON, etc.) pour POST/PUT")
        self.body_input.setStyleSheet("font-size: 14px; padding: 5px; border-radius: 5px;")
        self.body_input.setVisible(False)  # Masqué par défaut
        self.layout.addWidget(self.body_input)

        # Buttons layout
        self.buttons_layout = QVBoxLayout()
        self.layout.addLayout(self.buttons_layout)

        # "View Cookies" button
        self.view_cookies_button = QPushButton("View Cookies", self)
        self.view_cookies_button.setStyleSheet(self.button_style())
        self.view_cookies_button.clicked.connect(self.view_cookies)
        self.layout.addWidget(self.view_cookies_button)
        

        # Bouton pour envoyer la requête
        self.request_button = QPushButton("Envoyer la requête", self)
        self.request_button.setStyleSheet(self.button_style())
        self.request_button.clicked.connect(self.send_request)
        self.layout.addWidget(self.request_button)

        # Afficher la réponse brute
        self.response_view = QTextEdit(self)
        self.response_view.setReadOnly(True)
        self.response_view.setStyleSheet("font-size: 14px; padding: 5px; border-radius: 5px; background-color: #f0f0f0;")
        self.layout.addWidget(self.response_view)

        ## Navigateur intégré (A web engine to render the HTML content of the response)
        self.web_view = QWebEngineView(self)
        self.layout.addWidget(self.web_view)

        ## Connecter les mises à jour dynamiques 
        # (Methodes HTTP basées sur la version HTTP)
        self.update_methods()
        self.method_select.currentIndexChanged.connect(self.toggle_body_input)  # Masquer/afficher selon la méthode # Shows/hides the body input field for POST/PUT methods.
        self.version_select.currentIndexChanged.connect(self.handle_version_change) #  Allows specifying a custom HTTP version


    def style_sheet(self):
        return """
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 10px;
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                font-size: 16px;
                padding: 10px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QComboBox {
                background-color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 5px;
            }
        """

    def button_style(self):
        return """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                font-size: 16px;
                padding: 10px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """

    def update_methods(self):
        # Mettre à jour la liste des méthodes en fonction de la version HTTP
        self.method_select.clear()
        if self.version_select.currentText() == "HTTP/1.0":
            self.method_select.addItems(["GET", "POST", "HEAD"])
        else:
            self.method_select.addItems(["GET", "POST", "PUT", "DELETE", "HEAD"])

    def handle_version_change(self):
        # Gérer le changement de version HTTP, y compris 'Personnalisé'
        if self.version_select.currentText() == "Personnalisé":
            # Afficher une boîte de dialogue pour une version personnalisée
            version, ok = QInputDialog.getText(self, "Version HTTP personnalisée", "Entrez une version HTTP :")
            if ok and version:
                # Ajouter dynamiquement la version et la sélectionner
                self.version_select.addItem(version)
                self.version_select.setCurrentText(version)
        self.update_methods()

    def toggle_body_input(self):
        # Afficher ou masquer le champ de saisie en fonction de la méthode choisie
        method = self.method_select.currentText()
        if method in ["POST", "PUT"]:
            self.body_input.setVisible(True)  # Afficher le champ pour POST/PUT
        else:
            self.body_input.setVisible(False)  # Masquer pour les autres méthodes

    def send_request(self):
        url = self.url_input.text()
        method = self.method_select.currentText()
        http_version = self.version_select.currentText()


        if not url.startswith(("http://", "https://")):
            url = "http://" + url

        if http_version not in ["HTTP/1.1", "HTTP/1.0"]:
            QMessageBox.warning(self, "Version non supportée",
                                f"La version {http_version} n'est pas officiellement prise en charge.")
            return

        try:
            # Récupérer les en-têtes de cache (If-Modified-Since, etc...)
            cache_headers = self.cache_manager.get_cache_headers(url)

            # Ajouter des en-têtes pour éviter la mise en cache côté serveur
            cache_headers.update({
                "Cache-Control": "no-cache",  # Désactive le cache
                "Pragma": "no-cache",  # Anciennement utilisé pour les vieux navigateurs
                "Expires": "0"  # Assure que le cache est expiré
            })

            # comment cookies
            headers = self.cache_manager.get_cache_headers(url)
            
            #headers = self.cookies_manager.attach_cookies(url, headers)  # Attach cookies
            print(headers)

            # Add cookies for the URL
            cookies = self.cookies_manager.get_cookies(url)
            print(cookies)

            # Créer la session avec la version HTTP appropriée
            session = requests.Session()
            session.cookies.update(cookies)  # Add cookies to the session


            if http_version == "HTTP/1.0":
                session.headers.update({"Connection": "close"})  # Désactiver keep-alive pour HTTP/1.0

            # Inclure les données dans le corps si la méthode est POST ou PUT
            data = None
            if method in ["POST", "PUT"]:
                data = self.body_input.toPlainText()

            # Faire la requête avec les en-têtes de cache
            response = session.request(
                method=method,
                url=url,
                headers=cache_headers,
                data=data  # Ajouter le corps de la requête
            )

            # Handle cookies from the response
            for cookie in response.cookies:
                self.cookies_manager.add_cookie(url, cookie.name, cookie.value)


            # Vérifier la réponse et gérer le cache
            response_text = f"Version HTTP: {http_version}\nStatut: {response.status_code}"

            if response.status_code == 304:
                # Si la réponse est 304 (Not Modified), afficher les en-têtes et utiliser le contenu mis en cache
                response_text += " Not Modified\n\n"
                response_text += "En-têtes de la réponse:\n"
                for header, value in response.headers.items():
                    response_text += f"{header}: {value}\n"

                cached_content = self.cache_manager.get_cached_content(url)
                if cached_content:
                    response_text += f"\nContenu (depuis le cache) :\n{cached_content}"
                    # Afficher le contenu mis en cache
                    self.web_view.setHtml(cached_content, QUrl(url))
                else:
                    response_text += "Aucun contenu mis en cache disponible."

            elif response.status_code == 200:
                response_text += f" {response.reason}\n\n"
                response_text += "En-têtes de la réponse:\n"
                for header, value in response.headers.items():
                    response_text += f"{header}: {value}\n"

                if method != "HEAD":
                    # Mettre à jour le cache avec le nouveau contenu
                    self.cache_manager.update_cache(url, response)
                    response_text += f"\nContenu:\n{response.text}"
                    # Afficher le contenu dans le navigateur intégré
                    self.web_view.setHtml(response.text, QUrl(url))

            # Comment cookies
            #self.cookies_manager.update_cookies(url, response)
            self.response_view.setText(response_text)

        except Exception as e:
            self.response_view.setText(f"Erreur : {str(e)}")

    def view_cookies(self):
        cookies_text = self.get_cookies_text()
        
        # Create a dialog to display cookies
        text_dialog = QDialog(self)
        text_dialog.setWindowTitle("Cookies")
        text_dialog.setMinimumWidth(400)
        
        # Use a layout specific to the dialog
        dialog_layout = QVBoxLayout(text_dialog)

        # Create QTextEdit to display cookies
        text_edit = QTextEdit()
        text_edit.setPlainText(cookies_text)
        text_edit.setReadOnly(True)  # Make it read-only

        dialog_layout.addWidget(text_edit)

        # Style UI
        close_button = QPushButton("Fermer", text_dialog)
        close_button.setStyleSheet(self.button_style())
        close_button.clicked.connect(text_dialog.accept)
        dialog_layout.addWidget(close_button)

        # Show the dialog
        text_dialog.exec_()

    def get_cookies_text(self):
        cookies_text = ""
        for url, cookies in self.cookies_manager.cookies.items():
            cookies_text += f"URL: {url}\n"
            for cookie_name, cookie_value in cookies.items():
                cookies_text += f"  {cookie_name}: {cookie_value}\n"
            cookies_text += "\n"
        return cookies_text

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = CustomBrowser()
    browser.show()
    sys.exit(app.exec_())