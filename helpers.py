from discord import Embed, Color
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

def get_role(key: str):
    """Get a role name from the config file using a key

    Args:
        key (str): The key to get the role name of

    Returns:
        str: The role name
    """
    return config["Roles"][key]


def gen_embed(title: str, description: str = None, data: dict = {}):
    """Generate a Discord embed

    Args:
        title (str): The title of the embed
        description (str, optional): The description of the embed. Defaults to None.
        data (dict, optional): The fields of the embed. Defaults to {}.

    Returns:
        discord.Embed: A Discord embed ready to send
    """
    e = Embed(title=title, description=description, color=Color.teal())
    for key, value in data.items():
        e.add_field(name=key, value=value)
    return e
