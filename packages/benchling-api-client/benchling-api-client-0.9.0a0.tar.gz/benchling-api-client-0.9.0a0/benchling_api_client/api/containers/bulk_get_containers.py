from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.containers_list import ContainersList
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    container_ids: Optional[str] = None,
    barcodes: Optional[str] = None,
) -> Dict[str, Any]:
    url = "{}/containers:bulk-get".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    params: Dict[str, Any] = {}
    if container_ids is not None:
        params["containerIds"] = container_ids
    if barcodes is not None:
        params["barcodes"] = barcodes

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[ContainersList, BadRequestError]]:
    if response.status_code == 200:
        return ContainersList.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ContainersList, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    container_ids: Optional[str] = None,
    barcodes: Optional[str] = None,
) -> Response[Union[ContainersList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        container_ids=container_ids,
        barcodes=barcodes,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    container_ids: Optional[str] = None,
    barcodes: Optional[str] = None,
) -> Optional[Union[ContainersList, BadRequestError]]:
    """ Bulk get a set of containers. Provide either containerIds or barcodes, not both. """

    return sync_detailed(
        client=client,
        container_ids=container_ids,
        barcodes=barcodes,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    container_ids: Optional[str] = None,
    barcodes: Optional[str] = None,
) -> Response[Union[ContainersList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        container_ids=container_ids,
        barcodes=barcodes,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    container_ids: Optional[str] = None,
    barcodes: Optional[str] = None,
) -> Optional[Union[ContainersList, BadRequestError]]:
    """ Bulk get a set of containers. Provide either containerIds or barcodes, not both. """

    return (
        await asyncio_detailed(
            client=client,
            container_ids=container_ids,
            barcodes=barcodes,
        )
    ).parsed
