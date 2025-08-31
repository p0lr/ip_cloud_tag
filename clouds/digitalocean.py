from urllib.request import Request, urlopen
from ipaddress import ip_network


class digitalocean:
    """
    DigitalOcean IP range handler. Fetches, parses, and builds DigitalOcean IP range entries.
    """

    def __init__(self):
        """
        Initialize DigitalOcean handler and build IP ranges.
        """
        self.ip_ranges = self.build_digitalocean_ip_ranges()

    def get_digitalocean_ip_csv(self):
        """
        Fetch DigitalOcean IP ranges CSV from the official URL.
        Returns:
            list: List of CSV lines as strings.
        """
        url = "https://digitalocean.com/geo/google.csv"
        request = Request(url, headers={"User-Agent": "Assassin/0.1"})
        # Attempt to fetch the CSV data from DigitalOcean
        try:
            do_response = urlopen(request)
        except Exception as error:
            print(error)
            do_response = None
        if do_response:
            try:
                do_text = do_response.read().decode('utf-8')
                do_lines = do_text.splitlines()
            except:
                do_lines = None
            return [do_line.strip() for do_line in do_lines]

    def handle_digitalocean_line(self, line):
        """
        Parse a line from DigitalOcean CSV and convert to dict entry.
        Args:
            line (str): CSV line.
        Returns:
            dict: Entry with provider, region, start/end IPs.
        """
        line_parts = line.split(",")
        cidr = line_parts[0]
        country = line_parts[1]
        country_state = line_parts[2]
        city = line_parts[3]
        # Convert CIDR to network object
        try:
            network = ip_network(cidr)
        except Exception as error:
            print(error)
            network = None
        # Build entry if network is valid
        if network:
            entry = {
                "Provider": "DigitalOcean",
                "Region": f"{country_state}-{city}",
                "Start": int(network.network_address),
                "End": int(network.broadcast_address)
            }
            return entry

    def build_digitalocean_ip_ranges(self):
        """
        Build a list of DigitalOcean IP range entries from the CSV data.
        Returns:
            list: List of IP range dicts.
        """
        do_ip_ranges = []
        do_cidr_list = self.get_digitalocean_ip_csv()
        if do_cidr_list:
            # Iterate over all lines in the CSV
            for line in do_cidr_list:
                entry = self.handle_digitalocean_line(line)
                if entry:
                    do_ip_ranges.append(entry)
        return do_ip_ranges
