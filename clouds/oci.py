from urllib.request import urlopen
import json
from ipaddress import ip_network


class oci:
    """
    OCI IP range handler. Fetches, parses, and builds Oracle Cloud IP range entries.
    """

    def __init__(self):
        """
        Initialize OCI handler and build IP ranges.
        """
        # Build the OCI IP ranges on initialization
        self.ip_ranges = self.build_oci_ip_ranges()

    def get_oci_ip_json(self):
        """
        Fetch OCI IP ranges JSON from the official URL.
        Returns:
            dict: Parsed JSON data or None on error.
        """
        url = "https://docs.oracle.com/en-us/iaas/tools/public_ip_ranges.json"
        # Attempt to fetch the JSON data from Oracle Cloud
        try:
            oci_response = urlopen(url)
        except Exception as error:
            # Print error if fetch fails
            print(error)
            oci_response = None
        # Parse the JSON if response is valid
        if oci_response:
            try:
                oci_json = json.load(oci_response)
            except:
                # Print error if JSON parsing fails
                oci_json = None
            return oci_json

    def handle_oci_json_download(self, oci_ip_json):
        """
        Parse OCI JSON and build IP range entries.
        Args:
            oci_ip_json (dict): OCI IP JSON.
        Returns:
            list: List of IP range dicts.
        """
        oci_ip_ranges = []
        # Iterate over all regions in the JSON
        for region_container in oci_ip_json.get("regions", []):
            region_name = region_container.get("region")
            for cidr_container in region_container.get("cidrs", []):
                provider = "OCI"
                region = region_name
                cidr = cidr_container.get("cidr")
                for service in cidr_container.get("tags", []):
                    try:
                        network = ip_network(cidr)
                    except Exception as error:
                        # Print error if CIDR is invalid
                        print(error)
                        network = None
                    # ...existing code...
            
                    if network:
                        entry = {
                            "Provider": provider,
                            "Region": region,
                            "Service": service,
                            "Start": int(network.network_address),
                            "End": int(network.broadcast_address)
                        }
                        oci_ip_ranges.append(entry)

        return oci_ip_ranges

    def build_oci_ip_ranges(self):
        oci_ip_json = self.get_oci_ip_json()
        if oci_ip_json:
            oci_ip_ranges = self.handle_oci_json_download(oci_ip_json)
            return oci_ip_ranges
