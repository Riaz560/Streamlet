import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import StrMethodFormatter

# Set page config
st.set_page_config(page_title="Beautiful Graph", layout="wide")

# Title and description
st.title("📊 Beautiful Graph in Streamlit")
st.markdown("""
This app demonstrates how to create beautiful, interactive graphs in Streamlit using Matplotlib and Seaborn.
Customize the graph using the options in the sidebar!
""")

# Sidebar controls
with st.sidebar:
    st.header("Graph Controls")
    graph_type = st.selectbox(
        "Graph Type",
        ["Line Plot", "Scatter Plot", "Bar Chart", "Area Chart"],
        index=0
    )
    
    color_palette = st.selectbox(
        "Color Palette",
        ["deep", "muted", "bright", "pastel", "dark", "colorblind"],
        index=0
    )
    
    show_grid = st.checkbox("Show Grid", value=True)
    show_legend = st.checkbox("Show Legend", value=True)
    show_annotations = st.checkbox("Show Annotations", value=True)
    
    num_points = st.slider("Number of Points", 10, 500, 100)
    noise_level = st.slider("Noise Level", 0.0, 1.0, 0.1)

# Generate sample data based on user input
x = np.linspace(0, 10, num_points)
y1 = np.sin(x) + np.random.normal(0, noise_level, num_points)
y2 = np.cos(x) + np.random.normal(0, noise_level, num_points)
categories = np.random.choice(['A', 'B', 'C'], size=num_points)

# Set style
sns.set_style("whitegrid" if show_grid else "white")
sns.set_palette(color_palette)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))

# Plot based on selected type
if graph_type == "Line Plot":
    ax.plot(x, y1, label='Sine Wave', linewidth=2.5, marker='o', markevery=5, markersize=6)
    ax.plot(x, y2, label='Cosine Wave', linewidth=2.5, linestyle='--')
elif graph_type == "Scatter Plot":
    scatter = ax.scatter(x, y1, c=y2, cmap='viridis', s=100, alpha=0.7, label='Data Points')
    if show_annotations:
        ax.annotate('Peak Value', xy=(x[np.argmax(y1)], np.max(y1)), 
                    xytext=(x[np.argmax(y1)]+1, np.max(y1)+0.5),
                    arrowprops=dict(facecolor='black', shrink=0.05))
elif graph_type == "Bar Chart":
    ax.bar(x[::10], y1[::10], width=0.5, alpha=0.7, label='Sine Values')
    ax.bar(x[::10]+0.5, y2[::10], width=0.5, alpha=0.7, label='Cosine Values')
elif graph_type == "Area Chart":
    ax.fill_between(x, y1, alpha=0.4, label='Sine Wave')
    ax.fill_between(x, y2, alpha=0.4, label='Cosine Wave')

# Customize plot
ax.set_title(f'Beautiful {graph_type}', pad=20)
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.grid(show_grid, linestyle='--', alpha=0.6)
ax.set_axisbelow(True)
ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.1f}'))

if show_legend:
    ax.legend(loc='upper right', framealpha=1)

# Add colorbar for scatter plot if needed
if graph_type == "Scatter Plot" and 'scatter' in locals():
    cbar = plt.colorbar(scatter)
    cbar.set_label('Cosine Values')

# Display in Streamlit
st.pyplot(fig)

# Show data summary
with st.expander("Show Data Summary"):
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Max Sine Value", f"{np.max(y1):.2f}")
        st.metric("Min Sine Value", f"{np.min(y1):.2f}")
    with col2:
        st.metric("Max Cosine Value", f"{np.max(y2):.2f}")
        st.metric("Min Cosine Value", f"{np.min(y2):.2f}")

    st.write("Sample Data Points:")
    st.dataframe({
        "X Values": x[:5],
        "Sine Values": y1[:5],
        "Cosine Values": y2[:5]
    })

# Add some tips
st.markdown("""
### Tips for Beautiful Streamlit Graphs:
1. Use consistent color palettes
2. Add proper labels and titles
3. Include interactive controls
4. Show data summaries
5. Use appropriate chart types for your data
""")
