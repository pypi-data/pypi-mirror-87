import datetime
import json


# Allows us to customize the output based on the context.
def jsonify(ctx, entry):
    return entry


def json_output_default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
    return None


def output_json(ctx, entry):
    print(
        json.dumps(
            jsonify(ctx, entry), sort_keys=True, indent=2, default=json_output_default
        )
    )
