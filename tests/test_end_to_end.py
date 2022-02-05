import pytest
from botocore.stub import Stubber

from ecshelpers.inspector2_utils import inspector2Utils as insp
from ecshelpers.ecs_utils import ecsUtils as ecsUtils

# define some fixtures to make code cleaner
@pytest.fixture
def insp_instance():
    return insp(False)

@pytest.fixture
def utils_instance():
    return ecsUtils(False)


@pytest.mark.aws_integration
def test_find_all_tasks_and_associated_cves(assertions, insp_instance, utils_instance):
    # get all running image on the cluster
    task_results = utils_instance.get_image_info_for_tasks('TestCluster1', 'STOPPED')
    image_shas = {s['imageDigest'] for s in task_results}
    
    # loop through unique set to find CVEs for them
    for image_sha in image_shas:
        results = insp_instance.list_findings_for(image_sha)
        summary_results = insp_instance.extract_from_findings(results)
        assertions.assertEqual(10, len(summary_results))
