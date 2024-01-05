from django.shortcuts import reverse


class BaseTest:
    AUTHORIZATION_CHECK_METHOD: str = 'get'
    PARAM_PATHS: dict = {}
    API_URL_NAME: str
    APP_NAME: str

    DETAIL = False

    def get_api_url(self, param_paths=None) -> str:
        if param_paths is None:
            param_paths = {}
        return reverse(f'{self.APP_NAME}:{self.API_URL_NAME}', kwargs=param_paths)
