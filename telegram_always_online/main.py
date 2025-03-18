#!/usr/bin/env python3
"""
Telegram Always Online - Keep your Telegram account online 24/7
"""

import os
import time
import logging
import signal
import sys
from telethon import TelegramClient
from telethon.tl.functions.account import UpdateStatusRequest
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(name)

# Load environment variables from .env file
load_dotenv()

class TelegramOnline:
    def init(self):
        # Get API credentials from environment or config
        self.api_id = os.getenv('TELEGRAM_API_ID')
        self.api_hash = os.getenv('TELEGRAM_API_HASH')
        self.phone = os.getenv('TELEGRAM_PHONE')
        
        # Check if credentials are available
        if not all([self.api_id, self.api_hash, self.phone]):
            logger.error("Missing API credentials. Please set TELEGRAM_API_ID, TELEGRAM_API_HASH, and TELEGRAM_PHONE environment variables.")
            sys.exit(1)
            
        # Initialize client
        self.client = None
        self.is_running = False
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
        
    async def connect(self):
        """Connect to Telegram and authenticate"""
        try:
            # Create client with session name based on phone number
            session_name = f"always_online_{self.phone}"
            self.client = TelegramClient(session_name, self.api_id, self.api_hash)
            
            # Connect and ensure authorized
            await self.client.connect()
            
            if not await self.client.is_user_authorized():
                logger.info("First time authentication required")
                await self.client.send_code_request(self.phone)
                code = input("Enter the code you received: ")
                await self.client.sign_in(self.phone, code)
                
            logger.info("Successfully connected to Telegram")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            return False
            
    async def start_online_loop(self):
        """Main loop to keep the account online"""
        self.is_running = True
        
        try:
            while self.is_running:
                # Set offline=False to appear online
                await self.client(UpdateStatusRequest(offline=False))
                logger.info("Online status updated")
                
                # Wait before next update (every 5 minutes)
                # Telegram's online status typically times out after ~5-10 minutes
                await asyncio.sleep(300)
                
        except Exception as e:
            logger.error(f"Error in online loop: {e}")
            self.is_running = False
            
    def shutdown(self, signum, frame):
        """Handle shutdown gracefully"""
        logger.info("Shutdown signal received, closing connection...")
        self.is_running = False
        
        if self.client and self.client.is_connected():
            # Set status to offline before disconnecting
            self.client.loop.create_task(self.client(UpdateStatusRequest(offline=True)))
            self.client.disconnect()
            
        logger.info("Disconnected from Telegram")
        sys.exit(0)

async def main():
    """Main entry point"""
    telegram = TelegramOnline()
    
    if await telegram.connect():
        logger.info("Starting always online service")
        await telegram.start_online_loop()
    else:
        logger.error("Failed to start service")
        
if name == "main":
    import asyncio
    asyncio.run(main())