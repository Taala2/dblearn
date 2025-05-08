// api.js - Модуль для взаимодействия с бэкендом

// Базовый URL API (настраивается в зависимости от окружения)
// Получаем текущий хост, чтобы api.js работал в любом окружении
const API_BASE_URL = window.location.origin; 

// Универсальная функция для выполнения запросов к API
async function fetchApi(endpoint, options = {}) {
  try {
    const url = `${API_BASE_URL}${endpoint}`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    });

    if (!response.ok) {
      throw new Error(`API ошибка: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Ошибка API:', error);
    throw error;
  }
}

// Функции для работы с уроками
const lessonsApi = {
  // Получение списка уроков с пагинацией
  getList: async (page = 1, limit = 10) => {
    const skip = (page - 1) * limit;
    return fetchApi(`/lessons/?skip=${skip}&limit=${limit}`);
  },
  
  // Получение урока по ID
  getById: async (id) => {
    return fetchApi(`/lessons/${id}`);
  },
  
  // Получение урока по slug
  getBySlug: async (slug) => {
    return fetchApi(`/lessons/by-slug/${slug}`);
  }
};

// Функции для работы с упражнениями
const exercisesApi = {
  // Получение списка упражнений с пагинацией
  getList: async (page = 1, limit = 10, lessonId = null) => {
    const skip = (page - 1) * limit;
    let endpoint = `/exercises/?skip=${skip}&limit=${limit}`;
    
    // Если указан lesson_id, добавляем его в запрос
    if (lessonId) {
      endpoint += `&lesson_id=${lessonId}`;
    }
    
    return fetchApi(endpoint);
  },
  
  // Получение упражнения по ID
  getById: async (id) => {
    return fetchApi(`/exercises/${id}`);
  },
  
  // Запуск SQL-кода для упражнения
  runSql: async (exerciseId, sqlCode) => {
    return fetchApi(`/exercises/${exerciseId}/run`, {
      method: 'POST',
      body: JSON.stringify({ sql: sqlCode })
    });
  }
};

// Экспорт API модулей
export { lessonsApi, exercisesApi };    