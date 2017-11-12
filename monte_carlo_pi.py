# Getting Pi using Monte-Carlo Method
# Tested on Python 3.6.1, PyQt5, Matplotlib

from PyQt5.QtWidgets import QWidget, QGridLayout, QRadioButton, \
							QGroupBox, QPushButton, QLabel, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap, QTextCursor
from PyQt5.QtCore import Qt, QThread, QCoreApplication
from numbers import Real
from plot_graph import get_preview_shot, get_plot_shot
from numpy.random import uniform
from time import sleep


class MC_Pi_Framework(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()


	def initUI(self):
		# initialize UI

		grid = QGridLayout()
		grid.addWidget(self.add_graph_panel(),0,0,5,1)
		grid.addWidget(self.add_comment_panel(),0,1)
		grid.addWidget(self.add_status_panel(),1,1)
		grid.addWidget(self.add_settings_panel(),2,1)
		grid.addWidget(self.add_confirm_btn(),3,1)
		grid.addWidget(self.add_start_btn(),4,1)

		self.setLayout(grid)
		self.setWindowTitle("Monte Carlo Simulation - Assuming the Value of π")
		self.show()


	def add_graph_panel(self):
		box = QGroupBox('Graph')
		self.display = QLabel()
		self.display.setFixedSize(600,600)
		
		shot = QPixmap('./shots/default.png')

		shot = shot.scaled(self.display.size(), Qt.KeepAspectRatio, \
									transformMode = Qt.SmoothTransformation)

		self.display.setPixmap(shot)
		
		layout = QGridLayout()
		layout.addWidget(self.display)
		box.setLayout(layout)

		return box


	def add_comment_panel(self):
		box = QGroupBox()
		layout = QGridLayout()
		self.comment = QTextEdit()
		self.comment.setHtml("""
			if total_dots → &infin; ,<br>
			&nbsp; <font color=red>π</font> / 4 = (total_true / total_dots)<br>
			<br>
			<font color=grey>developed by <font color=red>@ChiantiBlaze</font></font>
		""")
		self.comment.setFixedHeight(100)
		self.comment.setReadOnly(True)
		layout.addWidget(self.comment)
		box.setLayout(layout)

		return box



	def add_status_panel(self):
		box = QGroupBox('Status')
		self.status_formula = QLabel('(x-{a})²+(y-{b})²=({r})²'.format(a=0.0,b=0.0,r=1.0))
		self.status_total = QLabel("0")
		self.status_true = QLabel("0")
		self.status_false = QLabel("0")
		self.status_pi = QLabel("0.0000000000")
		self.status_pi_4 = QLabel("0.0000000000")
		layout = QGridLayout()
		layout.addWidget(QLabel('Equation Formula          '), 0,0) # whitespace on purpose
		layout.addWidget(self.status_formula, 0,1)
		layout.addWidget(QLabel("Total Dots"), 1,0)
		layout.addWidget(self.status_total, 1,1)
		layout.addWidget(QLabel("Total True"), 2,0)
		layout.addWidget(self.status_true, 2,1)
		layout.addWidget(QLabel("Total False"), 3,0)
		layout.addWidget(self.status_false, 3,1)
		layout.addWidget(QLabel("Estimated π / 4"), 4,0)
		layout.addWidget(self.status_pi_4, 4,1)
		layout.addWidget(QLabel("Estimated π"), 5,0)
		layout.addWidget(self.status_pi, 5,1)
		box.setLayout(layout)

		return box


	def add_settings_panel(self):
		box = QGroupBox("Settings")
		layout = QGridLayout()

		# Dots per Action RadioBox #
		dsr_box = QGroupBox("Dots per Action: ")
		dsr_layout = QGridLayout()
		self.dsr_p1 = QRadioButton("1"); dsr_layout.addWidget(self.dsr_p1, 0,0)
		self.dsr_p64 = QRadioButton("64"); dsr_layout.addWidget(self.dsr_p64, 0,1)
		self.dsr_p256 = QRadioButton("256"); dsr_layout.addWidget(self.dsr_p256, 0,2)
		self.dsr_p2048 = QRadioButton("2048"); dsr_layout.addWidget(self.dsr_p2048, 0,3)
		self.dsr_p1.setChecked(True)
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


	def add_confirm_btn(self):
		self.confirm_btn = QPushButton("Confirm Criteria")

		return self.confirm_btn


	def add_start_btn(self):
		self.start_btn = QPushButton("Start Simulation")
		self.start_btn.setEnabled(False)

		return self.start_btn


class MC_Pi(MC_Pi_Framework):
	def __init__(self):
		super().__init__()

		self.confirm_btn.clicked.connect(self.confirm_settings)
		self.criterion_x.textChanged.connect(self.disable_start_btn)
		self.criterion_x.textChanged.connect(self.disable_start_btn)
		self.criterion_y.textChanged.connect(self.disable_start_btn)
		self.criterion_scale.textChanged.connect(self.disable_start_btn)

		self.start_btn.clicked.connect(self.start_plotting)


	def reset_settings(self):
		self.criterion_x.setText('')
		self.criterion_y.setText('')
		self.criterion_scale.setText('')
		self.display.setPixmap(QPixmap())
		shot = QPixmap('./shots/default.png')
		shot = shot.scaled(self.display.size(), Qt.KeepAspectRatio, \
								transformMode = Qt.SmoothTransformation)
		self.display.setPixmap(shot)


	def disable_start_btn(self):
		self.confirm_btn.setEnabled(True)
		self.start_btn.setEnabled(False)
		self.start_btn.setText('Start Simulation')


	def confirm_settings(self):
		# check if a,b,r is valid #
		try:
			a = float(self.criterion_x.text())
			b = float(self.criterion_y.text())
			r = float(self.criterion_scale.text())
			self.criterion_x.setText(str(a))
			self.criterion_y.setText(str(b))
			self.criterion_scale.setText(str(r))
		except ValueError:
			self.reset_settings()
			return

		# modify formula
		self.status_formula.setText('(x-{a})²+(y-{b})²=({r})²'.format(a=a,b=b,r=r))

		# get preview shot and update the image #
		get_preview_shot(a,b,r)
		shot = QPixmap('./shots/preview.png')
		shot = shot.scaled(self.display.size(), Qt.KeepAspectRatio, \
									transformMode = Qt.SmoothTransformation)
		self.display.setPixmap(shot)

		# Allow Start button #
		self.confirm_btn.setEnabled(False)
		self.start_btn.setEnabled(True)
		

	def start_plotting(self):
		self.start_btn.setEnabled(False)

		a = float(self.criterion_x.text())
		b = float(self.criterion_y.text())
		r = float(self.criterion_scale.text())
		x_range = (a, a+r)
		y_range = (b, b+r)

		# get counter #
		cnt = 1
		if self.dsr_p64.isChecked(): cnt = 64
		elif self.dsr_p256.isChecked(): cnt = 256
		elif self.dsr_p2048.isChecked(): cnt = 2048



		while True:
			# plot based on random number #
			dot_true, dot_false = get_plot_shot(\
				uniform(*x_range,cnt), uniform(*y_range,cnt),a,b,r)
			
			shot = QPixmap('./shots/plot.png')
			shot = shot.scaled(self.display.size(), Qt.KeepAspectRatio, \
									transformMode = Qt.SmoothTransformation)
			self.display.setPixmap(shot)

			# update status #
			self.status_total.setText(str(int(self.status_total.text())+cnt))
			self.status_true.setText(str(int(self.status_true.text())+dot_true))
			self.status_false.setText(str(int(self.status_false.text())+dot_false))

			if int(self.status_false.text()) != 0:
				self.status_pi_4.setText(str("%.10f"%(int(self.status_true.text())/int(self.status_total.text()))))
				self.status_pi.setText(str("%.10f"%(4*int(self.status_true.text())/int(self.status_total.text()))))
			

			QCoreApplication.processEvents()