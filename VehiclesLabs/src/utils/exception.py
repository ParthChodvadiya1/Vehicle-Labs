from rest_framework.views import exception_handler


# def custom_exception_handler(exc, context):
#     # Call REST framework's default exception handler first,
#     # to get the standard error response.
#     response = exception_handler(exc, context)

#     if response is not None:
#         # check if exception has dict items
#         if hasattr(exc.detail, 'items'):
#             # remove the initial value
#             response.data = {}
#             errors = []
#             for key, value in exc.detail.items():
#                 # append errors into the list
#                 errors.append("{} : {}".format(key, " ".join(value)))
            
#             # add property errors to the response
#             response.data['errors'] = errors

#         # serve status code in the response
#         response.data['status_code'] = response.status_code

#     return response



# def custom_exception_message(e):
#     msg = e.detail
#     typee = isinstance(msg, list)
#     # [print(i) for i in msg]
#     errors = {}
#     if typee == True:
#         for i in msg:
#             stri = msg[0]
#             errors["Availability"] = stri
#     else:
#         for i in msg:
#             stri = msg[i]
#             errors[i] = stri
#     return errors