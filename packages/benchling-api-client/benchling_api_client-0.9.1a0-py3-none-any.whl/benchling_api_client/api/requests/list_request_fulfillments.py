from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.requst_fulfillments_envelope import RequstFulfillmentsEnvelope
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    entry_id: str,
    next_token: Optional[str] = None,
    page_size: Optional[int] = 50,
) -> Dict[str, Any]:
    url = "{}/request-fulfillments".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    params: Dict[str, Any] = {
        "entry_id": entry_id,
    }
    if next_token is not None:
        params["nextToken"] = next_token
    if page_size is not None:
        params["pageSize"] = page_size

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[RequstFulfillmentsEnvelope, BadRequestError]]:
    if response.status_code == 200:
        return RequstFulfillmentsEnvelope.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[RequstFulfillmentsEnvelope, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    entry_id: str,
    next_token: Optional[str] = None,
    page_size: Optional[int] = 50,
) -> Response[Union[RequstFulfillmentsEnvelope, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        entry_id=entry_id,
        next_token=next_token,
        page_size=page_size,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    entry_id: str,
    next_token: Optional[str] = None,
    page_size: Optional[int] = 50,
) -> Optional[Union[RequstFulfillmentsEnvelope, BadRequestError]]:
    """ Get a request fulfillments in an entry """

    return sync_detailed(
        client=client,
        entry_id=entry_id,
        next_token=next_token,
        page_size=page_size,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    entry_id: str,
    next_token: Optional[str] = None,
    page_size: Optional[int] = 50,
) -> Response[Union[RequstFulfillmentsEnvelope, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        entry_id=entry_id,
        next_token=next_token,
        page_size=page_size,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    entry_id: str,
    next_token: Optional[str] = None,
    page_size: Optional[int] = 50,
) -> Optional[Union[RequstFulfillmentsEnvelope, BadRequestError]]:
    """ Get a request fulfillments in an entry """

    return (
        await asyncio_detailed(
            client=client,
            entry_id=entry_id,
            next_token=next_token,
            page_size=page_size,
        )
    ).parsed
