# DFP2024Fall_Project

A recommendation application to find our client to find the best rent option

## Table of Contents

1. [Installation](#installation)
2. [Directory Structure](#directory-structure)
2. [Usage](#usage)
3. [Features](#features)

## Installation

### Prerequisites

- **Python** (>=3.12): Make sure you have Python installed. You can check your version with:
  ```bash
  python --version
  ```
- **Required Libraries**: This project requires the following packages, which will be installed from `requirements.txt`:
  - `pandas`
  - `sodapy`
  - `requests`
  - `bs4`

### Install via `pip`
To install the required libraries, run the following command in your terminal:

```bash
pip install -r requirements.txt
```

## Directory Structure

- **`crawler/`**: Holds all the source code related to the web crawling component.
- **`data/raw/`**: Stores raw, unprocessed data collected by the crawler.
- **`data/processed/`**: Contains cleaned and transformed data after processing.
- **`data/final/`**: Contains final recommendation for users.
- **`processors/`**: This folder contains scripts to clean, merge, and filter data, enabling a modular approach to data processing.
- **`ui/`**: Contains the source code for user interface.
- **`requirements.txt`**: Specifies all the dependencies required for the project.
- **`README.md`**: The README file itself.
- **`config.py`**: Contains configuration settings such as file paths, or other environment variables needed for the application to run.

## Usage

To run the application, execute the following command:

```bash
python main.py
```
### Follow instructions

Follow the instructions in the interface and input your preferred living conditions.
```bash
# sample instructions
Which borough would you like to live in? (Enter number)
1. BRONX
2. BROOKLYN
3. MANHATTAN
4. QUEENS
5. Not to matter
```
Users should input valid integer based on the prompts.

### Output
After running the application, users will receive recommendations based on the collected data and preferences. The recommendations will be stored in a CSV file named in the format `[yyyyyyyy-mm-dd hh:mm:ss]recommendation_for_user.csv` under the `data/final` directory.


## Features
- Web crawling and scraping.
- Data cleaning and merging.
- User-friendly interface to analyze the data.
- Exporting processed data as recommendation for users.
