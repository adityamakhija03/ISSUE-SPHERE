# Issue Sphere - Intelligent Diagnostic Cluster Finder

![Issue Sphere Logo](./issue%20sphere.jpg)

Issue Sphere is an intelligent system that uses vector search and AI to find relevant diagnostic clusters for vehicle-related issues. It combines MongoDB's vector search capabilities with Google's Gemini AI to provide accurate and contextual recommendations, featuring Sentence Transformers for embedding generation.

## 🚀 Features

- **Vector-Based Search**: Utilizes MongoDB's vector search for semantic similarity matching
- **AI-Powered Analysis**: Leverages Google's Gemini AI for intelligent cluster recommendations
- **Interactive UI**: Built with Streamlit for a user-friendly experience
- **Real-time Processing**: Instant results with efficient embedding generation
- **Configurable**: Easy configuration using TOML format
- **Claims Reporting**: Built-in CSV report generation and download functionality

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **Database**: MongoDB Atlas with Vector Search
- **AI Models**: 
  - Google Gemini for cluster analysis
  - Sentence Transformers for embedding generation
- **Configuration**: TOML
- **Language**: Python 3.8+

## 📋 Prerequisites

- Python 3.8 or higher
- MongoDB Atlas account with Vector Search enabled
- Google Cloud API key with Gemini API access
- Git (for version control)

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/adityamakhija03/ISSUE-SPHERE.git
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `config.toml` file in the project root:
```toml
[mongodb]
uri = "your_mongodb_uri"
database = "myDatabase"
clusters_collection = "oem_clusters"
claims_collection = "oem_claims"

[api]
google_api_key = "your_google_api_key"

[model]
sentence_transformer = "sentence-transformers/model-name"
gemini_model = "gemini-model-name"

[app]
title = "Cluster Finder for issues"
image_path = "./issue sphere.jpg"
image_width = 150
```

4. Run the application:
```bash
streamlit run appp.py
```

## 🚀 Usage

1. Start the application using the command above
2. Enter a diagnostic issue in the text input field
3. Click "Find Clusters" to search for relevant clusters
4. View the top 3 matching clusters with similarity scores
5. Review the AI-generated recommendation for the best matching cluster
6. Access the Claims Report section to view and download CSV reports

## 💡 Example Queries

- "Engine making knocking noise at high RPM"
- "Battery not holding charge after overnight parking"
- "Transmission slipping during gear changes"


## 📊 Performance Features

- **Streamlit Caching**: 
  - Configuration loading (`@st.cache_resource`)
  - Model initialization (`@st.cache_resource`)
  - MongoDB connection (`@st.cache_resource`)
  - CSV data loading (`@st.cache_data`)
- **Error Handling**:
  - Comprehensive try-except blocks for all critical operations
  - User-friendly error messages
  - MongoDB connection timeout handling
- **Optimized Search**:
  - Vector search with exact matching
  - Limited to top 3 results for performance
  - Structured aggregation pipeline

## 🔐 Security Features

- Configuration file separation for sensitive data
- MongoDB connection timeout configuration
- Error handling to prevent exposure of sensitive information
- Remote code trust configuration for model loading

## 👥 Authors

- Aditya Makhija (@adityamakhija03)

## 📞 Support

For support, email aditya3makhija@gmail.com or create an issue in the repository.

## 🔮 Future Enhancements

- [ ] Add batch processing capabilities
- [ ] Implement user authentication
- [ ] Enhanced reporting features
- [ ] Create API endpoints
- [ ] Add visualization for cluster relationships
- [ ] Implement feedback mechanism
- [ ] Add data export options

## 🙏 Acknowledgments

- Streamlit for the web framework
- MongoDB Team for Vector Search capabilities
- Google for the Gemini API
- Sentence Transformers team for the embedding model

---