// Основные переменные
const mosquito = document.getElementById("mosquito-img"); // Комар
const gameContainer = document.getElementById("game-container");

let level = 1; // Текущий уровень
let score = 0; // Количество пойманных комаров
let mosquitoTarget = 0; // Цель уровня
let mosquitoSpeed = 1000; // Скорость комаров
let timeLeft = 30; // Время на уровень
let levelTimer, moveInterval;

// Проверяем, что элементы существуют
if (!mosquito || !gameContainer) {
    console.error("Ошибка: элементы mosquito или gameContainer не существуют.");
}

// Движение комара
function moveMosquito() {
    const containerWidth = gameContainer.offsetWidth;
    const containerHeight = gameContainer.offsetHeight;

    const x = Math.random() * (containerWidth - mosquito.offsetWidth);
    const y = Math.random() * (containerHeight - mosquito.offsetHeight);

    mosquito.style.left = `${x}px`;
    mosquito.style.top = `${y}px`;
}

// Запуск движения комара
function startMosquitoMovement() {
    clearInterval(moveInterval); // Убираем предыдущие интервалы
    moveInterval = setInterval(moveMosquito, mosquitoSpeed); // Комар двигается с заданной скоростью
}

// Обработка кликов по комару
mosquito.addEventListener("click", () => {
    score++;

    // Обновляем интерфейс
    const targetElement = document.getElementById("target");
    targetElement.textContent = mosquitoTarget - score;

    // Добавляем пятно крови
    const blood = document.createElement("div");
    blood.classList.add("blood");
    blood.style.left = `${mosquito.style.left}`;
    blood.style.top = `${mosquito.style.top}`;
    gameContainer.appendChild(blood);

    // Проверяем выполнение цели
    if (score >= mosquitoTarget) {
        clearInterval(levelTimer);
        clearInterval(moveInterval);
        showLevelComplete();
    }
});

// Начало уровня
function startLevel() {
    // Очищаем пятна крови
    const bloodStains = document.querySelectorAll(".blood");
    bloodStains.forEach((stain) => stain.remove());

    mosquitoTarget = Math.ceil(10 * (1.3 * level));
    score = 0;
    timeLeft = 30;

    // Обновляем интерфейс
    document.getElementById("level").textContent = level;
    document.getElementById("target").textContent = mosquitoTarget;
    document.getElementById("timer").textContent = timeLeft;

    mosquitoSpeed = Math.max(300, 1000 - level * 100);

    moveMosquito(); // Перемещаем комара сразу
    startMosquitoMovement(); // Запускаем его движение

    levelTimer = setInterval(updateTimer, 1000); // Запускаем таймер уровня
}

// Таймер уровня
function updateTimer() {
    const timerElement = document.getElementById("timer");
    timeLeft--;

    timerElement.textContent = timeLeft;

    if (timeLeft <= 0) {
        clearInterval(levelTimer);
        clearInterval(moveInterval);

        if (score >= mosquitoTarget) {
            showLevelComplete();
        } else {
            showModal("Ты не успел выполнить цель. Игра окончена!", resetGame);
        }
    }
}

// Завершение уровня
function showLevelComplete() {
    clearInterval(levelTimer);
    clearInterval(moveInterval);

    const malariaFacts = [
        "Малярия убивает более 600 тысяч человек ежегодно.",
        "Самки комаров Anopheles — переносчики малярии.",
        "Каждые 60 секунд от малярии умирает ребенок.",
        "Вакцина против малярии была разработана в 2021 году.",
        "Профилактика малярии спасает миллионы жизней."
    ];

    const fact = malariaFacts[Math.floor(Math.random() * malariaFacts.length)];
    showModal(`Поздравляем! Ты прошёл уровень ${level}!\n\nИнтересный факт: ${fact}`, () => {
        level++;
        startLevel(); // Переход к следующему уровню
    });
}

// Завершение игры
function resetGame() {
    level = 1;
    score = 0;
    startLevel();
}

// Показ модального окна
function showModal(message, callback) {
    const modal = document.getElementById("modal");
    const modalText = document.getElementById("modal-text");
    const modalButton = document.getElementById("modal-button");

    modalText.textContent = message; // Устанавливаем текст сообщения
    modal.classList.remove("hidden"); // Показываем модальное окно

    modalButton.onclick = () => {
        modal.classList.add("hidden"); // Скрываем окно
        if (callback) callback(); // Выполняем переданную функцию
    };
}

// Запуск игры
document.addEventListener("DOMContentLoaded", () => {
    startLevel(); // Игра начинается с первого уровня
});
