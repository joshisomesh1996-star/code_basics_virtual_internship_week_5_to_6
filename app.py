import streamlit as st
from model_helper import predict

# 🌟 Page Configuration
st.set_page_config(
    page_title="Harvest Classification",
    page_icon="🌿",
    layout="centered",
)

# 🌈 Custom CSS for modern styling
st.markdown(
    """
    <style>
    body {
        background-color: #f8fff9;
        font-family: 'Poppins', sans-serif;
    }
    .title {
        font-size: 3rem;
        font-weight: 800;
        color: #2E8B57;
        text-align: center;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
    }
    .upload-area {
        border: 3px dashed #2E8B57;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        background-color: #F5FFF8;
        transition: all 0.3s ease;
    }
    .upload-area:hover {
        border-color: #1E6F4A;
        background-color: #E8FBEF;
    }
    .prediction-box {
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 2rem;
        font-size: 1.5rem;
        font-weight: 700;
        text-align: center;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.12);
        transition: all 0.4s ease;
    }
    .fresh {
        background-color: #E9F7EF;
        border-left: 6px solid #28A745;
        color: #155724;
    }
    .spoiled {
        background-color: #FDEDEC;
        border-left: 6px solid #C82333;
        color: #721C24;
    }
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# 🌾 Title
st.markdown('<div class="title">Harvest Classification 🌾</div>', unsafe_allow_html=True)
st.write("Upload an image of a fruit (front or side view) to determine whether it is **Fresh** 🍏 or **Spoiled** 🍎 using a trained ResNet model.")

# 📤 File Uploader
uploaded_file = st.file_uploader(
    label="Drag and drop or click to upload a fruit image",
    type=["jpg", "png", "jpeg"],
    help="Accepted formats: JPG, PNG, JPEG",
)

# 🖼️ Display uploaded image and show prediction
if uploaded_file:
    # Save temporary file
    image_path = "temp_image.jpg"
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Display image
    st.image(uploaded_file, caption="📸 Uploaded Image", use_container_width=True)

    # Run prediction
    with st.spinner("🔍 Classifying... Please wait."):
        prediction = predict(image_path)

    # 🌿 Determine freshness and style dynamically
    if "(Fresh)" in prediction:
        box_class = "fresh"
        emoji = "🍃"
    else:
        box_class = "spoiled"
        emoji = "🍂"

    # 🧠 Display Prediction Box
    st.markdown(
        f'<div class="prediction-box {box_class}">{emoji} Predicted Class: <strong>{prediction}</strong></div>',
        unsafe_allow_html=True,
    )

# 💡 Footer
st.markdown(
    "<br><center><sub>Developed with ❤️ using Streamlit & PyTorch</sub></center>",
    unsafe_allow_html=True,
)
