#!/usr/bin/env python3
"""
Authentication module for Telegram Always Online
"""

import os
import sys
import logging
from telethon import TelegramClient
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(name)

# Load environment variables
load_dotenv()

def save_credentials(api_id, api_hash, phone):
    """Save credentials to .env file"""
    try:
        with open('.env', 'w') as f:
            f.write(f"TELEGRAM_API_ID={api_id}\n")
            f.write(f"TELEGRAM_API_HASH={api_hash}\n")
            f.write(f"TELEGRAM_PHONE={phone}\n")
        return True
    except Exception as e:
        logger.error(f"Failed to save credentials: {e}")
        return False

async def setup_authentication():
    """Interactive setup for first-time authentication"""
    print("\n==== Telegram Always Online - First Time Setup ====\n")
    
    # Check if credentials already exist
    if all([os.getenv('TELEGRAM_API_ID'), os.getenv('TELEGRAM_API_HASH'), os.getenv('TELEGRAM_PHONE')]):
        print("Credentials already configured. Do you want to reconfigure? (y/n)")
        choice = input().lower()
        if choice != 'y':
            return True
    
    # Get API credentials
    print("\nYou need to obtain your API ID and API Hash from Telegram:")
    print("1. Visit https://my.telegram.org/auth")
    print("2. Log in with your phone number")
    print("3. Click on 'API Development Tools'")
    print("4. Create a new application if needed")
    print("5. Copy the API ID and API Hash\n")
    
    api_id = input("Enter your API ID: ")
    api_hash = input("Enter your API Hash: ")
    phone = input("Enter your phone number (with country code, e.g., +1234567890): ")
    
    # Validate inputs
    if not api_id.strip() or not api_hash.strip() or not phone.strip():
        logger.error("All fields are required.")
        return False
    
    # Test authentication
    try:
        # Create temporary client to verify credentials
        client = TelegramClient('auth_test', api_id, api_hash)
        await client.connect()
        
        if not await client.is_user_authorized():
            print("\nRequesting verification code from Telegram...")
            await client.send_code_request(phone)
            code = input("Enter the code you received: ")
            await client.sign_in(phone, code)
            
        await client.disconnect()
        print("\nAuthentication successful!")
        
        # Save credentials
        if save_credentials(api_id, api_hash, phone):
            print("Credentials saved successfully.")
            return True
        else:
            print("Failed to save credentials.")
            return False
            
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        return False

if name == "main":
    import asyncio
    if asyncio.run(setup_authentication()):
        print("\nSetup completed successfully. You can now run the application.")
    else:
        print("\nSetup failed. Please try again.")