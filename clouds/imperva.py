from urllib.request import urlopen
import json
from ipaddress import ip_network


class imperva:
    """
    Imperva IP range handler. Fetches, parses, and builds Imperva IP range entries.
    """

    def __init__(self):
        """
        Initialize Imperva handler and build IP ranges.
        """
        # Build the Imperva IP ranges on initialization
        self.ip_ranges = self.build_imperva_ip_ranges()

    def get_imperva_ip_json(self):
        """
        Fetch Imperva IP ranges JSON from the official URL.
        Returns:
            dict: Parsed JSON data or None on error.
        """
        url = "https://my.imperva.com/api/integration/v1/ips"
        # Attempt to fetch the JSON data from Imperva
        try:
            imperva_response = urlopen(url)
        except Exception as error:
            # Print error if fetch fails
            print(error)
            imperva_response = None
        # Parse the JSON if response is valid
        if imperva_response:
            try:
                imperva_json = json.load(imperva_response)
            except:
                # Print error if JSON parsing fails
                imperva_json = None
            return imperva_json

    def handle_imperva_json(self, imperva_ip_json):
        """
        Parse Imperva JSON and build IP range entries.
        Args:
            imperva_ip_json (dict): Imperva IP JSON.
        Returns:
            list: List of IP range dicts.
        """
        imperva_ip_ranges = []
        # Iterate over all IPv4 ranges in the JSON
        for cidr in imperva_ip_json.get("ipRanges", []):
            try:
                network = ip_network(cidr)
            except Exception as error:
                # Print error if CIDR is invalid
                print(error)
                network = None
            if network:
                entry = {
                    "Provider": "Imperva",
                    "Start": int(network.network_address),
                    "End": int(network.broadcast_address)
                }
                imperva_ip_ranges.append(entry)
        # Iterate over all IPv6 ranges in the JSON
        for cidr in imperva_ip_json.get("ipv6Ranges", []):
            try:
                network = ip_network(cidr)
            except Exception as error:
                # Print error if CIDR is invalid
                print(error)
                network = None
            if network:
                entry = {
                    "Provider": "Imperva",
                    "Start": int(network.network_address),
                    "End": int(network.broadcast_address)
                }
                imperva_ip_ranges.append(entry)
        return imperva_ip_ranges

    def build_imperva_ip_ranges(self):
        """
        Build a list of Imperva IP range entries from the JSON data.
        Returns:
            list: List of IP range dicts.
        """
        imperva_ip_json = self.get_imperva_ip_json()
        if imperva_ip_json:
            imperva_ip_ranges = self.handle_imperva_json(imperva_ip_json)
            return imperva_ip_ranges
