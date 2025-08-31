from urllib.request import urlopen
from ipaddress import ip_network


class cachefly:
    """
    Cachefly IP range handler. Fetches, parses, and builds Cachefly IP range entries.
    """

    def __init__(self):
        """
        Initialize Cachefly handler and build IP ranges.
        """
        # Build the Cachefly IP ranges on initialization
        self.ip_ranges = self.build_cachefly_ip_ranges()

    def get_cachefly_ip_list(self):
        """
        Fetch Cachefly IP ranges list from the official URL.
        Returns:
            list: List of IPs as strings.
        """
        url = "https://cachefly.cachefly.net/ips/cdn.txt"
        # Attempt to fetch the IP list from Cachefly
        try:
            cachefly_response = urlopen(url)
        except Exception as error:
            # Print error if fetch fails
            print(error)
            cachefly_response = None
        if cachefly_response:
            try:
                cachefly_lines = [line for line in cachefly_response.read().decode('utf-8').splitlines() if line[0] != "#"]
            except:
                # Print error if parsing fails
                cachefly_lines = None
            return cachefly_lines

    def handle_cachefly_line(self, line):
        """
        Parse a line from Cachefly IP list and convert to dict entry.
        Args:
            line (str): IP line.
        Returns:
            dict: Entry with provider, start/end IPs.
        """
        # Convert line to network object
        try:
            network = ip_network(line)
        except Exception as error:
            # Print error if CIDR is invalid
            print(error)
            network = None
        # Build entry if network is valid
        if network:
            entry = {
                "Provider": "Cachefly",
                "Start": int(network.network_address),
                "End": int(network.broadcast_address)
            }
            return entry

    def build_cachefly_ip_ranges(self):
        cachefly_ip_ranges = []
        cachefly_ip_list = self.get_cachefly_ip_list()
        if cachefly_ip_list:
            for line in cachefly_ip_list:
                entry = self.handle_cachefly_line(line)
                if entry:
                    cachefly_ip_ranges.append(entry)
        return cachefly_ip_ranges
