from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.automation_file_output_list import AutomationFileOutputList
from ...models.bad_request_error import BadRequestError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    assay_run_id: str,
    next_token: Optional[str] = None,
) -> Dict[str, Any]:
    url = "{}/assay-runs/{assay_run_id}/automation-output-processors".format(client.base_url, assay_run_id=assay_run_id)

    headers: Dict[str, Any] = client.get_headers()

    params: Dict[str, Any] = {}
    if next_token is not None:
        params["nextToken"] = next_token

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[AutomationFileOutputList, BadRequestError]]:
    if response.status_code == 200:
        return AutomationFileOutputList.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[AutomationFileOutputList, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    assay_run_id: str,
    next_token: Optional[str] = None,
) -> Response[Union[AutomationFileOutputList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        assay_run_id=assay_run_id,
        next_token=next_token,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    assay_run_id: str,
    next_token: Optional[str] = None,
) -> Optional[Union[AutomationFileOutputList, BadRequestError]]:
    """  """

    return sync_detailed(
        client=client,
        assay_run_id=assay_run_id,
        next_token=next_token,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    assay_run_id: str,
    next_token: Optional[str] = None,
) -> Response[Union[AutomationFileOutputList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        assay_run_id=assay_run_id,
        next_token=next_token,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    assay_run_id: str,
    next_token: Optional[str] = None,
) -> Optional[Union[AutomationFileOutputList, BadRequestError]]:
    """  """

    return (
        await asyncio_detailed(
            client=client,
            assay_run_id=assay_run_id,
            next_token=next_token,
        )
    ).parsed
