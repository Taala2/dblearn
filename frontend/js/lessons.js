// lessons.js - Логика для страницы уроков
import { lessonsApi } from './api.js';

// Состояние для хранения текущей страницы и общего количества уроков
const state = {
  currentPage: 1,
  limit: 6, // Количество уроков на странице
  total: 0
};

// Инициализация страницы
document.addEventListener('DOMContentLoaded', () => {
  loadLessons();
  
  // Проверяем, существует ли объект window.changePage
  if (!window.changePage) {
    // Добавляем функцию changePage в глобальный объект window
    window.changePage = function(page) {
      if (page < 1 || page > Math.ceil(state.total / state.limit)) {
        return;
      }
      
      state.currentPage = page;
      loadLessons();
      
      // Прокручиваем страницу вверх
      window.scrollTo(0, 0);
    };
  }
});

// Загрузка уроков с API
async function loadLessons() {
  try {
    const lessonsContainer = document.getElementById('lessons-list');
    lessonsContainer.innerHTML = '<div class="loading">Загрузка уроков...</div>';
    
    const data = await lessonsApi.getList(state.currentPage, state.limit);
    
    // Обновляем информацию о количестве уроков
    state.total = data.total;
    
    // Сортируем уроки по полю order
    const sortedLessons = data.items.sort((a, b) => a.order - b.order);
    
    // Отображаем уроки
    displayLessons(sortedLessons);
    
    // Обновляем пагинацию
    updatePagination();
  } catch (error) {
    showError('Не удалось загрузить уроки. Пожалуйста, попробуйте позже.');
    console.error('Ошибка загрузки уроков:', error);
  }
}

function displayLessons(lessons) {
  const lessonsContainer = document.getElementById('lessons-list');
  
  if (lessons.length === 0) {
    lessonsContainer.innerHTML = '<p>Уроки не найдены.</p>';
    return;
  }
  
  // Создаем HTML для каждого урока
  const lessonsHtml = lessons.map(lesson => `
    <div class="lesson-card">
      <h3>${lesson.title}</h3>
      <p class="lesson-info">Урок ${lesson.order} | Обновлено: ${formatDate(lesson.updated_at)}</p>
      <p class="lesson-preview">${getPreview(lesson.body_md)}</p>
      <div class="card-actions">
        <a href="lesson.html?id=${lesson.id}" class="btn btn-primary">Читать урок</a>
        <a href="exercises.html?lesson_id=${lesson.id}" class="btn btn-outline">Упражнения</a>
      </div>
    </div>
  `).join('');
  
  lessonsContainer.innerHTML = lessonsHtml;
}

// Обновление пагинации
function updatePagination() {
  const paginationContainer = document.getElementById('pagination');
  const totalPages = Math.ceil(state.total / state.limit);
  
  if (totalPages <= 1) {
    paginationContainer.innerHTML = '';
    return;
  }
  
  let paginationHtml = '';
  
  // Кнопка "Предыдущая страница"
  paginationHtml += `
    <button 
      class="btn pagination-btn" 
      ${state.currentPage === 1 ? 'disabled' : ''} 
      onclick="changePage(${state.currentPage - 1})">
      &laquo; Назад
    </button>
  `;
  
  // Номера страниц
  for (let i = 1; i <= totalPages; i++) {
    paginationHtml += `
      <button 
        class="btn pagination-btn ${state.currentPage === i ? 'active' : ''}" 
        onclick="changePage(${i})">
        ${i}
      </button>
    `;
  }
  
  // Кнопка "Следующая страница"
  paginationHtml += `
    <button 
      class="btn pagination-btn" 
      ${state.currentPage === totalPages ? 'disabled' : ''} 
      onclick="changePage(${state.currentPage + 1})">
      Вперед &raquo;
    </button>
  `;
  
  paginationContainer.innerHTML = paginationHtml;
}

// Вспомогательные функции
function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('ru-RU', { 
    day: '2-digit', 
    month: '2-digit', 
    year: 'numeric' 
  });
}

function getPreview(markdown) {
  if (!markdown) return '';
  // Простая функция для получения превью из markdown
  const plainText = markdown.replace(/#{1,6}\s?/g, '').replace(/\*\*|\*|__|_/g, '');
  return plainText.length > 150 ? plainText.slice(0, 150) + '...' : plainText;
}

function showError(message) {
  const lessonsContainer = document.getElementById('lessons-list');
  lessonsContainer.innerHTML = `<div class="error">${message}</div>`;
}