#!/bin/bash

# Set the name of your conda environment
ENV_NAME="equity-transfers"

# Create a new conda environment and activate it
conda create -n $ENV_NAME python=3.12 -y
conda activate $ENV_NAME

# Install the required packages
pip install -r requirements.txt

# Launch the Streamlit application
streamlit run Home.py