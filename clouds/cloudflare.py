from urllib.request import Request, urlopen
from ipaddress import ip_network


class cloudflare:
    """
    Cloudflare IP range handler. Fetches, parses, and builds Cloudflare IP range entries.
    """


    def __init__(self):
        """
        Initialize Cloudflare handler and build IP ranges.
        """
        self.ip_ranges = self.build_cloudflare_ip_ranges()
    

    def get_cloudflare_url(self, url):
        """
        Fetch a list of IPs from a Cloudflare URL.
        Args:
            url (str): The URL to fetch.
        Returns:
            list: List of IPs as strings.
        """
        cf_request = Request(url, headers={"User-Agent": "Assassin/0.1"})
        # Attempt to fetch the IP list from Cloudflare
        try:
            cf_response = urlopen(cf_request)
        except Exception as error:
            print(error)
            cf_response = None
        if cf_response:
            try:
                cf_text = cf_response.read().decode('utf-8')
                cf_lines = cf_text.splitlines()
            except:
                cf_lines = None
            return [cf_line.strip() for cf_line in cf_lines]
        

    def get_cloudflare_ipv4_list(self):
        """
        Get the list of Cloudflare IPv4 ranges.
        Returns:
            list: List of IPv4 CIDR strings.
        """
        url = "https://www.cloudflare.com/ips-v4"
        ipv4_list = self.get_cloudflare_url(url)
        return ipv4_list
    

    def get_cloudflare_ipv6_list(self):
        """
        Get the list of Cloudflare IPv6 ranges.
        Returns:
            list: List of IPv6 CIDR strings.
        """
        url = "https://www.cloudflare.com/ips-v6/"
        ipv6_list = self.get_cloudflare_url(url)
        return ipv6_list
        

    def handle_cloudflare_prefix(self, cidr):
        """
        Parse a Cloudflare CIDR and convert to dict entry.
        Args:
            cidr (str): CIDR string.
        Returns:
            dict: Entry with provider, start/end IPs.
        """
        # Convert CIDR to network object
        try:
            network = ip_network(cidr)
        except Exception as error:
            print(error)
            network = None
        # Build entry if network is valid
        if network:
            entry = {
                "Provider": "Cloudflare",
                "Start": int(network.network_address),
                "End": int(network.broadcast_address)
            }
            return entry


    def build_cloudflare_ip_ranges(self):
        """
        Build a list of Cloudflare IP range entries from the IP lists.
        Returns:
            list: List of IP range dicts.
        """
        cf_ip_ranges = []
        cf_ipv4_list = self.get_cloudflare_ipv4_list()
        if cf_ipv4_list:
            # Iterate over all IPv4 CIDRs
            for cidr in cf_ipv4_list:
                entry = self.handle_cloudflare_prefix(cidr)
                if entry:
                    cf_ip_ranges.append(entry)
        # ...existing code...
        cf_ipv6_list = self.get_cloudflare_ipv6_list()
        if cf_ipv6_list:
            for cidr in cf_ipv6_list:
                entry = self.handle_cloudflare_prefix(cidr)
                if entry:
                    cf_ip_ranges.append(entry)
        return cf_ip_ranges
