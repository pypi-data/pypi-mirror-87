from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.dna_sequence_archive_response import DnaSequenceArchiveResponse
from ...models.dna_sequence_unarchive_request import DnaSequenceUnarchiveRequest
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: DnaSequenceUnarchiveRequest,
) -> Dict[str, Any]:
    url = "{}/dna-sequences:unarchive".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[DnaSequenceArchiveResponse, BadRequestError]]:
    if response.status_code == 200:
        return DnaSequenceArchiveResponse.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[DnaSequenceArchiveResponse, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: DnaSequenceUnarchiveRequest,
) -> Response[Union[DnaSequenceArchiveResponse, BadRequestError]]:
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
    json_body: DnaSequenceUnarchiveRequest,
) -> Optional[Union[DnaSequenceArchiveResponse, BadRequestError]]:
    """ Unarchive DNA sequences """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: DnaSequenceUnarchiveRequest,
) -> Response[Union[DnaSequenceArchiveResponse, BadRequestError]]:
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
    json_body: DnaSequenceUnarchiveRequest,
) -> Optional[Union[DnaSequenceArchiveResponse, BadRequestError]]:
    """ Unarchive DNA sequences """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
