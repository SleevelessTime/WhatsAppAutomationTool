# WhatsApp Automation Controller

A Python-based tool for automating WhatsApp operations using Selenium. This tool allows users to control the automation process, such as starting or stopping the automation, and provides additional functionality like saving messages as notes.

## Features
- **Start/Stop Automation**: Start or stop WhatsApp automation through a simple command-line interface.
- **Save Notes**: Save incoming WhatsApp messages as notes in a text file.
- **Send Commands**: Supports commands like `help`, `exit`, and `not` to interact with the automation.
- **Message Monitoring**: Automatically monitors and logs new messages from a specified phone number.

## Requirements
- Python 3.x
- Selenium
- BeautifulSoup
- ChromeDriver

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/WhatsAppAutomationTool.git
    ```

2. Navigate to the project directory:
    ```bash
    cd WhatsAppAutomationTool
    ```

3. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Download ChromeDriver matching your Chrome version from:
    [ChromeDriver Download](https://chromedriver.chromium.org/downloads)

5. Update the path to `chromedriver.exe` in the script.

## Usage

Run the controller script to start the automation:
```bash
python control.py
```

The script will prompt you to enter commands:
- `Start`: Starts WhatsApp automation.
- `Exit`: Stops the automation.
- `Help`: Displays available commands.
- `Not`: Saves incoming messages as notes until the command `not bitti` is issued.

## Contributing
Feel free to fork the repo, open issues, and submit pull requests. Contributions are welcome!
