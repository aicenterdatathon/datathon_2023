import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# Function to generate plots and display column information
def plotter(df_cluster, colvar, paleta):
    plt.figure(figsize=(10, 6))
    conteo = df_cluster[colvar].value_counts().sort_values(ascending=False)
    sns.countplot(x=colvar, data=df_cluster, order=conteo.index, palette=paleta)
    plt.title('Conteo de ' + colvar)
    plt.xlabel(colvar)
    plt.ylabel('Frecuencia')
    plt.xticks(rotation=90)

    # Save the plot to a BytesIO object
    img_data = BytesIO()
    plt.savefig(img_data, format='svg')
    img_data.seek(0)

    # Encode the SVG plot to base64
    encoded_img = base64.b64encode(img_data.read()).decode("utf-8")

    # Display the plot
    st.image(f"data:image/svg+xml;base64,{encoded_img}")

    # Display additional information about the column
    st.write(f"### Information about {colvar}")
    st.table(df_cluster[colvar].value_counts())

# Streamlit app
def main():
    st.title("Cluster Analysis App")

    # File upload
    uploaded_file = st.file_uploader("Upload CSV file already clusterized", type=["csv"])

    if uploaded_file is not None:
        # Read the CSV file
        df_cluster = pd.read_csv(uploaded_file)

        # Choose column for analysis
        colvar = st.selectbox("Select a column for analysis:", df_cluster.columns)

        # Select cluster number
        cluster_number = st.slider("Select Cluster Number (0 to 3):", 0, 3)

        # Determine color palette based on cluster number
        paleta_options = ["YlOrBr", "winter", "YlGn", "rocket"]
        paleta = paleta_options[cluster_number]

        # Filter data for the selected cluster
        cluster_data = df_cluster[df_cluster["cluster"] == cluster_number]

        # Generate and display plot with additional information
        plotter(cluster_data, colvar, paleta)

if __name__ == "__main__":
    main()
