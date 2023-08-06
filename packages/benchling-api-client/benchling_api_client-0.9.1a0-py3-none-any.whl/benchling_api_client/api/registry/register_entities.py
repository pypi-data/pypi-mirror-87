from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.async_task_link import AsyncTaskLink
from ...models.bad_request_error import BadRequestError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    registry_id: str,
    json_body: Dict[Any, Any],
) -> Dict[str, Any]:
    url = "{}/registries/{registry_id}:bulk-register-entities".format(client.base_url, registry_id=registry_id)

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[AsyncTaskLink, BadRequestError]]:
    if response.status_code == 202:
        return AsyncTaskLink.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[AsyncTaskLink, BadRequestError]]:
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
) -> Response[Union[AsyncTaskLink, BadRequestError]]:
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
) -> Optional[Union[AsyncTaskLink, BadRequestError]]:
    """Attempts to move entities into the registry. This endpoint will first check that the entities are all valid to be moved into the registry, given the namingStrategy. If any entities fail validation, no files will be moved and errors describing invalid entities is returned. If all entities pass validation, the entities are moved into the registry."""

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
) -> Response[Union[AsyncTaskLink, BadRequestError]]:
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
) -> Optional[Union[AsyncTaskLink, BadRequestError]]:
    """Attempts to move entities into the registry. This endpoint will first check that the entities are all valid to be moved into the registry, given the namingStrategy. If any entities fail validation, no files will be moved and errors describing invalid entities is returned. If all entities pass validation, the entities are moved into the registry."""

    return (
        await asyncio_detailed(
            client=client,
            registry_id=registry_id,
            json_body=json_body,
        )
    ).parsed
