import streamlit as st
import cv2
import numpy as np
from PIL import Image

def simulate_color_blindness(image, blindness_type="protanopia"):
    img = np.array(image.convert("RGB"))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    if blindness_type == "protanopia":
        matrix = np.array([
            [0.567, 0.433, 0],
            [0.558, 0.442, 0],
            [0, 0.242, 0.758]
        ])
    elif blindness_type == "deuteranopia":
        matrix = np.array([
            [0.625, 0.375, 0],
            [0.700, 0.300, 0],
            [0, 0.300, 0.700]
        ])
    elif blindness_type == "tritanopia":
        matrix = np.array([
            [0.950, 0.050, 0],
            [0, 0.433, 0.567],
            [0, 0.475, 0.525]
        ])
    else:
        return image
    
    transformed = cv2.transform(img, matrix)
    transformed = np.clip(transformed, 0, 255).astype(np.uint8)
    transformed = cv2.cvtColor(transformed, cv2.COLOR_BGR2RGB)
    return Image.fromarray(transformed)

st.set_page_config(page_title="色盲模拟器", layout="wide")
st.title("🎨 色盲模拟工具")
st.write("上传一张图片，看看色盲患者眼中的世界是什么样的")

blindness_type = st.selectbox(
    "选择色盲类型",
    ["protanopia (红色盲)", "deuteranopia (绿色盲)", "tritanopia (蓝黄色盲)"]
).split(" ")[0]

uploaded_file = st.file_uploader("上传图片", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("原图")
        st.image(image, use_column_width=True)
    
    with st.spinner("正在生成模拟效果..."):
        simulated_image = simulate_color_blindness(image, blindness_type)
    
    with col2:
        st.subheader("色盲患者视角")
        st.image(simulated_image, use_column_width=True)
