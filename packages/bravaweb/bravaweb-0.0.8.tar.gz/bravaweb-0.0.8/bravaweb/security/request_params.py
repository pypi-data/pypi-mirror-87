
import traceback
import configuration
from datetime import datetime

def ValidRequestParams(enviroment, action, klass):

    params = {}
    errors = []
    annotations = action.__annotations__

    # WHILE DECORATOR, GET ENCAPSULATE FUNCTION
    if "return" in annotations:
        while "decorator" in annotations["return"].__name__:
            annotations = annotations["return"].__annotations__

        # GET ANOTATION FUNCTION
        annotations = dict(annotations["return"].__annotations__)

        # SET ENVIROMENT RESPONSE TYPE
        enviroment.response_type = annotations["return"]

        # REMOVE RETURN FROM REQUIRED PARAMS
        try:
            del annotations["return"]
        except Exception as e:
            pass

        # GET REQUIRED PARAM IN REQUEST
        for param, instance in annotations.items():
            if param not in enviroment.request:
                errors.append(
                    "Field [{}] not present in the request".format(param))
            else:
                try:
                    if isinstance(enviroment.request[param], dict):
                        params[param] = instance(**enviroment.request[param])
                    elif instance.__name__ == "bool" and isinstance(enviroment.request[param], str):
                        params[param] = enviroment.request[param].lower() in ['true', '1']
                    elif instance.__name__ == "datetime" and isinstance(enviroment.request[param], str):
                        params[param] = datetime.strptime(enviroment.request[param], configuration.api.date_format)
                    else:
                        params[param] = instance(enviroment.request[param])
                except ValueError:
                    errors.append("Invalid value for [{}] field".format(param))
                except Exception as e:
                    errors.append("Unexpected [{}] field".format(param))

    return params, errors
