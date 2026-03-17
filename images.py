import os
import scrapy
from PIL import Image
from io import BytesIO
import pandas as pd


class ImagesSpider(scrapy.Spider):
    name = "images"

    custom_settings = {
        "DOWNLOAD_TIMEOUT": 30,
        "CONCURRENT_REQUESTS": 8,
        "LOG_LEVEL": "INFO",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.max_size = (1000, 1000)
        self.quality = 70

        self.headers = {
            'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Chromium";v="135", "Not-A.Brand";v="8"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'upgrade-insecure-requests': '1',
            'user-agent': (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/135.0.0.0 Safari/537.36'
            )
        }

    def start_requests(self):
        """
        Example input.
        Replace this with your real source (CSV, DB, response parsing, etc.)
        """
        
        df = pd.read_csv("gravityperformance_full_data2.csv")

        for row in df.itertuples():
            img_url = row.image
            folder_name = 'images'
            index = row.id
            # breakpoint()

            yield scrapy.Request(
                url=img_url,
                headers=self.headers,
                callback=self.save_image,
                meta={
                    "folder": folder_name,
                    "number": index,
                    
                },
                dont_filter=True
            )

    def save_image(self, response):
        folder_name = response.meta["folder"]
        image_number = response.meta["number"]

        folder_path = os.path.join("images", folder_name)
        os.makedirs(folder_path, exist_ok=True)

        try:
            image = Image.open(BytesIO(response.body))

            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")

            image.thumbnail(self.max_size)

            image_path = os.path.join(
                folder_path,
                f"{image_number}.jpg"
            )

            image.save(
                image_path,
                "JPEG",
                quality=self.quality,
                optimize=True
            )

            self.logger.info(f"Saved image: {image_path}")

        except Exception as e:
            self.logger.error(f"Failed image {response.url}: {e}")
            with open("errors_url.txt", "a", encoding="utf-8") as f:
                f.write(f"{response.url}\t{image_number}\n")
