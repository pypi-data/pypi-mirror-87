from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.not_found_error import NotFoundError
from ...models.request_fulfillment import RequestFulfillment
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    request_fulfillment_id: str,
) -> Dict[str, Any]:
    url = "{}/request-fulfillments/{request_fulfillment_id}".format(
        client.base_url, request_fulfillment_id=request_fulfillment_id
    )

    headers: Dict[str, Any] = client.get_headers()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[RequestFulfillment, NotFoundError]]:
    if response.status_code == 200:
        return RequestFulfillment.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 404:
        return NotFoundError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[RequestFulfillment, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    request_fulfillment_id: str,
) -> Response[Union[RequestFulfillment, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        request_fulfillment_id=request_fulfillment_id,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    request_fulfillment_id: str,
) -> Optional[Union[RequestFulfillment, NotFoundError]]:
    """ Get a request's fulfillment """

    return sync_detailed(
        client=client,
        request_fulfillment_id=request_fulfillment_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    request_fulfillment_id: str,
) -> Response[Union[RequestFulfillment, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        request_fulfillment_id=request_fulfillment_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    request_fulfillment_id: str,
) -> Optional[Union[RequestFulfillment, NotFoundError]]:
    """ Get a request's fulfillment """

    return (
        await asyncio_detailed(
            client=client,
            request_fulfillment_id=request_fulfillment_id,
        )
    ).parsed
