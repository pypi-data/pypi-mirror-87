"""
# AppSync Transformer Construct for AWS CDK

![build](https://github.com/kcwinner/cdk-appsync-transformer/workflows/Build/badge.svg)
[![codecov](https://codecov.io/gh/kcwinner/cdk-appsync-transformer/branch/main/graph/badge.svg)](https://codecov.io/gh/kcwinner/cdk-appsync-transformer)
[![dependencies Status](https://david-dm.org/kcwinner/cdk-appsync-transformer/status.svg)](https://david-dm.org/kcwinner/cdk-appsync-transformer)
[![npm](https://img.shields.io/npm/dt/cdk-appsync-transformer)](https://www.npmjs.com/package/cdk-appsync-transformer)

[![npm version](https://badge.fury.io/js/cdk-appsync-transformer.svg)](https://badge.fury.io/js/cdk-appsync-transformer)
[![PyPI version](https://badge.fury.io/py/cdk-appsync-transformer.svg)](https://badge.fury.io/py/cdk-appsync-transformer)

## Notice

For CDK versions < 1.64.0 please use [aws-cdk-appsync-transformer](https://github.com/kcwinner/aws-cdk-appsync-transformer).

## Why This Package

In April 2020 I wrote a [blog post](https://www.trek10.com/blog/appsync-with-the-aws-cloud-development-kit) on using the AWS Cloud Development Kit with AppSync. I wrote my own transformer in order to emulate AWS Amplify's method of using GraphQL directives in order to template a lot of the Schema Definition Language.

This package is my attempt to convert all of that effort into a separate construct in order to clean up the process.

## How Do I Use It

### Example Usage

API With Default Values

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_appsync_transformer import AppSyncTransformer
AppSyncTransformer(self, "my-cool-api",
    schema_path="schema.graphql"
)
```

schema.graphql

```graphql
type Customer @model
    @auth(rules: [
        { allow: groups, groups: ["Admins"] },
        { allow: private, provider: iam, operations: [read, update] }
    ]) {
        id: ID!
        firstName: String!
        lastName: String!
        active: Boolean!
        address: String!
}

type Product @model
    @auth(rules: [
        { allow: groups, groups: ["Admins"] },
        { allow: public, provider: iam, operations: [read] }
    ]) {
        id: ID!
        name: String!
        description: String!
        price: String!
        active: Boolean!
        added: AWSDateTime!
        orders: [Order] @connection
}

type Order @model
    @key(fields: ["id", "productID"]) {
        id: ID!
        productID: ID!
        total: String!
        ordered: AWSDateTime!
}
```

### [Supported Amplify Directives](https://docs.amplify.aws/cli/graphql-transformer/directives)

Tested:

* [@model](https://docs.amplify.aws/cli/graphql-transformer/directives#model)
* [@auth](https://docs.amplify.aws/cli/graphql-transformer/directives#auth)
* [@connection](https://docs.amplify.aws/cli/graphql-transformer/directives#connection)

Experimental:

* [@key](https://docs.amplify.aws/cli/graphql-transformer/directives#key)
* [@versioned](https://docs.amplify.aws/cli/graphql-transformer/directives#versioned)
* [@function](https://docs.amplify.aws/cli/graphql-transformer/directives#function)

  * These work differently here than they do in Amplify - see [Functions](#functions) below

Not Yet Supported:

* [@searchable](https://docs.amplify.aws/cli/graphql-transformer/directives#searchable)
* [@predictions](https://docs.amplify.aws/cli/graphql-transformer/directives#predictions)
* [@http](https://docs.amplify.aws/cli/graphql-transformer/directives#http)

### Authentication

User Pool Authentication

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
user_pool = UserPool(self, "my-cool-user-pool", ...
)
user_pool_client = UserPoolClient(self, f"{id}-client",
    user_pool=self.user_pool, ...
)
AppSyncTransformer(self, "my-cool-api",
    schema_path="schema.graphql",
    authorization_config={
        "default_authorization": {
            "authorization_type": AuthorizationType.USER_POOL,
            "user_pool_config": {
                "user_pool": user_pool,
                "app_id_client_regex": user_pool_client.user_pool_client_id,
                "default_action": UserPoolDefaultAction.ALLOW
            }
        }
    }
)
```

#### IAM

Unauth Role: TODO

Auth Role: Unsupported (for now?). Authorized roles (Lambda Functions, EC2 roles, etc) are required to setup their own role permissions.

### Functions

Fields with the `@function` directive will be accessible via `api.outputs.FUNCTION_RESOLVERS`. It will return an array like below.Currently these are not named and do not specify a region. There are improvements that can be made here but this simple way has worked for me so I've implemented it first. Typically I send all `@function` requests to one Lambda Function and have it route as necessary.

```js
[
  { typeName: 'Query', fieldName: 'listUsers' },
  { typeName: 'Query', fieldName: 'getUser' },
  { typeName: 'Mutation', fieldName: 'createUser' },
  { typeName: 'Mutation', fieldName: 'updateUser' }
]
```

### DataStore Support

1. Pass `syncEnabled: true` to the `AppSyncTransformerProps`
2. Generate necessary exports (see [Code Generation](#code-generation) below)

### Code Generation

I've written some helpers to generate code similarly to how AWS Amplify generates statements and types. You can find the code [here](https://github.com/kcwinner/advocacy/tree/master/cdk-amplify-appsync-helpers).

## Versioning

I will *attempt* to align the major and minor version of this package with [AWS CDK](https://aws.amazon.com/cdk), but always check the release descriptions for compatibility.

I currently support [![GitHub package.json dependency version (prod)](https://img.shields.io/github/package-json/dependency-version/kcwinner/cdk-appsync-transformer/@aws-cdk/core)](https://github.com/aws/aws-cdk)

## Limitations

*

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for details

## License

Distributed under [Apache License, Version 2.0](LICENSE)
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_appsync
import aws_cdk.core


class AppSyncTransformer(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-appsync-transformer.AppSyncTransformer",
):
    """(experimental) AppSyncTransformer Construct.

    :stability: experimental
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        schema_path: builtins.str,
        api_name: typing.Optional[builtins.str] = None,
        authorization_config: typing.Optional[aws_cdk.aws_appsync.AuthorizationConfig] = None,
        field_log_level: typing.Optional[aws_cdk.aws_appsync.FieldLogLevel] = None,
        sync_enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param schema_path: (experimental) Required. Relative path where schema.graphql exists
        :param api_name: (experimental) Optional. String value representing the api name Default: ``${id}-api``
        :param authorization_config: (experimental) Optional. {@link AuthorizationConfig} type defining authorization for AppSync GraphqlApi. Defaults to API_KEY Default: API_KEY authorization config
        :param field_log_level: (experimental) Optional. {@link FieldLogLevel} type for AppSync GraphqlApi log level Default: FieldLogLevel.NONE
        :param sync_enabled: (experimental) Optional. Boolean to enable DataStore Sync Tables Default: false

        :stability: experimental
        """
        props = AppSyncTransformerProps(
            schema_path=schema_path,
            api_name=api_name,
            authorization_config=authorization_config,
            field_log_level=field_log_level,
            sync_enabled=sync_enabled,
        )

        jsii.create(AppSyncTransformer, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="appsyncAPI")
    def appsync_api(self) -> aws_cdk.aws_appsync.GraphqlApi:
        """(experimental) The cdk GraphqlApi construct.

        :stability: experimental
        """
        return jsii.get(self, "appsyncAPI")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="functionResolvers")
    def function_resolvers(self) -> typing.Any:
        """(experimental) The Lambda Function resolvers designated by the function directive.

        :stability: experimental
        """
        return jsii.get(self, "functionResolvers")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="nestedAppsyncStack")
    def nested_appsync_stack(self) -> aws_cdk.core.NestedStack:
        """(experimental) The NestedStack that contains the AppSync resources.

        :stability: experimental
        """
        return jsii.get(self, "nestedAppsyncStack")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> typing.Any:
        """(experimental) The outputs from the SchemaTransformer.

        :stability: experimental
        """
        return jsii.get(self, "outputs")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="resolvers")
    def resolvers(self) -> typing.Any:
        """(experimental) The AppSync resolvers from the transformer minus any function resolvers.

        :stability: experimental
        """
        return jsii.get(self, "resolvers")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tableNameMap")
    def table_name_map(self) -> typing.Any:
        """(experimental) Map of cdk table tokens to table names.

        :stability: experimental
        """
        return jsii.get(self, "tableNameMap")


@jsii.data_type(
    jsii_type="cdk-appsync-transformer.AppSyncTransformerProps",
    jsii_struct_bases=[],
    name_mapping={
        "schema_path": "schemaPath",
        "api_name": "apiName",
        "authorization_config": "authorizationConfig",
        "field_log_level": "fieldLogLevel",
        "sync_enabled": "syncEnabled",
    },
)
class AppSyncTransformerProps:
    def __init__(
        self,
        *,
        schema_path: builtins.str,
        api_name: typing.Optional[builtins.str] = None,
        authorization_config: typing.Optional[aws_cdk.aws_appsync.AuthorizationConfig] = None,
        field_log_level: typing.Optional[aws_cdk.aws_appsync.FieldLogLevel] = None,
        sync_enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        """(experimental) Properties for AppSyncTransformer Construct.

        :param schema_path: (experimental) Required. Relative path where schema.graphql exists
        :param api_name: (experimental) Optional. String value representing the api name Default: ``${id}-api``
        :param authorization_config: (experimental) Optional. {@link AuthorizationConfig} type defining authorization for AppSync GraphqlApi. Defaults to API_KEY Default: API_KEY authorization config
        :param field_log_level: (experimental) Optional. {@link FieldLogLevel} type for AppSync GraphqlApi log level Default: FieldLogLevel.NONE
        :param sync_enabled: (experimental) Optional. Boolean to enable DataStore Sync Tables Default: false

        :stability: experimental
        :link: FieldLogLevel} type for AppSync GraphqlApi log level
        """
        if isinstance(authorization_config, dict):
            authorization_config = aws_cdk.aws_appsync.AuthorizationConfig(**authorization_config)
        self._values: typing.Dict[str, typing.Any] = {
            "schema_path": schema_path,
        }
        if api_name is not None:
            self._values["api_name"] = api_name
        if authorization_config is not None:
            self._values["authorization_config"] = authorization_config
        if field_log_level is not None:
            self._values["field_log_level"] = field_log_level
        if sync_enabled is not None:
            self._values["sync_enabled"] = sync_enabled

    @builtins.property
    def schema_path(self) -> builtins.str:
        """(experimental) Required.

        Relative path where schema.graphql exists

        :stability: experimental
        """
        result = self._values.get("schema_path")
        assert result is not None, "Required property 'schema_path' is missing"
        return result

    @builtins.property
    def api_name(self) -> typing.Optional[builtins.str]:
        """(experimental) Optional.

        String value representing the api name

        :default: ``${id}-api``

        :stability: experimental
        """
        result = self._values.get("api_name")
        return result

    @builtins.property
    def authorization_config(
        self,
    ) -> typing.Optional[aws_cdk.aws_appsync.AuthorizationConfig]:
        """(experimental) Optional.

        {@link AuthorizationConfig} type defining authorization for AppSync GraphqlApi. Defaults to API_KEY

        :default: API_KEY authorization config

        :stability: experimental
        """
        result = self._values.get("authorization_config")
        return result

    @builtins.property
    def field_log_level(self) -> typing.Optional[aws_cdk.aws_appsync.FieldLogLevel]:
        """(experimental) Optional.

        {@link FieldLogLevel} type for AppSync GraphqlApi log level

        :default: FieldLogLevel.NONE

        :stability: experimental
        """
        result = self._values.get("field_log_level")
        return result

    @builtins.property
    def sync_enabled(self) -> typing.Optional[builtins.bool]:
        """(experimental) Optional.

        Boolean to enable DataStore Sync Tables

        :default: false

        :stability: experimental
        """
        result = self._values.get("sync_enabled")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppSyncTransformerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AppSyncTransformer",
    "AppSyncTransformerProps",
]

publication.publish()
