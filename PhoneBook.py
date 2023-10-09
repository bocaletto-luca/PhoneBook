import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox, QHeaderView, QLabel, QDialog
from PyQt5 import QtCore

class Contatto:
    def __init__(self, nome, telefono):
        self.nome = nome
        self.telefono = telefono
        self.selezionato = False

class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Informazioni')
        self.setGeometry(200, 200, 300, 150)

        layout = QVBoxLayout()

        informazioni_label = QLabel('Informazioni')
        autore_label = QLabel('Autore: Bocaletto Luca')
        email_label = QLabel('Email: your@email.com')
        website_label = QLabel('https://www.elektronoide.it')

        layout.addWidget(informazioni_label)
        layout.addWidget(autore_label)
        layout.addWidget(email_label)

        self.setLayout(layout)

class ContattiApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Impostazione della finestra principale
        self.setWindowTitle('Rubrica Telefonica')
        self.setGeometry(100, 100, 600, 300)

        # Creazione del layout principale
        self.layout = QVBoxLayout()

        # Aggiunta di un titolo nella GUI
        self.titolo_label = QLabel('Rubrica Telefonica')
        self.titolo_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Centro il testo
        self.titolo_label.setStyleSheet("font-size: 24px; color: blue;")  # Imposta colore e dimensione del testo

        # Creazione dei campi di inserimento per Nome e Telefono
        self.nome_entry = QLineEdit()
        self.telefono_entry = QLineEdit()

        # Creazione dei pulsanti per Aggiungi Contatto, Elimina Contatti e About
        self.aggiungi_button = QPushButton('Aggiungi Contatto')
        self.elimina_button = QPushButton('Elimina Contatti')
        self.about_button = QPushButton('About')

        # Creazione della tabella per visualizzare i contatti
        self.tabella_contatti = QTableWidget()
        self.tabella_contatti.setColumnCount(3)  # Tre colonne: Nome, Telefono, Selezione
        self.tabella_contatti.setHorizontalHeaderLabels(['Nome', 'Telefono', 'Selezione'])
        self.tabella_contatti.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Ridimensionamento delle colonne

        # Aggiunta dei widget al layout principale
        self.layout.addWidget(self.titolo_label)
        self.layout.addWidget(self.nome_entry)
        self.layout.addWidget(self.telefono_entry)
        self.layout.addWidget(self.aggiungi_button)
        self.layout.addWidget(self.elimina_button)
        self.layout.addWidget(self.about_button)
        self.layout.addWidget(self.tabella_contatti)

        # Collegamento dei pulsanti alle funzioni
        self.aggiungi_button.clicked.connect(self.aggiungi_contatto)
        self.elimina_button.clicked.connect(self.elimina_contatti)
        self.about_button.clicked.connect(self.mostra_about)

        # Impostazione del layout principale
        self.setLayout(self.layout)

        # Caricamento dei contatti all'avvio dell'applicazione
        self.carica_contatti()

    def mostra_about(self):
        dialog = AboutDialog()
        dialog.exec_()

    def aggiungi_contatto(self):
        # Funzione per aggiungere un nuovo contatto
        nome = self.nome_entry.text().strip()  # Rimuove gli spazi vuoti iniziali e finali
        telefono = self.telefono_entry.text().strip()

        if not nome or not telefono:
            # Se uno o entrambi i campi sono vuoti, mostra un messaggio di avviso
            QMessageBox.critical(self, 'Errore', 'Nome e Telefono devono essere riempiti.')
            return  # Esce dalla funzione senza aggiungere il contatto

        # Aggiunge il contatto alla lista
        contatto = Contatto(nome, telefono)
        self.contatti.append(contatto)

        # Ordina la lista in base ai nomi
        self.contatti.sort(key=lambda x: x.nome)

        # Aggiorna la tabella
        self.aggiorna_tabella()

        self.nome_entry.clear()
        self.telefono_entry.clear()
        self.salva_contatti()

    def carica_contatti(self):
        # Funzione per caricare i contatti da un file all'avvio
        self.contatti = []  # Lista per mantenere i contatti

        try:
            with open("contatti.txt", "r") as file:
                for linea in file:
                    parts = linea.strip().split(': ')
                    if len(parts) == 2:
                        nome, telefono = parts
                        contatto = Contatto(nome, telefono)
                        self.contatti.append(contatto)

            # Ordina la lista in base ai nomi
            self.contatti.sort(key=lambda x: x.nome)

            # Aggiorna la tabella
            self.aggiorna_tabella()
        except FileNotFoundError:
            pass

    def salva_contatti(self):
        # Funzione per salvare i contatti su un file
        try:
            with open("contatti.txt", "w") as file:
                for contatto in self.contatti:
                    file.write(f"{contatto.nome}: {contatto.telefono}\n")
        except IOError:
            QMessageBox.critical(self, 'Errore', 'Impossibile salvare i contatti su file.')

    def aggiorna_tabella(self):
        # Funzione per aggiornare la tabella con i contatti attuali
        self.tabella_contatti.setRowCount(len(self.contatti))

        for row, contatto in enumerate(self.contatti):
            self.tabella_contatti.setItem(row, 0, QTableWidgetItem(contatto.nome))
            self.tabella_contatti.setItem(row, 1, QTableWidgetItem(contatto.telefono))

            # Aggiunge una casella di controllo alla terza colonna
            checkbox = QTableWidgetItem()
            checkbox.setFlags(checkbox.flags() | QtCore.Qt.ItemIsUserCheckable)
            checkbox.setCheckState(QtCore.Qt.Checked if contatto.selezionato else QtCore.Qt.Unchecked)
            self.tabella_contatti.setItem(row, 2, checkbox)

    def elimina_contatti(self):
        # Funzione per eliminare i contatti selezionati
        contatti_da_eliminare = []

        for row, contatto in enumerate(self.contatti):
            checkbox = self.tabella_contatti.item(row, 2)
            if checkbox and checkbox.checkState() == QtCore.Qt.Checked:
                contatti_da_eliminare.append(contatto)

        for contatto in contatti_da_eliminare:
            self.contatti.remove(contatto)

        # Aggiorna la tabella
        self.aggiorna_tabella()

        # Salva i contatti aggiornati
        self.salva_contatti()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ContattiApp()
    ex.show()
    sys.exit(app.exec_())
