from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.not_found_error import NotFoundError
from ...models.requests_bulk_get_response_body import RequestsBulkGetResponseBody
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    request_ids: Optional[str] = None,
    display_ids: Optional[str] = None,
) -> Dict[str, Any]:
    url = "{}/requests:bulk-get".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    params: Dict[str, Any] = {}
    if request_ids is not None:
        params["requestIds"] = request_ids
    if display_ids is not None:
        params["displayIds"] = display_ids

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[RequestsBulkGetResponseBody, NotFoundError]]:
    if response.status_code == 200:
        return RequestsBulkGetResponseBody.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 404:
        return NotFoundError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[RequestsBulkGetResponseBody, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    request_ids: Optional[str] = None,
    display_ids: Optional[str] = None,
) -> Response[Union[RequestsBulkGetResponseBody, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        request_ids=request_ids,
        display_ids=display_ids,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    request_ids: Optional[str] = None,
    display_ids: Optional[str] = None,
) -> Optional[Union[RequestsBulkGetResponseBody, NotFoundError]]:
    """ Bulk get requests by API ID or display ID """

    return sync_detailed(
        client=client,
        request_ids=request_ids,
        display_ids=display_ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    request_ids: Optional[str] = None,
    display_ids: Optional[str] = None,
) -> Response[Union[RequestsBulkGetResponseBody, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        request_ids=request_ids,
        display_ids=display_ids,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    request_ids: Optional[str] = None,
    display_ids: Optional[str] = None,
) -> Optional[Union[RequestsBulkGetResponseBody, NotFoundError]]:
    """ Bulk get requests by API ID or display ID """

    return (
        await asyncio_detailed(
            client=client,
            request_ids=request_ids,
            display_ids=display_ids,
        )
    ).parsed
