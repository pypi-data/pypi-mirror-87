#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from collections import OrderedDict
import ndjson
import requests
import sys
import uuid
import json
import requests
from datetime import datetime,timedelta

def ndjson2fhir(ndjsonfile, fhir_base_url, update=False, 
                output_http_response=False,
                oauth2_token=None, 
                authorization_uri=None, client_id=None, client_secret=None,
                resource=None, refresh_access_token_in_minutes=57):
    """Return a response_dict with a summary of ndjson2fhir transaction."""
    print("Starting the import of", ndjsonfile, "into", fhir_base_url, "...")
    response_dict = OrderedDict()
    index = 1
    error_list = []
    ids = []
    failed_lines = []
    with open(ndjsonfile) as f:
        data = ndjson.load(f, object_pairs_hook=OrderedDict)
        first_run = True
        start_time = datetime.now()
        next_token_refesh_time = start_time + timedelta(minutes=refresh_access_token_in_minutes)
        for item in data:
            # Check the age of the token.
            
            # if not access_token and a authorization_uri is supplied, attempt to get an access_token
            if next_token_refesh_time < datetime.now() or first_run:
                if authorization_uri and client_id and client_secret:
                    # Get the access_token  
                    print("Getting access token")
                    payload = {'client_id': client_id, 
                                'client_secret': client_secret,
                                'grant_type': 'client_credentials'}
                    if resource:
                        payload['resource'] = resource
                    print(payload)
                    # Get
                    r = requests.post(authorization_uri, data=payload)
                    jsr = json.loads(r.content)
                    if output_http_response:
                        print("Access token response", r.content)
                    oauth2_token = jsr['access_token']
                    next_token_refesh_time = datetime.now() + timedelta(minutes=refresh_access_token_in_minutes)
                    first_run=False

            try:
                if not isinstance(item, type(OrderedDict())):
                    error_message = "File " + \
                        str(item) + " did not contain a JSON object, i.e. {}."
                    error_list.append(error_message)
                # insert the item/document using an HTTP POST to a FHIR server
                if update:
                    # A PUT
                    if 'id' not in item.keys():
                        item['id'] = str(uuid.uuid4())
                    resource_url = "%s%s/%s" % (fhir_base_url, item["resourceType"], item['id'])
                else:
                    # A POST
                    if 'id' in item.keys():
                        del item['id']
                    resource_url = "%s%s" % (fhir_base_url, item["resourceType"])
                
                headers = {'Content-type': 'application/json'}
                
                # Set the Bearer token
                if oauth2_token:
                    headers["Authorization"] = "Bearer %s" % (oauth2_token)                
                
                if update:
                    # PUT UPDATE
                    r = requests.put(resource_url, json=item, headers=headers)

                    if r.status_code not in (200, 201,):
                        error_message = "Failed to PUT/UPDATE item number %s in the FHIR server." % (index)
                        error_list.append(error_message)
                        failed_lines.append(index)
                    else:
                        ids.append({index: r.json()['id']})
                else:
                    # POST CREATE
                    r = requests.post(resource_url, json=item, headers=headers)
                    if r.status_code not in (201,):
                        error_message = "Failed to POST/CREATE item number %s in the FHIR server." % (index)
                        error_list.append(error_message)
                        failed_lines.append(index)
                    else:
                        ids.append({index: r.json()['id']})
                # Output the response if requested.
                if output_http_response:
                    print("index=", index, "url=", resource_url, "status_code=",
                          r.status_code, "content=", r.content)
            except Exception:
                print(sys.exc_info())
                error_message = "File " + str(item) + str(sys.exc_info())
                error_list.append(error_message)
                failed_lines.append(index)
            index+=1
        if error_list:
            response_dict['file'] = ndjsonfile
            response_dict['fhir_base_url'] = fhir_base_url
            response_dict['num_fhir_resources_created'] = index -1
            response_dict['ids'] = ids
            response_dict['num_upload_errors'] = len(error_list)
            response_dict['errors'] = error_list
            response_dict['falied_lines'] = failed_lines
            response_dict['code'] = 400
            response_dict['message'] = "Completed with errors."

        else:
            response_dict['file'] = ndjsonfile
            response_dict['fhir_base_url'] = fhir_base_url
            response_dict['num_fhir_resources_created'] = index -1
            response_dict['ids'] = ids
            response_dict['num_file_errors'] = len(error_list)
            response_dict['falied_lines'] = failed_lines
            response_dict['code'] = 200
            response_dict['message'] = "Completed. No errors."

    return response_dict
