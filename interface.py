import sys #, os
import numpy as np
from PyQt5.QtWidgets import (QListWidget, QWidget, QMessageBox, QApplication, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QLabel,QPushButton, QComboBox)
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtGui import QIcon


class UiVectors(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setWindowIcon(QIcon('yasu.ico'))

        self.x = np.array([])
        self.y = np.array([])
        self.posx = np.array([])
        self.posy = np.array([])
        self.color = []

        self.l1 = QLabel('Entry elements:',self)
        self.l1.setStyleSheet('font: 11pt "Arial";')

        self.entry_x = QLineEdit(self)
        self.entry_x.setStyleSheet('font: 75 11pt "Arial";')
        self.entry_x.setPlaceholderText('x')

        self.entry_y = QLineEdit(self)
        self.entry_y.setStyleSheet('font: 75 11pt "Arial";')
        self.entry_y.setPlaceholderText('y')

        self.entry_posx = QLineEdit(self)
        self.entry_posx.setStyleSheet('font: 75 11pt "Arial";')
        self.entry_posx.setPlaceholderText('x origin')
        self.entry_posx.setText('0')

        self.entry_posy = QLineEdit(self)
        self.entry_posy.setStyleSheet('font: 75 11pt "Arial";')
        self.entry_posy.setPlaceholderText('y origin')
        self.entry_posy.setText('0')

        self.cbox = QComboBox(self)
        self.cbox.setStyleSheet('font: 75 11pt "Arial";')
        colors = ['red','green','orange','blue','skyblue','gold','brown', 'black']
        for c in colors:
            self.cbox.addItem(c)
        
        self.b_one = QPushButton('Send',self)
        self.b_one.setStyleSheet('font: 10pt "Arial";')
        self.b_one.clicked.connect(self.send_elements)

        self.b_clear = QPushButton('Clear',self)
        self.b_clear.setStyleSheet('font: 10pt "Arial";')
        self.b_clear.clicked.connect(self.clear_all)

        self.b_back = QPushButton('Back',self)
        self.b_back.setStyleSheet('font: 10pt "Arial";')
        self.b_back.clicked.connect(self.back_data)

        self.b_save = QPushButton('Save',self)
        self.b_save.setStyleSheet('font: 10pt "Arial";')
        self.b_save.clicked.connect(self.save_data)       

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        vbox.addWidget(self.l1)

        hbox.addWidget(self.entry_posx)
        hbox.addWidget(self.entry_x)
        vbox.addLayout(hbox)

        hbox = QHBoxLayout()
        hbox.addWidget(self.entry_posy)
        hbox.addWidget(self.entry_y)
        vbox.addLayout(hbox)

        vbox.addWidget(self.cbox)
        vbox.addWidget(self.b_one)
        vbox.addWidget(self.b_clear)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        vbox = QVBoxLayout()

        self.list = QListWidget()
        vbox.addWidget(self.list)
        hbox.addLayout(vbox)

        self.fig = Figure((450,450))
        self.canvas = FigureCanvas(self.fig)

        vbox = QVBoxLayout()

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.b_back)
        hbox2.addWidget(self.b_save)

        vbox.addLayout(hbox2)
        vbox.addWidget(self.canvas)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        del(hbox2)

        self.setWindowTitle('Yasu plots')
        self.resize(600,600)
        self.show()

    def send_elements(self):
        try:
            x,y,color = int(self.entry_x.text()), int(self.entry_y.text()), str(self.cbox.currentText())
            posx, posy = int(self.entry_posx.text()), int(self.entry_posy.text())
            self.list.addItem(f' origin: [{posx},{posy}] - vector: [{x}, {y}] - color: {color}.')

            self.x = np.append(self.x, x)
            self.y = np.append(self.y, y)
            self.color.append(color)
            self.posx = np.append(self.posx, posx)
            self.posy = np.append(self.posy, posy)

            self.draw_vectors(self.posx, self.posy, self.x,self.y,self.color)

        except:
            self.dialog()

        self.entry_x.clear()
        self.entry_y.clear()
        self.entry_posx.setText('0')
        self.entry_posy.setText('0')

    def draw_vectors(self, posx = np.array([0]), posy=np.array([0]), x = np.array([0]), y = np.array([0]), color = ['black']):
        self.fig.clear()
        auxx = posx + x
        auxy = posy + y
        xx, xy =  np.min(auxx), np.max(auxx)
        yx, yy = np.min(auxy), np.max(auxy)
        
        if xx < 0:
            xx -= 1
            if xy < 0:
                xy = 0
        else:
            xx = -1
        xy += 1
        if yx < 0:
            yx -=1
            if yy < 0:
                yy = 0
        else:
            yx = -1
        yy += 1

        try:
            ax = self.fig.add_subplot(111)
            for i,c in enumerate(color):
                ax.quiver([posx[i]],[posy[i]],[x[i]], [y[i]], color=c, angles='xy', scale_units='xy', scale=1, alpha=1)
            
            ax.axvline(x=0,c='gray',zorder=0) # zorder for background
            ax.axhline(y=0,c='gray',zorder=0)

            ax.axes.set_xlim([xx,xy])
            ax.axes.set_ylim([yx,yy])

            ax.set_title('Plot Vectors')
            
            ax.grid()
            self.canvas.draw()
        except:
            self.x = self.x[:-1]
            self.y = self.y[:-1]
            self.color.pop(-1)
            self.posx = self.posx[:-1]
            self.posy = self.posy[:-1]

    def clear_all(self):
        self.list.clear()
        self.x = np.array([])
        self.y = np.array([])
        self.color.clear()
        self.posx = np.array([])
        self.posy = np.array([])
        # self.fig.clear()
        self.draw_vectors()
        self.canvas.draw()

    def back_data(self):
        try:
            self.x = self.x[:-1]
            self.y = self.y[:-1]
            self.color.pop(-1)
            self.posx = self.posx[:-1]
            self.posy = self.posy[:-1]

            length = len(self.color)
            if length == 0:
                self.draw_vectors()
                self.list.takeItem(0)
            else:
                self.draw_vectors(self.posx, self.posy, self.x,self.y,self.color)
                self.list.takeItem(length-1)
        except:
            self.dialog()

    def save_data(self):
        #path = os.path.dirname(os.path.abspath(__file__)) + '\\vector.png'
        path = 'vector.png'
        self.canvas.print_png(path)
        self.dialog(title='Save', text=f'Successfully saved! with the name "{path}".', icon=QMessageBox.Information)

    def dialog(self, title='Error!', text = 'There was a mistake.', icon=QMessageBox.Warning):
        msgBox = QMessageBox(self)
        msgBox.setIcon(icon)
        msgBox.setText(text)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()


