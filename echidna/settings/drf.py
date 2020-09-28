"""
@author: liyao
@contact: liyao2598330@126.com
@time: 2020/7/31 12:30 下午
"""

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'echidna.utils.handlers.drf_exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'apps.user.utils.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1/second',
        'user': '5/second'
    },
    "UNAUTHENTICATED_TOKEN": None,  # 匿名，request.auth = None
    "DEFAULT_PARSER_CLASSES": [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',  # LimitOffsetPagination 分页风格
    'PAGE_SIZE': 20,
}
