from .resource import Resource
from operator import itemgetter
import boto3
import re


class EC2(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.attributes = kwargs["attributes"]
        self.known_attributes = kwargs["known_attributes"]
        self.order_by = kwargs["order_by"]
        self.tag_key = kwargs["tag_key"]
        self.tag_value = kwargs["tag_value"]

        self.ec2 = boto3.resource("ec2")

    def run(self):
        if self.known_attributes:
            self.print_known_attributes_and_return()
            return

        self.print_attributes_for_instances(self.get_instances(order_by=self.order_by))

    def get_instances(self, order_by="launch_time"):
        """Return a list of instances sorted by the "order_by" attribute.
        """
        instances = []

        # If tag_value exists, filter by tag_key and tag_value; otherwise filter
        # to find all resources that have a tag with tag_key, regardless of the
        # tag value.
        if self.tag_value:
            filters = [
                {"Name": f"tag:{tag_key}", "Values": self.tag_value,}
                for tag_key in self.tag_key
            ]
        else:
            filters = [
                {"Name": "tag-key", "Values": self.tag_key,},
            ]

        # Filter instances, sort them by the order_by attribute, then remove the
        # order_by attribute if it is not in the original attributes list.
        attributes = list(self.attributes)
        if not order_by in self.attributes:
            attributes.append(order_by)
        instances = [
            {
                attrib: getattr(inst, attrib, "UNKNOWN_ATTRIBUTE")
                for attrib in attributes
            }
            for inst in self.ec2.instances.filter(Filters=filters)
        ]
        instances = sorted(instances, key=itemgetter(order_by))
        if not order_by in self.attributes:
            instances = [
                {k: v for k, v in inst.items() if k != order_by} for inst in instances
            ]
            print(instances)

        return instances

    def print_attributes_for_instances(self, instances):
        for inst in instances:
            # Here we avoid the complexity of using a f-string and unpacking
            # the values list.
            print(*inst.values(), sep="\t")

    def get_known_attributes(self):
        return [
            "image_id",
            "instance_id",
            "instanceType",
            "key_name",
            "launch_time",
            "monitoring",
            "placement",
            "private_dns_name",
            "private_ip_address",
            "public_dns_name",
            "public_ip_address",
            "subnet_id",
            "vpc_id",
            "block_device_mappings",
            "ebs_optimized",
            "iam_instance_profile",
            "iam_instance_profile",
            "root_device_name",
            "root_device_type",
            "security_groups",
            "tags",
            "owner_id",
        ]
