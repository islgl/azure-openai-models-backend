# Fetches the latest preview and GA releases of Azure AI Services from the official Microsoft documentation
# https://learn.microsoft.com/en-us/azure/ai-services/openai/reference

import requests
from bs4 import BeautifulSoup


def get_all_code_content_from_table(table):
    result = {}
    rows = table.find_all('tr')
    for row in rows[1:]:
        cells = row.find_all('td')
        if len(cells) >= 3:
            api_name = cells[0].get_text(strip=True)
            latest_preview_release = cells[1].find('code').get_text(strip=True)
            latest_ga_release = cells[2].find('code').get_text(strip=True)
            result[api_name] = (latest_preview_release, latest_ga_release)
    return result


def get_latest_version(url: str = 'https://learn.microsoft.com/en-us/azure/ai-services/openai/reference'):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    th_element = soup.find('th', string='Latest preview release')

    api_versions = {}

    if th_element:
        table = th_element.find_parent('table')
        if table:
            raw_versions = get_all_code_content_from_table(table)
            for api_name, versions in raw_versions.items():
                api_versions[api_name] = {
                    "preview": versions[0],
                    "ga": versions[1]
                }
        else:
            raise Exception("The table containing 'latest preview release' was not found")
    else:
        raise Exception("The 'latest preview release' was not found")

    return api_versions
