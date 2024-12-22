


#####################################? 88 probels ######################################
########################################################################################

# ################################
#? Success Messages
# ################################
async def success_messages(message: str, status_code: int = 200, *args, **kwargs):
    """
    Success message

    :param message: str
    :param status_code: int
    :param args: list
    :param kwargs: dict
    :return: dict
    """
    response = {
            "status": "success",
            "status_code": status_code,
            "message": message + " successfully"
        }
    if args:
        response[args] = args
    if kwargs:
        response["data"] = kwargs
    return response

