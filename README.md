# Telegram Always Online

A Python tool to keep your Telegram account online 24/7. Works on Linux and Termux.

## Features

- Keep your Telegram account showing as "online" continuously
- Run in background mode (daemon)
- Easy setup and configuration
- Works on Linux and Android (via Termux)

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)
- A Telegram account

### From GitHub

# Clone the repository
git clone https://github.com/yourusername/telegram-always-online.git
cd telegram-always-online

# Install the package
pip install -e .
### On Termux (Android)

# Install required packages
pkg update
pkg install python git

# Clone the repository
git clone https://github.com/yourusername/telegram-always-online.git
cd telegram-always-online

# Install the package
pip install -e .
## Setup

Before using the tool, you need to obtain your Telegram API credentials:

1. Visit https://my.telegram.org/auth
2. Log in with your phone number
3. Click on "API Development Tools"
4. Create a new application
5. Note your API ID and API Hash

Then run the setup:

telegram-online --setup
Follow the prompts to enter your API ID, API Hash, and phone number. You'll receive a verification code from Telegram that you'll need to enter.

## Usage

### Basic Usage

Start the service in the background:

telegram-online --daemon
### Command Line Options

- --setup: Run first-time setup
- --run: Run the service in the foreground
- --daemon: Run the service in the background
- --interval VALUE: Set status update interval in seconds (default: 300)

## How It Works

The tool uses the Telethon library to interact with the Telegram API. It periodically sends a status update to Telegram servers to keep your account appearing online.

When running in daemon mode, the tool operates in the background and starts automatically when your device boots (if setup properly).

## Important Notes

- Keeping your account permanently online might increase battery usage on mobile devices
- The tool requires a constant internet connection
- Your Telegram account credentials are stored locally and securely

## License

MIT License - see the LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.