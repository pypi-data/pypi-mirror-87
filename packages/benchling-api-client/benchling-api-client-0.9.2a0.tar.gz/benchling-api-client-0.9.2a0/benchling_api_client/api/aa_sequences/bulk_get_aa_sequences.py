from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.aa_sequence_bulk_get_response import AaSequenceBulkGetResponse
from ...models.bad_request_error import BadRequestError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    aa_sequence_ids: str,
) -> Dict[str, Any]:
    url = "{}/aa-sequences:bulk-get".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    params: Dict[str, Any] = {
        "aaSequenceIds": aa_sequence_ids,
    }

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[AaSequenceBulkGetResponse, BadRequestError]]:
    if response.status_code == 200:
        return AaSequenceBulkGetResponse.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[AaSequenceBulkGetResponse, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    aa_sequence_ids: str,
) -> Response[Union[AaSequenceBulkGetResponse, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        aa_sequence_ids=aa_sequence_ids,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    aa_sequence_ids: str,
) -> Optional[Union[AaSequenceBulkGetResponse, BadRequestError]]:
    """ Bulk get AA sequences by ID """

    return sync_detailed(
        client=client,
        aa_sequence_ids=aa_sequence_ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    aa_sequence_ids: str,
) -> Response[Union[AaSequenceBulkGetResponse, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        aa_sequence_ids=aa_sequence_ids,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    aa_sequence_ids: str,
) -> Optional[Union[AaSequenceBulkGetResponse, BadRequestError]]:
    """ Bulk get AA sequences by ID """

    return (
        await asyncio_detailed(
            client=client,
            aa_sequence_ids=aa_sequence_ids,
        )
    ).parsed
