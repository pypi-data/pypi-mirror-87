import boto3


class Resources:
    def __init__(self, *args, **kwargs):
        self.types = kwargs["types"]
        self.with_tags = kwargs["with_tags"]
        self.count_by_service = kwargs["count_by_service"]

        self.client = boto3.client("resourcegroupstaggingapi")

    def run(self):
        resources = []
        paginator = self.client.get_paginator("get_resources")

        tag_filters = self._get_tag_filters(self.with_tags)
        resource_type_filters = self.types
        pagination_config = {
            "PageSize": 100,
        }

        while True:
            for res in paginator.paginate(
                TagFilters=tag_filters,
                ResourceTypeFilters=resource_type_filters,
                IncludeComplianceDetails=False,
                ExcludeCompliantResources=False,
                PaginationConfig=pagination_config,
            ):
                resources += [
                    item["ResourceARN"] for item in res["ResourceTagMappingList"]
                ]
            if res.get("NextMarker"):
                pagination_config["StartingToken"] = res["NextMarker"]
            else:
                break

        if self.count_by_service:
            self.show_resource_count_by_service(resources)
            return

        for item in sorted(resources):
            print(item)

    def show_resource_count_by_service(self, resource_arns):
        table = {}
        for arn in resource_arns:
            # See https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html
            # for ARN examples.
            splitted_arn = arn.split(":")
            if len(splitted_arn) == 6:
                (_, _, service, region, account_id, resource_with_id) = splitted_arn
                # Some resource ids (e.g. cloudformation stack) may contain slashes, thus
                # we just take the item of the first column.
                resource_type = resource_with_id.split("/")[0]
            elif len(splitted_arn) == 7:
                (
                    _,
                    _,
                    service,
                    region,
                    account_id,
                    resource_type,
                    resource_id,
                ) = splitted_arn
            else:
                raise ValueError(f"Un-recognized ARN: {arn}")

            if not service in table:
                table[service] = 1
            else:
                table[service] += 1
            if not f"{service}:{resource_type}" in table:
                table[f"{service}:{resource_type}"] = 1
            else:
                table[f"{service}:{resource_type}"] += 1

        for key in sorted(table.keys()):
            print(f"{key}: {table[key]}")

    def _get_tag_filters(self, tags):
        filters = []

        for tag in tags:
            key, value = tag.split(":")
            if value:
                filters.append({"Key": key, "Values": value.split(",")})
            else:
                filters.append({"Key": key})

        return filters
