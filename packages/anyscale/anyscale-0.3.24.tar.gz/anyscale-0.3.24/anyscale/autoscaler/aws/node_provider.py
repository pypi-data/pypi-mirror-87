import logging
from typing import Any, Dict, List

# This try block exists because
# 1. This module is passed to the autoscaler on the head node as an external node provider
# 2. Import paths are different for different versions of ray
try:
    from ray.autoscaler._private.aws.node_provider import (
        AWSNodeProvider,
        from_aws_format,
        to_aws_format,
    )
    from ray.autoscaler._private.aws.utils import boto_exception_handler
    from ray.autoscaler._private.log_timer import LogTimer

except ModuleNotFoundError:
    from ray.autoscaler.aws.node_provider import (
        AWSNodeProvider,
        from_aws_format,
        to_aws_format,
    )
    from ray.autoscaler.aws.utils import boto_exception_handler
    from ray.autoscaler.log_timer import LogTimer

from ray.autoscaler.tags import (
    TAG_RAY_CLUSTER_NAME,
    TAG_RAY_NODE_NAME,
)

from anyscale.autoscaler.node_provided_cache import NodeProviderCache
import anyscale.conf

logger = logging.getLogger(__name__)

TAG_ANYSCALE_HOST = "anyscale-host"
node_cache = NodeProviderCache()


class AnyscaleAWSNodeProvider(AWSNodeProvider):  # type: ignore
    def __init__(self, provider_config: Dict[str, Any], cluster_name: str) -> None:
        super().__init__(provider_config, cluster_name)

        self.provider_cache = node_cache

    def create_node(
        self, node_config: Dict[str, Any], tags: Dict[str, str], count: int
    ) -> None:
        # TODO (yiran): Populate cache.
        super().create_node(node_config, tags, count)

    def non_terminated_nodes(self, tag_filters: Dict[str, str]) -> List[str]:
        """Override parent implementation.

        The logic around AWS is exactly the same, but access to the nodes is needed to handle cache
        properly, which cannot be accessed by calling the parent method.
        """
        tag_filters = to_aws_format(tag_filters)
        filters = [
            {"Name": "instance-state-name", "Values": ["pending", "running"]},
            {"Name": f"tag:{TAG_RAY_CLUSTER_NAME}", "Values": [self.cluster_name]},
        ]
        for k, v in tag_filters.items():
            filters.append({"Name": f"tag:{k}", "Values": [v]})

        with boto_exception_handler("Failed to fetch running instances from AWS."):
            nodes = list(self.ec2.instances.filter(Filters=filters))

        # Clear and re-populate cache.
        self.provider_cache.cleanup()
        for node in nodes:
            self.provider_cache.set_node(node.id, node)
            tags = from_aws_format({x["Key"]: x["Value"] for x in node.tags})
            self.provider_cache.set_tags(node.id, tags)

        return [node.id for node in nodes]

    def set_node_tags(self, node_id: str, node_tags: Dict[Any, Any]) -> None:
        """Override parent implementation.

        Set tags synchronously instead of relying on _node_tag_update_loop, so there won't be nodes
        with outdated tags, and total throughput across many node providers can be centrally
        throttled.
        """
        node_tags[TAG_ANYSCALE_HOST] = anyscale.conf.ANYSCALE_HOST

        for k, v in node_tags.items():
            m = "Set tag {}={} on {}".format(k, v, node_id)
            with LogTimer("AWSNodeProvider: {}".format(m)):
                if k == TAG_RAY_NODE_NAME:
                    k = "Name"
                self.ec2.meta.client.create_tags(
                    Resources=[node_id], Tags=[{"Key": k, "Value": v}],
                )

        # Populate cache.
        self.provider_cache.set_tags(node_id, node_tags)

    def node_tags(self, node_id: str) -> Dict[str, str]:
        # Check cache first.
        if self.provider_cache.tags_exist(node_id):
            return self.provider_cache.get_tags(node_id)

        node = super()._get_cached_node(node_id)

        # Populate cache.
        self.provider_cache.set_node(node_id, node)
        tags: Dict[str, str] = from_aws_format(
            {x["Key"]: x["Value"] for x in node.tags}
        )
        self.provider_cache.set_tags(node.id, tags)

        return tags

    def terminate_node(self, node_id: str) -> None:
        # Delete from cache.
        self.provider_cache.delete_node_and_tags(node_id)

        super().terminate_node(node_id)

    def terminate_nodes(self, node_ids: List[str]) -> None:
        # Delete from cache.
        for node_id in node_ids:
            self.provider_cache.delete_node_and_tags(node_id)

        super().terminate_nodes(node_ids)

    def _get_node(self, node_id: str) -> Any:
        # Side effect: clear and updates cache of all nodes.
        # TODO (yiran): make it more granular.
        node = super()._get_node(node_id)

        # Populate cache.
        self.provider_cache.set_node(node_id, node)
        tags = from_aws_format({x["Key"]: x["Value"] for x in node.tags})
        self.provider_cache.set_tags(node.id, tags)

        return node

    def _get_cached_node(self, node_id: str) -> Any:
        # Check cache first.
        if self.provider_cache.node_exists(node_id):
            return self.provider_cache.get_node(node_id)

        node = super()._get_node(node_id)

        # Populate cache.
        self.provider_cache.set_node(node_id, node)
        tags = from_aws_format({x["Key"]: x["Value"] for x in node.tags})
        self.provider_cache.set_tags(node.id, tags)

        return node
