"""NodeProvider classes that add product-specific behaviour."""

import logging
from typing import Any, Dict, List

# This try block exists because
# 1. This module is passed to the autoscaler on the head node as an external node provider
# 2. Import paths are different for different versions of ray
try:
    from ray.autoscaler._private.aws.node_provider import NodeProvider
    from ray.autoscaler._private.providers import (
        _get_node_provider,
        _NODE_PROVIDERS,
    )
except ModuleNotFoundError:
    from ray.autoscaler.aws.node_provider import NodeProvider
    from ray.autoscaler.node_provider import (
        get_node_provider as _get_node_provider,
        NODE_PROVIDERS as _NODE_PROVIDERS,
    )

logger = logging.getLogger(__name__)


class AnyscalePoolingNodeProvider:
    """NodeProvider wrapper for injecting product-specific functionality.

    Currently a no-op wrapper,
    but we plan on adding instance pool functionality here soon:
        https://docs.google.com/document/d/15goOexCiGkbzz7tUbILMc10Gmjf86PiyCtIl75-xGUw/edit
    """

    def __init__(self, provider_config: Dict[str, Any], cluster_name: str) -> None:
        """Implements manual inheritance from NodeProvider.

        This class follows the signature of the NodeProvider base class.
        However, we are not inheriting from NodeProvider
        because we are wrapping around a class that is
        dynamically provided in provider_config;
        we implement this inheritance manually using __getattr__.

        provider_config:
            a configuration dictionary as per the NodeProvider base class,
            but must also have a "inner_provider" key.
            The "inner_provider" field is the provider_config
            of the original NodeProvider class which we are wrapping around.
        """

        inner_provider_config = provider_config["inner_provider"]
        # This is the actual NodeProvider object we are wrapping around.
        self.inner_provider = _get_node_provider(inner_provider_config, cluster_name)

    @staticmethod
    def _get_inner_provider_class_from_config(cluster_config: Dict[str, Any]) -> Any:
        """Helper for passing through static methods.

        NodeProvider has static methods.
        To pass these through to an inner provider object,
        we must also have a static method for getting the inner provider class.

        This is a helper method takes a cluster_config and returns the
        *class* (not the object) of the inner provider.
        """
        inner_provider_config = cluster_config["provider"]["inner_provider"]
        importer = _NODE_PROVIDERS.get(inner_provider_config["type"])
        inner_provider_cls = importer(inner_provider_config)
        return inner_provider_cls

    @staticmethod
    def bootstrap_config(cluster_config: Dict[str, Any]) -> Dict[str, Any]:
        # Get the inner_provider class for the static method.
        inner_provider_cls = AnyscalePoolingNodeProvider._get_inner_provider_class_from_config(
            cluster_config
        )

        # We can't just call the inner_provider method directly,
        # since it expects cluster_config["provider"] to be its own class.
        # Thus, we'll swap in the inner_provider for the primary provider first
        # (and save the primary provider for later).
        primary_provider = cluster_config["provider"]
        cluster_config["provider"] = cluster_config["provider"]["inner_provider"]

        # Pass through to submethod.
        cluster_config = inner_provider_cls.bootstrap_config(cluster_config)

        # Restore primary provider.
        primary_provider["inner_provider"] = cluster_config["provider"]
        cluster_config["provider"] = primary_provider
        return cluster_config

    @staticmethod
    def fillout_available_node_types_resources(
        cluster_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        inner_provider_cls = AnyscalePoolingNodeProvider._get_inner_provider_class_from_config(
            cluster_config
        )

        primary_provider = cluster_config["provider"]
        cluster_config["provider"] = cluster_config["provider"]["inner_provider"]

        cluster_config = inner_provider_cls.fillout_available_node_types_resources(
            cluster_config
        )

        primary_provider["inner_provider"] = cluster_config["provider"]
        cluster_config["provider"] = primary_provider
        return cluster_config

    def __getattr__(self, name: str) -> Any:
        """Implements inheritance from self.inner_provider."""
        return getattr(self.inner_provider, name)


class AnyscaleExecNodeProvider(NodeProvider):  # type: ignore
    """A temporary class for making `anyscale exec` faster.

    Only used in the frontend CLI.
    """

    def __init__(self, provider_config: Dict[str, Any], cluster_name: str) -> None:
        super().__init__(provider_config, cluster_name)
        self.dns_address = provider_config["dns_address"]

    def non_terminated_nodes(self, tag_filters: List[str]) -> List[str]:
        return [self.dns_address]

    def external_ip(self, node_id: str) -> str:
        return node_id
