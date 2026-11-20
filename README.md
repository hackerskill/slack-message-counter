# slack-message-counter
A Slack Bot to count number of message sent by a person or a bot in a specific channel

## Description
A Slack Bot to count number of message sent by a person or a bot in a specific channel and can be called using both slash command and app mentions.

## Features

- **Slack Bot** Integrates into the Slack workspace.
- **Dual Usage Approach** Can be called using both slash command and app mention.
- **Socket Mode** Utilises socket mode to maintain persistent connection.
- **User Token Usage** Uses user token to perfom quick searches.
- **Threading** Automatically threads message when app is used using app mention.

## Setup

1. Create a New App on [Slack API Dashboard](https://api.slack.com/apps).

2. Under `OAuth & Permissions`, provide `commands`, `app_mentions:read`, `chat:write`, `users:read` Bot Token Scope and `search:read` User Token Scope.

3. Under `Slash Commands`, create a new command and ensure `Escape channels, users, and links sent to your app` is checked.

4. Under `Event Subscriptions`, enable event and subscribe to `app_mention` event.

5. Install the app from `Install App`

6. Clone the repo

7. **Change `.env.example` to `.env` with the following keys-**
    * Bot User OAuth Token which can be obtained from `OAuth & Permissions`
    * User OAuth Token which can be obtained from `OAuth & Permissions`
    * App-Level Tokens which can be obtained from `Basic Information`

8. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

The bot can be used in 2 ways-
1. App mention, pinging the bot gives the response. This reponse is viewable to everyone and is threaded.
2. Using the slash command set in the code like `/count`, this returns a ephemeral reponse, only visible to the person who used the command.

### Running the Application

Once setup is verified, `main.py` can be run to start the discord bot.
