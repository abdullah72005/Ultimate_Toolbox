import base64
import os
from PIL import Image, ImageFilter

# Dictionary containing filter options and their corresponding Pillow filter objects
filters_dic = {
    "Blur": ImageFilter.GaussianBlur,  # Gaussian blur filter
    "Contour": ImageFilter.CONTOUR,  # Contour filter
    "Detail": ImageFilter.DETAIL,  # Detail enhancement filter
    "Enhance": ImageFilter.EDGE_ENHANCE,  # Edge enhancement filter
    "Emboss": ImageFilter.EMBOSS,  # Emboss filter
    "Edge": ImageFilter.FIND_EDGES,  # Edge detection filter
    "Sharpen": ImageFilter.SHARPEN,  # Sharpen filter
    "Smooth": ImageFilter.SMOOTH,  # Smooth filter
    # "Very smooth": ImageFilter.SMOOTH_MORE  # Very smooth filter
}

# Function to apply filter to image
def filterImg(imgPath, filter_name, fileName):
    # Open the original image
    originalImg = Image.open(imgPath)
    
    # Convert the image to RGB mode if it's already cropped
    originalImg = originalImg.convert("RGB")

    filteredImg = originalImg.filter(filters_dic[filter_name])

    # Save the filtered image to a file
    output_path = f"static/uploads/New{fileName}"
    filteredImg.save(output_path)
    
    return output_path

# Function to crop image
def cropImg(croppedImg ,fileName):

    # Decode the base64 cropped image data
    try:
        cropped_image_bytes = base64.b64decode(croppedImg.split(',')[1])

    except Exception as e:
        print("Error decoding base64 image data:", e)
        return
    
    # Save the cropped image to a file
    croppedImgName = "New" + fileName
    print(croppedImgName)
    cropped_image_path = os.path.join('static/uploads', croppedImgName)

    try:
        with open(cropped_image_path, 'wb') as file:
            file.write(cropped_image_bytes)

    except Exception as e:
        print("Error writing image data to file:", e)
        return
    
    # Return cropped img path and name
    return cropped_image_path, croppedImgName