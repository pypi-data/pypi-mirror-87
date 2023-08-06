from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.blob_url import BlobUrl
from ...models.not_found_error import NotFoundError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    blob_id: str,
) -> Dict[str, Any]:
    url = "{}/blobs/{blob_id}/download-url".format(client.base_url, blob_id=blob_id)

    headers: Dict[str, Any] = client.get_headers()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[BlobUrl, BadRequestError, NotFoundError]]:
    if response.status_code == 200:
        return BlobUrl.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 404:
        return NotFoundError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[BlobUrl, BadRequestError, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    blob_id: str,
) -> Response[Union[BlobUrl, BadRequestError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        blob_id=blob_id,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    blob_id: str,
) -> Optional[Union[BlobUrl, BadRequestError, NotFoundError]]:
    """ Get a Blob's download url """

    return sync_detailed(
        client=client,
        blob_id=blob_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    blob_id: str,
) -> Response[Union[BlobUrl, BadRequestError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        blob_id=blob_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    blob_id: str,
) -> Optional[Union[BlobUrl, BadRequestError, NotFoundError]]:
    """ Get a Blob's download url """

    return (
        await asyncio_detailed(
            client=client,
            blob_id=blob_id,
        )
    ).parsed
