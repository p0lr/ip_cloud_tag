from urllib.request import urlopen
import json
from ipaddress import ip_network


class exoscale:
    """
    Exoscale IP range handler. Fetches, parses, and builds Exoscale IP range entries.
    """

    def __init__(self):
        """
        Initialize Exoscale handler and build IP ranges.
        """
        self.ip_ranges = self.build_exoscale_ip_ranges()

    def get_exoscale_ip_json(self):
        """
        Fetch Exoscale IP ranges JSON from the official URL.
        Returns:
            dict: Parsed JSON data or None on error.
        """
        url = "https://exoscale-prefixes.sos-ch-dk-2.exo.io/exoscale_prefixes.json"
        # Attempt to fetch the JSON data from Exoscale
        try:
            exoscale_response = urlopen(url)
        except:
            exoscale_response = None
        if exoscale_response:
            try:
                exoscale_json = json.load(exoscale_response)
            except:
                exoscale_json = None
            return exoscale_json

    def handle_exoscale_json_download(self, exoscale_ip_json):
        """
        Parse Exoscale JSON and build IP range entries.
        Args:
            exoscale_ip_json (dict): Exoscale prefixes JSON.
        Returns:
            list: List of IP range dicts.
        """
        exoscale_ip_ranges = []
        # Iterate over all prefixes in the JSON
        for prefix_container in exoscale_ip_json.get("prefixes", []):
            region = prefix_container.get("zone")
            cidr = prefix_container.get("IPv4Prefix")
            if not cidr:
                cidr = prefix_container.get("IPv6Prefix")
            if cidr:
                try:
                    network = ip_network(cidr)
                except Exception as error:
                    print(error)
                    network = None
                # ...existing code...
        
                if network:
                    entry = {
                        "Provider": "Exoscale",
                        "Region": region,
                        "Start": int(network.network_address),
                        "End": int(network.broadcast_address)
                    }
                    exoscale_ip_ranges.append(entry)

        return exoscale_ip_ranges

    def build_exoscale_ip_ranges(self):
        exoscale_ip_json = self.get_exoscale_ip_json()
        if exoscale_ip_json:
            exoscale_ip_ranges = self.handle_exoscale_json_download(exoscale_ip_json)
            return exoscale_ip_ranges
