from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.box_bulk_get_response import BoxBulkGetResponse
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    box_ids: Optional[str] = None,
    barcodes: Optional[str] = None,
) -> Dict[str, Any]:
    url = "{}/boxes:bulk-get".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    params: Dict[str, Any] = {}
    if box_ids is not None:
        params["boxIds"] = box_ids
    if barcodes is not None:
        params["barcodes"] = barcodes

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[BoxBulkGetResponse, BadRequestError]]:
    if response.status_code == 200:
        return BoxBulkGetResponse.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[BoxBulkGetResponse, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    box_ids: Optional[str] = None,
    barcodes: Optional[str] = None,
) -> Response[Union[BoxBulkGetResponse, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        box_ids=box_ids,
        barcodes=barcodes,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    box_ids: Optional[str] = None,
    barcodes: Optional[str] = None,
) -> Optional[Union[BoxBulkGetResponse, BadRequestError]]:
    """ BulkGet boxes """

    return sync_detailed(
        client=client,
        box_ids=box_ids,
        barcodes=barcodes,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    box_ids: Optional[str] = None,
    barcodes: Optional[str] = None,
) -> Response[Union[BoxBulkGetResponse, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        box_ids=box_ids,
        barcodes=barcodes,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    box_ids: Optional[str] = None,
    barcodes: Optional[str] = None,
) -> Optional[Union[BoxBulkGetResponse, BadRequestError]]:
    """ BulkGet boxes """

    return (
        await asyncio_detailed(
            client=client,
            box_ids=box_ids,
            barcodes=barcodes,
        )
    ).parsed
