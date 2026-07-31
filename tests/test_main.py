import datetime
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient
from fastapi import status

from app.main import TASK_STORE, app

@pytest.fixture(autouse=True)
def clear_task_store() -> None:
    TASK_STORE.clear()

@pytest.mark.anyio
async def test_list_tasks_empty() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://testserver') as client:
        response = await client.get('/api/tasks')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.anyio
async def test_health_returns_200() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://testserver') as client:
        response = await client.get('/health')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'ok'}

@pytest.mark.anyio
async def test_create_task_with_due_date_and_tags() -> None:
    payload = {
        'title': 'Track release',
        'description': 'Add due date and tags to the task',
        'status': 'TODO',
        'priority': 'HIGH',
        'assignee': 'Dana',
        'due_date': datetime.date.today().isoformat(),
        'tags': ['release', 'frontend'],
    }

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://testserver') as client:
        response = await client.post('/api/tasks', json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body['title'] == payload['title']
    assert body['due_date'] == payload['due_date']
    assert body['tags'] == payload['tags']
    assert body['is_overdue'] is False

@pytest.mark.anyio
async def test_overdue_filter_returns_only_overdue_tasks() -> None:
    today = datetime.date.today()
    overdue_payload = {
        'title': 'Old task',
        'description': 'This task should be overdue',
        'status': 'TODO',
        'priority': 'LOW',
        'due_date': (today - datetime.timedelta(days=1)).isoformat(),
        'tags': ['urgent'],
    }
    future_payload = {
        'title': 'Future task',
        'description': 'Not overdue yet',
        'status': 'TODO',
        'priority': 'MEDIUM',
        'due_date': (today + datetime.timedelta(days=5)).isoformat(),
        'tags': ['planning'],
    }

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://testserver') as client:
        await client.post('/api/tasks', json=overdue_payload)
        await client.post('/api/tasks', json=future_payload)
        overdue_response = await client.get('/api/tasks?overdue=true')

    assert overdue_response.status_code == status.HTTP_200_OK
    tasks = overdue_response.json()
    assert len(tasks) == 1
    assert tasks[0]['title'] == overdue_payload['title']
    assert tasks[0]['is_overdue'] is True

@pytest.mark.anyio
async def test_tag_filter_matches_task_tags() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://testserver') as client:
        await client.post('/api/tasks', json={
            'title': 'Backend bug',
            'description': 'Fix API error',
            'status': 'TODO',
            'priority': 'MEDIUM',
            'tags': ['backend', 'bug'],
        })
        await client.post('/api/tasks', json={
            'title': 'UI polish',
            'description': 'Button styles',
            'status': 'TODO',
            'priority': 'LOW',
            'tags': ['frontend'],
        })
        filtered = await client.get('/api/tasks?tag=backend')

    assert filtered.status_code == status.HTTP_200_OK
    tasks = filtered.json()
    assert len(tasks) == 1
    assert tasks[0]['title'] == 'Backend bug'

@pytest.mark.anyio
async def test_update_task() -> None:
    initial_payload = {
        'title': 'Update demo',
        'description': 'Verify task update works',
        'status': 'TODO',
        'priority': 'MEDIUM',
        'assignee': 'Charlie',
    }

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://testserver') as client:
        create_response = await client.post('/api/tasks', json=initial_payload)
        task_id = create_response.json()['id']
        update_payload = {
            'status': 'IN_PROGRESS',
            'assignee': 'Dana',
            'tags': ['review'],
        }
        update_response = await client.patch(f'/api/tasks/{task_id}', json=update_payload)

    assert update_response.status_code == status.HTTP_200_OK
    body = update_response.json()
    assert body['id'] == task_id
    assert body['title'] == initial_payload['title']
    assert body['status'] == 'IN_PROGRESS'
    assert body['assignee'] == 'Dana'
    assert body['tags'] == ['review']


@pytest.mark.anyio
async def test_valid_status_transition_chain_returns_200() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://testserver') as client:
        created = await client.post('/api/tasks', json={'title': 'Transition task'})
        task_id = created.json()['id']
        in_progress = await client.patch(
            f'/api/tasks/{task_id}',
            json={'status': 'IN_PROGRESS'},
        )
        done = await client.patch(
            f'/api/tasks/{task_id}',
            json={'status': 'DONE'},
        )

    assert in_progress.status_code == status.HTTP_200_OK
    assert in_progress.json()['status'] == 'IN_PROGRESS'
    assert done.status_code == status.HTTP_200_OK
    assert done.json()['status'] == 'DONE'


@pytest.mark.anyio
async def test_todo_to_done_transition_returns_422() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://testserver') as client:
        created = await client.post('/api/tasks', json={'title': 'No skipping'})
        task_id = created.json()['id']
        response = await client.patch(
            f'/api/tasks/{task_id}',
            json={'status': 'DONE'},
        )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert 'Invalid status transition' in response.json()['detail']
    assert TASK_STORE[0].status.value == 'TODO'


@pytest.mark.anyio
async def test_same_status_transition_returns_422() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://testserver') as client:
        created = await client.post('/api/tasks', json={'title': 'No no-op status'})
        task_id = created.json()['id']
        response = await client.patch(
            f'/api/tasks/{task_id}',
            json={'status': 'TODO'},
        )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


@pytest.mark.anyio
async def test_explicit_null_title_update_returns_422() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://testserver') as client:
        created = await client.post('/api/tasks', json={'title': 'Keep this title'})
        task_id = created.json()['id']
        response = await client.patch(
            f'/api/tasks/{task_id}',
            json={'title': None},
        )
        stored = await client.get(f'/api/tasks/{task_id}')

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert stored.json()['title'] == 'Keep this title'


@pytest.mark.anyio
async def test_explicit_null_status_returns_422_without_corrupting_task() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://testserver') as client:
        created = await client.post('/api/tasks', json={'title': 'Keep valid status'})
        task_id = created.json()['id']
        rejected = await client.patch(
            f'/api/tasks/{task_id}',
            json={'status': None},
        )
        valid_update = await client.patch(
            f'/api/tasks/{task_id}',
            json={'status': 'IN_PROGRESS'},
        )

    assert rejected.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert valid_update.status_code == status.HTTP_200_OK
    assert valid_update.json()['status'] == 'IN_PROGRESS'


@pytest.mark.parametrize(
    ('field_name', 'original_value'),
    [
        ('description', 'Keep this description'),
        ('priority', 'HIGH'),
        ('tags', ['keep']),
    ],
)
@pytest.mark.anyio
async def test_explicit_null_required_update_fields_return_422(
    field_name: str,
    original_value,
) -> None:
    payload = {
        'title': 'Keep required fields valid',
        'description': 'Keep this description',
        'priority': 'HIGH',
        'tags': ['keep'],
    }
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://testserver') as client:
        created = await client.post('/api/tasks', json=payload)
        task_id = created.json()['id']
        rejected = await client.patch(
            f'/api/tasks/{task_id}',
            json={field_name: None},
        )
        stored = await client.get(f'/api/tasks/{task_id}')

    assert rejected.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert stored.json()[field_name] == original_value


def test_frontend_render_inserts_cards_into_tasks_container() -> None:
    javascript = (
        Path(__file__).resolve().parents[1]
        .joinpath('frontend', 'app.js')
        .read_text(encoding='utf-8')
    )

    assert 'tasksNode.appendChild(card);' in javascript


def test_frontend_edit_omits_unchanged_status_from_patch() -> None:
    javascript = (
        Path(__file__).resolve().parents[1]
        .joinpath('frontend', 'app.js')
        .read_text(encoding='utf-8')
    )

    assert 'editingTaskStatus = task.status;' in javascript
    assert 'statusInput.value === editingTaskStatus' in javascript
    assert 'delete payload.status;' in javascript


def test_frontend_uses_text_content_for_task_title() -> None:
    javascript = (
        Path(__file__).resolve().parents[1]
        .joinpath('frontend', 'app.js')
        .read_text(encoding='utf-8')
    )

    assert 'title.textContent = task.title;' in javascript
    assert 'meta.innerHTML' not in javascript


@pytest.mark.anyio
async def test_get_task_not_found() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://testserver') as client:
        response = await client.get('/api/tasks/nonexistent')
    assert response.status_code == status.HTTP_404_NOT_FOUND
