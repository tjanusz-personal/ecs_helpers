from audioop import add
from typing import List
import boto3


class ecsUtils:

    def __init__(self, verbose_mode = False) -> None:
        self.ecs_client = boto3.client('ecs')
        self.verbose_mode = verbose_mode

    def get_cluster_info(self, cluster_name) -> None:
        # Print out cluster info (assume TestCluster1)
        response = self.ecs_client.describe_clusters( clusters = [cluster_name])
        if self.verbose_mode:
            print("## Cluster Info:")
        
        results = []
        for a_cluster in response.get('clusters', []):
            cluster_info = 'Name: {0} Arn: {1}'.format(a_cluster.get('clusterName', 'N/A'), a_cluster.get('clusterArn', 'N/A'))
            results.append(cluster_info)
            if self.verbose_mode:
                print(cluster_info)

        return results

    def get_task_arns(self, cluster_name, task_status) -> None:
        if self.verbose_mode:
            print("### Pulling tasks")

        # list out tasks to find for this cluster (STOPPED)
        ecs_tasks = self.ecs_client.list_tasks(cluster = cluster_name, desiredStatus = task_status)
        if self.verbose_mode:
            print(ecs_tasks)

        # collect up task arns
        task_arns = [i for i in ecs_tasks.get('taskArns', [])]
        if self.verbose_mode:
            for a_task_arn in task_arns:
                print(a_task_arn)

        return task_arns

    def get_image_info_for_tasks(self, cluster_name, task_status) -> List:
        task_arns = self.get_task_arns(cluster_name, task_status)

        if not task_arns:
            print("No task ARNs found")
            return []

        # pull out the details of the tasks related to docker images
        if self.verbose_mode:
            print("### Pulling tasks details to find docker images")
            
        task_descriptions = self.ecs_client.describe_tasks(cluster = cluster_name, tasks = task_arns)
        image_infos = []

        for a_task_def in task_descriptions.get('tasks', []):
            all_containers = a_task_def.get('containers', [])
            for a_container in all_containers:
                image_info = { 
                    'Name' : a_container.get('name','N/A'), 
                    'image': a_container.get('image','N/A'), 
                    'imageDigest': a_container.get('imageDigest','N/A')}
                # image_info = 'Name: {0} image: {1} imageDigest: {2}'.format(a_container.get('name','N/A'), a_container.get('image','N/A'), a_container.get('imageDigest','N/A'))
                image_infos.append(image_info)

        return image_infos