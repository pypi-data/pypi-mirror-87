from typing import Any, Dict, Optional, cast

import httpx

from ...client import Client
from ...models.assay_result_transaction_post_response import AssayResultTransactionPostResponse
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    transaction_id: str,
) -> Dict[str, Any]:
    url = "{}/result-transactions/{transaction_id}:commit".format(client.base_url, transaction_id=transaction_id)

    headers: Dict[str, Any] = client.get_headers()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[AssayResultTransactionPostResponse]:
    if response.status_code == 200:
        return AssayResultTransactionPostResponse.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[AssayResultTransactionPostResponse]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    transaction_id: str,
) -> Response[AssayResultTransactionPostResponse]:
    kwargs = _get_kwargs(
        client=client,
        transaction_id=transaction_id,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    transaction_id: str,
) -> Optional[AssayResultTransactionPostResponse]:
    """ Committing a transaction will cause all results that have been uploaded to be saved and visible to others. """

    return sync_detailed(
        client=client,
        transaction_id=transaction_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    transaction_id: str,
) -> Response[AssayResultTransactionPostResponse]:
    kwargs = _get_kwargs(
        client=client,
        transaction_id=transaction_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    transaction_id: str,
) -> Optional[AssayResultTransactionPostResponse]:
    """ Committing a transaction will cause all results that have been uploaded to be saved and visible to others. """

    return (
        await asyncio_detailed(
            client=client,
            transaction_id=transaction_id,
        )
    ).parsed
