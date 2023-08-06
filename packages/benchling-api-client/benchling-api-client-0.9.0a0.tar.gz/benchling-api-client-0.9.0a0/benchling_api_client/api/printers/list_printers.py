from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.not_found_error import NotFoundError
from ...models.printers_list import PrintersList
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    registry_id: str,
) -> Dict[str, Any]:
    url = "{}/registries/{registry_id}/label-printers".format(client.base_url, registry_id=registry_id)

    headers: Dict[str, Any] = client.get_headers()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[PrintersList, BadRequestError, NotFoundError]]:
    if response.status_code == 200:
        return PrintersList.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 404:
        return NotFoundError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[PrintersList, BadRequestError, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    registry_id: str,
) -> Response[Union[PrintersList, BadRequestError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        registry_id=registry_id,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    registry_id: str,
) -> Optional[Union[PrintersList, BadRequestError, NotFoundError]]:
    """ List printers """

    return sync_detailed(
        client=client,
        registry_id=registry_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    registry_id: str,
) -> Response[Union[PrintersList, BadRequestError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        registry_id=registry_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    registry_id: str,
) -> Optional[Union[PrintersList, BadRequestError, NotFoundError]]:
    """ List printers """

    return (
        await asyncio_detailed(
            client=client,
            registry_id=registry_id,
        )
    ).parsed
