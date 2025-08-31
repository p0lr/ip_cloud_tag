import json
from ipaddress import ip_address


def read_clouds():
    with open("clouds.json", "r") as file_object:
        return json.load(file_object)


def input_ip():
    input_ip = input("Provide an IP adddress to check against Cloud IP ranges: ")
    try:
        return int(ip_address(input_ip.strip()))
    except:
        print("Invalid IP address")


def tag_clouds(test_ip):
    clouds = read_clouds()
    tags = []
    for cloud_range in clouds:
        if cloud_range["Start"] <= test_ip <= cloud_range["End"]:

            provider = cloud_range.get("Provider")
            if provider is not None and provider != "":
                provider_tag = {"Provider": provider}
                if provider_tag not in tags:
                    tags.append(provider_tag)

            region = cloud_range.get("Region")
            if region is not None and region != "":
                region_tag = {"Region": region}
                if region_tag not in tags:
                    tags.append(region_tag)

            service = cloud_range.get("Service")
            if service is not None and service != "":
                service_tag = {"Service": service}
                if service_tag not in tags:
                    tags.append(service_tag)
    return tags


def main():

    test_ip = input_ip()

    if test_ip:
        tags = tag_clouds(test_ip)
        if tags:
            for tag in tags:
                for key, value in tag.items():
                    print(f"{key}: {value}")


if __name__ == "__main__":
    main()
