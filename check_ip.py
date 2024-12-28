import os
import asyncio
import aiohttp
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the Discord token and user ID (DM target) from the environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
USER_ID = int(os.getenv("USER_ID"))
SLEEP_SECONDS = int(os.getenv("SLEEP_SECONDS"))

# Determine if the script is running inside Docker
def is_docker():
    try:
        # Check for the existence of a Docker-specific file
        with open('/proc/1/cgroup', 'r') as f:
            return 'docker' in f.read()
    except FileNotFoundError:
        # File not found on non-Linux systems or if running locally
        return False

# Set the IP file path based on the environment
if is_docker():
    IP_FILE = "/app/data/last_ip.txt"  # Path inside the Docker container
else:
    IP_FILE = "data/last_ip.txt"  # Local path when running outside Docker

# API to fetch public IP
IP_API = "https://api.ipify.org"

# Set up intents for bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

async def fetch_current_ip():
    """Fetch the current public IP address using aiohttp."""
    async with aiohttp.ClientSession() as session:
        async with session.get(IP_API) as response:
            response.raise_for_status()
            return await response.text()

def load_last_ip():
    """Load the last known IP address from a file."""
    if os.path.exists(IP_FILE):
        with open(IP_FILE, "r") as file:
            return file.read().strip()
    return None

def save_last_ip(ip):
    """Save the current IP address to a file."""
    with open(IP_FILE, "w") as file:
        file.write(ip)

async def notify_ip_change(new_ip, bot):
    """Notify the user via Discord DM about the IP change."""
    print("Sending Discord notification")

    print("Fetching discord user")
    user = await bot.fetch_user(USER_ID)
    print("Done fetching discord user!")
    if user:
        print("Creating DM channel")
        channel = await user.create_dm()
        print("Done creating channel!")

        print("sending DM via channel")
        await channel.send(f"Your public IP has changed to: {new_ip}")
        print("Done sending DM via channel!")
    else:
        print("User not found. Unable to send Discord notification.")

async def run_bot():
    """Run the bot repeatedly with a delay."""
    while True:
        # Create a new bot instance for each iteration
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True

        bot = commands.Bot(command_prefix="!", intents=intents)

        @bot.event
        async def on_ready():
            print(f"Logged in as {bot.user}")
            print("Checking IP...")
            current_ip = await fetch_current_ip()  # Fetch asynchronously
            last_ip = load_last_ip()

            if current_ip != last_ip:
                print(f"IP changed! Old: {last_ip}, New: {current_ip}")
                await notify_ip_change(current_ip, bot)
                save_last_ip(current_ip)
            else:
                print("No change in IP.")
            print("done. shutting down bot")
            await bot.close()

        try:
            await bot.start(DISCORD_TOKEN)
        except Exception as e:
            print(f"Bot encountered an error: {e}")

        print(f"Sleeping for {SLEEP_SECONDS} seconds...")
        await asyncio.sleep(SLEEP_SECONDS)

if __name__ == "__main__":
    print("App started")
    asyncio.run(run_bot())
