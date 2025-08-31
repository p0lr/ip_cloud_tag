import json

def main():
    """
    Main function to collect IP ranges from all cloud providers and write them to a JSON file.
    """
    # List to store all IP ranges from all providers
    cloud_ranges = []

    # Import and collect IP ranges from each provider
    from clouds.atlassian import atlassian
    atlassian_ips = atlassian()  # Instantiate Atlassian provider
    atlassian_ip_ranges = atlassian_ips.ip_ranges  # Get IP ranges
    if atlassian_ip_ranges:
        print(f"Retrieved {len(atlassian_ip_ranges)} Atlassian IP ranges.")
        cloud_ranges.extend(atlassian_ip_ranges)

    from clouds.aws import aws
    aws_ips = aws()
    aws_ip_ranges = aws_ips.ip_ranges
    if aws_ip_ranges:
        print(f"Retrieved {len(aws_ip_ranges)} AWS IP ranges.")
        cloud_ranges.extend(aws_ip_ranges)

    from clouds.azure import azure
    azure_ips = azure()
    azure_ip_ranges = azure_ips.ip_ranges
    if azure_ip_ranges:
        print(f"Retrieved {len(azure_ip_ranges)} Azure IP ranges.")
        cloud_ranges.extend(azure_ip_ranges)

    from clouds.cachefly import cachefly
    cachefly_ips = cachefly()
    cachefly_ip_ranges = cachefly_ips.ip_ranges
    if cachefly_ip_ranges:
        print(f"Retrieved {len(cachefly_ip_ranges)} Cachefly IP ranges.")
        cloud_ranges.extend(cachefly_ip_ranges)

    from clouds.cloudflare import cloudflare
    cf_ips = cloudflare()
    cf_ip_ranges = cf_ips.ip_ranges
    if cf_ip_ranges:
        print(f"Retrieved {len(cf_ip_ranges)} Cloudflare IP ranges.")
        cloud_ranges.extend(cf_ip_ranges)
    
    from clouds.datadog import datadog
    datadog_ips = datadog()
    datadog_ip_ranges = datadog_ips.ip_ranges
    if datadog_ip_ranges:
        print(f"Retrieved {len(datadog_ip_ranges)} Datadog IP ranges.")
        cloud_ranges.extend(datadog_ip_ranges)

    from clouds.digitalocean import digitalocean
    do_ips = digitalocean()
    do_ip_ranges = do_ips.ip_ranges
    if do_ip_ranges:
        print(f"Retrieved {len(do_ip_ranges)} DigitalOcean IP ranges.")
        cloud_ranges.extend(do_ip_ranges)

    from clouds.exoscale import exoscale
    exoscale_ips = exoscale()
    exoscale_ip_ranges = exoscale_ips.ip_ranges
    if exoscale_ip_ranges:
        print(f"Retrieved {len(exoscale_ip_ranges)} Exoscale IP ranges.")
        cloud_ranges.extend(exoscale_ip_ranges)

    from clouds.fastly import fastly
    fastly_ips = fastly()
    fastly_ip_ranges = fastly_ips.ip_ranges
    if fastly_ip_ranges:
        print(f"Retrieved {len(fastly_ip_ranges)} Fastly IP ranges.")
        cloud_ranges.extend(fastly_ip_ranges)

    from clouds.gcp import gcp
    gcp_ips = gcp()
    gcp_ip_ranges = gcp_ips.ip_ranges
    if gcp_ip_ranges:
        print(f"Retrieved {len(gcp_ip_ranges)} GCP IP ranges.")
        cloud_ranges.extend(gcp_ip_ranges)

    from clouds.imperva import imperva
    imperva_ips = imperva()
    imperva_ip_ranges = imperva_ips.ip_ranges
    if imperva_ip_ranges:
        print(f"Retrieved {len(imperva_ip_ranges)} Imperva IP ranges.")
        cloud_ranges.extend(imperva_ip_ranges)

    from clouds.linode import linode
    linode_ips = linode()
    linode_ip_ranges = linode_ips.ip_ranges
    if linode_ip_ranges:
        print(f"Retrieved {len(linode_ip_ranges)} Linode IP ranges.")
        cloud_ranges.extend(linode_ip_ranges)

    from clouds.oci import oci
    oci_ips = oci()
    oci_ip_ranges = oci_ips.ip_ranges
    if oci_ip_ranges:
        print(f"Retrieved {len(oci_ip_ranges)} OCI IP ranges.")
        cloud_ranges.extend(oci_ip_ranges)

    from clouds.okta import okta
    okta_ips = okta()
    okta_ip_ranges = okta_ips.ip_ranges
    if okta_ip_ranges:
        print(f"Retrieved {len(okta_ip_ranges)} Okta IP ranges.")
        cloud_ranges.extend(okta_ip_ranges)
    
    from clouds.salesforce import salesforce
    salesforce_ips = salesforce()
    salesforce_ip_ranges = salesforce_ips.ip_ranges
    if salesforce_ip_ranges:
        print(f"Retrieved {len(salesforce_ip_ranges)} Salesforce IP ranges.")
        cloud_ranges.extend(salesforce_ip_ranges)

    from clouds.zscaler import zscaler
    zscaler_ips = zscaler()
    zscaler_ip_ranges = zscaler_ips.ip_ranges
    if zscaler_ip_ranges:
        print(f"Retrieved {len(zscaler_ip_ranges)} Zscaler IP ranges.")
        cloud_ranges.extend(zscaler_ip_ranges)

    # Print total number of IP ranges collected
    print(f"Total IP ranges collected: {len(cloud_ranges)}")

    # Write all collected IP ranges to clouds.json
    with open("clouds.json", "w") as file_object:
        json.dump(cloud_ranges, file_object, indent=4)

# Entry point for the build script. Calls main().
if __name__ == "__main__":
    main()