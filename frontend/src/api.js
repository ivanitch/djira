export function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// apiFetch('/api/tracker/tasks/move', { method: 'POST', body: ... })
export async function apiFetch(url, options = {}) {
  const csrftoken = getCookie('csrftoken');

  const defaultHeaders = {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrftoken, // Добавляем токен для Django
  };

  const finalOptions = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  };

  return fetch(url, finalOptions);
}
