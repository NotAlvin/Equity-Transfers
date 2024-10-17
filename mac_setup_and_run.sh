#!/bin/bash

# Set the name of your conda environment
ENV_NAME="equity-transfers"

# Create a new conda environment and activate it
conda create -n $ENV_NAME python=3.12 -y
source activate $ENV_NAME

# Install the required packages
pip install -r requirements.txt

# Launch the Streamlit application
streamlit run Home.py

# Note: Replace 'your_streamlit_app.py' with the actual name of your Streamlit app
