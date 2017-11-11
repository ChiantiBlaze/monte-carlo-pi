def main():
	import sys
	from monte_carlo_pi import MC_Pi
	from PyQt5.QtWidgets import QApplication

	app = QApplication(sys.argv)
	mc_pi = MC_Pi()
	sys.exit(app.exec_())


if __name__ == "__main__":
	main()