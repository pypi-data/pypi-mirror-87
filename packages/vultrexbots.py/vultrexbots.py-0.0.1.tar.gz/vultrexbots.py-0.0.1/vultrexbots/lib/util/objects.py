class botInfo:
    def __init__(self, data):
        self.json = data

        try: self.botId: int = data["id"]
        except (KeyError, TypeError): self.botId: int = -1

        try: self.prefix: str = data["prefix"]
        except (KeyError, TypeError): self.prefix: str = "Undefined"

        try: self.library: str = data["library"]
        except (KeyError, TypeError): self.library: str = "Undefined"

        try: self.description: str = data["description"]
        except (KeyError, TypeError): self.description: str = "Undefined Description"

        try: self.overview: str = data["overview"]
        except (KeyError, TypeError): self.overview: str = "Undefined Overview"

        try: self.discordInvite: str = data["discordInvite"]
        except (KeyError, TypeError): self.discordInvite: str = "Undefined Invite"

        try: self.boosted: bool = data["boosted"]
        except (KeyError, TypeError): self.boosted: bool = False

        try: self.promoted: bool = data["promoted"]
        except (KeyError, TypeError): self.promoted: bool = False

        try: self.vanity: str = data["vanity"]
        except (KeyError, TypeError): self.vanity: str = "Undefined Vanity"

        try: self.github: str = data["github"]
        except (KeyError, TypeError): self.github: str = "Undefined Github"

        try: self.donateUrl: str = data["donateUrl"]
        except (KeyError, TypeError): self.donateUrl: str = "Undefined DonateUrl"

        try: self.serverCount: int = data["serverCount"]
        except (KeyError, TypeError): self.serverCount: int = -1

        try: self.shardCount: int = data["shardCount"]
        except (KeyError, TypeError): self.shardCount: int = -1

        # Lists
        try: self.owners: str = data["owners"]
        except (KeyError, TypeError): self.owners: str = "Undefined List"

        try: self.voters: str = data["voters"]
        except (KeyError, TypeError): self.voters: str = "Undefined List"

        try: self.tags: str = data["tags"]
        except (KeyError, TypeError): self.tags: str = "Undefined List"

        # Made by https://wezacon.com - Team Wezacon