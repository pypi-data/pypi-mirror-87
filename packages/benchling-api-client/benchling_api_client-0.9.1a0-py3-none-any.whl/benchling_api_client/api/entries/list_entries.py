from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.entry_list import EntryList
from ...models.review_status import ReviewStatus
from ...models.sort import Sort
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: Client,
    page_size: Optional[int] = 50,
    next_token: Optional[str] = None,
    sort: Optional[Sort] = Sort.MODIFIEDATDESC,
    modified_at: Optional[str] = None,
    name: Optional[str] = None,
    project_id: Optional[str] = None,
    archive_reason: Optional[str] = None,
    review_status: Optional[ReviewStatus] = None,
    mentioned_in: Optional[str] = None,
    mentions: Optional[str] = None,
    ids: Optional[str] = None,
) -> Dict[str, Any]:
    url = "{}/entries".format(client.base_url)

    headers: Dict[str, Any] = client.get_headers()

    if sort is UNSET:
        json_sort = UNSET
    else:
        json_sort = sort.value if sort else None

    if review_status is UNSET:
        json_review_status = UNSET
    else:
        json_review_status = review_status.value if review_status else None

    params: Dict[str, Any] = {}
    if page_size is not None:
        params["pageSize"] = page_size
    if next_token is not None:
        params["nextToken"] = next_token
    if sort is not None:
        params["sort"] = json_sort
    if modified_at is not None:
        params["modifiedAt"] = modified_at
    if name is not None:
        params["name"] = name
    if project_id is not None:
        params["projectId"] = project_id
    if archive_reason is not None:
        params["archiveReason"] = archive_reason
    if review_status is not None:
        params["reviewStatus"] = json_review_status
    if mentioned_in is not None:
        params["mentionedIn"] = mentioned_in
    if mentions is not None:
        params["mentions"] = mentions
    if ids is not None:
        params["ids"] = ids

    return {
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[EntryList, BadRequestError]]:
    if response.status_code == 200:
        return EntryList.from_dict(cast(Dict[str, Any], response.json()))
    if response.status_code == 400:
        return BadRequestError.from_dict(cast(Dict[str, Any], response.json()))
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[EntryList, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    page_size: Optional[int] = 50,
    next_token: Optional[str] = None,
    sort: Optional[Sort] = Sort.MODIFIEDATDESC,
    modified_at: Optional[str] = None,
    name: Optional[str] = None,
    project_id: Optional[str] = None,
    archive_reason: Optional[str] = None,
    review_status: Optional[ReviewStatus] = None,
    mentioned_in: Optional[str] = None,
    mentions: Optional[str] = None,
    ids: Optional[str] = None,
) -> Response[Union[EntryList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        modified_at=modified_at,
        name=name,
        project_id=project_id,
        archive_reason=archive_reason,
        review_status=review_status,
        mentioned_in=mentioned_in,
        mentions=mentions,
        ids=ids,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    page_size: Optional[int] = 50,
    next_token: Optional[str] = None,
    sort: Optional[Sort] = Sort.MODIFIEDATDESC,
    modified_at: Optional[str] = None,
    name: Optional[str] = None,
    project_id: Optional[str] = None,
    archive_reason: Optional[str] = None,
    review_status: Optional[ReviewStatus] = None,
    mentioned_in: Optional[str] = None,
    mentions: Optional[str] = None,
    ids: Optional[str] = None,
) -> Optional[Union[EntryList, BadRequestError]]:
    """ List notebook entries """

    return sync_detailed(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        modified_at=modified_at,
        name=name,
        project_id=project_id,
        archive_reason=archive_reason,
        review_status=review_status,
        mentioned_in=mentioned_in,
        mentions=mentions,
        ids=ids,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page_size: Optional[int] = 50,
    next_token: Optional[str] = None,
    sort: Optional[Sort] = Sort.MODIFIEDATDESC,
    modified_at: Optional[str] = None,
    name: Optional[str] = None,
    project_id: Optional[str] = None,
    archive_reason: Optional[str] = None,
    review_status: Optional[ReviewStatus] = None,
    mentioned_in: Optional[str] = None,
    mentions: Optional[str] = None,
    ids: Optional[str] = None,
) -> Response[Union[EntryList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        sort=sort,
        modified_at=modified_at,
        name=name,
        project_id=project_id,
        archive_reason=archive_reason,
        review_status=review_status,
        mentioned_in=mentioned_in,
        mentions=mentions,
        ids=ids,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    page_size: Optional[int] = 50,
    next_token: Optional[str] = None,
    sort: Optional[Sort] = Sort.MODIFIEDATDESC,
    modified_at: Optional[str] = None,
    name: Optional[str] = None,
    project_id: Optional[str] = None,
    archive_reason: Optional[str] = None,
    review_status: Optional[ReviewStatus] = None,
    mentioned_in: Optional[str] = None,
    mentions: Optional[str] = None,
    ids: Optional[str] = None,
) -> Optional[Union[EntryList, BadRequestError]]:
    """ List notebook entries """

    return (
        await asyncio_detailed(
            client=client,
            page_size=page_size,
            next_token=next_token,
            sort=sort,
            modified_at=modified_at,
            name=name,
            project_id=project_id,
            archive_reason=archive_reason,
            review_status=review_status,
            mentioned_in=mentioned_in,
            mentions=mentions,
            ids=ids,
        )
    ).parsed
