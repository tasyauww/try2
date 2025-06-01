import numpy as np
import matplotlib.pyplot as plt

def show_image(image, title):
    """Menampilkan citra biner"""
    plt.figure(figsize=(6, 6))
    plt.imshow(image, cmap='gray')
    plt.title(title)
    plt.axis('off')  # Mematikan sumbu koordinat
    plt.show()

def dilation(image, structuring_element):
    """Operasi dilasi pada citra biner"""
    h, w = image.shape
    se_h, se_w = structuring_element.shape
    pad_h, pad_w = se_h // 2, se_w // 2
    
    # Padding citra asli
    padded_image = np.zeros((h + 2*pad_h, w + 2*pad_w))
    padded_image[pad_h:pad_h+h, pad_w:pad_w+w] = image
    
    result = np.zeros_like(image)
    
    # Proses dilasi
    for i in range(h):
        for j in range(w):
            window = padded_image[i:i+se_h, j:j+se_w]
            if np.any(window * structuring_element == 1):
                result[i, j] = 1
                
    return result

def erosion(image, structuring_element):
    """Operasi erosi pada citra biner"""
    h, w = image.shape
    se_h, se_w = structuring_element.shape
    pad_h, pad_w = se_h // 2, se_w // 2
    
    # Padding citra asli
    padded_image = np.zeros((h + 2*pad_h, w + 2*pad_w))
    padded_image[pad_h:pad_h+h, pad_w:pad_w+w] = image
    
    result = np.zeros_like(image)
    
    # Proses erosi
    for i in range(h):
        for j in range(w):
            window = padded_image[i:i+se_h, j:j+se_w]
            if np.all((window * structuring_element) == structuring_element):
                result[i, j] = 1
                
    return result

def closing(image, structuring_element):
    """Operasi closing: dilasi diikuti erosi"""
    dilated = dilation(image, structuring_element)
    return erosion(dilated, structuring_element)

def opening(image, structuring_element):
    """Operasi opening: erosi diikuti dilasi"""
    eroded = erosion(image, structuring_element)
    return dilation(eroded, structuring_element)

# Citra biner contoh dari gambar
binary_image = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

# Structuring element 3x3 (semua bernilai 1)
se = np.ones((3, 3), dtype=int)

# Menjalankan operasi morfologi
dilated_image = dilation(binary_image, se)
eroded_image = erosion(binary_image, se)
closed_image = closing(binary_image, se)
opened_image = opening(binary_image, se)

# Visualisasi hasil
plt.figure(figsize=(15, 10))

plt.subplot(2, 3, 1)
plt.imshow(binary_image, cmap='gray')
plt.title('Citra Asli')
plt.axis('off')

plt.subplot(2, 3, 2)
plt.imshow(dilated_image, cmap='gray')
plt.title('Dilasi')
plt.axis('off')

plt.subplot(2, 3, 3)
plt.imshow(eroded_image, cmap='gray')
plt.title('Erosi')
plt.axis('off')

plt.subplot(2, 3, 4)
plt.imshow(se, cmap='gray')
plt.title('Structuring Element')
plt.axis('off')

plt.subplot(2, 3, 5)
plt.imshow(closed_image, cmap='gray')
plt.title('Closing')
plt.axis('off')

plt.subplot(2, 3, 6)
plt.imshow(opened_image, cmap='gray')
plt.title('Opening')
plt.axis('off')

plt.tight_layout()
plt.subplots_adjust(wspace=0.3, hspace=0.3)  # Menambah jarak antar subplot
plt.show()

# Jika ingin menampilkan satu per satu dengan jarak
def plot_images_separately():
    show_image(binary_image, 'Citra Asli')
    show_image(dilated_image, 'Hasil Dilasi')
    show_image(eroded_image, 'Hasil Erosi')
    show_image(se, 'Structuring Element')
    show_image(closed_image, 'Hasil Closing')
    show_image(opened_image, 'Hasil Opening')

# Untuk menjalankan secara terpisah dan melihat nilai piksel
print("Citra Asli:")
print(binary_image)
print("\nHasil Dilasi:")
print(dilated_image)
print("\nHasil Erosi:")
print(eroded_image)
print("\nHasil Closing:")
print(closed_image)
print("\nHasil Opening:")
print(opened_image)