from urllib.request import urlopen
import json
from ipaddress import ip_network


class atlassian:
    """
    Atlassian IP range handler. Fetches, parses, and builds Atlassian IP range entries.
    """

    def __init__(self):
        """
        Initialize Atlassian handler and build IP ranges.
        """
        # Build the Atlassian IP ranges on initialization
        self.ip_ranges = self.build_atlassian_ip_ranges()

    def get_atlassian_ip_json(self):
        """
        Fetch Atlassian IP ranges JSON from the official URL.
        Returns:
            dict: Parsed JSON data or None on error.
        """
        url = "https://ip-ranges.atlassian.com/"
        # Attempt to fetch the JSON data from Atlassian
        try:
            atlassian_response = urlopen(url)
        except Exception as error:
            # Print error if fetch fails
            print(error)
            atlassian_response = None
        # Parse the JSON if response is valid
        if atlassian_response:
            try:
                atlassian_json = json.load(atlassian_response)
            except:
                # Print error if JSON parsing fails
                atlassian_json = None
            return atlassian_json

    def handle_atlassian_json(self, atlassian_ip_json):
        """
        Parse Atlassian JSON and build IP range entries.
        Args:
            atlassian_ip_json (dict): Atlassian IP JSON.
        Returns:
            list: List of IP range dicts.
        """
        atlassian_ip_ranges = []
        # Iterate over all items in the JSON
        for item in atlassian_ip_json.get("items", []):
            cidr = item.get("cidr")
            try:
                network = ip_network(cidr)
            except Exception as error:
                # Print error if CIDR is invalid
                print(error)
                network = None
            if network:
                # For each region and product, build an entry
                for region in item.get("region", []):
                    for service in item.get("product", []):
                        entry = {
                            "Provider": "Atlassian",
                            "Region": region,
                            "Service": service,
                            "Start": int(network.network_address),
                            "End": int(network.broadcast_address)
                        }
                        atlassian_ip_ranges.append(entry)
        return atlassian_ip_ranges

    def build_atlassian_ip_ranges(self):
        """
        Build a list of Atlassian IP range entries from the JSON data.
        Returns:
            list: List of IP range dicts.
        """
        atlassian_ip_json = self.get_atlassian_ip_json()
        if atlassian_ip_json:
            atlassian_ip_ranges = self.handle_atlassian_json(atlassian_ip_json)
            return atlassian_ip_ranges
