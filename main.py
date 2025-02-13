import tkinter as tk
from tkinter import filedialog, messagebox
import os
import time
from PIL import Image
from PIL.ExifTags import TAGS

class FileMetadataViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Metadata Viewer")
        self.geometry("600x500")
        self.configure(bg="#f0f4f8")  # Light pastel background
        self.create_widgets()

    def create_widgets(self):
        # Title
        tk.Label(self, text="File Metadata Viewer", font=("Verdana", 24, "bold"), bg="#f0f4f8", fg="#2c3e50").pack(pady=20)
        
        # Select File Button
        tk.Button(self, text="Select File", command=self.select_file, font=("Verdana", 14), bg="#3498db", fg="white", width=15).pack(pady=10)
        
        # Export Metadata Button
        tk.Button(self, text="Export Metadata", command=self.export_metadata, font=("Verdana", 14), bg="#2ecc71", fg="white", width=15).pack(pady=10)
        
        # Metadata display area
        self.result_text = tk.Text(self, font=("Verdana", 12), height=15, width=70, state=tk.DISABLED, wrap=tk.WORD)
        self.result_text.pack(pady=10)
        
        self.current_metadata = ""  # Store metadata for export

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Select a File")
        if not file_path:
            return
        try:
            metadata = self.get_file_metadata(file_path)
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                image_metadata = self.get_image_metadata(file_path)
                metadata.update(image_metadata)
            self.display_metadata(metadata)
            self.current_metadata = metadata
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def get_file_metadata(self, file_path):
        file_stats = os.stat(file_path)
        metadata = {
            "File Name": os.path.basename(file_path),
            "File Size": f"{file_stats.st_size} bytes",
            "Creation Date": time.ctime(file_stats.st_ctime),
            "Modification Date": time.ctime(file_stats.st_mtime),
            "File Path": file_path
        }
        return metadata
    
    def get_image_metadata(self, file_path):
        image = Image.open(file_path)
        info = image._getexif()
        image_metadata = {}
        if info:
            for tag, value in info.items():
                tag_name = TAGS.get(tag, tag)
                image_metadata[tag_name] = value
        return image_metadata

    def display_metadata(self, metadata):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        for key, value in metadata.items():
            self.result_text.insert(tk.END, f"{key}: {value}\n")
        self.result_text.config(state=tk.DISABLED)
    
    def export_metadata(self):
        if not self.current_metadata:
            messagebox.showwarning("No Metadata", "No metadata to export. Please select a file first.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")], title="Save Metadata")
        if file_path:
            try:
                with open(file_path, "w") as file:
                    for key, value in self.current_metadata.items():
                        file.write(f"{key}: {value}\n")
                messagebox.showinfo("Success", f"Metadata exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving: {str(e)}")

if __name__ == "__main__":
    app = FileMetadataViewer()
    app.mainloop()
