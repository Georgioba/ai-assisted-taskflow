const apiBase = '/api/tasks';
const tasksNode = document.getElementById('tasks');
const form = document.getElementById('create-task-form');
const errorNode = document.getElementById('form-error');
const titleInput = document.getElementById('title');
const descriptionInput = document.getElementById('description');
const statusInput = document.getElementById('status');
const priorityInput = document.getElementById('priority');
const assigneeInput = document.getElementById('assignee');
const dueDateInput = document.getElementById('due-date');
const tagsInput = document.getElementById('tags');
const taskIdInput = document.getElementById('task-id');
const submitButton = document.getElementById('submit-button');
const cancelButton = document.getElementById('cancel-button');
const formHeading = document.getElementById('form-heading');
const filterOverdueInput = document.getElementById('filter-overdue');
const filterTagInput = document.getElementById('filter-tag');
const applyFiltersButton = document.getElementById('apply-filters');
const clearFiltersButton = document.getElementById('clear-filters');

let editingTaskId = null;

function buildQueryString() {
  const params = new URLSearchParams();
  if (filterOverdueInput.checked) {
    params.set('overdue', 'true');
  }
  if (filterTagInput.value.trim()) {
    params.set('tag', filterTagInput.value.trim());
  }
  return params.toString();
}

async function fetchTasks() {
  const query = buildQueryString();
  const url = query ? `${apiBase}?${query}` : apiBase;
  const response = await fetch(url);
  const tasks = await response.json();
  renderTasks(tasks);
}

function renderTasks(tasks) {
  tasksNode.innerHTML = '';
  if (!tasks.length) {
    tasksNode.textContent = 'No tasks yet.';
    return;
  }

  tasks.forEach(task => {
    const card = document.createElement('div');
    card.className = 'task-card';

    const meta = document.createElement('div');
    meta.className = 'meta';
    const overdueLabel = task.is_overdue ? '<span class="task-pill">Overdue</span>' : '';
    meta.innerHTML = `
      <strong>${task.title}</strong>
      <span>${task.status}</span>
      <span>${task.priority}</span>
      <span>${task.assignee || 'Unassigned'}</span>
      ${overdueLabel}
    `;

    const description = document.createElement('p');
    description.textContent = task.description;

    const dateLine = document.createElement('p');
    dateLine.textContent = task.due_date ? `Due ${task.due_date}` : 'No due date';

    const tagsLine = document.createElement('div');
    tagsLine.className = 'task-tags';
    task.tags.forEach(tag => {
      const chip = document.createElement('span');
      chip.className = 'task-chip';
      chip.textContent = tag;
      tagsLine.appendChild(chip);
    });

    const editButton = document.createElement('button');
    editButton.textContent = 'Edit';
    editButton.addEventListener('click', () => setFormMode(task));

    const deleteButton = document.createElement('button');
    deleteButton.className = 'secondary';
    deleteButton.textContent = 'Delete';
    deleteButton.addEventListener('click', () => deleteTask(task.id));

    card.append(meta, description, dateLine, tagsLine, editButton, deleteButton);
    tasksNode.appendChild(card);
  });
}

function parseTags(value) {
  return value
    .split(',')
    .map(tag => tag.trim())
    .filter(Boolean);
}

function setFormMode(task = null) {
  if (task) {
    editingTaskId = task.id;
    taskIdInput.value = task.id;
    titleInput.value = task.title;
    descriptionInput.value = task.description;
    statusInput.value = task.status;
    priorityInput.value = task.priority;
    assigneeInput.value = task.assignee || '';
    dueDateInput.value = task.due_date || '';
    tagsInput.value = task.tags.join(', ');
    formHeading.textContent = 'Edit Task';
    submitButton.textContent = 'Update task';
    cancelButton.classList.remove('hidden');
  } else {
    editingTaskId = null;
    taskIdInput.value = '';
    form.reset();
    formHeading.textContent = 'Create Task';
    submitButton.textContent = 'Create task';
    cancelButton.classList.add('hidden');
  }
}

async function submitTask(event) {
  event.preventDefault();
  errorNode.textContent = '';

  const payload = {
    title: titleInput.value,
    description: descriptionInput.value,
    status: statusInput.value,
    priority: priorityInput.value,
    assignee: assigneeInput.value || undefined,
    due_date: dueDateInput.value || undefined,
    tags: parseTags(tagsInput.value),
  };

  const url = editingTaskId ? `${apiBase}/${editingTaskId}` : apiBase;
  const method = editingTaskId ? 'PATCH' : 'POST';

  const response = await fetch(url, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const error = await response.json();
    errorNode.textContent = error.detail || 'Failed to save task';
    return;
  }

  setFormMode(null);
  await fetchTasks();
}

async function deleteTask(taskId) {
  await fetch(`${apiBase}/${taskId}`, { method: 'DELETE' });
  await fetchTasks();
}

function clearFilters() {
  filterOverdueInput.checked = false;
  filterTagInput.value = '';
  fetchTasks();
}

form.addEventListener('submit', submitTask);
cancelButton.addEventListener('click', () => setFormMode(null));
applyFiltersButton.addEventListener('click', fetchTasks);
clearFiltersButton.addEventListener('click', clearFilters);
fetchTasks();
