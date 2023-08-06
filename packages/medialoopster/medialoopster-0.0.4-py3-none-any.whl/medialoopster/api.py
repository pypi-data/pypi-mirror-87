from requests import Session
from requests.exceptions import RequestException
from requests.auth import HTTPBasicAuth


class Medialoopster():
    def __init__(self, url, user=None, password=None, verify=False):
        self.session = Session()
        self.session.verify = verify

        if all([user, password]):
            self.session.auth = HTTPBasicAuth(user, password)

        self.url = url

    def __enter__(self):
        """Enable context management."""
        return self

    def __exit__(self, *args):
        """Clean up."""
        self.close()

    def ping(self):
        try:
            response = self.session.get(self.url + "ping/")
            response.raise_for_status()
        except RequestException:
            return False

        return True

    def asset_import(self, production=None, asset_type=None, move_asset=False, name=None, description=None, approval=0,
                     path_file=None, meta_field_store={}):
        request = {
            "production": production,
            "type": asset_type,
            "move_asset": move_asset,
            "asset": {
                "asset_meta": {
                    "name": name,
                    "description": description,
                    "approval": approval,
                    "path_file": path_file,
                    "meta_field_store": meta_field_store
                }
            }
        }

        response = self.session.post(self.url + "asset/import/", json=request)
        response.raise_for_status()

        response_json = response.json()

        return response_json.get("asset_import_id", None)

    def get_url(self, asset_type="videoassets"):
        try:
            response = self.session.get(url=self.url)
            response.raise_for_status()

            response_json = response.json()
        except RequestException:
            return None

        return response_json.get(asset_type, None)

    def get_from_api(self, asset_type="videoassets", url=None):
        if url is None:
            url = self.get_url(asset_type=asset_type)

        while url:
            try:
                response = self.session.get(url=url)
                response.raise_for_status()
            except RequestException:
                continue

            if response.links is not None:
                url = response.links.get("next", {}).get("url", None)
            else:
                url = None

            for response_json in response.json():
                yield response_json

    def get_productions(self):
        return self.get_from_api(asset_type="productions")

    def get_videoassets(self):
        return self.get_from_api(asset_type="videoassets")

    def get_asset(self, asset_id, asset_type="videoassets", with_sequences=True):
        url = f"{self.get_url(asset_type=asset_type)}{asset_id}/"

        if asset_type == "videoassets" and with_sequences is True:
            url = f"{url}?with_sequences=true"

        response = self.session.get(url=url)
        response.raise_for_status()

        response_json = response.json()

        return response_json

    def search_meta_field_store(self, field: str = None, value: str = None, asset_type: str = "videoassets"):
        assets = []

        for asset in self.get_from_api(asset_type=asset_type):
            meta_field_store = asset.get("meta_field_store")
            if meta_field_store is not None:
                field_value = meta_field_store.get(field)
                if field_value is not None and field_value == value:
                    print(asset.get("id"))
                    assets.append(asset.get("id"))

        return assets
