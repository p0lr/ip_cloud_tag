from urllib.request import urlopen
import json
from ipaddress import ip_network



class aws:
    """
    AWS IP range handler. Fetches, parses, and builds AWS IP range entries.
    """



    def __init__(self):
        """
        Initialize AWS handler and build IP ranges.
        """
        # Build the AWS IP ranges on initialization
        self.ip_ranges = self.build_aws_ip_ranges()



    def get_aws_ip_json(self):
        """
        Fetch AWS IP ranges JSON from the official URL.
        Returns:
            dict: Parsed JSON data or None on error.
        """
        url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
        # Attempt to fetch the JSON data from AWS
        try:
            aws_response = urlopen(url)
        except Exception as error:
            # Print error if fetch fails
            print(error)
            aws_response = None
        # Parse the JSON if response is valid
        if aws_response:
            try:
                aws_json = json.load(aws_response)
            except:
                # Print error if JSON parsing fails
                aws_json = None
            return aws_json



    def handle_aws_prefix(self, prefix, ipversion=4):
        """
        Parse a prefix entry from AWS JSON and convert to dict.
        Args:
            prefix (dict): Prefix entry from AWS JSON.
            ipversion (int): 4 for IPv4, 6 for IPv6.
        Returns:
            dict: Entry with provider, region, service, start/end IPs.
        """
        # Select the correct CIDR field based on IP version
        if ipversion == 4:
            cidr = prefix.get("ip_prefix")  # IPv4
        else:
            cidr = prefix.get("ipv6_prefix")  # IPv6
        region = prefix.get("region")
        service = prefix.get("service")
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
                "Provider": "AWS",
                "Region": region,
                "Service": service,
                "Start": int(network.network_address),
                "End": int(network.broadcast_address)
            }
            return entry



    def build_aws_ip_ranges(self):
        """
        Build a list of AWS IP range entries from the JSON data.
        Returns:
            list: List of IP range dicts.
        """
        aws_ip_json = self.get_aws_ip_json()
        if aws_ip_json:
            aws_ip_ranges = []
            # Iterate over all IPv4 prefixes in the JSON
            for prefix in aws_ip_json.get("prefixes", []):
                entry = self.handle_aws_prefix(prefix, ipversion=4)
                if entry:
                    aws_ip_ranges.append(entry)
            # Iterate over all IPv6 prefixes in the JSON
            for prefix in aws_ip_json.get("ipv6_prefixes", []):
                entry = self.handle_aws_prefix(prefix, ipversion=6)
                if entry:
                    aws_ip_ranges.append(entry)
            return aws_ip_ranges
