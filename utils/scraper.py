import requests
from bs4 import BeautifulSoup


class WebsiteScraper:

    def fetch_text(self, url: str) -> str:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            # REMOVE JUNK TAGS
            for tag in soup(["script", "style", "noscript", "header", "footer", "svg"]):
                tag.extract()

            # -------------------------
            # PRIORITY EXTRACTION (BETTER SIGNAL)
            # -------------------------

            priority_text = []

            # META DESCRIPTION (VERY IMPORTANT — ADD HERE)
            meta = soup.find("meta", attrs={"name": "description"})
            if meta:
                priority_text.insert(0, meta.get("content"))
            
            # headings first (MOST IMPORTANT)
            for tag in soup.find_all(["h1", "h2", "h3"]):
                priority_text.append(tag.get_text())

            # hero + paragraphs
            for tag in soup.find_all("p"):
                priority_text.append(tag.get_text())

            # fallback full text
            fallback_text = soup.get_text(separator=" ")

            combined = " ".join(priority_text) + " " + fallback_text

            # CLEAN TEXT
            cleaned_text = " ".join(combined.split())

            return cleaned_text[:12000]

        except Exception as e:
            return f"ERROR_FETCHING: {str(e)}"