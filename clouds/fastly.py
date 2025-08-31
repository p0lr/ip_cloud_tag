from urllib.request import urlopen
import json
from ipaddress import ip_network


class fastly:
    """
    Fastly IP range handler. Fetches, parses, and builds Fastly IP range entries.
    """

    def __init__(self):
        """
        Initialize Fastly handler and build IP ranges.
        """
        # Build the Fastly IP ranges on initialization
        self.ip_ranges = self.build_fastly_ip_ranges()

    def get_fastly_ip_json(self):
        """
        Fetch Fastly IP ranges JSON from the official URL.
        Returns:
            dict: Parsed JSON data or None on error.
        """
        url = "https://api.fastly.com/public-ip-list"
        # Attempt to fetch the JSON data from Fastly
        try:
            fastly_response = urlopen(url)
        except Exception as error:
            # Print error if fetch fails
            print(error)
            fastly_response = None
        # Parse the JSON if response is valid
        if fastly_response:
            try:
                fastly_json = json.load(fastly_response)
            except:
                # Print error if JSON parsing fails
                fastly_json = None
            return fastly_json

    def handle_fastly_json(self, fastly_ip_json):
        """
        Parse Fastly JSON and build IP range entries.
        Args:
            fastly_ip_json (dict): Fastly IP JSON.
        Returns:
            list: List of IP range dicts.
        """
        fastly_ip_ranges = []
        # Iterate over all addresses in the JSON
        for cidr in fastly_ip_json.get("addresses", []):
            try:
                network = ip_network(cidr)
            except Exception as error:
                # Print error if CIDR is invalid
                print(error)
                network = None
            if network:
                entry = {
                    "Provider": "Fastly",
                    "Start": int(network.network_address),
                    "End": int(network.broadcast_address)
                }
                fastly_ip_ranges.append(entry)
        return fastly_ip_ranges

    def build_fastly_ip_ranges(self):
        """
        Build a list of Fastly IP range entries from the JSON data.
        Returns:
            list: List of IP range dicts.
        """
        fastly_ip_json = self.get_fastly_ip_json()
        if fastly_ip_json:
            fastly_ip_ranges = self.handle_fastly_json(fastly_ip_json)
            return fastly_ip_ranges
