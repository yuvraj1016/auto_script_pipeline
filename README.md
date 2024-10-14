# stream-flow : Video Processing and Transcription Automation Data Pipeline

## Demo Video :


https://github.com/AashishKumar-3002/stream-flow/assets/110625812/eb79131f-1b63-4aeb-adb9-16ea4f654f34



This project automates the process of downloading videos from URLs, transcribing them, updating transcriptions, and processing the data for final output. It supports parallel processing to handle multiple URLs simultaneously and ensures that files are uniquely identified to avoid conflicts.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Command Line Mode](#command-line-mode)
  - [Flask API Mode](#flask-api-mode)
- [Options](#options)
- [Contributing](#contributing)
- [License](#license)

## Features
- Download videos and audio from URLs.
- Transcribe videos.
- Update and manage transcriptions.
- Upsert transcriptions to Google Sheets.
- Final processing to format and organize data.
- Parallel processing for handling multiple URLs.
- Unique identification of videos to avoid conflicts.

## Prerequisites
- Python 3.10.12 or higher
- Required Python libraries:
  - `yt_dlp`
  - `concurrent.futures`
  - `flask`
  - Other dependencies as mentioned in `requirements.txt`
- Make sure you have sign-in to your Youtube and instagram account on your default browser to avoid any error while downloading the video by `yt_dlp`.

## Installation
1. `Clone` the repository:
   ```bash
   git clone https://github.com/AashishKumar-3002/stream-flow.git
   cd stream-flow

2. Install the required package(`ffmpeg`) mentioned in `package.txt`:
   ```bash
    # on Ubuntu or Debian
    sudo apt update && sudo apt install ffmpeg

    # on Arch Linux
    sudo pacman -S ffmpeg

    # on MacOS using Homebrew (https://brew.sh/)
    brew install ffmpeg

    # on Windows using Chocolatey (https://chocolatey.org/)
    choco install ffmpeg

    # on Windows using Scoop (https://scoop.sh/)
    scoop install ffmpeg
   ```

3. Install the required `dependencies`:

  - For `Linux` and `MacOS`:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
  - For `Windows`:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```
  - Install the required packages:
    ```bash
      pip install -r requirements.txt
    ```

4. Whisper also requires `Tiktoken` if you do not encounter any error in the above tiktoken installation. Then you may skip the below steps else follow the steps below.

    4.1. comment out the following line in `requirements.txt`:
    ```bash
        # tiktoken
    ```
    4.2. Re Run the following command:
    ```bash
        pip install -r requirements.txt
    ```
    4.3. You may need [`rust`](http://rust-lang.org) installed as well, in case [tiktoken](https://github.com/openai/tiktoken) does not provide a pre-built wheel for your platform. If you see installation errors during the `pip install` command above, please follow the [Getting started page](https://www.rust-lang.org/learn/get-started) to install Rust development environment. Additionally, you may need to configure the `PATH` environment variable, e.g. `export PATH="$HOME/.cargo/bin:$PATH"`. If the installation fails with `No module named 'setuptools_rust'`, you need to install `setuptools_rust`, e.g. by running:

    ```bash
    pip install setuptools-rust
    ```

    Note : The above basically means that you need to install the rust compiler on your system. and then source install the `tiktoken` package. setuptools-rust is a python package that allows you to compile rust code from python.

5. Install `Ollama`:

   To proceed, you need to have a local Ollama server running. Follow the steps below to set it up:

   - Download Ollama from the official website: [https://ollama.com/](https://ollama.com/)
   - Run an LLM (Ollama Language Model) from the Ollama library: [https://ollama.com/library](https://ollama.com/library)
     - For instance, you can run the `phi3` model using the command: `ollama run phi3`

   After setting up the Ollama environment, install and start the Ollama server on your local machine using the following commands:

   ```bash
   curl https://ollama.ai/install.sh | sh
   ollama serve
   ```
## Configuration &#128295;:

Setting Up `config.yaml`:
- Copy the `config.yaml.example` file to `config.yaml`:
  ```bash
  cp config.yaml.example config.yaml
  ```
- Update the `config.yaml` file with your Google API credentials and other required configurations.

Description of the fields in `config.yaml`:

- `extraction`:
  - Contains the video length limit in seconds. Default is 1 hr (3600 seconds).
- `google`:
  - `sheets`:
    - `credentials_file`: Google API credentials file (e.g., "credentials.json").
    - `spreadsheet_id`: Your Google Sheet ID.
  - Create a new project in the Google Cloud Console and enable the Google Sheets API to get the credentials file.
  - The spreadsheet ID can be found in the URL of the Google Sheet.
  - Share the Google Sheet with the email address in the credentials file.
  - Place the credentials file in the project root.
  - Refer to the [Google Sheets Video](https://www.youtube.com/watch?v=cnPlKLEGR7E) for a detailed walkthrough (from timestamp 0:30 to 4:40).
- `paths`:
  - `raw_videos`: Path for storing raw videos.
  - `preprocessed_videos`: Path for storing preprocessed videos.
  - `processed_transcripts`: Path for storing processed transcripts.
  - `final_dir_name`: Name of the final output file.
- `ollama`:
  - `model_name`: Ollama model name (e.g., `phi3`). 
  - I have use phi3 model in this project. You can use any model from the Ollama library.
- `transcription`:
  - `model_name`: Whisper model name (e.g., `openai/whisper-small`).
  - `batch_size`: Batch size for processing.
  - `file_limit_mb`: File size limit in MB.
  - `huggingface_api_key`: Hugging Face API key (optional).
  - Available Whisper models:
    - `openai/whisper-tiny`
    - `openai/whisper-base`
    - `openai/whisper-small`
    - `openai/whisper-medium`
    - `openai/whisper-large-v2`
    - `openai/whisper-large-v3`
  - Model size, parameters, required VRAM, and relative speed:

    |  Size  | Parameters |      model name | Required VRAM| Relative speed |
    |:------:|:----------:|:---------------:|:------------:|:--------------:|
    |  tiny  |    39 M    |     `tiny`      |    ~1 GB     |      ~32x      |
    |  base  |    74 M    |     `base`      |    ~1 GB     |      ~16x      |
    | small  |   244 M    |     `small`     |    ~2 GB     |      ~6x       |
    | medium |   769 M    |    `medium`     |    ~5 GB     |      ~2x       |
    | large  |   1550 M   |    `large`      |    ~10 GB    |       1x       |

## Usage &#128187;:

### Command Line Mode

- Run the project in command-line mode:
  ```bash
  python3 main.py URL1 URL2 URL3 ...
  ```
  - Replace `URL1`, `URL2`, `URL3`, etc., with the URLs of the videos you want to process.
  - For Windows, use `python` instead of `python3`.
- Example:
  ```bash
  python main.py https://www.youtube.com/watch?v=VIDEO_ID1 https://www.instagram.com/reel/C5Gj8oMrOkd/?igsh=ZjF2eXhkenUwYXB0
  ```

### Flask API Mode

- Run the project in Flask API mode:
  ```bash
  python3 app.py
  ```
  - For Windows, use `python` instead of `python3`.
- Make a POST request to http://localhost:5000/process with a JSON body:
  ```json
  {
    "urls": [
      "https://www.instagram.com/reel/C0eV7_fCYKs/?igsh=MXRsZGszODRobnJ1MA==",
      "https://www.instagram.com/reel/C6wcq9xCAaX/"
    ]
  }
  ```
- Example Usage:
  - Using `curl`:
    ```bash
    curl -X POST http://127.0.0.1:5000/process -H "Content-Type: application/json" -d '{
      "urls": [
        "https://www.instagram.com/reel/C0eV7_fCYKs/?igsh=MXRsZGszODRobnJ1MA==",
        "https://www.instagram.com/reel/C6wcq9xCAaX/"
      ]
    }'
    ```
  - Using `Postman`:
    - Open Postman.
    - Create a new POST request to http://127.0.0.1:5000/process.
    - In the body tab, select raw and JSON, and enter:
      ```json
      {
        "urls": [
          "https://www.instagram.com/reel/C0eV7_fCYKs/?igsh=MXRsZGszODRobnJ1MA==",
          "https://www.instagram.com/reel/C6wcq9xCAaX/"
        ]
      }
      ```
    - Send the request.

### Final Output

- The final output is a JSON file named `DataPipeline.json` in the `data/processed` directory.
- The JSON file contains the following fields:
  - Date: The date of the video.
  - Reference_url: The URL of the video.
  - Hook: The opening statement that grabs the audience's attention.
  - Build Up: The section that provides context or setup for the main content.
  - Body: The main content of the video.
  - Call To Action: The closing statement that encourages the audience to take action.

- The final output can also be accessed from the Google Sheet provided in the `config.yaml` file.
- Demo Google Sheet: [sheets](https://docs.google.com/spreadsheets/d/1-aziZm13WFxdLEx0MHqT5VnSOC0LjvMQOAHsTsPoDxw)

- Live testing link: Will be updated soon.

## License &#128220;:

- This project is licensed under the Apache License 2.0.
- See the LICENSE file for details.
