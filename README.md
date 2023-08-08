---
title: Discord Banshare Bot
description: A Discord bot written in python to facilitate the sharing of bans between servers
tags:
  - python
  - discord.py
---

# Discord Banshare Bot

This bot uses the Discord.py library [discord.py](https://discordpy.readthedocs.io/en/stable/).

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/PxM3nl)

## ✨ Features

- Python
- Discord.py

## 💁‍♀️ How to use

- Install packages using `pip install -r requirements.txt`
- Start the bot using `python main.py`

Commands:
This bot uses Discord slash commands.

/set_channel(TextChannel)
This command sets the channel in your server where banshares are posted.

/share_ban(UserID,Reason,Evidence)
This command bans a member and then shares the ban and evidence to all servers that have the bot set up.
UserID and Reason are strings(text), and Evidence is a Discord Attachement (image).
If a user has already been banned prior to using this command, this command will still send share the ban with other servers.

## 📝 Notes
Contact Cozen (cozen. on Discord) for questions. Developed for the Conference de Fontaine Network.
