# IP Cloud Tag

This repo is intended to be a subcomponent of a larger attack surface discovery and assessment tool.

This repo builds (build.py) a JSON document (clouds.json) containing the IP address ranges and metadata such as region and service utilized by several cloud and SaaS providers.

You can test an IP address (test.py) and see the cloud/SaaS provider tags that are returned.

The build and test functions live at the root of the repo.  All provider-specific functions called by the build code live in the "clouds" directory.

To add a new provider, write a module to parse its published IP address ranges into the following format for each range:
```
{
  "Provider": "<provider name> (Required)",
  "Region": "<provider region> (Optional)",
  "Service": "<provider service> (Optional)",
  "Start": an interger representing the starting IP address of the range (Required),
  "End": an interget representing the ending IP address of the range (Required)
}
```

## Current Providers and Sources

* Atlassian
  * https://ip-ranges.atlassian.com/
* AWS (Amazon Web Services)
  * https://ip-ranges.amazonaws.com/ip-ranges.json
* Azure
  * Ths URL rotates.  The code finds and utilizes the current latest download link.
* Cachefly
  * https://cachefly.cachefly.net/ips/cdn.txt
* Cloudflare
  * https://www.cloudflare.com/ips-v4
  * https://www.cloudflare.com/ips-v6/
* Datadog
  * https://ip-ranges.datadoghq.com/
* DigitalOcean
  * https://digitalocean.com/geo/google.csv
* Exoscale
  * https://exoscale-prefixes.sos-ch-dk-2.exo.io/exoscale_prefixes.json
* Fastly
  * https://api.fastly.com/public-ip-list
* GCP (Google Cloud Platform)
  * https://www.gstatic.com/ipranges/cloud.json
* Imperva
  * https://my.imperva.com/api/integration/v1/ips
* Linode
  * https://geoip.linode.com/
* OCI (Oracle Cloud Infrastructure)
  * https://docs.oracle.com/en-us/iaas/tools/public_ip_ranges.json
* Okta
  * https://s3.amazonaws.com/okta-ip-ranges/ip_ranges.json
* Salesforce - Hyperforce
  * https://ip-ranges.salesforce.com/ip-ranges.json
* Zendesk
  * Static IP range - 216.198.0.0/18
* Zscaler
  * https://config.zscaler.com/api/zscalerthree.net/cenr/json
  * https://config.zscaler.com/api/zscalertwo.net/cenr/json
  * https://config.zscaler.com/api/zscalerone.net/cenr/json