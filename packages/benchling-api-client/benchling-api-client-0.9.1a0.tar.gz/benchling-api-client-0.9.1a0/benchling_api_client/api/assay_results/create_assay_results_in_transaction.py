from typing import Any, Dict, Optional, cast

import httpx

from ...client import Client
from ...models.assay_result_bulk_create import AssayResultBulkCreate
from ...models.assay_result_post_response import AssayResultPostResponse
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    transaction_id: str,
    json_body: AssayResultBulkCreate,
) -> Dict[str, Any]:
    url = "{}/result-transactions/{transaction_id}/results".format(client.base_url, transaction_id=transaction_id)

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[AssayResultPostResponse]:
    if response.status_code == 200:
        return AssayResultPostResponse.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[AssayResultPostResponse]:
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
    json_body: AssayResultBulkCreate,
) -> Response[AssayResultPostResponse]:
    kwargs = _get_kwargs(
        client=client,
        transaction_id=transaction_id,
        json_body=json_body,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    transaction_id: str,
    json_body: AssayResultBulkCreate,
) -> Optional[AssayResultPostResponse]:
    """  """

    return sync_detailed(
        client=client,
        transaction_id=transaction_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    transaction_id: str,
    json_body: AssayResultBulkCreate,
) -> Response[AssayResultPostResponse]:
    kwargs = _get_kwargs(
        client=client,
        transaction_id=transaction_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    transaction_id: str,
    json_body: AssayResultBulkCreate,
) -> Optional[AssayResultPostResponse]:
    """  """

    return (
        await asyncio_detailed(
            client=client,
            transaction_id=transaction_id,
            json_body=json_body,
        )
    ).parsed
