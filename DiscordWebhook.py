from discord_webhook import DiscordWebhook, DiscordEmbed 


def discordWebhook(url, name, price, image):
    

    webhook = DiscordWebhook(url="https://discord.com/api/webhooks/1242352992708067338/lqTnn9985LOSs55jwkxYPPAdD8OxviUp4-YBemJkTRxojbAroYvZzR8RqSWg6FtKo6Ks")

    # create embed object for webhook
    embed = DiscordEmbed(title=name, description="Lorem ipsum dolor sit", color="03b2f8")

    # set author
    embed.set_author(name=url, url=url, icon_url=url)

    # set image with the provided link
    embed.set_image(url=image)

    # set thumbnail with the same or different image
    embed.set_thumbnail(url=image)
    
    # set footer
    embed.set_footer(text="Aran Saseelan Bot", icon_url=url)

    # set timestamp (default is now) accepted types are int, float and datetime
    embed.set_timestamp()
    

    # add embed object to webhook
    webhook.add_embed(embed)
    response = webhook.execute()
    