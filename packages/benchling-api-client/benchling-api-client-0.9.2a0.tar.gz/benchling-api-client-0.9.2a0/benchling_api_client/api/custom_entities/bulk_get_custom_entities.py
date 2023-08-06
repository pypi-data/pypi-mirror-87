from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.custom_entities import CustomEntities
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    custom_entity_ids: str,
) -> Dict[str, Any]:
    url = "{}/custom-entities:bulk-get".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    params: Dict[str, Any] = {
        "customEntityIds": custom_entity_ids,
    }

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[CustomEntities, BadRequestError]]:
    if response.status_code == 200:
        return CustomEntities.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[CustomEntities, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    custom_entity_ids: str,
) -> Response[Union[CustomEntities, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        custom_entity_ids=custom_entity_ids,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    custom_entity_ids: str,
) -> Optional[Union[CustomEntities, BadRequestError]]:
    """ Bulk get custom entities by ID """

    return sync_detailed(
        client=client,
        custom_entity_ids=custom_entity_ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    custom_entity_ids: str,
) -> Response[Union[CustomEntities, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        custom_entity_ids=custom_entity_ids,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    custom_entity_ids: str,
) -> Optional[Union[CustomEntities, BadRequestError]]:
    """ Bulk get custom entities by ID """

    return (
        await asyncio_detailed(
            client=client,
            custom_entity_ids=custom_entity_ids,
        )
    ).parsed
