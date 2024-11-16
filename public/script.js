const mosquito = document.getElementById("mosquito");
const message = document.getElementById("message");
const gameContainer = document.getElementById("game-container");

let score = 0;
let missed = 0; // Считаем "укусы"
let speed = 1000; // Начальная скорость движения (мс)
let moveInterval;
let biteTimer;

// Факты о малярии
const malariaFacts = [
    "Малярия убивает более 600 тысяч человек ежегодно.",
    "Самки комаров Anopheles — переносчики малярии.",
    "Каждые 60 секунд от малярии умирает ребенок.",
    "Вакцина против малярии была разработана в 2021 году.",
    "Профилактика малярии спасает миллионы жизней."
];

// Устанавливаем начальную позицию комара
function moveMosquito() {
    const x = Math.random() * (gameContainer.offsetWidth - mosquito.offsetWidth);
    const y = Math.random() * (gameContainer.offsetHeight - mosquito.offsetHeight);
    mosquito.style.left = `${x}px`;
    mosquito.style.top = `${y}px`;
}

// Показываем случайный факт о малярии
function showMalariaFact() {
    const fact = malariaFacts[Math.floor(Math.random() * malariaFacts.length)];
    alert(`Факт о малярии:\n${fact}`);
}

// Запускаем цикл движения комара
function startMosquitoMovement() {
    moveInterval = setInterval(() => {
        moveMosquito();
    }, speed);
    startBiteTimer(); // Запускаем таймер укусов
}

// Таймер укусов
function startBiteTimer() {
    clearTimeout(biteTimer); // Убираем предыдущий таймер
    biteTimer = setTimeout(() => {
        missed++;
        message.textContent = `Счёт: ${score} | Укусы: ${missed}`;

        // Показываем факт о малярии на каждый 3-й укус
        if (missed % 3 === 0) {
            showMalariaFact();
        }

        // Перезапускаем таймер укусов для следующего комара
        startBiteTimer();
    }, 3000); // 3 секунды на реакцию
}

// Когда игрок "убивает" комара
mosquito.addEventListener("click", () => {
    score++;
    message.textContent = `Счёт: ${score} | Укусы: ${missed}`;
    clearTimeout(biteTimer); // Отменяем укус, если игрок успел

    // Каждая 5-я поимка увеличивает скорость
    if (score % 5 === 0) {
        speed = Math.max(100, speed * 0.8); // Минимальная скорость — 100 мс
        clearInterval(moveInterval);
        startMosquitoMovement(); // Перезапускаем движение с новой скоростью
    }

    moveMosquito(); // Сразу перемещаем комара
    startBiteTimer(); // Перезапускаем таймер укусов
});

// Запускаем игру
moveMosquito();
startMosquitoMovement();
