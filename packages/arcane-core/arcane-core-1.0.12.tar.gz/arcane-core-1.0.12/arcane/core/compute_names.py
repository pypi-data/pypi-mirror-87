# All functions computing a name used across components

def get_google_ads_extract_table_name(account_id: str, client_id: str) -> str:
    return f'{client_id}.google-ads_extract_{account_id}_campaign'
