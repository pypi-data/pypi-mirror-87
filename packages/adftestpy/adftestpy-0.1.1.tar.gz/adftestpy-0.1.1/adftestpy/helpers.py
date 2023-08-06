from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import RunFilterParameters
import time
import functools as ft
# import yaml
# from datetime import datetime, timedelta
# import time
# import os, sys


def authenticate(clientid, secret, tenant):
    credentials = ServicePrincipalCredentials(
        client_id=clientid, 
        secret=secret, 
        tenant=tenant
    )
    return credentials

def connect_to_df(credentials, subscription_id):
    adf_client = DataFactoryManagementClient(credentials, subscription_id)
    return adf_client

def create_pipeline_run(adf_client, pipeline_args):
    """Pipeline args are resource_group_name,factory_name, pipeline_name and optional parameters={}
    """
    run_response = adf_client.pipelines.create_run(**pipeline_args)
    return run_response

def monitor_pipeline_run(adf_client, get_run_args):
    "get_run_args is resource_group_name, factory_name, and run_id. Get the run_id after creating the pipelinerun"
    pipeline_run = adf_client.pipeline_runs.get(**get_run_args)
    return pipeline_run

def wait_for_pipeline_to_finish(adf_client, get_run_args):
    i = 1
    pipeline_run = monitor_pipeline_run(adf_client, get_run_args)
    while pipeline_run.status in ["Queued", "InProgress", "Canceling"]:
        time.sleep(10)
        print("loop #%s" % i)
        print(pipeline_run.status)
        pipeline_run = monitor_pipeline_run(adf_client, get_run_args)
        i+=1
    print(pipeline_run.status)
    return pipeline_run.status

def get_specific_activity(adf_client, get_run_args, activity_name):
    pipelinerun = monitor_pipeline_run(adf_client, get_run_args)
    filters = RunFilterParameters(last_updated_after=pipelinerun.run_start, last_updated_before=pipelinerun.run_end)
    factoryname = get_run_args['factory_name']
    resourcegroup = get_run_args['resource_group_name']
    activityruns = adf_client.activity_runs.query_by_pipeline_run(
    factory_name = factoryname,
    run_id= pipelinerun.run_id,
    filter_parameters = filters,
    resource_group_name = resourcegroup)
    activity_search = [x.as_dict() for x in activityruns.value if x.as_dict()['activity_name'] == activity_name]
    if activity_search == []:
        print("No activity with name {} found.".format(activity_name))
        return
    elif len(activity_search)>1:
        print("More than one activity found with name {}. Name your activities more specifically.".format(activity_name))
        return
    elif len(activity_search) == 1:
        print("Activity {} found".format(activity_name))
        activity = activity_search[0]
        return activity
    else:
        print("Something else went randomly wrong in looking for activity {}.".format(activity_name))
        return

def get_activity_attribute(activity, attribute_search):
    if type(attribute_search) == str:
        attribute = activity[attribute_search]
        return attribute
    elif type(attribute_search) == list:
        attribute = ft.reduce(lambda val, key: val.get(key) if val else None, attribute_search, activity)
        return attribute
    else:
        print("Need to pass str or list for attribute_search")
        return

def process_attribute_search_string(attribute_search_base):
    if "[" in attribute_search_base:
        attribute_search = list(map(str, attribute_search_base.strip('[]').split(',')))
        attribute_search = [x.replace(" ", "") for x in attribute_search]
    elif "[" not in attribute_search_base:
        attribute_search = attribute_search_base
    else:
        print("Invalid construction for attribute search passed, setting attribute search to None")
        attribute_search = None   
    return attribute_search
