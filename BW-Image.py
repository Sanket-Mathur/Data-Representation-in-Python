import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

img = Image.open('data/img.jpg')

imgmatrix = np.array(img)

imggray = imgmatrix.mean(axis=2)

plt.figure()

fig1 = plt.subplot(1,2,1)
fig1.imshow(imgmatrix)

fig1.set_title('Original')
fig1.axis('off')

fig2 = plt.subplot(1,2,2)
fig2.imshow(imggray, cmap='gray')
fig2.text(50, 3200, 'Sanket-Mathur')

fig2.set_title('Converted')
fig2.axis('off')

plt.show()
