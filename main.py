import streamlit as st
from rembg import remove
from PIL import Image
import io
import easyocr
import tempfile

def main():
    st.title("Background Removal and Text Extraction App")

    image_file = st.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png'])

    if image_file is not None:
        image = Image.open(image_file)
        st.image(image, caption='Original Image', use_column_width=True)

        if st.button("Remove Background and Extract Text"):
            with st.spinner("Processing..."):
                # Remove background
                result_image = remove(image)
                result_image_rgb = result_image.convert("RGB")

                # Save the background-removed image to a temporary file
                with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
                    result_image_rgb.save(tmp_file, format="JPEG")
                    tmp_file_path = tmp_file.name

                # Extract Text from the image
                reader = easyocr.Reader(['en'])
                result = reader.readtext(tmp_file_path)

                st.header("Extracted Text:")
                for detection in result:
                    st.write(detection[1])  # Display the detected text

                # Display the background-removed image
                st.image(result_image_rgb, caption='Background Removed', use_column_width=True)

                # Create a download button for the background-removed image
                st.download_button(
                    label="Download Background Removed Image",
                    data=tmp_file_path,
                    file_name="out.jpg"
                )


if __name__ == "__main__":
    main()
