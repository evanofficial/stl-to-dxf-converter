import streamlit as st
import trimesh
import numpy as np
import ezdxf
import os
import tempfile
import plotly.graph_objects as go

def convert_stl_to_dxf(mesh, axis_name, slice_val):
    # Map axis name to normal vector and index
    axis_map = {
        'Z': {'normal': [0, 0, 1], 'index': 2},
        'Y': {'normal': [0, 1, 0], 'index': 1},
        'X': {'normal': [1, 0, 0], 'index': 0}
    }
    
    config = axis_map[axis_name]
    normal = config['normal']
    
    # Define the plane origin based on the user's slice value
    plane_origin = list(mesh.centroid)
    plane_origin[config['index']] = slice_val
    
    slice_3d = mesh.section(plane_origin=plane_origin, plane_normal=normal)
    
    if slice_3d is None or len(slice_3d.entities) == 0:
        return None, None
    
    # Return both the 2D planar (for DXF) and the 3D slice (for plotting)
    slice_2d, to_3D = slice_3d.to_planar()
    
    return slice_2d, slice_3d

def get_plot_fig(mesh, slice_3d=None):
    # Create the 3D figure
    fig = go.Figure()
    
    # 1. Add the Mesh (Green, Transparent)
    # Trimesh vertices/faces are numpy arrays, easy to pass to Plotly
    fig.add_trace(go.Mesh3d(
        x=mesh.vertices[:,0],
        y=mesh.vertices[:,1],
        z=mesh.vertices[:,2],
        i=mesh.faces[:,0],
        j=mesh.faces[:,1],
        k=mesh.faces[:,2],
        color='lightgreen',
        opacity=0.3,
        name='Model'
    ))
    
    # 2. Add the Slice (Red Lines)
    if slice_3d is not None:
        # slice_3d.entities is a list of lines/arcs. 
        # For visualization, we can just extract the discrete path (polylines).
        # discrete returns a lists of (N, 3) vertices
        
        for entity in slice_3d.discrete:
            fig.add_trace(go.Scatter3d(
                x=entity[:,0],
                y=entity[:,1],
                z=entity[:,2],
                mode='lines',
                line=dict(color='red', width=5),
                name='Slice'
            ))

    fig.update_layout(
        scene=dict(
            aspectmode='data'
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        height=500
    )
    return fig

st.set_page_config(page_title="STL to DXF Converter", page_icon="📐", layout="wide")

st.title("📐 STL to DXF Converter")
st.write("Upload a 3D STL file and convert it to a 2D DXF sketch.")
st.info("💡 **Note:** This tool works best with models created by **uniform extrusion** (prismatic shapes). Irregular, organic, or tapered geometries may not produce a usable 2D profile.")

uploaded_file = st.file_uploader("Choose an STL file", type=['stl'])

if uploaded_file is not None:
    with st.spinner("Loading mesh..."):
        try:
            mesh = trimesh.load(uploaded_file, file_type='stl')
            
            # Layout: Left column for controls, Right column for 3D View
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.success(f"Loaded! V: {len(mesh.vertices)}, F: {len(mesh.faces)}")
                
                axis_option = st.selectbox(
                    "Select Extraction Axis",
                    ('Z', 'Y', 'X'),
                    index=0,
                    help="The axis along which the object was extruded."
                )
                
                # --- Slider Logic ---
                axis_indices = {'X': 0, 'Y': 1, 'Z': 2}
                ax_idx = axis_indices[axis_option]
                
                min_val = float(mesh.bounds[0][ax_idx])
                max_val = float(mesh.bounds[1][ax_idx])
                mid_val = (min_val + max_val) / 2.0
                
                st.markdown("### ✂️ Slice Position")
                slice_value = st.slider(
                    "Move slider to slice",
                    min_value=min_val,
                    max_value=max_val,
                    value=mid_val,
                    step=(max_val - min_val) / 100.0 if max_val != min_val else 0.1,
                    format="%.2f"
                )
                
                # Perform slice calculation for dynamic preview
                result_2d, result_3d = convert_stl_to_dxf(mesh, axis_option, slice_value)
                
                if st.button("Download DXF"):
                    if result_2d:
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.dxf') as tmp:
                            result_2d.export(tmp.name)
                            tmp.seek(0)
                            dxf_data = tmp.read()
                            
                            st.download_button(
                                label="📥 Click to Save DXF",
                                data=dxf_data,
                                file_name=f"{uploaded_file.name.replace('.stl', '')}_slice_{slice_value:.2f}.dxf",
                                mime="application/dxf"
                            )
                        try:
                            os.unlink(tmp.name)
                        except:
                            pass
                    else:
                        st.error("No valid slice found at this position.")

            with col2:
                st.subheader("3D Preview")
                # Generate and show the plot
                fig = get_plot_fig(mesh, result_3d)
                st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading STL: {e}")

st.markdown("---")
st.markdown("Built with Python, Trimesh, Plotly, and Streamlit.")
