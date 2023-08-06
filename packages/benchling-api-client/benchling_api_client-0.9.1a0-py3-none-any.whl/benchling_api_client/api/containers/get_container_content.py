from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.container_content import ContainerContent
from ...models.not_found_error import NotFoundError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    container_id: str,
    containable_id: str,
) -> Dict[str, Any]:
    url = "{}/containers/{container_id}/contents/{containable_id}".format(
        client.base_url, container_id=container_id, containable_id=containable_id
    )

    headers: Dict[str, Any] = client.get_headers()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[ContainerContent, BadRequestError, NotFoundError]]:
    if response.status_code == 200:
        return ContainerContent.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 404:
        return NotFoundError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ContainerContent, BadRequestError, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    container_id: str,
    containable_id: str,
) -> Response[Union[ContainerContent, BadRequestError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        container_id=container_id,
        containable_id=containable_id,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    container_id: str,
    containable_id: str,
) -> Optional[Union[ContainerContent, BadRequestError, NotFoundError]]:
    """ Get a container content """

    return sync_detailed(
        client=client,
        container_id=container_id,
        containable_id=containable_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    container_id: str,
    containable_id: str,
) -> Response[Union[ContainerContent, BadRequestError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        container_id=container_id,
        containable_id=containable_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    container_id: str,
    containable_id: str,
) -> Optional[Union[ContainerContent, BadRequestError, NotFoundError]]:
    """ Get a container content """

    return (
        await asyncio_detailed(
            client=client,
            container_id=container_id,
            containable_id=containable_id,
        )
    ).parsed
