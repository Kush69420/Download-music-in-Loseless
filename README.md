# Spotify to Lossless Downloader

This Python script reads a CSV export of a Spotify playlist and searches for high-quality (Lossless/Hi-Res) versions of the tracks using the Triton API (Tidal).

Features

CSV Parsing: Automatically reads Track Name and Artist Name from Spotify export files.

Smart Search: Searches for tracks and prioritizes HIRES_LOSSLESS quality tags.

Skipped Log: Automatically creates a CSV file (skipped_songs2.csv) listing any tracks that could not be found, ensuring you know exactly what is missing.

Metadata Extraction: Retrieves Track IDs and Metadata.

Rate Limiting: Includes delays to prevent API blocking.

Prerequisites

Python 3.x

A Spotify playlist exported as .csv (e.g., using Exportify or similar tools).

# Installation

Clone the repository:

git clone [https://github.com/Kush69420/Download-music-in-Loseless.git](https://github.com/Kush69420/Download-music-in-Loseless.git)
cd Download-music-in-Loseless


Install required libraries:

pip install -r requirements.txt


# Usage

Open script.py in a text editor (like VS Code or Notepad).

Update the CONFIGURATION section at the top of the script to match your local file paths.

Example Configuration:

# CONFIGURATION 
CSV_FILE = r"E:\"
DOWNLOAD_FOLDER = r"E:\"
SKIPPED_FILE = r"E:\"


Run the script:

python script.py


Check Results:

Successfully found tracks will be processed/downloaded to your DOWNLOAD_FOLDER.

Tracks that could not be found will be saved to skipped_songs.csv.

Disclaimer

This tool is for educational purposes only. Please ensure you have the right to download and use the media you are accessing.
