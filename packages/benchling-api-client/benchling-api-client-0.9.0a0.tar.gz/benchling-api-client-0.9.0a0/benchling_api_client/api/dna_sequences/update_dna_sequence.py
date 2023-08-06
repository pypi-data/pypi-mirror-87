from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.dna_sequence import DnaSequence
from ...models.dna_sequence_patch import DnaSequencePatch
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    dna_sequence_id: str,
    json_body: DnaSequencePatch,
) -> Dict[str, Any]:
    url = "{}/dna-sequences/{dna_sequence_id}".format(client.base_url, dna_sequence_id=dna_sequence_id)

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[DnaSequence, BadRequestError]]:
    if response.status_code == 200:
        return DnaSequence.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[DnaSequence, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    dna_sequence_id: str,
    json_body: DnaSequencePatch,
) -> Response[Union[DnaSequence, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        dna_sequence_id=dna_sequence_id,
        json_body=json_body,
    )

    response = httpx.patch(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    dna_sequence_id: str,
    json_body: DnaSequencePatch,
) -> Optional[Union[DnaSequence, BadRequestError]]:
    """ Update a DNA sequence """

    return sync_detailed(
        client=client,
        dna_sequence_id=dna_sequence_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    dna_sequence_id: str,
    json_body: DnaSequencePatch,
) -> Response[Union[DnaSequence, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        dna_sequence_id=dna_sequence_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.patch(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    dna_sequence_id: str,
    json_body: DnaSequencePatch,
) -> Optional[Union[DnaSequence, BadRequestError]]:
    """ Update a DNA sequence """

    return (
        await asyncio_detailed(
            client=client,
            dna_sequence_id=dna_sequence_id,
            json_body=json_body,
        )
    ).parsed
