# 📐 STL to DXF Converter

[![Try It Online](https://img.shields.io/badge/Try%20It-Online-success?style=for-the-badge&logo=streamlit)](https://stl-to-dxf-converter.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)

A simple, open-source web application to convert 3D **STL** files into 2D **DXF** sketches.  
Ideal for generating laser cutting profiles, CNC paths, or floor plans from 3D models.

![App Screenshot](screenshot.png)

## ✨ Features
- **🎯 Precise Manual Slicing**: The standout feature! Use the interactive slider to pick the **exact height** of the cut. Perfect for models with multiple extrusions or levels.
- **👀 Interactive 3D Viewer**: Visualize your model in 3D (green) and see the exact **cut path (red)** update in real-time as you move the slider.
- **🔄 Multi-Axis Support**: Slice along the X, Y, or Z axis to capture the correct profile.
- **📂 Easy Workflow**: Drag and drop your `.stl` file and get an instant `.dxf` download.
- **📊 Instant Stats**: See vertex/face counts and bounding box dimensions immediately.
- **🌐 Cross-Platform**: Run it in your browser anywhere (Windows, Mac, Linux).

> [!NOTE] 
> This tool is best suited for **prismatic shapes** (extrusions). Because you can **manually select the slice height**, you can easily extract profiles from different levels of a stacked model (e.g., a base plate vs. a top detail) by downloading them as separate DXF files.

## 🚀 How to Run Locally

You can run this app on your own machine using Python.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/evanofficial/stl-to-dxf-converter.git
    cd stl-to-dxf-converter
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the app:**
    ```bash
    streamlit run app.py
    ```

The app will open automatically in your web browser at `http://localhost:8501`.

## 🛠️ Built With
- **[Streamlit](https://streamlit.io/)** - For the web interface.
- **[Trimesh](https://trimesh.org/)** - For loading and slicing 3D meshes.
- **[Plotly](https://plotly.com/python/)** - For interactive 3D visualization.
- **[Ezdxf](https://ezdxf.mozman.at/)** - For creating valid DXF files.
- **[NumPy](https://numpy.org/)** - For high-performance vector math.

## 📄 License
This project is open source and available under the [MIT License](LICENSE).
