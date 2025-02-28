# Telegram Group Management Bot

This is a Telegram bot for managing groups. It includes commands for adding, removing, listing members, kicking, pinning, unpinning, muting, unmuting, getting stats, getting info, and antilink.

## Requirements

- Python 3.6+
- `python-telegram-bot` library

## Installation

1. Clone the repository:

```sh
$ git clone https://github.com/yourusername/telegram-group-management-bot.git
$ cd telegram-group-management-bot
```

2. Install the dependencies:

```sh
$ pip install -r requirements.txt
```

3. Create a `.env` file and add your bot token:

```
TOKEN=your-telegram-bot-token
```

## Running the Bot

```sh
$ python bot.py
```

## Deploying to Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

1. Create a Heroku app:

```sh
$ heroku create
```

2. Set the bot token in Heroku:

```sh
$ heroku config:set TOKEN=your-telegram-bot-token
```

3. Deploy the code:

```sh
$ git push heroku main
```

4. Scale the bot:

```sh
$ heroku ps:scale web=1
```

The bot should now be running on Heroku.

## Commands

- `/start` - Start the bot
- `/help` - Get help
- `/add` - Add a member
- `/remove` - Remove a member
- `/list` - List members
- `/kick` - Kick a member
- `/pin` - Pin a message
- `/unpin` - Unpin all messages
- `/mute` - Mute a member
- `/unmute` - Unmute a member
- `/stats` - Get stats
- `/info` - Get chat info
- `/antilink` - Enable antilink
