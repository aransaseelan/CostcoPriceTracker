from discord_webhook import DiscordWebhook, DiscordEmbed 


def discordWebhook(url, name, price, image, discount, limited_offer, stock):
    
    webhooks = ['https://discord.com/api/webhooks/1242352992708067338/lqTnn9985LOSs55jwkxYPPAdD8OxviUp4-YBemJkTRxojbAroYvZzR8RqSWg6FtKo6Ks', 'https://discordapp.com/api/webhooks/1247270776391077888/yyIBmetMUs-3_qIXa7mNAKMheb50PalkMLyQLUKHw3FgM3HtoWqxBsXCUryscsspc68e']

    # Always post to the first URL
    post_to_discord(webhooks[0], url, name, price, image, discount, stock)

    # Only post to the second URL when the discount is not zero or the price ends with .97
    if discount != "0" or str(price).endswith('.97') or limited_offer == True:
        post_to_discord(webhooks[1], url, name, price, image, discount, stock)

def post_to_discord(webhook_url, url, name, price, image, discount, stock):
    webhook = DiscordWebhook(url=webhook_url)
    # create embed object for webhook
    embed = DiscordEmbed(title=stock, description=price, color="03b2f8")

    # set author
    embed.set_author(name=name, url=url, icon_url=url)

    # set image with the provided link
    embed.set_image(url=url)

    # set thumbnail with the same or different image
    embed.set_thumbnail(url=image)
    
    embed.add_embed_field(name="Discount", value=discount)
    
    # set footer
    embed.set_footer(text="Aran Saseelan Bot", icon_url=url)

    # set timestamp (default is now) accepted types are int, float and datetime
    embed.set_timestamp()

    # add embed object to webhook
    webhook.add_embed(embed)

    # execute the webhook
    webhook.execute()