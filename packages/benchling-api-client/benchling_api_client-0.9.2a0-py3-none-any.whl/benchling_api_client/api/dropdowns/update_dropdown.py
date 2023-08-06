from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.dropdown import Dropdown
from ...models.dropdown_patch import DropdownPatch
from ...models.forbidden_error import ForbiddenError
from ...models.not_found_error import NotFoundError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    dropdown_id: str,
    json_body: DropdownPatch,
) -> Dict[str, Any]:
    url = "{}/dropdowns/{dropdown_id}".format(client.base_url, dropdown_id=dropdown_id)

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[Dropdown, BadRequestError, ForbiddenError, NotFoundError]]:
    if response.status_code == 200:
        return Dropdown.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 403:
        return ForbiddenError.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 404:
        return NotFoundError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[Dropdown, BadRequestError, ForbiddenError, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    dropdown_id: str,
    json_body: DropdownPatch,
) -> Response[Union[Dropdown, BadRequestError, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        dropdown_id=dropdown_id,
        json_body=json_body,
    )

    response = httpx.patch(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    dropdown_id: str,
    json_body: DropdownPatch,
) -> Optional[Union[Dropdown, BadRequestError, ForbiddenError, NotFoundError]]:
    """ Update a dropdown """

    return sync_detailed(
        client=client,
        dropdown_id=dropdown_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    dropdown_id: str,
    json_body: DropdownPatch,
) -> Response[Union[Dropdown, BadRequestError, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        dropdown_id=dropdown_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.patch(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    dropdown_id: str,
    json_body: DropdownPatch,
) -> Optional[Union[Dropdown, BadRequestError, ForbiddenError, NotFoundError]]:
    """ Update a dropdown """

    return (
        await asyncio_detailed(
            client=client,
            dropdown_id=dropdown_id,
            json_body=json_body,
        )
    ).parsed
