import time
import requests
import isodate
from datetime import date

requests.packages.urllib3.disable_warnings()


# Collapsing multiple REST calls into single function
def execute_rest(method, url, bearertoken, payload):
    headers = {
        'Authorization': 'BEARER ' + bearertoken + '',
        'Content-Type': 'application/json'
    }
    response = requests.request(
        method, url, headers=headers, data=payload, verify=False)
    json = response.json()  # type: object

    return json


# Execute tenant workflow based on evaluation criteria supplied by child functions
# Returns job execution ID for status check
def call_tenant_workflow(bearertoken, ostype, instanceid, morpheus_hostname, bucket):
    workflow = get_tenant_workflow_id(instanceid, ostype, bearertoken, morpheus_hostname, bucket)

    url = "https://" + morpheus_hostname + "/api/task-sets/" + str(workflow) + "/execute"

    payload = ('{"job":{ "targetType": "instance", "instances": [' + instanceid + '] }}')

    response = execute_rest("POST", url, bearertoken, payload)

    return response["job"]["id"]


# Execute tenant workflow based on evaluation criteria supplied by child functions
# Returns job execution ID for status check
def call_group_workflow(bearertoken, ostype, instanceid, morpheus_hostname, bucket):
    workflow = get_group_workflow_id(instanceid, ostype, bearertoken, morpheus_hostname, bucket)

    url = "https://" + morpheus_hostname + "/api/task-sets/" + str(workflow) + "/execute"

    payload = ('{"job":{ "targetType": "instance", "instances": [' + instanceid + '] }}')

    response = execute_rest("POST", url, bearertoken, payload)

    return response["job"]["id"]


def get_instance_tenant_id(instanceid, bearertoken, morpheus_hostname):
    url = "https://" + morpheus_hostname + "/api/instances/" + str(instanceid) + ""
    response = execute_rest("GET", url, bearertoken, "")
    tenantName = response["instance"]["accountId"]
    return tenantName


def get_group_workflow_id(instanceid, ostype, bearertoken, morpheus_hostname, bucket):
    url = "https://" + morpheus_hostname + "/public-archives/download/" + bucket + "/workflow_id.json"

    response = requests.get(url, verify=False)
    group_code = get_group_code(instanceid, bearertoken, morpheus_hostname)
    account_id = get_instance_tenant_id(instanceid, bearertoken, morpheus_hostname)
    data = response.json()
    group_id = data["tenantIds"][str(account_id)]["groupCode"][group_code][ostype]
    return group_id


def get_tenant_workflow_id(instanceid, ostype, bearertoken, morpheus_hostname, bucket):
    url = "https://" + morpheus_hostname + "/public-archives/download/" + bucket + "/workflow_id.json"

    response = requests.get(url, verify=False)
    group_code = "all"
    account_id = get_instance_tenant_id(instanceid, bearertoken, morpheus_hostname)
    data = response.json()
    group_id = data["tenantIds"][str(account_id)]["groupCode"][group_code][ostype]
    return group_id


def await_job_exec_status(jobid, bearertoken, morpheus_hostname):
    url = "https://" + morpheus_hostname + "/api/job-executions/" + str(jobid) + ""
    status = ""
    while status == "queued" or status == "running" or status == "":
        response = execute_rest("GET", url, bearertoken, "")
        status = response["jobExecution"]["status"]
        time.sleep(2)
    return status


def await_job_exec_info(jobid, bearertoken, morpheus_hostname):
    url = "https://" + morpheus_hostname + "/api/job-executions/" + str(jobid) + ""
    status = ""
    while status == "queued" or status == "running" or status == "":
        response = execute_rest("GET", url, bearertoken, "")
        status = response["jobExecution"]["status"]
        time.sleep(2)
    return response


def get_group_code(instanceid, bearertoken, morpheus_hostname):
    url = "https://" + morpheus_hostname + "/api/instances/" + str(instanceid) + ""

    response_group_id = execute_rest("GET", url, bearertoken, "")

    group_id = response_group_id["instance"]["group"]["id"]
    url2 = "https://" + morpheus_hostname + "/api/groups/" + str(group_id) + ""

    response_group_code = execute_rest("GET", url2, bearertoken, "")

    group_code = response_group_code
    return group_code["group"]["code"]


def refresh_access_token(appliance_name, client_id, refresh_token):
    method = 'POST'
    url = "https://" + appliance_name + "/oauth/token?grant_type=refresh_token&client_id=" + client_id + "&scope=write"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = 'refresh_token=' + refresh_token + ''

    response = requests.request(
        method, url, headers=headers, data=payload, verify=False)
    json = response.json()  # type: object

    return json


def get_current_token(appliance_name, client_id, username, password):
    method = 'POST'
    url = "https://" + appliance_name + "/oauth/token?grant_type=password&client_id=" + client_id + "&scope=write"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = 'username=' + username + '&password=' + password + ''

    response = requests.request(
        method, url, headers=headers, data=payload, verify=False)
    json = response.json()  # type: object

    return json


# Lease duration can be set in seconds or human readable format
def create_cypher(secret_value, secret_name, appliance_name, token, lease_duration=""):
    if not lease_duration:
        ttl = 0
    else:
        ttl = lease_duration
    url = "https://" + appliance_name + "/api/cypher/secret/" + secret_name + "?value=" + secret_value + "&type=string&ttl=" + str(
        ttl)

    payload = {}
    headers = {
        'Authorization': 'Bearer ' + token + ''
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    if response.json()['success']:
        print "Cypher entry for " + secret_name + " was created successfully."


def days_until_expire(appliance_name, secret_name, access_token):
    url = "https://" + appliance_name + "/api/cypher/secret/" + secret_name
    response = execute_rest("GET", url, access_token, payload="")
    if response[u'cypher'][u'expireDate'] != None:
        exp_date = isodate.parse_date(response[u'cypher'][u'expireDate'])
        remaining = exp_date - date.today()
        remaining = remaining.days
    else:
        remaining = 0
    return remaining
