import os

# Define the paths to the folders
folder_paths = ['./result/A/', './result/B/', './result/C/', './result/D/']

# Initialize empty lists to store image file paths for each folder
image_paths = [[] for _ in folder_paths]

# Define the list of supported image file extensions
supported_extensions = ['.jpg', '.jpeg', '.png']

# Iterate through each folder and list image files with supported extensions
for i, folder in enumerate(folder_paths):
    if os.path.exists(folder):
        image_files = [f for f in os.listdir(folder) if any(f.lower().endswith(ext) for ext in supported_extensions)]
        # Create full paths to the image files
        image_paths[i] = [os.path.join(folder, file) for file in image_files]
        print(image_paths[i])
    else:
        print(f"Folder '{folder}' does not exist.")

# Now image_paths contains lists of image file paths for each folder
# image_paths[0] contains image paths for folder A, image_paths[1] for folder B, and so on.
