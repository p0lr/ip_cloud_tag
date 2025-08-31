from urllib.request import urlopen
import json
from ipaddress import ip_network


class gcp:
    """
    GCP IP range handler. Fetches, parses, and builds GCP IP range entries.
    """

    def __init__(self):
        """
        Initialize GCP handler and build IP ranges.
        """
        # Build the GCP IP ranges on initialization
        self.ip_ranges = self.build_gcp_ip_ranges()

    def get_gcp_ip_json(self):
        """
        Fetch GCP IP ranges JSON from the official URL.
        Returns:
            dict: Parsed JSON data or None on error.
        """
        url = "https://www.gstatic.com/ipranges/cloud.json"
        # Attempt to fetch the JSON data from GCP
        try:
            gcp_response = urlopen(url)
        except Exception as error:
            # Print error if fetch fails
            print(error)
            gcp_response = None
        # Parse the JSON if response is valid
        if gcp_response:
            try:
                gcp_json = json.load(gcp_response)
            except:
                # Print error if JSON parsing fails
                gcp_json = None
            return gcp_json

    def handle_gcp_prefix(self, prefix, ipversion=4):
        """
        Parse a prefix entry from GCP JSON and convert to dict.
        Args:
            prefix (dict): Prefix entry from GCP JSON.
            ipversion (int): 4 for IPv4, 6 for IPv6.
        Returns:
            dict: Entry with provider, region, service, start/end IPs.
        """
        # Select the correct CIDR field based on IP version
        if ipversion == 4:
            cidr = prefix.get("ipv4Prefix")  # IPv4
        else:
            cidr = prefix.get("ipv6Prefix")  # IPv6
        service = prefix.get("service")
        scope = prefix.get("scope")
        # Convert CIDR to network object
        try:
            network = ip_network(cidr)
        except Exception as error:
            # Print error if CIDR is invalid
            print(error)
            network = None
        # Build entry if network is valid
        if network:
            entry = {
                "Provider": "GCP",
                "Region": scope,
                "Service": service,
                "Start": int(network.network_address),
                "End": int(network.broadcast_address)
            }
            return entry

    def build_gcp_ip_ranges(self):
        """
        Build a list of GCP IP range entries from the JSON data.
        Returns:
            list: List of IP range dicts.
        """
        gcp_ip_json = self.get_gcp_ip_json()
        if gcp_ip_json:
            gcp_ip_ranges = []
            # Iterate over all prefixes in the JSON
            for prefix in gcp_ip_json.get("prefixes", []):
                if "ipv4Prefix" in prefix:
                    entry = self.handle_gcp_prefix(prefix, ipversion=4)
                elif "ipv6Prefix" in prefix:
                    entry = self.handle_gcp_prefix(prefix, ipversion=6)
                else:
                    entry = None
                if entry:
                    gcp_ip_ranges.append(entry)
            return gcp_ip_ranges
