# IP Monitor with Discord Notification

This project monitors your public IP address and notifies you via a Discord bot when your IP changes. The bot will send you a direct message with your new IP address.

## Setup

To get started, follow these steps:

### 1. Clone the repository

```bash
git clone https://your-repository-url.git
cd your-repository-directory
```

### 2. Configure the `.env` file

- Rename the `.env_example` file to `.env`:

```bash
mv .env_example .env
```

- Open the .env file and replace the placeholder values with your actual information
  - `DISCORD_TOKEN`: Your Discord bot token. If you don't have a bot, you can create one via the Discord Developer Portal.
  - `USER_ID`: Your Discord user ID. You can obtain this by enabling Developer Mode in Discord settings and right-clicking your username to copy the user ID.
  - `SLEEP_SECONDS`: The number of seconds the script will wait before checking for an IP change again. By default, it’s set to 10.800 seconds (3 hours).

### 3. Build and run the application with Docker

- Build the Docker image:

```bash
docker-compose build
```

- Start the service:

```bash
docker-compose up
```

This will start the app inside a Docker container. It will check your public IP address periodically (every 3 hours by default) and notify you via Discord DM if the IP changes.
