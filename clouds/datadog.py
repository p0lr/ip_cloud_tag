from urllib.request import urlopen
import json
from ipaddress import ip_network


class datadog:
    """
    IP range handler. Fetches, parses, and buildsIP range entries.
    """

    def __init__(self):
        """
        Initialize Datadog handler and build IP ranges.
        """
        # Build the Datadog IP ranges on initialization
        self.ip_ranges = self.build_ip_ranges()

    def get_ip_json(self):
        """
        Fetch Datadog IP ranges JSON from the official URL.
        Returns:
            dict: Parsed JSON data or None on error.
        """

        # Attempt to fetch the JSON data from Datadog
        url = "https://ip-ranges.datadoghq.com/"
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
    
    def handle_cidr(self, service, cidr):
        try:
            network = ip_network(cidr)
        except Exception as error:
            # Print error if CIDR is invalid
            print(error)
            network = None
        if network:
            entry = {
                "Provider": "Datadog",
                "Service": service,
                "Start": int(network.network_address),
                "End": int(network.broadcast_address)
            }
            return entry

    def handle_json(self, response_json):
        """
        Parse Zscaler JSON and build IP range entries.
        Args:
            response_json (dict): Zscaler IP JSON.
        Returns:
            list: List of IP range dicts.
        """
        ip_ranges = []
        for service in response_json:
            if type(response_json[service]) is dict:
                for cidr in response_json[service].get("prefixes_ipv4", []):
                    entry = self.handle_cidr(service, cidr)
                    if entry:
                        ip_ranges.append(entry)
                for cidr in response_json[service].get("prefixes_ipv6", []):
                    entry = self.handle_cidr(service, cidr)
                    if entry:
                        ip_ranges.append(entry)
        return ip_ranges

    def build_ip_ranges(self):
        """
        Build a list of Zscaler IP range entries from the JSON data.
        Returns:
            list: List of IP range dicts.
        """
        ip_json = self.get_ip_json()
        if ip_json:
            ip_ranges = self.handle_json(ip_json)
            return ip_ranges
