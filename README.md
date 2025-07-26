# ML-Driven Microgrid Optimization Platform

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-0.10.1-green.svg)](https://flask.palletsprojects.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-0.19.1-orange.svg)](https://scikit-learn.org/)
[![NetworkX](https://img.shields.io/badge/NetworkX-2.0-red.svg)](https://networkx.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Interactive web application for intelligent microgrid design using machine learning and network optimization algorithms.**

## 🚀 Key Features

- **ML-Powered Energy Prediction**: Random Forest model predicts building energy demand based on area, type, and weather conditions
- **Intelligent Clustering**: DBSCAN algorithm groups buildings by geographic proximity (500m radius) and energy consumption patterns  
- **Network Optimization**: Minimum spanning tree algorithms minimize cable costs while ensuring grid connectivity
- **Interactive Visualizations**: Real-time Bokeh maps display optimized microgrid networks overlaid on downtown Toronto
- **Weather Integration**: Incorporates extreme weather scenarios for robust grid planning

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- pip package manager

### Installation & Setup
```bash
# Clone the repository
git clone <repository-url>
cd ml_microgrids

# Install required dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Usage
1. Open your web browser and navigate to `http://localhost:5000`
2. Access the interactive microgrid optimization interface
3. Input building parameters and weather conditions
4. View ML-generated energy predictions and optimized network topology
5. Explore interactive Bokeh visualizations of the microgrid design

## 📁 Project Structure

```
ml_microgrids/
├── app.py                          # Main Flask application with ML pipeline
├── requirements.txt                # Python dependencies
├── conda-requirements.txt          # Conda environment specifications
├── Procfile                        # Heroku deployment configuration
├── runtime.txt                     # Python runtime version
├── data/                           # Data files and ML models
│   ├── mlmicrogrid.pkl            # Trained Random Forest model
│   ├── testweather.csv            # Weather data for predictions
│   ├── Downtown Toronto.gml       # Network graph for Toronto case study
│   ├── dowtown_toronto_lat_long.csv # Building coordinates
│   ├── xs.pkl & ys.pkl            # Cached coordinate data
└── templates/                      # HTML templates
    ├── index.html                  # Main input interface
    ├── analysis.html               # Results visualization
    ├── toronto.html                # Toronto case study
    └── about.html                  # Tool information
```

## 🛠️ Technical Stack

**Backend**: Flask, scikit-learn, NetworkX, pandas, NumPy  
**ML Algorithms**: Random Forest, DBSCAN Clustering, PCA  
**Visualization**: Bokeh interactive maps with CartoDB tiles  
**Geospatial**: PyProj coordinate transformations, Haversine distance calculations  
**Deployment**: Heroku-ready with gunicorn

## 📊 Capabilities Demonstrated

- **Machine Learning**: Supervised learning for energy demand forecasting with weather feature engineering
- **Unsupervised Learning**: Density-based spatial clustering for optimal building groupings
- **Graph Theory**: Network analysis and minimum spanning tree optimization  
- **Geospatial Analysis**: Coordinate system transformations and distance calculations
- **Full-Stack Development**: End-to-end web application with interactive frontend and ML backend

## 🎯 Business Impact

Optimizes microgrid infrastructure for urban environments, reducing energy costs and improving grid resilience during extreme weather events through intelligent ML-driven network design.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Akshay Sharma**
- Data Scientist
- Expertise in large-scale data processing and machine learning