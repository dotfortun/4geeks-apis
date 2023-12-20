import re

from drf_spectacular.generators import SchemaGenerator
from rest_framework.request import Request


def doc_splitter(
    result: dict,
    generator: SchemaGenerator,
    request: Request,
    public: bool
):
    match (request.path.split("/")[1]):
        case "todoapi":
            print("This is the Todo API")
            generator.endpoints = list(filter(
                lambda x: re.match(r"/todoapi", x[0]),
                generator.endpoints
            ))
        case "contactapi":
            print("This is the Contact List API")
        case _:
            print("This is some other API")
    return result
