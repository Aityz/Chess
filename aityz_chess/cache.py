"""Cache System for aityz_chess."""

import os
import re
import json


def clear_cache() -> None:
    """Clears all the cache for the Caching System.
    """
    cache_dir = 'aityz_cache'
    if os.path.exists(cache_dir):
        for file in os.listdir(cache_dir):
            os.remove(os.path.join(cache_dir, file))
        os.rmdir(cache_dir)

def sanitize_url(url: str) -> str:
    """Cleans URLs to be used in file names.

    Args:
        url (str): This URL will be used in the name of the file after being sanitized.

    Returns:
        str: A string with the cleansed URL.
    """
    url = url.replace('https://', '')
    url = re.sub(r'\W+', '-', url)
    return url

def save_subset(data: dict, url: str) -> None:
    """Save some JSON data to the Caching System.

    Args:
        data (dict): JSON formatted data that will be saved.
        url (str): The URL (that will be cleansed), and will eventually be the save location.
    """
    cache_dir = 'aityz_cache'
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)
    safe_subset_name = sanitize_url(url)
    with open(os.path.join(cache_dir, f'{safe_subset_name}.json'), 'w') as f:
        json.dump(data, f, indent=4)

def load_subset(subset_name: str) -> dict:
    """Loads some JSON data from the Caching System.

    Args:
        subset_name (str): This will be an uncleansed URL that will be cleansed, and checked.

    Returns:
        dict: The JSON data for the subset.
    """
    safe_subset_name = sanitize_url(subset_name)
    with open(os.path.join('aityz_cache', f'{safe_subset_name}.json'), 'r') as f:
        data = json.load(f)
    return data

def find_subsets() -> list:
    """Lists all the cache that is stored in the Caching System.

    Returns:
        list: This will be a list of names (without the .json). They will be in Cleansed URL form.
    """
    cache_dir = 'aityz_cache'
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)
        return []
    subsets = [file.replace('.json', '') for file in os.listdir(cache_dir)]
    return subsets