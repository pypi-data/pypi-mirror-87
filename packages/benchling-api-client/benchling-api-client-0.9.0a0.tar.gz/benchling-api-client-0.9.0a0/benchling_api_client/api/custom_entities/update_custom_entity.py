from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.custom_entity import CustomEntity
from ...models.custom_entity_patch import CustomEntityPatch
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    custom_entity_id: str,
    json_body: CustomEntityPatch,
) -> Dict[str, Any]:
    url = "{}/custom-entities/{custom_entity_id}".format(client.base_url, custom_entity_id=custom_entity_id)

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[CustomEntity, BadRequestError]]:
    if response.status_code == 200:
        return CustomEntity.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[CustomEntity, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    custom_entity_id: str,
    json_body: CustomEntityPatch,
) -> Response[Union[CustomEntity, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        custom_entity_id=custom_entity_id,
        json_body=json_body,
    )

    response = httpx.patch(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    custom_entity_id: str,
    json_body: CustomEntityPatch,
) -> Optional[Union[CustomEntity, BadRequestError]]:
    """ Update a custom entity """

    return sync_detailed(
        client=client,
        custom_entity_id=custom_entity_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    custom_entity_id: str,
    json_body: CustomEntityPatch,
) -> Response[Union[CustomEntity, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        custom_entity_id=custom_entity_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.patch(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    custom_entity_id: str,
    json_body: CustomEntityPatch,
) -> Optional[Union[CustomEntity, BadRequestError]]:
    """ Update a custom entity """

    return (
        await asyncio_detailed(
            client=client,
            custom_entity_id=custom_entity_id,
            json_body=json_body,
        )
    ).parsed
