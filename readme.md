
# Equity Transfers Management Application

## Overview
This application allows users to create, manage, and visualize equity portfolios. Users can add equities, track their vesting schedules, and generate reports with insights on portfolio valuations.

## Features
- Add equities with vesting dates and historical price data.
- Visualize stock price changes over time with interactive charts.
- Calculate portfolio value using various methods.
- Convert non-USD currencies to USD based on real-time exchange rates.

## Requirements
Make sure you have the following installed:
- [Anaconda](https://www.anaconda.com/products/distribution) (recommended for managing environments)
- [Python](https://www.python.org/downloads/) (version 3.12 recommended)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/NotAlvin/Equity-Transfers.git
   cd Equity-Transfers
   ```

2. **Create and activate a Conda environment:**
   You can do this manually, or use the provided setup script (see below).

3. **Install dependencies:**
   Run the following command to install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   You can launch the application using:
   ```bash
   streamlit run your_streamlit_app.py
   ```

## Usage

1. **Create a Portfolio:**
   - Navigate to the portfolio creation page.
   - Add equities with their respective vesting dates and other details.

2. **Generate a Report:**
   - Select an existing portfolio from the dropdown.
   - Choose a calculation method for the portfolio value.
   - Click "Generate Report" to view the results.

3. **Visualizations:**
   - View stock price changes over the past year for each equity in the selected portfolio.

## Loading Script
To quickly set up the environment and run the application, you can use the provided script:

### For Linux/macOS:
```bash
./setup_and_run.sh
```

### For Windows:
```batch
setup_and_run.bat
```

## Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request with your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For any questions or issues, please reach out to [alvin_leung@u.nus.edu](mailto:alvin_leung@u.nus.edu).
