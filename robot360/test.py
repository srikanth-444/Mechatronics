import cv2
from matplotlib import pyplot as plt

image_path = r"C:\Users\popur\Downloads\pred_depth_0.png"
image_path2 = r"C:\Users\popur\Downloads\pred_depth_0 (1).png"
# Step 2: Read the image with OpenCV and apply grayscale colormap
image1 = cv2.imread(image_path)
gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
image2 = cv2.imread(image_path2)
gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
# Display the image in grayscale
fig,ax=plt.subplots(1,2)
ax[0].imshow(gray_image1, cmap='gray')
ax[0].axis('off')  # Hide axes for better display
ax[1].imshow(gray_image2, cmap='gray')
ax[1].axis('off')  # Hide axes for better display
plt.show()