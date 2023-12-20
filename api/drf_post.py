import re

from drf_spectacular.generators import SchemaGenerator
from rest_framework.request import Request


def doc_splitter(
    result: dict,
    generator: SchemaGenerator,
    request: Request,
    public: bool
):
    """
    This post-processing step splits the various schemas
    based on routing.  This is probably where translation
    should happen, too (but I still need to do that).
    """
    match (request.path.split("/")[1]):
        case "todoapi":
            filtered_paths = {
                k: v
                for k, v in result["paths"].items()
                if re.search(r'todoapi', k)
            }
            result["paths"] = filtered_paths

            filtered_schemas = {
                k: v
                for k, v in result["components"]["schemas"].items()
                if re.search(r'Todo', k)
            }
            result["components"]["schemas"] = filtered_schemas

            result["info"]["title"] = "Todo List API"
            result["info"]["description"] = ""
            result["securitySchemes"] = {}
        case "contactapi":
            filtered_paths = {
                k: v
                for k, v in result["paths"].items()
                if re.search(r'contactapi', k)
            }
            result["paths"] = filtered_paths

            filtered_schemas = {
                k: v
                for k, v in result["components"]["schemas"].items()
                if re.search(r'Contact', k)
            }
            result["components"]["schemas"] = filtered_schemas

            result["info"]["title"] = "Contact List API"
            result["info"]["description"] = ""
            result["securitySchemes"] = {}
        case _:
            print("This is some other API")
    return result
