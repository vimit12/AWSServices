from http import HTTPStatus


RESPONSE_DATA = {
    "message": None,
    "error": None,
    "status_code": HTTPStatus.INTERNAL_SERVER_ERROR,
}
USER_NAME_EXISTS = "Username already exists."
USER_NAME_AVAILABLE = "Username is available."

USER_CREATED = "User created successfully."
USER_NOT_FOUND = "User not found."
USER_UPDATED = "User updated successfully."
USER_LIST_NOT_FOUND = "User List not found"
USER_AUTH_FAIL = "Username or password is incorrect."

USER_LOGGED_OUT = "User has being logged out."
