@echo off

REM Set the name of your conda environment
SET ENV_NAME=equity-transfers

REM Create a new conda environment and activate it
conda create -n %ENV_NAME% python=3.12 -y
conda activate %ENV_NAME%

REM Install the required packages
pip install -r requirements.txt

REM Launch the Streamlit application
streamlit run Home.py