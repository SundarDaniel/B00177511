import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img = mpimg.imread('bean_counter.png')
imgplot = plt.imshow(img)
plt.show()

# This effectively loads and renders the image in a plot window using matplotlib.