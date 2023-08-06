from typing import Any, Dict, Optional, cast

import httpx

from ...client import Client
from ...models.entry_unarchival_response import EntryUnarchivalResponse
from ...models.entry_unarchive import EntryUnarchive
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: EntryUnarchive,
) -> Dict[str, Any]:
    url = "{}/entries:unarchive".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[EntryUnarchivalResponse]:
    if response.status_code == 200:
        return EntryUnarchivalResponse.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[EntryUnarchivalResponse]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: EntryUnarchive,
) -> Response[EntryUnarchivalResponse]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: EntryUnarchive,
) -> Optional[EntryUnarchivalResponse]:
    """ Unarchive notebook entries """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: EntryUnarchive,
) -> Response[EntryUnarchivalResponse]:
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: EntryUnarchive,
) -> Optional[EntryUnarchivalResponse]:
    """ Unarchive notebook entries """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
