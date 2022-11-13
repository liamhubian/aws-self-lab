import boto3


ec2 = boto3.resource('ec2')


def main():
    vpc = ec2.Vpc('vpc-0fddc2bd5429f4fbe')

    print_vpc(vpc)

    print("\n", "-" * 150, "\n")
    print_subnets(vpc)
    
    print("\n", "-" * 150, "\n")
    print_route_table_associations_attribute(vpc)
    
    print("\n", "-" * 150, "\n")
    print_route_tables(vpc)

    print("\n", "-" * 150, "\n")
    print_vpc_instances(vpc)

def print_vpc(vpc):
    
    print("*** VPC INFORMATION ***\n")
    print("VPC ID:", vpc.id)
    print("Name  :", get_tag_name(vpc.tags))
    print("CIDR  :", vpc.cidr_block)
    print("Owner :", vpc.owner_id)

def print_subnets(vpc):

    print("SUBNET LIST\n")
    print("| {:<25} | {:<30} | {:<15} | {:<28} | {:<15} |".format("subnet_id", "name", "CIDR", "AZ", "auto map ipv4"))
    print("| {} | {} | {} | {} | {} |".format("-" * 25, "-" * 30, "-" * 15, "-" * 28, "-" * 15))
    for subnet in vpc.subnets.all():
        print("| {:<25} | {:<30} | {:<15} | {:<15} ({:<10}) | {:<15} |"
                .format(subnet.id, get_tag_name(subnet.tags), subnet.cidr_block, subnet.availability_zone, subnet.availability_zone_id, subnet.map_public_ip_on_launch))

def print_route_table_associations_attribute(vpc):

    print("ROUTE TABLE ASSOCIATION\n")
    print("| {:<30} | {:<25} | {:<25} | {:<5} |".format("association id", "rtb_id", "subnet_id", "main"))
    print("| {} | {} | {} | {} |".format("-" * 30, "-" * 25, "-" * 25, "-" * 5))

    for rtb in vpc.route_tables.all():
        for att in rtb.associations_attribute:
            print("| {:<30} | {:<25} | {:<25} | {:<5} |"
                    .format(att["RouteTableAssociationId"], att["RouteTableId"], att["SubnetId"] if "SubnetId" in att else "", att["Main"]))

def print_route_tables(vpc):

    print("ROUTE TABLE ROUTES\n")
    print("| {:<25} | {:<30} | {:<15} | {:<25} |".format("rtb_id", "name", "destination", "target"))
    print("| {} | {} | {} | {} |".format("-" * 25, "-" * 30, "-" * 15, "-" * 25))

    for rtb in vpc.route_tables.all():
        print("| {:<25} | {:<30} | {:<15} | {:<25} |".format(rtb.id, get_tag_name(rtb.tags), "", ""))

        for att in rtb.routes_attribute:
            print("| {:<25} | {:<30} | {:<15} | {:<25} |".format("", "", get_rtb_att_destination(att), get_rtb_att_target(att)))

def print_vpc_instances(vpc):

    print("INSTANCES RUN IN VPC\n")
    print("| {:<25} | {:<30} | {:<15} | {:<15} | {:<25} |".format("instance_id", "name", "public_ip", "private_ip", "SG"))
    print("| {} | {} | {} | {} | {} |".format("-" * 25, "-" * 30, "-" * 15, "-" * 15, "-" * 25))
    for instance in vpc.instances.all():
        print("| {:<25} | {:<30} | {:<15} | {:<15} | {:<25} |"
                .format(instance.id, get_tag_name(instance.tags), instance.public_ip_address, instance.private_ip_address, str(instance.security_groups)))

def print_vpc_security_group(vpc):

    print("SECURITY GROUPS\n")
    print("| {:<25} | {:<30} | {:<15} | {:<15} | {:<25} |".format("group_id", "group_name", "from port", "protocol", "ip range"))
    print("| {} | {} | {} | {} | {} |".format("-" * 25, "-" * 30, "-" * 15, "-" * 15, "-" * 25))
    for instance in vpc.instances.all():
        print("| {:<25} | {:<30} | {:<15} | {:<15} | {:<25} |"
                .format(instance.id, get_tag_name(instance.tags), instance.public_ip_address, instance.private_ip_address, str(instance.security_groups)))


def get_tag_name(tag_list):
    for tag in tag_list:
        if tag["Key"] == "Name" or tag["Key"] == "name":
            return tag["Value"]
    return "<no tag Name>"

def get_rtb_att_destination(att):
    if "DestinationCidrBlock" in att:
        return att["DestinationCidrBlock"]
    elif "DestinationIpv6CidrBlock" in att:
        return att["DestinationIpv6CidrBlock"]
    elif "DestinationIpv6CidrBlock" in att:
        return att["DestinationIpv6CidrBlock"]
    else:
        return "Unreachable destination"

def get_rtb_att_target(att):
    if "DestinationIpv6CidrBlock" in att:
        return att["DestinationIpv6CidrBlock"]
    elif "GatewayId" in att:
        return att["GatewayId"]
    elif "InstanceId" in att:
        return att["InstanceId"]
    elif "NatGatewayId" in att:
        return att["NatGatewayId"]
    elif "TransitGatewayId" in att:
        return att["TransitGatewayId"]
    elif "LocalGatewayId" in att:
        return att["LocalGatewayId"]
    elif "NatGatewayId" in att:
        return att["NatGatewayId"]
    else:
        return "Unreachable destination"

if __name__ == "__main__":
    main()

