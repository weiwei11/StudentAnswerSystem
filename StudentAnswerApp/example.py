# # import the logging library
# import logging
#
# # Get an instance of a logger
# logger = logging.getLogger(__name__)
# logger = logging.getLogger('django')
#
# def my_view(request, arg1, arg):
#     if bad_mojo:
#         # Log an error message
#         logger.error('Something went wrong!')


# # Loging
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
#         },
#         'simple': {
#             'format': '%(levelname)s %(message)s'
#         },
#     },
#     'filters': {
#         'special': {
#           '()': 'project.logging.SpecialFilter',
#           'foo': 'bar',
#         },
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'INFO',
#             'filter': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple',
#         },
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(BASE_DIR, 'log/debug.log'),
#         },
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler',
#             'filter': ['special'],
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'propagate': True,
#         },
#         # 'django': {
#         #     'handlers': ['file'],
#         #     'level': 'DEBUG',
#         #     'propagate': True,
#         # },
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'myproject.custom': {
#             'handlers': ['console', 'mail_admins'],
#             'level': 'INFO',
#             'filters': ['special'],
#         },
#     },
# }
