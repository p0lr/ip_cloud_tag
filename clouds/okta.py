from urllib.request import urlopen
import json
from ipaddress import ip_network


class okta:
    """
    Okta IP range handler. Fetches, parses, and builds Okta IP range entries.
    """

    def __init__(self):
        """
        Initialize Okta handler and build IP ranges.
        """
        # Build the Okta IP ranges on initialization
        self.ip_ranges = self.build_okta_ip_ranges()

    def get_okta_ip_json(self):
        """
        Fetch Okta IP ranges JSON from the official URL.
        Returns:
            dict: Parsed JSON data or None on error.
        """
        url = "https://s3.amazonaws.com/okta-ip-ranges/ip_ranges.json"
        # Attempt to fetch the JSON data from Okta
        try:
            okta_response = urlopen(url)
        except Exception as error:
            # Print error if fetch fails
            print(error)
            okta_response = None
        # Parse the JSON if response is valid
        if okta_response:
            try:
                okta_json = json.load(okta_response)
            except:
                # Print error if JSON parsing fails
                okta_json = None
            return okta_json

    def handle_okta_json(self, okta_json):
        """
        Parse Okta JSON and build IP range entries.
        Args:
            okta_json (dict): Okta IP JSON.
        Returns:
            list: List of IP range dicts.
        """
        okta_ip_ranges = []
        # Iterate over all regions in the JSON
        for region in okta_json:
            cidrs = okta_json[region].get("ip_ranges", [])
            for cidr in cidrs:
                try:
                    network = ip_network(cidr)
                except Exception as error:
                    # Print error if CIDR is invalid
                    print(error)
                    network = None
                if network:
                    entry = {
                        "Provider": "Okta",
                        "Region": region,
                        "Start": int(network.network_address),
                        "End": int(network.broadcast_address)
                    }
                    okta_ip_ranges.append(entry)
        return okta_ip_ranges

    def build_okta_ip_ranges(self):
        """
        Build a list of Okta IP range entries from the JSON data.
        Returns:
            list: List of IP range dicts.
        """
        okta_ip_json = self.get_okta_ip_json()
        if okta_ip_json:
            okta_ip_ranges = self.handle_okta_json(okta_ip_json)
            return okta_ip_ranges
