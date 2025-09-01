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
* AWS (Amazon Web Services)
* Azure
* Cachefly
* Cloudflare
* Datadog
* DigitalOcean
* Exoscale
* Fastly
* Fortanix
* GCP (Google Cloud Platform)
* GitHub
* Google Workspace
* Imperva
* Linode
* Microsoft365
* OCI (Oracle Cloud Infrastructure)
* Okta
* Salesforce - Hyperforce
* Vultr
* Zendesk
* Zscaler
