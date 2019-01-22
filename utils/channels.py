def system_or_first(guild, bot):
    if guild.system_channel is not None:
        return guild.system_channel
    else:
        for channel in guild.text_channels:
            if not dict(channel.permissions_for(guild.get_member(bot.user.id)))["send_messages"]:
                continue
            return channel
