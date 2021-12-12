import streamlit as st
import io
import requests
from PIL import Image
from PIL import ImageDraw

st.title('顔認識アプリ')

SUBSCRIPTION_KEY = st.secrets['SUBSCRIPTION_KEY']
API_URL = st.secrets['API_URL']

uploaded_file = st.file_uploader("Choose an image...", type='jpg')
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_image = output.getvalue()

    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
    }
    params = {
        'returnFaceId': 'true',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }

    response = requests.post(API_URL, params=params, headers=headers, data=binary_image)
    results = response.json()

    for result in results:
        rect = result['faceRectangle']
        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect['left'], rect['top']), (rect['left']+rect['width'], rect['top']+rect['height'])], fill=None, outline='green', width=10)
        text = f"gender:{result['faceAttributes']['gender']}, age:{result['faceAttributes']['age']}"
        st.write(text)
    st.image(img, caption='Uploaded Image.', use_column_width=True)
    st.write(results)
