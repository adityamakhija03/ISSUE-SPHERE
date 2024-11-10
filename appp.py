import streamlit as st
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
import pandas as pd
import toml

# Configure page
st.set_page_config(
    page_title="Issue Sphere - Cluster Finder",
    page_icon="🔍"
)

# Load configuration
@st.cache_resource
def load_config():
    try:
        return toml.load("config.toml")
    except Exception as e:
        st.error(f"Failed to load configuration: {str(e)}")
        return None

# Initialize the embedding model and Google Gemini API
@st.cache_resource
def initialize_models(config):
    try:
        model = SentenceTransformer(config["model"]["sentence_transformer"], trust_remote_code=True)
        genai.configure(api_key=config["api"]["google_api_key"])
        return model, genai.GenerativeModel(config["model"]["gemini_model"])
    except Exception as e:
        st.error(f"Failed to initialize models: {str(e)}")
        return None, None

# MongoDB connection with error handling
@st.cache_resource
def initialize_mongodb(config):
    try:
        client = MongoClient(config["mongodb"]["uri"], serverSelectionTimeoutMS=5000)
        client.server_info()  # Verify connection
        db = client[config["mongodb"]["database"]]
        return db
    except Exception as e:
        st.error(f"Failed to connect to MongoDB: {str(e)}")
        return None

# Function to generate embeddings
def get_embedding(model, data):
    try:
        return model.encode(data).tolist()
    except Exception as e:
        st.error(f"Failed to generate embedding: {str(e)}")
        return None

# Load and cache CSV data
@st.cache_data
def load_csv_data(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Failed to load CSV file: {str(e)}")
        return None

def main():
    # Load configuration
    config = load_config()
    if config is None:
        st.error("Cannot proceed without configuration. Please check config.toml file.")
        return

    # Page Header
    try:
        st.image(config["app"]["image_path"], width=config["app"]["image_width"])
    except:
        st.warning("Logo image not found. Please check the image path.")

    st.title(config["app"]["title"])

    # Initialize models and MongoDB
    model, gemini_model = initialize_models(config)
    db = initialize_mongodb(config)

    # Check if all components were initialized successfully
    if model is None or gemini_model is None or db is None:
        st.error("Failed to initialize required components. Please check the error messages above.")
        return

    collection_clusters = db[config["mongodb"]["clusters_collection"]]
    collection_claims = db[config["mongodb"]["claims_collection"]]

    # Cluster Search Section
    st.subheader("Search Clusters")
    prompt = st.text_input("Enter a diagnostic issue to find relevant clusters:")

    if st.button("Find Clusters"):
        if prompt:
            # Generate embedding and search
            query_embedding = get_embedding(model, prompt)
            if query_embedding:
                try:
                    # Vector search pipeline
                    pipeline = [
                        {
                            "$vectorSearch": {
                                "index": "vector_index",
                                "queryVector": query_embedding,
                                "path": "embedding",
                                "exact": True,
                                "limit": 3
                            }
                        },
                        {
                            "$project": {
                                "_id": 0,
                                "Cluster #": 1,
                                "Cluster Name": 1,
                                "Description": 1,
                                "score": {
                                    "$meta": "vectorSearchScore"
                                }
                            }
                        }
                    ]

                    results = list(collection_clusters.aggregate(pipeline))

                    if not results:
                        st.warning("No matching clusters found.")
                        return

                    # Display results
                    top_clusters = []
                    with st.expander("Cluster Results", expanded=True):
                        for i, cluster in enumerate(results):
                            cluster_info = (f"Cluster #{cluster['Cluster #']}: "
                                            f"{cluster['Cluster Name']}\n"
                                            f"Description: {cluster['Description']}\n"
                                            f"Score: {cluster['score']:.4f}\n")
                            st.markdown(f"**Cluster {i + 1}:**\n{cluster_info}")
                            top_clusters.append(cluster_info)

                    # Generate AI recommendation
                    if len(top_clusters) == 3:
                        gemini_prompt = f"""
                        You are an expert vehicle diagnostics assistant. Based on the following cluster information,
                        suggest which cluster best addresses the issue of "{prompt}", and explain your reasoning:

                        {top_clusters[0]}
                        {top_clusters[1]}
                        {top_clusters[2]}

                        Which cluster would you recommend, and why?
                        """
                        with st.expander("**Recommendations**", expanded=True):
                            st.subheader("Gemini Recommendation")
                            response = gemini_model.generate_content(gemini_prompt)
                            st.write(response.text)

                except Exception as e:
                    st.error(f"Error during cluster search: {str(e)}")
        else:
            st.info("Please enter a diagnostic issue to search.")

    # Report Section
    st.subheader("Claims Report")
    if st.button("Show Report"):
        data = load_csv_data(config["app"]["file_path"])
        if data is not None:
            st.dataframe(
                data,
                use_container_width=True,
                hide_index=True
            )

            # Add download button
            csv = data.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="claims_report.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()
