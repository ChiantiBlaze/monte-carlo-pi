# Getting Pi using Monte-Carlo Method
# Tested on Python 3.6.1, PyQt5, Matplotlib

from PyQt5.QtWidgets import QWidget, QGridLayout, QRadioButton, \
							QGroupBox, QPushButton, QLabel, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MC_Pi(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()


	def initUI(self):
		# initialize UI

		grid = QGridLayout()
		grid.addWidget(self.add_graph_panel(),0,0,4,1)
		grid.addWidget(self.add_log_panel(),0,1)
		grid.addWidget(self.add_status_panel(),1,1)
		grid.addWidget(self.add_settings_panel(),2,1)
		grid.addWidget(self.add_btn_panel(),3,1)

		self.setLayout(grid)
		self.setWindowTitle("Monte Carlo Simulation - Value of Pi")
		self.show()


	def add_graph_panel(self):
		box = QGroupBox('Graph')
		self.display = QLabel()
		self.display.setFixedSize(550,550)
		
		shots = QPixmap('./shots/default.png')

		shots = shots.scaled(self.display.size(), Qt.KeepAspectRatio, \
									transformMode = Qt.SmoothTransformation)

		self.display.setPixmap(shots)
		
		layout = QGridLayout()
		layout.addWidget(self.display)
		box.setLayout(layout)

		return box

	def add_log_panel(self):
		box = QGroupBox('Log')
		layout = QGridLayout()
		self.log = QTextEdit("(0.032345, 0.40589)   <font color=#00a8ff>True</font>")
		self.log.setFixedHeight(120)
		self.log.setReadOnly(True)
		layout.addWidget(self.log)
		box.setLayout(layout)

		return box



	def add_status_panel(self):
		box = QGroupBox('Status')
		self.status_formula = QLabel('(x-{a})²+(y-{b})²=({r})²'.format(a=0,b=0,r=1))
		self.status_total = QLabel("0")
		self.status_pi = QLabel("0.0000000000")
		self.status_pi_4 = QLabel("0.0000000000")
		layout = QGridLayout()
		layout.addWidget(QLabel('Equation Formula          '), 0,0) # whitespace on purpose
		layout.addWidget(self.status_formula, 0,1)
		layout.addWidget(QLabel("Total Dots"), 1,0)
		layout.addWidget(self.status_total, 1,1)
		layout.addWidget(QLabel("Estimated π / 4"), 2,0)
		layout.addWidget(self.status_pi_4, 2,1)
		layout.addWidget(QLabel("Estimated π"), 3,0)
		layout.addWidget(self.status_pi, 3,1)
		box.setLayout(layout)

		return box


	def add_settings_panel(self):
		box = QGroupBox('Settings')
		layout = QGridLayout()

		# Dots per Action RadioBox #
		dsr_box = QGroupBox("Dots per Action: ")
		dsr_layout = QGridLayout()
		dsr_p1 = QRadioButton("1"); dsr_layout.addWidget(dsr_p1, 0,0)
		dsr_p10 = QRadioButton("10"); dsr_layout.addWidget(dsr_p10, 0,1)
		dsr_p25 = QRadioButton("25"); dsr_layout.addWidget(dsr_p25, 0,2)
		dsr_p100 = QRadioButton("100"); dsr_layout.addWidget(dsr_p100, 0,3)
		dsr_p1.setChecked(True)
		dsr_box.setLayout(dsr_layout)

		# Area Criteria #
		ac_box = QGroupBox("Area Criteria: ")
		ac_layout = QGridLayout()
		self.criterion_x = QLineEdit('0')
		self.criterion_y = QLineEdit('0')
		self.criterion_scale = QLineEdit('1')
		ac_layout.addWidget(QLabel('a (X)'), 0,0)
		ac_layout.addWidget(self.criterion_x, 0,1)
		ac_layout.addWidget(QLabel('b (Y)'), 1,0)
		ac_layout.addWidget(self.criterion_y, 1,1)
		ac_layout.addWidget(QLabel('r (Scale)'), 2,0)
		ac_layout.addWidget(self.criterion_scale, 2,1)
		ac_box.setLayout(ac_layout)

		layout.addWidget(dsr_box, 0,0)
		layout.addWidget(ac_box, 1,0)

		box.setLayout(layout)
		return box


	def add_btn_panel(self):
		self.start_btn = QPushButton("Start Simulation")

		return self.start_btn