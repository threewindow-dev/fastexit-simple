"""
Common API error responses for Swagger/OpenAPI documentation.

Use in routers: responses={**common_responses}
"""

common_responses = {
    401: {"description": "Unauthorized"},
    403: {"description": "Forbidden"},
    500: {"description": "Server error"},
}
