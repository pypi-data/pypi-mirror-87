from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.blob_bulk_get_response import BlobBulkGetResponse
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    blob_ids: Optional[str] = None,
) -> Dict[str, Any]:
    url = "{}/blobs:bulk-get".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    params: Dict[str, Any] = {}
    if blob_ids is not None:
        params["blobIds"] = blob_ids

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[BlobBulkGetResponse, BadRequestError]]:
    if response.status_code == 200:
        return BlobBulkGetResponse.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[BlobBulkGetResponse, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    blob_ids: Optional[str] = None,
) -> Response[Union[BlobBulkGetResponse, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        blob_ids=blob_ids,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    blob_ids: Optional[str] = None,
) -> Optional[Union[BlobBulkGetResponse, BadRequestError]]:
    """ Bulk get Blobs by UUID """

    return sync_detailed(
        client=client,
        blob_ids=blob_ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    blob_ids: Optional[str] = None,
) -> Response[Union[BlobBulkGetResponse, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        blob_ids=blob_ids,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    blob_ids: Optional[str] = None,
) -> Optional[Union[BlobBulkGetResponse, BadRequestError]]:
    """ Bulk get Blobs by UUID """

    return (
        await asyncio_detailed(
            client=client,
            blob_ids=blob_ids,
        )
    ).parsed
