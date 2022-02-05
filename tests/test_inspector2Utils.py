import pytest
from botocore.stub import Stubber

from ecshelpers.inspector2_utils import inspector2Utils as insp

# define some fixtures to make code cleaner
@pytest.fixture
def insp_instance():
    return insp(False)

def test_create_filter_criteria_with_two_severities(assertions, insp_instance):
    image_digest = "sha256:d5e4"
    severities = ['CRITICAL', 'HIGH']
    criteria = insp_instance.create_filter_criteria(image_digest, severities)
    expectedCriteria = {
        'ecrImageHash': [ {'comparison': 'EQUALS', 'value': 'sha256:d5e4'}],
        'severity' : [ {'comparison': 'EQUALS', 'value': 'CRITICAL'}, 
            {'comparison': 'EQUALS', 'value': 'HIGH'}, 
        ]
    }
    assertions.assertEqual(['ecrImageHash', 'severity'], list(criteria.keys()))
    assertions.assertEqual(expectedCriteria, criteria)
    assert criteria['ecrImageHash'][0]['value'] == "sha256:d5e4"

def test_create_filter_criteria_with_no_severities_does_not_add_severity_critieria(assertions, insp_instance):
    image_digest = "sha256:d5e4"
    severities = []
    criteria = insp_instance.create_filter_criteria(image_digest, severities)
    expectedCriteria = {
        'ecrImageHash': [ {'comparison': 'EQUALS', 'value': 'sha256:d5e4'}]
    }
    assertions.assertEqual(['ecrImageHash'], list(criteria.keys()))
    assertions.assertEqual(expectedCriteria, criteria)

def test_extract_from_findings_returns_empty_list_with_no_results(assertions, insp_instance):
    actual_results = insp_instance.extract_from_findings({})
    assert len(actual_results) == 0

def test_extract_from_findings_handles_single_result(assertions, insp_instance):
    dummy_finding = {
        'awsAccountId': '12345',
        'severity': 'CRITICAL',
        'description': 'ignoring this for now',
        'title': 'CVE-2020-36180',
        'type': 'PACKAGE_VULNERABILITY'
    }
    findings = [ dummy_finding ]
    actual_results = insp_instance.extract_from_findings({ 'findings': findings})
    assert len(actual_results) == 1
    expected_result_str = 'AccountId: 12345 Severity: CRITICAL Type: PACKAGE_VULNERABILITY, Title: CVE-2020-36180 '
    assert actual_results[0] == expected_result_str

def test_extract_from_findings_handles_multiple_results(assertions, insp_instance):
    dummy_finding = {
        'awsAccountId': '12345',
        'severity': 'CRITICAL',
        'description': 'ignoring this for now',
        'title': 'CVE-2020-36180',
        'type': 'PACKAGE_VULNERABILITY'
    }
    dummy_finding2 = {
        'awsAccountId': '12345',
        'severity': 'HIGH',
        'description': 'ignoring this for now',
        'title': 'IN1-JAVA-ORGAPACHELOGGINGLOG4J-2314720',
        'type': 'PACKAGE_VULNERABILITY'
    }
    findings = [ dummy_finding, dummy_finding2 ]
    actual_results = insp_instance.extract_from_findings({ 'findings': findings})
    assert len(actual_results) == 2
    expected_result_str = 'AccountId: 12345 Severity: CRITICAL Type: PACKAGE_VULNERABILITY, Title: CVE-2020-36180 '
    expected_result_str2 = 'AccountId: 12345 Severity: HIGH Type: PACKAGE_VULNERABILITY, Title: IN1-JAVA-ORGAPACHELOGGINGLOG4J-2314720 '
    assert actual_results[0] == expected_result_str
    assert actual_results[1] == expected_result_str2

def test_list_findings_for_invokes_aws_with_default_args(assertions, insp_instance):
    # use stubber to 'mock' out the actual call to AWS
    stubber = Stubber(insp_instance.insp_client)

    response = {
        'findings': []
    }
    # always searches for CRITICAL, HIGH serverities
    # always sorts on SEVERITY DESC
    expected_params = {
        'filterCriteria': {'ecrImageHash': [{'comparison': 'EQUALS', 'value': 'sha256:d5e4'}],
            'severity': [{'comparison': 'EQUALS', 'value': 'CRITICAL'}, {'comparison': 'EQUALS', 'value': 'HIGH'}]},
            'maxResults': 10,
            'sortCriteria': {'field': 'SEVERITY', 'sortOrder': 'DESC'}
        }

    stubber.add_response('list_findings', response, expected_params)
    stubber.activate()
    image_digest = "sha256:d5e4"
    insp_instance.list_findings_for(image_digest)
    stubber.deactivate()

@pytest.mark.aws_integration
def test_list_findings_for_aws_integration(assertions, insp_instance):
    image_sha = "sha256:d5e4eeeef5f2cb0382c3c452f715090bd56899494acdff910d0e6e901e23e3ee"
    results = insp_instance.list_findings_for(image_sha)
    summary_results = insp_instance.extract_from_findings(results)
    assertions.assertEqual(10, len(summary_results))
    # how many CRITICAL findings
    critical_count = sum("Severity: CRITICAL" in s for s in summary_results)
    assertions.assertEqual(6, critical_count)
    # how many HIGH 
    high_count = sum("Severity: HIGH" in s for s in summary_results)
    assertions.assertEqual(4, high_count)
