from urllib.request import urlopen
import json
from ipaddress import ip_network


class zendesk:
    """
    IP range handler. Fetches, parses, and builds IP range entries.
    """

    def __init__(self):
        """
        Initialize handler and build IP ranges.
        """
        # Build the IP ranges on initialization
        self.ip_ranges = self.build_ip_ranges()

    def handle_cidr(self, cidr):
        try:
            network = ip_network(cidr)
        except Exception as error:
            # Print error if CIDR is invalid
            print(error)
            network = None
        if network:
            entry = {
                "Provider": "Zendesk",
                "Start": int(network.network_address),
                "End": int(network.broadcast_address)
            }
            return entry

    def build_ip_ranges(self):
        """
        Build a list of IP range entries.
        Returns:
            list: List of IP range dicts.
        """
        ip_ranges = []
        cidrs = [
            "216.198.0.0/18"
        ]
        for cidr in cidrs:
            entry = self.handle_cidr(cidr)
            if entry:
                ip_ranges.append(entry)
        return ip_ranges
