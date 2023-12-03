import os
import sys
import json

from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout, QLabel, QComboBox, QLineEdit, QFileDialog, QCheckBox, QSizePolicy, QHBoxLayout
from PySide6.QtGui import QIntValidator, QPixmap, QIcon, QDesktopServices
from PySide6.QtCore import Qt, QUrl

from aes128cbcencryptdecrypt import encrypt, decrypt


# PLANET_ID = {
#     'Experimental': 0,
#     'Assurance': 1,
#     'Vow': 2,
#     '71 Gordian': 3,
#     'March': 4,
#     'Rend': 5,
#     'Dine': 6,
#     'Offense': 7,
#     'Titan': 8
# }

APP_NAME = 'REO NOMURA SIMPLE LC SAVE EDITOR (SUPER LAZY VER.)'

# For windows only
# ChatGPT writes alot of code, Yes too lazy.
DEFAULT_SAVE_FILE_LOCATION = os.path.join(os.path.expanduser('~'), 'AppData', 'LocalLow', 'ZeekerssRBLX', 'Lethal Company')
CURRENT_DIRECTORY = None
SAVE_FILE_CONTENT = None
FULL_SAVE_FILE_PATH = None


class MyWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self):
        # Load the image
        image_path = 'reo.jpg'
        pixmap = QPixmap(image_path)

        # Create a label for the image
        image_label = QLabel(self)

        # Set size policy to make QLabel expand to fit the image
        image_label.setPixmap(pixmap)
        image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        image_label.setScaledContents(True)

        # Create a label for a selected save file
        # save_file_label = QLabel('Save file:', self)
        save_file_dropdown = QComboBox(self)
        save_file_dropdown.setObjectName('save_file_dropdown')
        save_file_dropdown.currentIndexChanged.connect(self.load_file_content)

        # Create a label for the planet selection
        planet_label = QLabel('Planet:', self)

        # Create a dropdown box with the specified values
        planets = ['Experimental', 'Assurance', 'Vow', '71 Gordion', 'March', 'Rend', 'Dine', 'Offense', 'Titan']
        planet_dropdown = QComboBox(self)
        planet_dropdown.setObjectName('planet_dropdown')
        planet_dropdown.addItems(planets)
        planet_dropdown.currentIndexChanged.connect(lambda index: self.buffer_file_content('CurrentPlanetID', index))


        # Create a label for the money input
        money_label = QLabel('Money:', self)

        # Create a text field for entering the amount of money
        money_input = QLineEdit(self)
        money_input.setObjectName('money_input')
        money_input.setValidator(QIntValidator())  # Allow only integer input

        # Handle exmpty string, too lazy to write a better code
        money_input.textChanged.connect(lambda money: self.buffer_file_content('GroupCredits', int(0 if money == '' else money)))

        # Create a label for the deadline input
        deadline_label = QLabel('Deadline (days):', self)

        # Create a text field for entering the deadline
        deadline_input = QLineEdit(self)
        deadline_input.setObjectName('deadline_input')
        deadline_input.setValidator(QIntValidator())  # Allow only integer input

        # Handle exmpty string, too lazy to write a better code
        deadline_input.textChanged.connect(lambda deadline: self.buffer_file_content('DeadlineTime', int(0 if deadline == '' else deadline) * 1080))

        # Create a label for the quota input
        quota_label = QLabel('Quota:', self)

        # Create a text field for entering the quota
        quota_input = QLineEdit(self)
        quota_input.setObjectName('quota_input')
        quota_input.setValidator(QIntValidator())  # Allow only integer input

        # Handle exmpty string, too lazy to write a better code
        quota_input.textChanged.connect(lambda quota: self.buffer_file_content('ProfitQuota', int(0 if quota == '' else quota)))

        # Create a label for the seed input
        seed_label = QLabel('Seed:', self)

        # Create a text field for entering the seed
        seed_input = QLineEdit(self)
        seed_input.setObjectName('seed_input')
        seed_input.setValidator(QIntValidator())  # Allow only integer input

        # Handle exmpty string, too lazy to write a better code
        seed_input.textChanged.connect(lambda seed: self.buffer_file_content('RandomSeed', int(0 if seed == '' else seed)))

        # Create a button to browse for a directory
        browse_button = QPushButton('Browse save files', self)
        browse_button.clicked.connect(lambda:self.browse_directory(None))

        # Create a label for selected save files directory
        save_dir_label = QLabel('Selected dir:', self)
        save_dir_label.setObjectName('save_dir_label')

        # Create a checkbox for QuotaFulfilled
        quota_fulfilled_checkbox = QCheckBox('Quota Fulfilled', self)
        quota_fulfilled_checkbox.setObjectName('quota_fulfilled_checkbox')
        quota_fulfilled_checkbox.stateChanged.connect(lambda checked: self.buffer_file_content('QuotaFulfilled', 1 if checked else 0))

        # Create a label for the QuotaPassed input
        quota_passed_label = QLabel('Quota Passed:', self)

        # Create a text field for entering the QuotaPassed value
        quota_passed_input = QLineEdit(self)
        quota_passed_input.setObjectName('quota_passed_input')
        quota_passed_input.setValidator(QIntValidator())  # Allow only integer input

        # Handle exmpty string, too lazy to write a better code
        quota_passed_input.textChanged.connect(lambda quota_passed: self.buffer_file_content('QuotasPassed', int(0 if quota_passed == '' else quota_passed)))

        # Create contact
        contact_label = QLabel('<span style="font-weight: bold;">CONTACT ME:</span>')
        fb_label = QLabel('<a href="https://www.facebook.com/nomurareo">🟦 <span style="color: #0000EE; font-weight: bold;">Facebook</span></a>')
        x_label = QLabel('<a href="https://twitter.com/nomura_reo">⬛ <span style="color: #0000EE; font-weight: bold;">X (Twitter)</span></a>')
        fb_label.setOpenExternalLinks(True)
        x_label.setOpenExternalLinks(True)
        fb_label.linkActivated.connect(self.open_link)
        x_label.linkActivated.connect(self.open_link)

        # Create a warning label
        warning_label = QLabel('<span style="color: red; font-weight: bold;">DANGER:</span> YOU MUST CREATE YOUR OWN SAVE FILE BACKUP CUZ I\'M TOO LAZY', self)

        # Create a button
        save_button = QPushButton('SAVE', self)
        save_button.setStyleSheet('font-weight: bold; background-color: #CBC3E3;')
        save_button.clicked.connect(self.save_file_content)

        # Set up the layout
        layout = QVBoxLayout(self)
        h_layout = QHBoxLayout(self)
        h_layout.setAlignment(Qt.AlignLeft)

        layout.addWidget(image_label)
        layout.addWidget(save_dir_label)
        layout.addWidget(save_file_dropdown)
        layout.addWidget(browse_button)
        layout.addWidget(planet_label)
        layout.addWidget(planet_dropdown)
        layout.addWidget(money_label)
        layout.addWidget(money_input)
        layout.addWidget(deadline_label)
        layout.addWidget(deadline_input)
        layout.addWidget(seed_label)
        layout.addWidget(seed_input)
        layout.addWidget(quota_label)
        layout.addWidget(quota_input)
        layout.addWidget(quota_passed_label)
        layout.addWidget(quota_passed_input)
        layout.addWidget(quota_fulfilled_checkbox)
        layout.addWidget(warning_label)
        
        h_layout.addWidget(contact_label)
        h_layout.addWidget(fb_label)
        h_layout.addWidget(x_label)
        layout.addLayout(h_layout)
        layout.addWidget(save_button)

        # Set default save file location
        # Handling non default saved directory and also I'M TOO DAMN LAZY FOR NOW
        try:
            self.browse_directory(DEFAULT_SAVE_FILE_LOCATION)  
        except FileNotFoundError:
            pass

        # Set window properties
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QIcon(image_path))
        self.show()


    def open_link(self, url):
        QDesktopServices.openUrl(QUrl(url))

    def load_file_content(self, index):
        if index > -1:
            # Update the FULL_SAVE_FILE_PATH global used to access the latest save file content CUZ I'M TOO LAZY
            global FULL_SAVE_FILE_PATH
            FULL_SAVE_FILE_PATH = os.path.join(CURRENT_DIRECTORY, self.findChild(QComboBox, 'save_file_dropdown').currentText())
            with open(FULL_SAVE_FILE_PATH, 'rb') as save_file:
                # Update the SAVE_FILE_CONTENT global used to access the latest save file content CUZ I'M TOO LAZY
                global SAVE_FILE_CONTENT
                SAVE_FILE_CONTENT = json.loads(decrypt(save_file.read()))
                self.findChild(QComboBox, 'planet_dropdown').setCurrentIndex(SAVE_FILE_CONTENT['CurrentPlanetID']['value'])
                self.findChild(QLineEdit, 'money_input').setText(str(SAVE_FILE_CONTENT['GroupCredits']['value']))
                self.findChild(QLineEdit, 'deadline_input').setText(str(SAVE_FILE_CONTENT['DeadlineTime']['value'] // 1080))
                self.findChild(QLineEdit, 'seed_input').setText(str(SAVE_FILE_CONTENT['RandomSeed']['value']))
                self.findChild(QLineEdit, 'quota_input').setText(str(SAVE_FILE_CONTENT['ProfitQuota']['value']))
                self.findChild(QLineEdit, 'quota_passed_input').setText(str(SAVE_FILE_CONTENT['QuotasPassed']['value']))
                self.findChild(QCheckBox, 'quota_fulfilled_checkbox').setChecked(bool(SAVE_FILE_CONTENT['QuotaFulfilled']['value']))


    def buffer_file_content(self, field, value):
        if isinstance(value, int):
            if value < 0:
                value = 0
            
            if field == 'GroupCredits':
                if value > 99999:
                    value = 99999
            elif field == 'DeadlineTime':
                if value > 1000:
                    value = 10000
            elif field == 'RandomSeed':
                if value > 1e9:
                    value = 1e9
            elif field == 'ProfitQuota':
                if value > 9999:
                    value = 9999
            elif field == 'QuotasPassed':
                if value > 99999:
                    value = 99999
            elif field == 'QuotaFulfilled':
                if value > 1:
                    value = 1
        
        SAVE_FILE_CONTENT[field]['value'] = value


    def save_file_content(self):
        print('saving file content')

        # print(SAVE_FILE_CONTENT)
        with open(FULL_SAVE_FILE_PATH, 'wb') as save_file:
            save_file.write(encrypt(json.dumps(SAVE_FILE_CONTENT)))

        # Display a 'OK DONE!' message box.
        QMessageBox.information(self, 'REO NOMURA', 'SAVED, ENJOY!')


    def browse_directory(self, directory):
        options = QFileDialog.Options() | QFileDialog.DontUseNativeDialog
        
        if not directory:
            directory = QFileDialog.getExistingDirectory(self, 'Select Directory', options=options)

        # Update the CURRENT_DIRECTORY global used to access the latest save file directory CUZ I'M TOO LAZY
        global CURRENT_DIRECTORY
        CURRENT_DIRECTORY = directory

        # Update the directory label with the selected directory
        directory_label = self.findChild(QLabel, 'save_dir_label')
        directory_label.setText(f'Selected Directory: {directory}')

        # Clear existing items in the files dropdown
        files_dropdown = self.findChild(QComboBox, 'save_file_dropdown')
        files_dropdown.clear()

        # raise RuntimeError(directory)

        # Populate the files dropdown with files from the selected directory
        if directory:
            files = [f for f in os.listdir(directory) if f.startswith('LCSaveFile') and os.path.isfile(os.path.join(directory, f))]
            files_dropdown.addItems(files)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec())
