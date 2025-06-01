import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import os
import sys
import traceback

# Check for required modules
def check_imports():
    missing_modules = []
    required_modules = ["PIL", "cv2", "matplotlib"]
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        error_msg = "Missing required libraries: " + ", ".join(missing_modules)
        error_msg += "\n\nPlease install them using pip:"
        for module in missing_modules:
            if module == "PIL":
                error_msg += "\npip install Pillow"
            elif module == "cv2":
                error_msg += "\npip install opencv-python"
            else:
                error_msg += f"\npip install {module}"
        return error_msg
    return None

missing_modules_error = check_imports()
if missing_modules_error:
    print(missing_modules_error)
    input("\nPress Enter to exit...")
    sys.exit(1)

try:
    from PIL import Image, ImageTk
    import cv2
    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except Exception as e:
    print(f"Error importing modules: {str(e)}")
    traceback.print_exc()
    input("\nPress Enter to exit...")
    sys.exit(1)

class FingerprintProcessor:
    def __init__(self, root):
        try:
            self.root = root
            self.root.title("Fingerprint Identification using Morphological Operations")
            self.root.geometry("1200x700")
            self.root.configure(bg="#f0f0f0")
            self.root.option_add('*Font', 'Arial 10')
            self.root.report_callback_exception = self.report_callback_exception
            
            self.original_image = None
            self.current_image = None
            self.processed_image = None
            self.kernel_size = tk.IntVar(value=3)
            
            self.create_frames()
            self.create_widgets()
            self.load_sample_image()
        except Exception as e:
            print(f"Initialization error: {str(e)}")
            traceback.print_exc()
            messagebox.showerror("Initialization Error", f"Error initializing application: {str(e)}")

    def report_callback_exception(self, exc_type, exc_value, exc_traceback):
        error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        print(f"Uncaught exception: {error_msg}")
        messagebox.showerror("Error", f"An unexpected error occurred:\n{str(exc_value)}")

    def create_frames(self):
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.control_frame = tk.LabelFrame(self.main_frame, text="Control Panel", bg="#f0f0f0", font=("Arial", 12, "bold"), padx=10, pady=10)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.display_frame = tk.LabelFrame(self.main_frame, text="Image Display", bg="#f0f0f0", font=("Arial", 12, "bold"), padx=10, pady=10)
        self.display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_widgets(self):
        tk.Label(self.control_frame, text="Fingerprint Processing", font=("Arial", 14, "bold"), bg="#f0f0f0", fg="#333333").pack(pady=10)

        file_frame = tk.Frame(self.control_frame, bg="#f0f0f0")
        file_frame.pack(fill=tk.X, pady=10)

        center_frame = tk.Frame(file_frame, bg="#f0f0f0")
        center_frame.pack(pady=5)

        tk.Button(center_frame, text="Load Image", command=self.load_image, bg="#4CAF50", fg="white", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(center_frame, text="Reset Image", command=self.reset_image, bg="#f44336", fg="white", width=15).pack(side=tk.LEFT, padx=5)

        kernel_frame = tk.Frame(self.control_frame, bg="#f0f0f0")
        kernel_frame.pack(fill=tk.X, pady=10)
        tk.Label(kernel_frame, text="Kernel Size:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        for size in [3, 5, 7, 9, 11]:
            tk.Radiobutton(kernel_frame, text=str(size), variable=self.kernel_size, value=size, bg="#f0f0f0").pack(side=tk.LEFT)

        tk.Label(self.control_frame, text="Morphological Operations", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=10)
        operations_frame = tk.Frame(self.control_frame, bg="#f0f0f0")
        operations_frame.pack(fill=tk.X, pady=5)

        button_config = {'width': 15, 'pady': 5, 'font': ('Arial', 10), 'relief': tk.RAISED}

        tk.Button(operations_frame, text="Dilation", command=lambda: self.apply_operation('dilation'), bg="#2196F3", fg="white", **button_config).pack(fill=tk.X, pady=5)
        tk.Button(operations_frame, text="Erosion", command=lambda: self.apply_operation('erosion'), bg="#FF9800", fg="white", **button_config).pack(fill=tk.X, pady=5)
        tk.Button(operations_frame, text="Opening", command=lambda: self.apply_operation('opening'), bg="#9C27B0", fg="white", **button_config).pack(fill=tk.X, pady=5)
        tk.Button(operations_frame, text="Closing", command=lambda: self.apply_operation('closing'), bg="#009688", fg="white", **button_config).pack(fill=tk.X, pady=5)
        tk.Button(operations_frame, text="Show All Operations", command=self.show_all_operations, bg="#795548", fg="white", **button_config).pack(fill=tk.X, pady=5)

        info_frame = tk.LabelFrame(self.control_frame, text="Information", bg="#f0f0f0", font=("Arial", 12, "bold"))
        info_frame.pack(fill=tk.X, pady=10, padx=5)

        info_text = """
Morphological Operations:

Dilation: Expands the image, thickens ridges
Erosion: Shrinks the image, thins ridges
Opening: Erosion then Dilation
Closing: Dilation then Erosion
        """
        tk.Label(info_frame, text=info_text, justify=tk.LEFT, bg="#f0f0f0", fg="#333333", pady=5).pack(fill=tk.X)

        credits_frame = tk.Frame(self.control_frame, bg="#f0f0f0")
        credits_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)

        tk.Label(credits_frame, text="Based on paper: Fingerprint Identification using Morphological Operations", bg="#f0f0f0", fg="#666666", font=("Arial", 8), wraplength=250).pack()

        try:
            self.fig, self.axes = plt.subplots(1, 2, figsize=(12, 6))
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.display_frame)
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            self.axes[0].set_title("Original Image")
            self.axes[1].set_title("Processed Image")
            self.axes[0].axis('off')
            self.axes[1].axis('off')
        except Exception:
            self.fallback_canvas()

    def fallback_canvas(self):
        self.canvas_frame = tk.Frame(self.display_frame, bg="black")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.left_frame = tk.Frame(self.canvas_frame, bg="black")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_frame = tk.Frame(self.canvas_frame, bg="black")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(self.left_frame, text="Original Image", bg="black", fg="white").pack()
        self.left_label = tk.Label(self.left_frame, bg="black")
        self.left_label.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.right_frame, text="Processed Image", bg="black", fg="white").pack()
        self.right_label = tk.Label(self.right_frame, bg="black")
        self.right_label.pack(fill=tk.BOTH, expand=True)

        self.use_fallback = True

    def load_sample_image(self):
        try:
            img = np.zeros((200, 200), dtype=np.uint8)
            for i in range(50, 150, 10):
                cv2.line(img, (i, 50), (i+30, 150), 255, 3)
            img = cv2.GaussianBlur(img, (5, 5), 0)
            _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

            self.original_image = img
            self.current_image = img.copy()
            self.display_image(self.current_image, "Sample Fingerprint")
        except:
            self.original_image = np.zeros((200, 200), dtype=np.uint8)
            self.current_image = self.original_image.copy()
            self.display_image(self.current_image, "Empty Image")

    def load_image(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff")])
            if file_path:
                img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    raise Exception("Image cannot be read")
                _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
                self.original_image = img
                self.current_image = img.copy()
                self.display_image(self.current_image, f"Original: {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def reset_image(self):
        if self.original_image is not None:
            self.current_image = self.original_image.copy()
            self.display_image(self.current_image, "Original Image")
        else:
            messagebox.showinfo("Info", "No image loaded yet")

    def apply_operation(self, operation):
        if self.current_image is None:
            messagebox.showinfo("Info", "Please load an image first")
            return

        kernel = np.ones((self.kernel_size.get(), self.kernel_size.get()), np.uint8)
        if operation == 'dilation':
            result = cv2.dilate(self.current_image, kernel, iterations=1)
            title = "Dilation"
        elif operation == 'erosion':
            result = cv2.erode(self.current_image, kernel, iterations=1)
            title = "Erosion"
        elif operation == 'opening':
            result = cv2.morphologyEx(self.current_image, cv2.MORPH_OPEN, kernel)
            title = "Opening"
        elif operation == 'closing':
            result = cv2.morphologyEx(self.current_image, cv2.MORPH_CLOSE, kernel)
            title = "Closing"
        else:
            return
        self.processed_image = result
        self.display_side_by_side(self.original_image, result, title)

    def display_side_by_side(self, original, processed, title="Processed"):
        if hasattr(self, 'use_fallback') and self.use_fallback:
            original_tk = ImageTk.PhotoImage(Image.fromarray(original))
            self.left_label.configure(image=original_tk)
            self.left_label.image = original_tk

            processed_tk = ImageTk.PhotoImage(Image.fromarray(processed))
            self.right_label.configure(image=processed_tk)
            self.right_label.image = processed_tk
            return

        self.axes[0].clear()
        self.axes[1].clear()
        self.axes[0].imshow(original, cmap='gray')
        self.axes[1].imshow(processed, cmap='gray')
        self.axes[0].set_title("Original Image")
        self.axes[1].set_title(title)
        self.axes[0].axis('off')
        self.axes[1].axis('off')
        self.fig.tight_layout()
        self.canvas.draw()

    def display_image(self, image, title="Image"):
        self.display_side_by_side(image, image, title)

    def show_all_operations(self):
        if self.current_image is None:
            messagebox.showinfo("Info", "Load image first")
            return
        kernel = np.ones((self.kernel_size.get(), self.kernel_size.get()), np.uint8)
        dilation = cv2.dilate(self.current_image, kernel, iterations=1)
        erosion = cv2.erode(self.current_image, kernel, iterations=1)
        opening = cv2.morphologyEx(self.current_image, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(self.current_image, cv2.MORPH_CLOSE, kernel)

        fig, axes = plt.subplots(1, 4, figsize=(16, 4))
        titles = ['Dilation', 'Erosion', 'Opening', 'Closing']
        images = [dilation, erosion, opening, closing]
        for ax, img, title in zip(axes, images, titles):
            ax.imshow(img, cmap='gray')
            ax.set_title(title)
            ax.axis('off')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = FingerprintProcessor(root)
    root.mainloop()