// exercises.js - Логика для страницы упражнений
import { exercisesApi } from './api.js';

// Состояние для хранения текущей страницы и общего количества упражнений
const state = {
  currentPage: 1,
  limit: 6, // Количество упражнений на странице
  total: 0,
  lessonId: null // ID урока, если упражнения фильтруются по уроку
};

// Инициализация страницы
document.addEventListener('DOMContentLoaded', () => {
  // Получаем параметры из URL
  const urlParams = new URLSearchParams(window.location.search);
  
  // Если в URL есть lesson_id, устанавливаем его в состоянии
  const lessonId = urlParams.get('lesson_id');
  if (lessonId) {
    state.lessonId = lessonId;
    
    // Добавляем информацию о фильтрации по уроку
    const headerElement = document.querySelector('.exercises-section h2');
    if (headerElement) {
      headerElement.innerHTML = 'Упражнения по уроку <span class="lesson-link"></span>';
      
      // Добавляем ссылку на урок
      const lessonLink = document.createElement('a');
      lessonLink.href = `/lesson.html?id=${lessonId}`;
      lessonLink.textContent = `#${lessonId}`;
      lessonLink.className = 'lesson-filter-link';
      document.querySelector('.lesson-link').appendChild(lessonLink);
    }
  }
  
  // Загружаем упражнения
  loadExercises();

  // Проверяем, существует ли объект window.changePage
  if (!window.changePage) {
    // Добавляем функцию changePage в глобальный объект window
    window.changePage = function(page) {
      if (page < 1 || page > Math.ceil(state.total / state.limit)) {
        return;
      }
      
      state.currentPage = page;
      loadExercises();
      
      // Прокручиваем страницу вверх
      window.scrollTo(0, 0);
    };
  }
});



// Загрузка упражнений с API
async function loadExercises() {
  try {
    const exercisesContainer = document.getElementById('exercises-list');
    exercisesContainer.innerHTML = '<div class="loading">Загрузка упражнений...</div>';
    
    // Загружаем упражнения (с фильтрацией по уроку, если нужно)
    const data = await exercisesApi.getList(state.currentPage, state.limit, state.lessonId);

    // Обновляем информацию о количестве упражнений
    state.total = data.total;
    
    // Отображаем упражнения
    displayExercises(data.items);


    // Обновляем пагинацию
    updatePagination();
  } catch (error) {
    showError('Не удалось загрузить упражнения. Пожалуйста, попробуйте позже.');
    console.error('Ошибка загрузки упражнений:', error);
  }
}
let sqlEditor = null;
// Улучшенная инициализация редактора SQL-кода
function initSqlEditor(initialCode) {
    sqlEditor = CodeMirror(document.getElementById('sql-editor'), {
      value: initialCode,
      mode: 'text/x-sql',
      theme: 'darcula',  // Темная тема для лучшей читаемости
      lineNumbers: true,
      indentWithTabs: false,
      tabSize: 2,
      indentUnit: 2,
      autoCloseBrackets: true,
      matchBrackets: true,
      extraKeys: {
        "Ctrl-Enter": runSqlCode,  // Запуск кода по Ctrl+Enter
        "Cmd-Enter": runSqlCode,   // Для Mac
        "Tab": "insertSoftTab"
      },
      hintOptions: {
        tables: {
          customers: ["id", "first_name", "last_name", "email", "city", "country", "birth_date"],
          products: ["id", "name", "description", "price", "category", "stock"],
          orders: ["id", "customer_id", "order_date", "total_amount", "status"]
        }
      }
    });
    
    // Включаем автозавершение
    sqlEditor.on("keyup", function (cm, event) {
      if (!cm.state.completionActive && 
          event.keyCode != 13 && 
          event.keyCode != 27) {
        CodeMirror.commands.autocomplete(cm, null, {completeSingle: false});
      }
    });
  }

// Отображение упражнений на странице
function displayExercises(exercises) {
  const exercisesContainer = document.getElementById('exercises-list');
  
  if (exercises.length === 0) {
    exercisesContainer.innerHTML = '<p>Упражнения не найдены.</p>';
    return;
  }
  
  // Создаем HTML для каждого упражнения
  const exercisesHtml = exercises.map(exercise => `
    <div class="exercise-card">
      <h3>${exercise.title}</h3>
      <p class="exercise-info">
        Порядок: ${exercise.order} | 
        Создано: ${formatDate(exercise.created_at)}
      </p>
      <p class="exercise-preview">${getPreview(exercise.description_md)}</p>
      <a href="/exercise.html?id=${exercise.id}" class="btn">Выполнить упражнение</a>
    </div>
  `).join('');
  
  exercisesContainer.innerHTML = exercisesHtml;
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
  // Простая функция для получения превью из markdown
  // В реальном приложении можно использовать библиотеку для обработки markdown
  if (!markdown) return '';
  const plainText = markdown.replace(/#{1,6}\s?/g, '').replace(/\*\*|\*|__|_/g, '');
  return plainText.length > 150 ? plainText.slice(0, 150) + '...' : plainText;
}

function showError(message) {
  const exercisesContainer = document.getElementById('exercises-list');
  exercisesContainer.innerHTML = `<div class="error">${message}</div>`;
}