import json
import os
import requests

KEY_SIGNATURE = 'ASUS_CLOUDINFRA_SIGNATURE'
KEY_HOST = 'ASUS_CLOUDINFRA_API_HOST'
KEY_PROJECT = 'ASUS_CLOUDINFRA_PROJECT_ID'
KEY_INFERENCE = 'ASUS_CLOUDINFRA_CONTAINER_ID'

def api_count_inc():
    try:
        # have to same with ai maker
        signature = os.environ[KEY_SIGNATURE]
        url = os.environ[KEY_HOST]
        # inference name/id
        # have to same with ai maker
        project = os.environ[KEY_PROJECT]
        # inference name/id
        # have to same with ai maker
        inference = os.environ[KEY_INFERENCE]
    except KeyError as e:
        print("[KeyError] Please assign {} value".format(str(e)))
        return -1

    headers = {"content-type": "application/json",
               "x-cloud-infra-signature": signature}
    body = json.dumps({
        "label": "inference"
    })
    url = url + "/api/v1/monitor-svc/projects/" + project + \
          "/inferences/" + inference + \
          "/charts/" + "asus_api_counts" + \
          "/counter"
    print(url)
    return requests.post(url, data=body, headers=headers)

def counter_inc(chart, label):
    try:
        # have to same with ai maker
        signature = os.environ[KEY_SIGNATURE]
        url = os.environ[KEY_HOST]
        # inference name/id
        # have to same with ai maker
        project = os.environ[KEY_PROJECT]
        # inference name/id
        # have to same with ai maker
        inference = os.environ[KEY_INFERENCE]
    except KeyError as e:
        print("[KeyError] Please assign {} value".format(str(e)))
        return -1
    headers = {"content-type": "application/json",
               "x-cloud-infra-signature": signature}
    body = json.dumps({
        "label": label
    })
    url = url + "/api/v1/monitor-svc/projects/" + project + \
          "/inferences/" + inference + \
          "/charts/" + chart + \
          "/counter"
    print(url)
    return requests.post(url, data=body, headers=headers)


def gauge_set(chart, label, value):
    try:
        url = os.environ[KEY_HOST]
        signature = os.environ[KEY_SIGNATURE]
        project = os.environ[KEY_PROJECT]
        inference = os.environ[KEY_INFERENCE]
    except KeyError as e:
        print("[KeyError] Please assign {} value".format(str(e)))
        return -1
    headers = {"content-type": "application/json",
               "x-cloud-infra-signature": signature}
    body = json.dumps({
        "label": label,
        "value": value
    })
    url = url + "/api/v1/monitor-svc/projects/" + project + \
          "/inferences/" + inference + \
          "/charts/" + chart + \
          "/gauge"
    return requests.post(url, data=body, headers=headers)
