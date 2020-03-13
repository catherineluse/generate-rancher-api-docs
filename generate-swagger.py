#!/usr/bin/python
import json
import yaml
import pprint

# {
#         "collection": "https://ec2-52-33-26-235.us-west-2.compute.amazonaws.com/v3/users",
#         "self": "https://ec2-52-33-26-235.us-west-2.compute.amazonaws.com/v3/schemas/user"
#       }


def transform_schema(properties):
    required = []
    transformed_schema = {
        "type": "object",
        "properties": {},
    }

    for property in properties:

        property_data = properties[property]
        transformed_schema['properties'][property] = {}

        for metadata in property_data:

            if metadata == 'required':
                required.append(property)
            elif metadata == 'default' or metadata == 'description' or metadata == 'options' or metadata == 'max' or metadata == 'min':
                transformed_schema['properties'][property][metadata] = property_data[metadata]
            elif metadata == 'type' and property_data[metadata] == 'number':
                transformed_schema['properties'][property][metadata] = 'int'
            elif metadata == 'type':
                transformed_schema['properties'][property][metadata] = property_data[metadata]
    
    if len(required) > 0:
        transformed_schema['required'] = required
    return transformed_schema

def build_swagger(schemas):
    swagger = {
        "definitions": {},
        "paths": {}
    }
    
    for schema in schemas:
        schema_name = schema['id']
        links = schema['links']

        if "collection" in links.keys():
            collection_path = links['collection']
            path_start = collection_path.find("/v3/") + 3
            short_path = collection_path[path_start:]
            swagger['paths'][short_path ] = {
              "get": {
                  "tags": [schema_name]
              },
              "post": {
                  "tags": [schema_name]
              }
            }
        
        properties = schema['resourceFields']
        transformed_schema = transform_schema(properties)
        swagger["definitions"][schema_name] = transformed_schema
    
    # print(paths)
    return swagger
    
with open('rancher-api-schema.json') as f:
  schemas = json.load(f)
  data = schemas['data']

  # Convert the original JSON to a Python dict
  # in a Swagger friendly structure
  swagger = build_swagger(data)

  with open('frontmatter.yaml', 'r') as front_matter:
    front_matter_text = front_matter.read()
    # Convert the Python dict to Swagger YAML format
    with open('swagger_yaml_type_reference.yaml', 'w') as yml:
        yml.write(front_matter_text)
        yaml.safe_dump(swagger, yml)
        yml.close()

  # Convert the Python dict to Swagger JSON format
  swagger_json = json.dumps(swagger)
  result = open('swagger_json_type_reference.json', 'w')
  result.write(swagger_json)
  result.close()


front_matter.close()