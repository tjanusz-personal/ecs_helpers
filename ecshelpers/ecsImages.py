import boto3

import ecs_utils as ecs
import inspector2_utils as insp2
import docker_image_analyzer as dia 

cluster_name = "TestCluster1"

ecs_utils_inst = ecs.ecsUtils(cluster_name)
insp2_inst = insp2.inspector2Utils()

# pull all image info for given tasks
# image_infos = ecs_utils_inst.get_image_info_for_tasks(cluster_name, "STOPPED")
# for info in image_infos:
#     print(info)
#     image_digest = info.get('imageDigest', 'N/A')
#     results = insp2_inst.list_findings_for(image_digest)
#     sum_results = insp2_inst.extract_from_findings(results)
#     print(sum_results)

image_digest = 'sha256:d5e4eeeef5f2cb0382c3c452f715090bd56899494acdff910d0e6e901e23e3ee'
# image_digest = 'sha256:d5e4eeeef5f2cb0382c3c452f715090bd56899494acdff910d0e6e901e23e3ee'
results = insp2_inst.list_findings_for(image_digest)
sum_results = insp2_inst.extract_from_findings(results)
print(sum_results)

