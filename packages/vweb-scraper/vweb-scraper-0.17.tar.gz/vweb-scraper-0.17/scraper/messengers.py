from discord_webhook.webhook import DiscordEmbed, DiscordWebhook
import requests
import random

from scraper.utils import RequestManager, Logger


class DiscordMessenger:
    DISCORD_WEBHOOK_URL: str = None
    MESSAGE_FORMAT: str = None
    # ``CUSTOM_IMAGE_SERVER_DATA`` must contain dict of these values for using it to host images.
    # {
    #     "url": "",
    #     "key": ""
    # }
    CUSTOM_IMAGE_SERVER_DATA: dict = None
    WEBSITE_BASE_URL: str = None
    WEBSITE_LOGO_URL: str = None
    request_manager: RequestManager = None
    logger: Logger = None
    SCRAPER_NAME: str = None

    def __get_custom_image_data(self, product_image):
        self.CUSTOM_IMAGE_SERVER_DATA.setdefault("files", {
            "img": self.request_manager.get(product_image)
        })
        resp = requests.post(**self.CUSTOM_IMAGE_SERVER_DATA).json()

        assert resp.get("error") is None, (
            "Please provide a valid API key for image API in ``CUSTOM_IMAGE_SERVER_DATA``"
        )
        return product_image.get('url')

    def default_format(
            self,
            restock: bool = False,
            product_image: (list, str) = "No Product Image Found",
            product_price: str = "No Product Price Found",
            product_url: str = "No Product Url Found.",
            product_brand: str = "No Product Brand Found.",
            product_name: str = "No Product Name Found.",
            product_sizes: (list, str) = "No Size Found.",
            product_colors: (list, str) = "No Color Found."
    ):
        """If no format is provided then this will be used"""
        self.logger("SENDING MESSAGE !!", "messenger")

        product_image = random.choice(product_image) if type(product_image) == list else product_image
        if self.CUSTOM_IMAGE_SERVER_DATA:
            product_image = self.__get_custom_image_data(product_image)

        webhook = DiscordWebhook(
            url=self.DISCORD_WEBHOOK_URL
        )
        embed = DiscordEmbed(
            title=product_name,
            description=f"{'New product added with'} {product_name} from {product_brand} {'got Restocked' if restock else ''}",
            color=242424
        )
        embed.set_author(
            name=self.SCRAPER_NAME, icon_url=self.WEBSITE_LOGO_URL
        )

        embed.set_thumbnail(url=product_image)

        embed.add_embed_field(name='Product Url', value=product_url)
        embed.add_embed_field(
            name='sizes & Color', value=f'"{",".join(product_sizes)}" sizes available of color "{product_colors}"'
        )

        embed.add_embed_field(name='Site & price', value=f"{self.WEBSITE_BASE_URL}, {product_price}")

        embed.set_timestamp()

        webhook.add_embed(embed)
        msg_res = webhook.execute()

        self.logger(f"Message sent to discord with response ``{msg_res}``", "messenger")

    def send_discord_message(self, webhook_url: str = None, message_format: str = "default", *args, **kwargs):
        """Sends message to discord"""
        webhook_url = webhook_url or self.DISCORD_WEBHOOK_URL
        assert webhook_url is not None, (
            "Either set a constant ``DISCORD_WEBHOOK_URL`` OR pass webhook_url as "
            "keyword argument to send_discord_message"
        )

        message = getattr(self, f"{message_format}_format", None)
        assert message is not None, (
            f"`{message_format}` is not available please add ``{message_format}_format`` method to allow that format"
        )
        message = message(*args, **kwargs)
        self.logger(message)
