from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.location_bulk_get_response import LocationBulkGetResponse
from ...models.not_found_error import NotFoundError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    location_ids: Optional[str] = None,
    barcodes: Optional[str] = None,
) -> Dict[str, Any]:
    url = "{}/locations:bulk-get".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    params: Dict[str, Any] = {}
    if location_ids is not None:
        params["locationIds"] = location_ids
    if barcodes is not None:
        params["barcodes"] = barcodes

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[LocationBulkGetResponse, BadRequestError, NotFoundError]]:
    if response.status_code == 200:
        return LocationBulkGetResponse.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 404:
        return NotFoundError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[LocationBulkGetResponse, BadRequestError, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    location_ids: Optional[str] = None,
    barcodes: Optional[str] = None,
) -> Response[Union[LocationBulkGetResponse, BadRequestError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        location_ids=location_ids,
        barcodes=barcodes,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    location_ids: Optional[str] = None,
    barcodes: Optional[str] = None,
) -> Optional[Union[LocationBulkGetResponse, BadRequestError, NotFoundError]]:
    """ BulkGet locations """

    return sync_detailed(
        client=client,
        location_ids=location_ids,
        barcodes=barcodes,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    location_ids: Optional[str] = None,
    barcodes: Optional[str] = None,
) -> Response[Union[LocationBulkGetResponse, BadRequestError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        location_ids=location_ids,
        barcodes=barcodes,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    location_ids: Optional[str] = None,
    barcodes: Optional[str] = None,
) -> Optional[Union[LocationBulkGetResponse, BadRequestError, NotFoundError]]:
    """ BulkGet locations """

    return (
        await asyncio_detailed(
            client=client,
            location_ids=location_ids,
            barcodes=barcodes,
        )
    ).parsed
