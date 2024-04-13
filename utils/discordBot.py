
from dhooks import Webhook

url="https://discord.com/api/webhooks/1228826956787748886/bKItvCbwhtGQ0x4y_LEv6yXmoO1AApFBRNPHXTKWuYITOhZoIuvrglCWwaKGxo-8jany"
def sendDiscordAlert(product):
    url="https://discord.com/api/webhooks/1228826956787748886/bKItvCbwhtGQ0x4y_LEv6yXmoO1AApFBRNPHXTKWuYITOhZoIuvrglCWwaKGxo-8jany"
    message = f"New Deal Found from {product['shop']}: {product['set_num']} {product["name"]} at {product['price']} $. Target price was:{product['target_price']} Link: {product['link'] }"
    hook = Webhook(url)
    hook.send(message)
    print("Sent Discord Alert")


