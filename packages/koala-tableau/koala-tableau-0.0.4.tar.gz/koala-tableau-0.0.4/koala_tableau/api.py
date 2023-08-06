import os
import backoff
import requests

from koala_tableau.exceptions import exceptions


@backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=4)
def requests_get_wrapper(url, **kwargs):
    res = requests.get(url, **kwargs)
    res.raise_for_status()
    return res


def authenticate():
    try:
        res = requests.post(f"{os.environ['TABLEAU_URL']}/api/{os.environ['TABLEAU_API_VERSION']}/auth/signin",
                            headers={"Content": "application/json", "Accept": "application/json"},
                            json={
                                "credentials": {
                                    "personalAccessTokenName": os.environ['TABLEAU_API_USER'],
                                    "personalAccessTokenSecret": os.environ['TABLEAU_API_PASS'],
                                    "site": {
                                        "contentUrl": ""
                                    }
                                }
                            })
        res.raise_for_status()
    except KeyError as env_name:
        raise exceptions.RequiredEnvNotSet(env_name)
    else:
        return res.json()


def get_workbooks(site_id: str, api_token: str):
    res = requests_get_wrapper(f"{os.environ['TABLEAU_URL']}/api/{os.environ['TABLEAU_API_VERSION']}/sites/{site_id}/workbooks",
                               headers={"X-Tableau-Auth": api_token, "Content": "application/json",
                                        "Accept": "application/json"})
    return res.json()


def get_views(site_id: str, workbook_id: str, api_token: str):
    res = requests_get_wrapper(f"{os.environ['TABLEAU_URL']}/api/{os.environ['TABLEAU_API_VERSION']}/sites/{site_id}/"
                               f"workbooks/{workbook_id}",
                               headers={"X-Tableau-Auth": api_token, "Content": "application/json", "Accept": "application/json"})
    return res.json()


def get_view_image(site_id: str, workbook_id: str, view_id: str, api_token: str):
    res = requests_get_wrapper(f"{os.environ['TABLEAU_URL']}/api/{os.environ['TABLEAU_API_VERSION']}/sites/{site_id}/"
                               f"workbooks/{workbook_id}/views/{view_id}/previewImage",
                               headers={"X-Tableau-Auth": api_token, "Content": "application/json", "Accept": "application/json"})
    return res.content


def logout(api_token: str):
    res = requests.post(f"{os.environ['TABLEAU_URL']}/api/{os.environ['TABLEAU_API_VERSION']}/auth/signout",
                        headers={"X-Tableau-Auth": api_token, "Content": "application/json",
                                 "Accept": "application/json"})
    res.raise_for_status()
