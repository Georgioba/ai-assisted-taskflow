import datetime

import pytest
from httpx import ASGITransport, AsyncClient
from fastapi import status

from app.main import TASK_STORE, app

@pytest.fixture(autouse=True)
def clear_task_store() -> None:
    TASK_STORE.clear()

@pytest.mark.anyio
async def test_empty_tag_returns_422() -> None:
    payload = {
        'title': 'Reject empty tag',
        'status': 'TODO',
        'priority': 'LOW',
        'tags': ['first', '   ', 'second'],
    }
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://testserver') as client:
        response = await client.post('/api/tasks', json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

@pytest.mark.anyio
async def test_too_many_tags_returns_422() -> None:
    payload = {
        'title': 'Too many tags',
        'status': 'TODO',
        'priority': 'LOW',
        'tags': ['a','b','c','d','e','f'],
    }
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://testserver') as client:
        response = await client.post('/api/tasks', json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

@pytest.mark.anyio
async def test_invalid_due_date_format_returns_422() -> None:
    payload = {
        'title': 'Bad date',
        'status': 'TODO',
        'priority': 'LOW',
        'due_date': 'not-a-date',
    }
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://testserver') as client:
        response = await client.post('/api/tasks', json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

@pytest.mark.anyio
async def test_overdue_flag_detected() -> None:
    today = datetime.date.today()
    payload = {
        'title': 'Overdue test',
        'status': 'TODO',
        'priority': 'LOW',
        'due_date': (today - datetime.timedelta(days=2)).isoformat(),
    }
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://testserver') as client:
        r = await client.post('/api/tasks', json=payload)
        assert r.status_code == status.HTTP_201_CREATED
        tasks = await client.get('/api/tasks?overdue=true')
    assert tasks.status_code == status.HTTP_200_OK
    body = tasks.json()
    assert any(t['title'] == 'Overdue test' and t['is_overdue'] for t in body)

@pytest.mark.anyio
async def test_tags_preserved_on_unrelated_patch() -> None:
    payload = {
        'title': 'Preserve tags',
        'status': 'TODO',
        'priority': 'LOW',
        'tags': ['persist'],
    }
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://testserver') as client:
        create = await client.post('/api/tasks', json=payload)
        task_id = create.json()['id']
        patch = await client.patch(f'/api/tasks/{task_id}', json={'description': 'updated'})
    assert patch.status_code == status.HTTP_200_OK
    body = patch.json()
    assert body['tags'] == ['persist']


@pytest.mark.anyio
async def test_due_date_can_be_updated() -> None:
    today = datetime.date.today()
    payload = {
        'title': 'Update due date',
        'status': 'TODO',
        'priority': 'MEDIUM',
        'due_date': (today + datetime.timedelta(days=5)).isoformat(),
    }
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://testserver') as client:
        created = await client.post('/api/tasks', json=payload)
        task_id = created.json()['id']
        new_due_date = (today - datetime.timedelta(days=1)).isoformat()
        response = await client.patch(
            f'/api/tasks/{task_id}',
            json={'due_date': new_due_date},
        )

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body['due_date'] == new_due_date
    assert body['is_overdue'] is True
