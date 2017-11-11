import tkinter
import numpy as np
import matplotlib.pyplot as plt

DPI = 10

def get_preview_shot(a,b,r):
	# Clear previous data #
	plt.gcf().clear()
	
	# Basic Grid Settings #
	plt.gca().set_xlim(a,a+r)
	plt.gca().set_ylim(b,b+r)
	plt.gca().set_autoscale_on(False)
	plt.gcf().set_size_inches(72.0/float(DPI),72.0/float(DPI))

	plt.gca().set_xticks(np.arange(a,a+r, r/10))
	plt.gca().set_yticks(np.arange(b,b+r, r/10))
	plt.grid(linestyle='dotted')

	# Plot boundary #
	boundary = plt.Circle((a,b), radius=r, color='red', alpha=0.2)
	plt.gca().add_artist(boundary)

	plt.savefig('shots/preview.png')


def get_plot_shot(x,y):
	plt.plot(x,y, "v")
	plt.savefig('shots/plot.png')
	return (x,y)

