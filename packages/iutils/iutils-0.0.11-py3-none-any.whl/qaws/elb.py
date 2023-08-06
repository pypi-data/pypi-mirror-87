import boto3
import click

from .resource import Resource


class ELB(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.show_limits = kwargs["show_limits"]
        self._list = kwargs["list"]
        self.tag_key = kwargs.get("tag_key")
        self.tag_value = kwargs.get("tag_value")

        self.client = boto3.client("elb")
        self.tagging_api_client = boto3.client("resourcegroupstaggingapi")

    def run(self):
        if self.show_limits:
            self.show_elb_limits()
            return
        if self._list:
            self.list_elbs()

    def show_elb_limits(self):
        limits = []

        paginator = self.client.get_paginator("describe_account_limits")
        pagination_config = {
            "MaxItems": 100,
            "PageSize": 100,  # PageSize should never be greater than MaxItems.
        }

        while True:
            for res in paginator.paginate(PaginationConfig=pagination_config):
                limits += res["Limits"]
            if res.get("NextMarker"):
                pagination_config["StartingToken"] = res["NextMarker"]
            else:
                break

        for item in limits:
            click.echo(f"{item['Name']}: {item['Max']} max")

    def list_elbs(self):
        print(f'Use the "qaws resources --types elasticloadbalancing" command instead.')
