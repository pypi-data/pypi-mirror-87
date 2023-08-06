from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.location import Location
from ...models.location_update import LocationUpdate
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    location_id: str,
    json_body: LocationUpdate,
) -> Dict[str, Any]:
    url = "{}/locations/{location_id}".format(client.base_url, location_id=location_id)

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Location, BadRequestError]]:
    if response.status_code == 200:
        return Location.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Location, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    location_id: str,
    json_body: LocationUpdate,
) -> Response[Union[Location, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        location_id=location_id,
        json_body=json_body,
    )

    response = httpx.patch(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    location_id: str,
    json_body: LocationUpdate,
) -> Optional[Union[Location, BadRequestError]]:
    """  """

    return sync_detailed(
        client=client,
        location_id=location_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    location_id: str,
    json_body: LocationUpdate,
) -> Response[Union[Location, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        location_id=location_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.patch(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    location_id: str,
    json_body: LocationUpdate,
) -> Optional[Union[Location, BadRequestError]]:
    """  """

    return (
        await asyncio_detailed(
            client=client,
            location_id=location_id,
            json_body=json_body,
        )
    ).parsed
