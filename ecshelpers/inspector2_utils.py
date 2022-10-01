import boto3


class inspector2Utils:
    ''' Simple methods for interacting with AWS insepctor2 w/in an account.'''


    def __init__(self, verbose_mode = False) -> None:
        self.insp_client = boto3.client('inspector2')
        self.verbose_mode = verbose_mode

    def create_filter_criteria(self, imageDigest, severities) -> dict:
        filter_criteria = {
                'ecrImageHash' : [{
                'comparison': 'EQUALS',
                'value' : imageDigest
            }]
        }

        if severities:
            severities_to_add = []
            for sev in severities:
                severities_to_add.append( {
                    'comparison': 'EQUALS',
                    'value' : sev
                })
            filter_criteria['severity'] = severities_to_add

        return filter_criteria

    def list_findings_for(self, imageDigest) -> dict:
        ''' lists all findings for a given docker image digest. (with hard coded values of status, field)'''
        
        filter_criteria = self.create_filter_criteria(imageDigest, ['CRITICAL', 'HIGH'])
        results = self.insp_client.list_findings(
            filterCriteria = filter_criteria,
            maxResults = 10, sortCriteria={
                'field' : 'SEVERITY',
                'sortOrder' : 'DESC'
            })
        return results

    def extract_from_findings(self, finding_results) -> list:
        findings = finding_results.get('findings', [])
        finding_summary = []
        for finding in findings:
            acctId = finding.get('awsAccountId', 'N/A')
            severity = finding.get('severity', 'N/A')
            # desc = finding.get('description', 'N/A')
            title = finding.get('title', 'N/A')
            type_val = finding.get('type', 'N/A')
            result = f"AccountId: {acctId} Severity: {severity} Type: {type_val}, Title: {title} "
            # print(result)
            finding_summary.append(result)
        return finding_summary
