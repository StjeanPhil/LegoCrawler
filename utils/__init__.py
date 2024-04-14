# Export symbols from module1 and module2
from discordBot import sendDiscordAlert


# Define what symbols are exported when using from package import *
__all__ = ['sendDiscordAlert']