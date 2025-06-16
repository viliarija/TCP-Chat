# Chat Server with Email Verification

## Overview

This project is a multithreaded chat server written in Python, using CustomTkinter as the backbone for the GUI. It allows users to register accounts with email verification, log in, join chat rooms, and exchange messages with other users in real time. All user data and chat room information is stored in an SQLite3 database.

## Features

* **User Registration** with email-based verification codes
* **User Login** with secure password hashing (SHA-256)
* **Chat Rooms**: Join existing rooms via room code
* **Real-time Messaging** between members of a chat room
* **Email Notifications**: Verification codes sent via email (requires a Gmail account)
* **Multi-threaded Handling**: Supports multiple clients simultaneously

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/viliarija/TCP-Chat.git
   cd TCP-Chat
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   Required Python packages:

   * `bcrypt`
   * `customtkinter`
   * `Pillow`

3. Database Setup:

   The server will automatically create the required SQLite database (`server.db`) with necessary tables upon first run.

## Configuration

1. **Email Configuration (for verification codes)**

   Edit `mail.py` with your Gmail credentials:

   ```python
   EMAIL = "your_email@gmail.com"
   PASSWORD = "your_app_password"  # Use an app password from Google
   ```

2. **Port Configuration**

   Default server port: `55555`

   Modify in `server.py` if needed:

   ```python
   HOST = "0.0.0.0"
   PORT = 55555
   ```

## Usage

1. **Run the Server**

   ```bash
   python3 server.py
   ```

2. **Client Usage**

   ```bash
   python3 app.py
   ```

## Disclaimer

This is an **old project** that I decided to publish while getting started with GitHub. I’m uploading old work here mostly as an archive or reference for myself and others. It’s provided **as-is**, primarily for demonstration and educational purposes. While functional, it may contain bugs or incomplete features and is **not intended for production use**. Use at your own discretion.

## License

MIT License
