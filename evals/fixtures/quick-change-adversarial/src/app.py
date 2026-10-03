def serialize_account(account):
    return {"accountId": account["id"], "displayName": account["display_name"]}


def authenticate_request(headers, verify_token):
    claims = verify_token(headers["Authorization"])
    return claims["sub"]


def old_account_ids(accounts, cutoff):
    return [account["id"] for account in accounts if account["last_seen"] < cutoff]


def load_account(account_id, database, shared_cache=None):
    return database.read(account_id)
