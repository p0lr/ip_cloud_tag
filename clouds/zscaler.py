from urllib.request import urlopen
import json
from ipaddress import ip_network


class zscaler:
    """
    Zscaler IP range handler. Fetches, parses, and builds Zscaler IP range entries.
    """

    def __init__(self):
        """
        Initialize Zscaler handler and build IP ranges.
        """
        # Build the Zscaler IP ranges on initialization
        self.ip_ranges = self.build_ip_ranges()

    def get_ip_json(self, url):
        """
        Fetch Zscaler IP ranges JSON from the official URL.
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
        Parse Zscaler JSON and build IP range entries.
        Args:
            response_json (dict): Zscaler IP JSON.
        Returns:
            list: List of IP range dicts.
        """
        ip_ranges = []
        # Iterate over all clouds in the JSON
        for cloud in response_json:
            for continent in response_json[cloud]:
                continent_name = continent.split(":")[1].strip()
                for city in response_json[cloud][continent]:
                    city_name = city.split(":")[1].strip()
                    for container in response_json[cloud][continent][city]:
                        cidr = container.get("range")
                        region = f"{continent_name}-{city_name}"
                        try:
                            network = ip_network(cidr)
                        except Exception as error:
                            # Print error if CIDR is invalid
                            print(error)
                            network = None
                        if network:
                            entry = {
                                "Provider": "Zscaler",
                                "Region": region,
                                "Start": int(network.network_address),
                                "End": int(network.broadcast_address)
                            }
                            ip_ranges.append(entry)
        return ip_ranges

    def build_ip_ranges(self):
        """
        Build a list of Zscaler IP range entries from the JSON data.
        Returns:
            list: List of IP range dicts.
        """
        urls = [
            "https://config.zscaler.com/api/zscalerthree.net/cenr/json",
            "https://config.zscaler.com/api/zscalertwo.net/cenr/json",
            "https://config.zscaler.com/api/zscalerone.net/cenr/json"
        ]
        ranges = []
        for url in urls:
            ip_json = self.get_ip_json(url)
            if ip_json:
                ip_ranges = self.handle_json(ip_json)
                ranges.extend(ip_ranges)
        return ranges
