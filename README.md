# Generating Rancher API Docs

Currently, the Rancher API is self-documented. It can be accessed by going to a running instance of the Rancher management server at [Rancher server URL]/v3.

In this script, I have not tried to generate documentation for endpoints and methods, because after a few discussions, we decided that the types should be the first part of the API to have automatically generated documentation.

I have created a type reference in Swagger and the results look promising.

## Approach

To generate the Swagger docs, this is what I did:

1. In Postman, did a GET request to [Rancher server URL]/v3/schemas, because I'm starting with global-scoped APIs.
2. Copy-pasted the large JSON response into `rancher-api-schema.json`.
3. Wrote a script in `generate-swagger.py` that converted the properties of each schema in the big JSON file into Swagger-formatted properties in a Python dictionary. This was not a clean process. See errors below. I think https://goswagger.io/ might help with this.
4. Convert the Python dictionary into YAML format at `swagger_json_type_reference.yaml`.
5. To test this output in the Swagger editor (https://editor.swagger.io/), I pasted it over the "definitions" section in the sample Swagger and kept the rest of the boilerplate front matter.

## Errors

In the Rancher API, all the nested types just have the name of the type inside them. But in Swagger format, you can't just name the nested type, you have to replace the contents of the nested type with the path to the type's definition. (See the Swagger docs on nested objects https://swagger.io/docs/specification/data-models/data-types/)

I'm getting many of these errors in the Swagger editor:

```
Semantic error at definitions.groupMember.properties.creatorId.$ref
$refs must reference a valid location in the document
Jump to line 6395

Semantic error at definitions.groupMember.properties.creatorId.$ref
$ref values must be RFC3986-compliant percent-encoded URIs
Jump to line 6395
```

I hope https://goswagger.io/ will be able to solve this problem.

More things to fix:

- Enums are being treated as objects in the Swagger output. They shouldn't be.
- Swagger thinks "info" is both required and a reserved word. One of the types is named "info" as well, so it errors out in the Swagger editor.
- In the Rancher API, some types are defined as arrays or maps. I have written some code to convert non-nested array types to YAML format. For example, `array[string]` needs to be converted to:

```
type: array
items:
  type: string
```

This code for converting array types to YAML doesn't work for nested arrays yet. Sometimes in the Rancher API, a type is defined as an array within an array within an array, so that will need to be added to the script.

Then there's also the problem of what to do when the type is a map. Not sure how to convert that.