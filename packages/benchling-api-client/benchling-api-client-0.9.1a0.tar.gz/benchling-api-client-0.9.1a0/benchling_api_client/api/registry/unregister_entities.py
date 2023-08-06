from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.empty_object import EmptyObject
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    registry_id: str,
    json_body: Dict[Any, Any],
) -> Dict[str, Any]:
    url = "{}/registries/{registry_id}:unregister-entities".format(client.base_url, registry_id=registry_id)

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[EmptyObject, BadRequestError]]:
    if response.status_code == 200:
        return EmptyObject.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[EmptyObject, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    registry_id: str,
    json_body: Dict[Any, Any],
) -> Response[Union[EmptyObject, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        registry_id=registry_id,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    registry_id: str,
    json_body: Dict[Any, Any],
) -> Optional[Union[EmptyObject, BadRequestError]]:
    """ Unregisters entities and moves them to a folder """

    return sync_detailed(
        client=client,
        registry_id=registry_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    registry_id: str,
    json_body: Dict[Any, Any],
) -> Response[Union[EmptyObject, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        registry_id=registry_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    registry_id: str,
    json_body: Dict[Any, Any],
) -> Optional[Union[EmptyObject, BadRequestError]]:
    """ Unregisters entities and moves them to a folder """

    return (
        await asyncio_detailed(
            client=client,
            registry_id=registry_id,
            json_body=json_body,
        )
    ).parsed
