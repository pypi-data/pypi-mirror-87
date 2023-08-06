from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.dna_sequence_bulk_get_response import DnaSequenceBulkGetResponse
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    dna_sequence_ids: str,
) -> Dict[str, Any]:
    url = "{}/dna-sequences:bulk-get".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    params: Dict[str, Any] = {
        "dnaSequenceIds": dna_sequence_ids,
    }

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[DnaSequenceBulkGetResponse, BadRequestError]]:
    if response.status_code == 200:
        return DnaSequenceBulkGetResponse.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[DnaSequenceBulkGetResponse, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    dna_sequence_ids: str,
) -> Response[Union[DnaSequenceBulkGetResponse, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        dna_sequence_ids=dna_sequence_ids,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    dna_sequence_ids: str,
) -> Optional[Union[DnaSequenceBulkGetResponse, BadRequestError]]:
    """ Bulk get DNA sequences by ID """

    return sync_detailed(
        client=client,
        dna_sequence_ids=dna_sequence_ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    dna_sequence_ids: str,
) -> Response[Union[DnaSequenceBulkGetResponse, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        dna_sequence_ids=dna_sequence_ids,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    dna_sequence_ids: str,
) -> Optional[Union[DnaSequenceBulkGetResponse, BadRequestError]]:
    """ Bulk get DNA sequences by ID """

    return (
        await asyncio_detailed(
            client=client,
            dna_sequence_ids=dna_sequence_ids,
        )
    ).parsed
