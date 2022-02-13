import pytest
from botocore.stub import Stubber
import csv
from ecshelpers.inspector2_utils import inspector2Utils as insp
from ecshelpers.ecs_utils import ecsUtils as ecsUtils
from ecshelpers.docker_image_analyzer import dockerImageAnalyzer as dia 

# define some fixtures to make code cleaner
@pytest.fixture
def insp_instance():
    return insp(False)

@pytest.fixture
def utils_instance():
    return ecsUtils(False)

@pytest.fixture
def dia_instance():
    return dia(False)

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

@pytest.mark.aws_integration
def test_print_current_base_image_statuses(assertions, dia_instance, utils_instance):
    s3_bucket_name = "tjanusz-personal-demo-stuff"
    s3_object_key = "dockerImagesSecInfo/validBaseImages.csv"
    base_images = dia_instance.fetch_base_images_from_s3(s3_bucket_name, s3_object_key)
    # print(base_images)

    # get all running image on the cluster
    task_results = utils_instance.get_image_info_for_tasks('TestCluster1', 'STOPPED')

    # decorate task result w/results of matchings to base images
    for task_result in task_results:
        result = dia_instance.image_matches_current_bases(task_result['image'], base_images)
        task_result['validBaseImage'] = result
    
    field_names = ['account_id', 'name', 'group', 'validBaseImage', 'image', 'imageDigest', 'cluster_arn']
    with open('test4.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = field_names)
        writer.writeheader()
        writer.writerows(task_results)

    print(task_results)

