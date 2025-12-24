import streamlit as st
import trimesh
import numpy as np
import ezdxf
import os
import tempfile

def convert_stl_to_dxf(mesh, axis_name):
    # Map axis name to normal vector
    axis_map = {
        'Z': [0, 0, 1],
        'Y': [0, 1, 0],
        'X': [1, 0, 0]
    }
    normal = axis_map[axis_name]
    
    # 1. Project/Section
    # We slice at the centroid
    plane_origin = mesh.centroid
    
    slice_3d = mesh.section(plane_origin=plane_origin, plane_normal=normal)
    
    if slice_3d is None or len(slice_3d.entities) == 0:
        return None
        
    # 2. Convert to planar
    # to_planar returns (Path2D, transformation_matrix)
    slice_2d, to_3D = slice_3d.to_planar()
    
    return slice_2d

st.set_page_config(page_title="STL to DXF Converter", page_icon="📐")

st.title("📐 STL to DXF Converter")
st.write("Upload a 3D STL file and convert it to a 2D DXF sketch.")
st.info("💡 **Note:** This tool works best with models created by **uniform extrusion** (prismatic shapes). Irregular, organic, or tapered geometries may not produce a usable 2D profile.")

uploaded_file = st.file_uploader("Choose an STL file", type=['stl'])

if uploaded_file is not None:
    # Save the uploaded file to a temporary file because trimesh loads from path best
    # or we can load from file object with fileType hint
    
    with st.spinner("Loading mesh..."):
        try:
             # Trimesh can load from a file-like object
            mesh = trimesh.load(uploaded_file, file_type='stl')
            
            st.success(f"Loaded mesh! Vertices: {len(mesh.vertices)}, Faces: {len(mesh.faces)}")
            
            # Show bounds
            st.code(f"Bounds:\n{mesh.bounds}")
            
            # Options
            axis_option = st.selectbox(
                "Select Extraction Axis",
                ('Z', 'Y', 'X'),
                index=0,
                help="The axis along which the object was extruded. The slice will be perpendicular to this axis."
            )
            
            if st.button("Convert to DXF"):
                with st.spinner("Processing..."):
                    result_2d = convert_stl_to_dxf(mesh, axis_option)
                    
                    if result_2d:
                        st.balloons()
                        st.success("Conversion successful!")
                        
                        # Save to a temp file to read it back as bytes for the downloader
                        # ezdxf/trimesh export might return a string or bytes, let's allow trimesh to write to temp
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.dxf') as tmp:
                            result_2d.export(tmp.name)
                            tmp.seek(0)
                            dxf_data = tmp.read()
                            
                            st.download_button(
                                label="📥 Download DXF",
                                data=dxf_data,
                                file_name=f"{uploaded_file.name.replace('.stl', '')}.dxf",
                                mime="application/dxf"
                            )
                            
                        # Cleanup temp file
                        try:
                            os.unlink(tmp.name)
                        except:
                            pass
                            
                    else:
                        st.error("Could not find a valid slice for this axis. try a different axis.")
            
        except Exception as e:
            st.error(f"Error loading STL: {e}")

st.markdown("---")
st.markdown("Built with Python, Trimesh, and Streamlit.")
