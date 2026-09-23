from gateway.core.config import USER_SERVICE_URL


ROUTES={
    "users":{
        "service_url":USER_SERVICE_URL,
        "upstream_path":"/users",
    },

    "auth": {
        "service_url": USER_SERVICE_URL,
        "upstream_path": "/auth",
    },

   
}


def get_route(service_name: str):
    return ROUTES.get(service_name)

