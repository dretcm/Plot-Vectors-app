from interface import UiVectors, QApplication, sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UiVectors()
    sys.exit(app.exec_())