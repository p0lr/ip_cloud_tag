from urllib.request import urlopen
import json
from ipaddress import ip_network


class azure:
    """
    Azure IP range handler. Fetches, parses, and builds Azure IP range entries.
    """


    def __init__(self):
        """
        Initialize Azure handler and build IP ranges.
        """
        self.ip_ranges = self.build_azure_ip_ranges()


    def get_azure_bootstrap_url(self):
        """
        Fetch the Azure ServiceTags JSON download URL from the bootstrap page.
        Returns:
            str: Direct download URL for the ServiceTags JSON.
        """
        url = "https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519"
        # Fetch the bootstrap page and extract the download date
        try:
            bootstrap_response = urlopen(url).read().decode('utf-8')
        except:
            bootstrap_response = None
        if bootstrap_response:
            url_start = bootstrap_response.find("ServiceTags_Public_") + len("ServiceTags_Public_")
            url_end = bootstrap_response.find(".json", url_start)
            download_date = bootstrap_response[url_start:url_end]
            return f"https://download.microsoft.com/download/7/1/d/71d86715-5596-4529-9b13-da13a5de5b63/ServiceTags_Public_{download_date}.json"
        

    def get_azure_ip_json(self):
        """
        Fetch Azure IP ranges JSON from the download URL.
        Returns:
            dict: Parsed JSON data or None on error.
        """
        download_url = self.get_azure_bootstrap_url()
        if download_url:
            try:
                azure_response = urlopen(download_url)
            except:
                azure_response = None
            try:
                azure_json = json.load(azure_response)
            except:
                azure_json = None
            return azure_json
    

    def handle_azure_json_download(self, azure_ip_json):
        """
        Parse Azure JSON and build IP range entries.
        Args:
            azure_ip_json (dict): Azure ServiceTags JSON.
        Returns:
            list: List of IP range dicts.
        """
        values = azure_ip_json.get("values", [])
        azure_ip_ranges = []
        # Iterate over all values in the JSON
        for value in values:
            properties = value.get("properties", {})
            provider = properties.get("platform")
            region = properties.get("region")
            service = properties.get("systemService")
            address_prefixes = properties.get("addressPrefixes", [])
            for cidr in address_prefixes:
                try:
                    network = ip_network(cidr)
                except Exception as error:
                    print(error)
                    network = None
                if network:
                    entry = {
                        "Provider": provider,
                        "Region": region,
                        "Service": service,
                        "Start": int(network.network_address),
                        "End": int(network.broadcast_address)
                    }
                    azure_ip_ranges.append(entry)
        return azure_ip_ranges


    def build_azure_ip_ranges(self):
        """
        Build a list of Azure IP range entries from the JSON data.
        Returns:
            list: List of IP range dicts.
        """
        azure_ip_json = self.get_azure_ip_json()
        if azure_ip_json:
            azure_ip_ranges = self.handle_azure_json_download(azure_ip_json)
            return azure_ip_ranges
