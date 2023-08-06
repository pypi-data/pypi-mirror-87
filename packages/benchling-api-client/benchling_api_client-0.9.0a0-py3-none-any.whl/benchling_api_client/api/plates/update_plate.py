from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.not_found_error import NotFoundError
from ...models.plate import Plate
from ...models.plate_patch import PlatePatch
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    plate_id: str,
    json_body: PlatePatch,
) -> Dict[str, Any]:
    url = "{}/plates/{plate_id}".format(client.base_url, plate_id=plate_id)

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Plate, BadRequestError, NotFoundError]]:
    if response.status_code == 200:
        return Plate.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 404:
        return NotFoundError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Plate, BadRequestError, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    plate_id: str,
    json_body: PlatePatch,
) -> Response[Union[Plate, BadRequestError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        plate_id=plate_id,
        json_body=json_body,
    )

    response = httpx.patch(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    plate_id: str,
    json_body: PlatePatch,
) -> Optional[Union[Plate, BadRequestError, NotFoundError]]:
    """ Update a plate """

    return sync_detailed(
        client=client,
        plate_id=plate_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    plate_id: str,
    json_body: PlatePatch,
) -> Response[Union[Plate, BadRequestError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        plate_id=plate_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.patch(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    plate_id: str,
    json_body: PlatePatch,
) -> Optional[Union[Plate, BadRequestError, NotFoundError]]:
    """ Update a plate """

    return (
        await asyncio_detailed(
            client=client,
            plate_id=plate_id,
            json_body=json_body,
        )
    ).parsed
