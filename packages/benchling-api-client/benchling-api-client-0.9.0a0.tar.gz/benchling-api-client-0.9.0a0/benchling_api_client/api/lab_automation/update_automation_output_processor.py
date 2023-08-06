from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.automation_output_processor import AutomationOutputProcessor
from ...models.bad_request_error import BadRequestError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    output_processor_id: str,
    json_body: Dict[Any, Any],
) -> Dict[str, Any]:
    url = "{}/automation-output-processors/{output_processor_id}".format(
        client.base_url, output_processor_id=output_processor_id
    )

    headers: Dict[str, Any] = client.get_headers()

    json_json_body = json_body

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[AutomationOutputProcessor, BadRequestError]]:
    if response.status_code == 200:
        return AutomationOutputProcessor.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[AutomationOutputProcessor, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    output_processor_id: str,
    json_body: Dict[Any, Any],
) -> Response[Union[AutomationOutputProcessor, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        output_processor_id=output_processor_id,
        json_body=json_body,
    )

    response = httpx.patch(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    output_processor_id: str,
    json_body: Dict[Any, Any],
) -> Optional[Union[AutomationOutputProcessor, BadRequestError]]:
    """  """

    return sync_detailed(
        client=client,
        output_processor_id=output_processor_id,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    output_processor_id: str,
    json_body: Dict[Any, Any],
) -> Response[Union[AutomationOutputProcessor, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        output_processor_id=output_processor_id,
        json_body=json_body,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.patch(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    output_processor_id: str,
    json_body: Dict[Any, Any],
) -> Optional[Union[AutomationOutputProcessor, BadRequestError]]:
    """  """

    return (
        await asyncio_detailed(
            client=client,
            output_processor_id=output_processor_id,
            json_body=json_body,
        )
    ).parsed
