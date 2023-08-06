from typing import Any, Dict, Optional, cast

import httpx

from ...client import Client
from ...models.box_archive_response import BoxArchiveResponse
from ...models.box_unarchive_request import BoxUnarchiveRequest
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: BoxUnarchiveRequest,
) -> Dict[str, Any]:
    url = "{}/boxes:unarchive".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[BoxArchiveResponse]:
    if response.status_code == 200:
        return BoxArchiveResponse.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[BoxArchiveResponse]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: BoxUnarchiveRequest,
) -> Response[BoxArchiveResponse]:
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
    json_body: BoxUnarchiveRequest,
) -> Optional[BoxArchiveResponse]:
    """ Unarchive boxes and the containers that were archived along with them """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: BoxUnarchiveRequest,
) -> Response[BoxArchiveResponse]:
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
    json_body: BoxUnarchiveRequest,
) -> Optional[BoxArchiveResponse]:
    """ Unarchive boxes and the containers that were archived along with them """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
