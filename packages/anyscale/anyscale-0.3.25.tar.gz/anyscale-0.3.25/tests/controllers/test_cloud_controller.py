from unittest.mock import Mock, patch

from click import ClickException
import pytest

from anyscale.client.openapi_client.models import (  # type: ignore
    AnyscaleAWSAccount,
    AnyscaleawsaccountResponse,
    Cloud,
    CloudResponse,
)
from anyscale.controllers.cloud_controller import CloudController


@pytest.fixture()  # type: ignore
def mock_api_client(cloud_test_data: Cloud) -> Mock:
    mock_api_client = Mock()
    mock_api_client.get_cloud_api_v2_clouds_cloud_id_get = Mock(
        return_value=CloudResponse(result=cloud_test_data)
    )
    mock_api_client.find_cloud_by_name_api_v2_clouds_find_by_name_post = Mock(
        return_value=CloudResponse(result=cloud_test_data)
    )
    mock_api_client.delete_cloud_api_v2_clouds_cloud_id_delete = Mock(return_value={})

    return mock_api_client


def test_setup_cloud_aws(mock_api_client: Mock) -> None:
    with patch.object(
        CloudController, "setup_aws", return_value=None
    ) as mock_setup_aws:
        cloud_controller = CloudController(api_client=mock_api_client)
        cloud_controller.setup_cloud(provider="aws", region=None, name="test-aws")

        mock_setup_aws.assert_called_once_with(region="us-west-2", name="test-aws")


def test_setup_cloud_gcp(mock_api_client: Mock) -> None:
    mock_launch_gcp_cloud_setup = Mock(return_value=None)
    with patch.multiple(
        "anyscale.controllers.cloud_controller",
        launch_gcp_cloud_setup=mock_launch_gcp_cloud_setup,
    ):
        cloud_controller = CloudController(api_client=mock_api_client)
        cloud_controller.setup_cloud(provider="gcp", region=None, name="test-gcp")

        mock_launch_gcp_cloud_setup.assert_called_once_with(
            region="us-west1", name="test-gcp"
        )


def test_setup_cloud_invalid_provider(mock_api_client: Mock) -> None:
    cloud_controller = CloudController(api_client=mock_api_client)
    with pytest.raises(ClickException):
        cloud_controller.setup_cloud(
            provider="azure", region="azure-west-1", name="invalid cloud provider"
        )


def test_delete_cloud_by_name(cloud_test_data: Cloud, mock_api_client: Mock) -> None:
    cloud_controller = CloudController(api_client=mock_api_client)
    success = cloud_controller.delete_cloud(
        cloud_id=None, cloud_name=cloud_test_data.name, skip_confirmation=True
    )
    assert success

    mock_api_client.find_cloud_by_name_api_v2_clouds_find_by_name_post.assert_called_once_with(
        cloud_name_options={"name": cloud_test_data.name}
    )
    mock_api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
        cloud_id=cloud_test_data.id
    )


def test_delete_cloud_by_id(cloud_test_data: Cloud, mock_api_client: Mock) -> None:
    cloud_controller = CloudController(api_client=mock_api_client)
    success = cloud_controller.delete_cloud(
        cloud_id=cloud_test_data.id, cloud_name=None, skip_confirmation=True
    )
    assert success

    mock_api_client.get_cloud_api_v2_clouds_cloud_id_get.assert_called_once_with(
        cloud_id=cloud_test_data.id
    )
    mock_api_client.delete_cloud_api_v2_clouds_cloud_id_delete(
        cloud_id=cloud_test_data.id
    )


def test_delete_cloud_without_name_or_id(mock_api_client: Mock) -> None:
    cloud_controller = CloudController(api_client=mock_api_client)

    with pytest.raises(ClickException):
        cloud_controller.delete_cloud(None, None, True)


def test_setup_cross_region(mock_api_client: Mock) -> None:
    mock_api_client.get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get = Mock(
        return_value=AnyscaleawsaccountResponse(
            result=AnyscaleAWSAccount(anyscale_aws_account="aws_account_type")
        )
    )
    mock_role = Mock()
    mock_role.attach_policy = Mock()
    mock_role.arn = "ARN"
    with patch.multiple(
        "anyscale.controllers.cloud_controller", _get_role=Mock(return_value=mock_role)
    ):
        cloud_controller = CloudController(api_client=mock_api_client)
        cloud_controller.setup_aws_cross_account_role("us-west-2", "user_id", "name")
    mock_api_client.get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get.assert_called_once()
    mock_role.attach_policy.assert_called()
