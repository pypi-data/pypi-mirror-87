from typing import Any, Dict, Optional, cast

import httpx

from ...client import Client
from ...models.assay_result_transaction_post_response import AssayResultTransactionPostResponse
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/result-transactions".format(client.base_url)

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
) -> Response[AssayResultTransactionPostResponse]:
    kwargs = _get_kwargs(
        client=client,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
) -> Optional[AssayResultTransactionPostResponse]:
    """Transactions allow results to be upload in multiple requests. This endpoint lets you create a transaction. You can then upload results to the transaction, abort the transaction, or commit the transaction."""

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
) -> Response[AssayResultTransactionPostResponse]:
    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
) -> Optional[AssayResultTransactionPostResponse]:
    """Transactions allow results to be upload in multiple requests. This endpoint lets you create a transaction. You can then upload results to the transaction, abort the transaction, or commit the transaction."""

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
