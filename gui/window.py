from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QSizePolicy,
)
from translator import Translator


class GUI(QMainWindow):
    def __init__(self, debug: bool = False, parent=None):
        super().__init__(parent)
        self.debug = debug
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Translator")
        self.resize(1200, 600)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Input and output fields row
        row_layout = QHBoxLayout()
        row_layout.setSpacing(10)

        # Error field
        self.error_text = QTextEdit()
        self.error_text.setPlaceholderText("Ошибки трансляции...")
        self.error_text.setReadOnly(True)
        self.error_text.setMaximumHeight(80)
        self.error_text.setStyleSheet("color: grey;")

        main_layout.addLayout(row_layout, 1)
        main_layout.addWidget(self.error_text)

        # Input text field
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Введите текст для трансляции...")
        self.input_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.input_text.textChanged.connect(self.translate_code)

        # Output text field
        self.output_text = QTextEdit()
        self.output_text.setPlaceholderText("Результат трансляции...")
        self.output_text.setReadOnly(True)
        self.output_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        row_layout.addWidget(self.input_text)
        row_layout.addWidget(self.output_text)

    def translate_code(self):
        input_text = self.input_text.toPlainText()

        translated_text, error = Translator.translate(text=input_text, debug=self.debug)

        if error:
            self.output_text.clear()
            self.error_text.setPlainText(str(error))
            self.error_text.setStyleSheet("color: red;")
        else:
            self.error_text.clear()
            self.error_text.setStyleSheet("color: grey;")
            self.output_text.setPlainText(translated_text)


def invoke_gui(debug: bool = False):
    app = QApplication([])
    window = GUI(debug=debug)
    window.show()
    app.exec_()
