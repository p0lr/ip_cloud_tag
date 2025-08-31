from urllib.request import urlopen
import json
from ipaddress import ip_network


class github:
    """
    IP range handler. Fetches, parses, and builds IP range entries.
    """

    def __init__(self):
        """
        Initialize handler and build IP ranges.
        """
        # Build the IP ranges on initialization
        self.ip_ranges = self.build_ip_ranges()

    def get_ip_json(self, url):
        """
        Fetch IP ranges JSON from the official URL.
        Returns:
            dict: Parsed JSON data or None on error.
        """

        # Attempt to fetch the JSON data from Zscaler
        try:
            response = urlopen(url)
        except Exception as error:
            # Print error if fetch fails
            print(error)
            response = None
        # Parse the JSON if response is valid
        if response:
            try:
                response_json = json.load(response)
            except:
                # Print error if JSON parsing fails
                response_json = None
            return response_json

    def handle_json(self, response_json):
        """
        Parse JSON and build IP range entries.
        Args:
            response_json (dict): IP JSON.
        Returns:
            list: List of IP range dicts.
        """
        ip_ranges = []
        # Iterate over all clouds in the JSON
        for service in response_json:
            value = response_json[service]
            if type(value) is list:
                for cidr in value:
                    try:
                        network = ip_network(cidr)
                    except Exception as error:
                        network = None
                    if network:
                        entry = {
                            "Provider": "GitHub",
                            "Service": service,
                            "Start": int(network.network_address),
                            "End": int(network.broadcast_address)
                        }
                        ip_ranges.append(entry)
        return ip_ranges

    def build_ip_ranges(self):
        """
        Build a list of IP range entries from the JSON data.
        Returns:
            list: List of IP range dicts.
        """
        url = "https://api.github.com/meta"
        ip_json = self.get_ip_json(url)
        if ip_json:
            ip_ranges = self.handle_json(ip_json)
            if ip_ranges:
                return ip_ranges
