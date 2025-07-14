import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="📸 Perfect Photo Capture", layout="centered")
st.title("📸 Perfect Frame Photo Capture Using JavaScript")

html_code = """
<!DOCTYPE html>
<html>
<head>
  <style>
    video, canvas {
      width: 480px;
      height: 360px;
      border: 2px solid #00bfff;
      border-radius: 8px;
      margin: 10px 0;
    }
    button {
      background-color: #00bfff;
      color: white;
      padding: 10px 20px;
      border: none;
      border-radius: 5px;
      font-size: 16px;
      margin-top: 10px;
      cursor: pointer;
    }
  </style>
</head>
<body>

<video id="video" autoplay playsinline></video><br>
<button onclick="takePhoto()">📸 Capture</button><br>
<canvas id="canvas"></canvas>

<script>
  const video = document.getElementById('video');
  const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d');

  // Set fixed dimensions
  const width = 480;
  const height = 360;
  video.width = width;
  video.height = height;
  canvas.width = width;
  canvas.height = height;

  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
      video.srcObject = stream;
    });

  function takePhoto() {
    ctx.drawImage(video, 0, 0, width, height);
  }
</script>

</body>
</html>
"""

components.html(html_code, height=650)
