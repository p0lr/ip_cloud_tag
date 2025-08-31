from urllib.request import urlopen
import json
from ipaddress import ip_network


class salesforce:
    """
    IP range handler. Fetches, parses, and builds IP range entries.
    """

    def __init__(self):
        """
        Initialize Salesforce handler and build IP ranges.
        """
        # Build the Salesforce IP ranges on initialization
        self.ip_ranges = self.build_ip_ranges()

    def get_ip_json(self):
        """
        Fetch Okta IP ranges JSON from the official URL.
        Returns:
            dict: Parsed JSON data or None on error.
        """
        url = "https://ip-ranges.salesforce.com/ip-ranges.json"
        # Attempt to fetch the JSON data from Salesforce
        try:
            response = urlopen(url)
        except Exception as error:
            # Print error if fetch fails
            print(error)
            response = None
        # Parse the JSON if response is valid
        if response:
            try:
                json_data = json.load(response)
            except:
                # Print error if JSON parsing fails
                json_data = None
            return json_data

    def handle_ip_json(self, json_data):
        """
        Parse Salesforce JSON and build IP range entries.
        Args:
            json_data (dict): Salesforce IP JSON.
        Returns:
            list: List of IP range dicts.
        """
        ip_ranges = []
        # Iterate over all regions in the JSON
        prefixes = json_data.get("prefixes", [])
        for prefix in prefixes:
            region = prefix.get("region")
            cidrs = prefix.get("ip_prefix")
            for cidr in cidrs:
                try:
                    network = ip_network(cidr)
                except Exception as error:
                    # Print error if CIDR is invalid
                    print(error)
                    network = None
                if network:
                    entry = {
                        "Provider": "Salesforce",
                        "Region": region,
                        "Start": int(network.network_address),
                        "End": int(network.broadcast_address)
                    }
                    ip_ranges.append(entry)
        return ip_ranges

    def build_ip_ranges(self):
        """
        Build a list of Salesforce IP range entries from the JSON data.
        Returns:
            list: List of IP range dicts.
        """
        ip_json = self.get_ip_json()
        if ip_json:
            ip_ranges = self.handle_ip_json(ip_json)
            return ip_ranges
