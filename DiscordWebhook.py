from discord_webhook import DiscordWebhook, DiscordEmbed 


def discordWebhook(URL, elements):
    

    webhook = DiscordWebhook(url="https://discord.com/api/webhooks/1242352992708067338/lqTnn9985LOSs55jwkxYPPAdD8OxviUp4-YBemJkTRxojbAroYvZzR8RqSWg6FtKo6Ks")

    # create embed object for webhook
    embed = DiscordEmbed(title=elements[0], description="Lorem ipsum dolor sit", color="03b2f8")

    # set author
    embed.set_author(name="Author Name", url=URL, icon_url=URL)

    # set image with the provided link
    embed.set_image(url=elements[0])

    # set thumbnail with the same or different image
    embed.set_thumbnail(url=elements[0])
    print(elements[0])
    
    # set footer
    embed.set_footer(text="Embed Footer Text", icon_url=URL)

    # set timestamp (default is now) accepted types are int, float and datetime
    embed.set_timestamp()
    
    # add fields to embed
    embed.add_embed_field(name="Field 1", value="Lorem ipsum")
    embed.add_embed_field(name="Field 2", value="dolor sit")

    # add embed object to webhook
    webhook.add_embed(embed)

    response = webhook.execute()
    