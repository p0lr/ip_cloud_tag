from urllib.request import Request, urlopen
from ipaddress import ip_network


class linode:
    """
    Linode IP range handler. Fetches, parses, and builds Linode IP range entries.
    """

    def __init__(self):
        """
        Initialize Linode handler and build IP ranges.
        """
        # Build the Linode IP ranges on initialization
        self.ip_ranges = self.build_linode_ip_ranges()

    def get_linode_ip_list(self):
        """
        Fetch Linode IP ranges list from the official URL.
        Returns:
            list: List of IPs as strings.
        """
        url = "https://geoip.linode.com/"
        request = Request(url, headers={"User-Agent": "Assassin/0.1"})
        # Attempt to fetch the IP list from Linode
        try:
            linode_response = urlopen(request)
        except Exception as error:
            # Print error if fetch fails
            print(error)
            linode_response = None
        if linode_response:
            try:
                linode_lines = [line for line in linode_response.read().decode('utf-8').splitlines() if line[0] != "#"]
            except:
                # Print error if parsing fails
                linode_lines = None
            return linode_lines

    def handle_linode_line(self, line):
        """
        Parse a line from Linode IP list and convert to dict entry.
        Args:
            line (str): CSV line.
        Returns:
            dict: Entry with provider, region, start/end IPs.
        """
        line_parts = line.strip().split(",")
        cidr = line_parts[0]
        country = line_parts[1]
        country_state = line_parts[2]
        city = line_parts[3]
        region = f"{country_state}-{city}"
        # Convert CIDR to network object
        try:
            network = ip_network(cidr)
        except Exception as error:
            # Print error if CIDR is invalid
            print(error)
            network = None
        # ...existing code...
        
        if network:
            entry = {
                "Provider": "Linode",
                "Region": region,
                "Start": int(network.network_address),
                "End": int(network.broadcast_address)
            }
            
            return entry

    def build_linode_ip_ranges(self):
        linode_ip_ranges = []
        linode_ip_list = self.get_linode_ip_list()
        if linode_ip_list:
            for line in linode_ip_list:
                entry = self.handle_linode_line(line)
                if entry:
                    linode_ip_ranges.append(entry)
        return linode_ip_ranges
