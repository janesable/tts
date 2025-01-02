print("Код начал выполняться...")
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.types import WebAppInfo
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен твоего бота
TOKEN = "7110746024:AAEoPCxb06_4IN0fY8aMVkVw0VIDSEVmHVE"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Данные викторины
quiz_data = [
    {
        "question": "1. Какой комар является переносчиком малярии?",
        "options": ["Culex", "Anopheles", "Aedes"],
        "correct": 1,
        "explanation": "Комары рода *Anopheles* являются основными и единственными переносчиками возбудителя малярии - малярийного плазмодия. Узнать больше можно по [ссылке](https://www.who.int/ru/news-room/fact-sheets/detail/malaria)."
    },
    {
        "question": "2. Сколько стадий жизненного цикла претерпевает малярийный плазмодий, попадая в кровь человека?",
        "options": ["2", "3", "4"],
        "correct": 2,
        "explanation": "Развитие плазмодиев в эритроцитах проходит четыре стадии: кольца (трофозоита), амебовидного шизонта, фрагментации (образования морулы) и (для части паразитов) образования гаметоцитов.. Подробнее [здесь](https://www.medicoverhospitals.in/ru/articles/malaria-life-cycle)."
    },
    {
         "question": "3. Сколько видов малярийных комаров рода Anopheles способны переносить малярию?",
         "options": ["Менее 10", "Около 30", "Более 60", "Более 200"],
         "correct": 2,
         "explanation": " Только около 70 из более чем 450 видов Anopheles способны эффективно переносить малярию. Не веришь? Смотри [здесь] (https://www.science.org/doi/10.1126/science.1258522)"
    },
    {
         "question": "4. Какой вид малярийного паразита вызывает самые тяжелые формы заболевания у человека?",
         "options": ["Plasmodium vivax", "Plasmodium malariae", "Plasmodium falciparum", "Plasmodium ovale"],
         "correct": 2,
         "explanation": " Plasmodium falciparum является наиболее смертоносным видом малярийного паразита, вызывая так называемую тропическую малярию и около 90% всех смертей от малярии. В свою очередь, Plasmodium vivax ответственный за нелетальную трех-дневную малярию, которая менее опасная. [Источник](https://www.who.int/ru/news-room/facts-in-pictures/detail/malaria)"
    },
    {
         "question": "5. Какой орган малярийный паразит поражает первым после укуса комара?",
         "options": ["Сердце", "Печень", "Легкие", "Головной мозг"],
         "correct": 1,
         "explanation": "После укуса комара паразит мигрирует в печень, где размножается перед выходом в кровь. [Источник](https://ru.wikipedia.org/wiki/Малярия#Этиология_и_патогенез)"
    },
    {
         "question": "6. Что привлекает малярийных комаров к человеку?",
         "options": ["Свет", "Углекислый газ", "Высокая температура", "Все вышеперечисленное"],
         "correct": 3,
         "explanation": "Малярийные комары ориентируются на тепло тела, запах пота и углекислый газ, выделяемый дыханием. Где почитать? [Здесь](https://malariajournal.biomedcentral.com/articles/10.1186/1475-2875-9-292)"
    },
    {
         "question": "7. Какой основной способ предотвращения передачи малярии?",
         "options": ["Вакцинация", "Использование москитных сеток с инсектицидами", "Постоянное применение антибиотиков", "Снижение влажности воздуха"],
         "correct": 1,
         "explanation": "Москитные сетки, обработанные инсектицидами, являются наиболее экономически доступным и эффективным методом профилактики. Так говорит [ВОЗ](https://www.who.int/ru/news-room/facts-in-pictures/detail/malaria)"
    },
    {
         "question": "8. Какой вид малярийного комара является основным переносчиком малярии в Африке?",
         "options": ["Anopheles stephensi", "Anopheles albimanus", "Anopheles gambiae", "Anopheles quadrimaculatus"],
         "correct": 2,
         "explanation": "Anopheles stephensi можно встретить на Аравийском полуострове, Anopheles albimanus - постоянный житель регионов Центральной Америки, Anopheles quadrimaculatus скоромно летает по Соединенным Штатам. Есть хорошая [картинка](https://upload.wikimedia.org/wikipedia/commons/a/ad/Anopheles-range-map.png), которая примерно показывает распространение малярийных комаров"
    },
    {
         "question": "9. Какой из следующих методов используется для генетической модификации малярийных комаров с целью снижения их способности передавать малярию?",
         "options": ["CRISPR-Cas9", "RNA interference", "TALENs", "ZFN"],
         "correct": 0,
         "explanation": "CRISPR-Cas9 широко используется для редактирования генома малярийных комаров, чтобы снизить их способность передавать возбудителя малярии. [Подробнее об этом](https://pmc.ncbi.nlm.nih.gov/articles/PMC4913862/)"
    },
    {
         "question": "10. Какой из следующих факторов НЕ способствует распространению малярии?",
         "options": ["Стоячая вода", "Высокая температура", "Низкая влажность", "Плотная растительность"],
         "correct": 2,
         "explanation": "Ну давайте рассудим логически: стоячая вода и плотная растительность - это то, что любят большинство Anopheles. Главное чтобы их не беспокоили и было где спрятаться. Высокая температура в целом, тоже не является проблемой, так как некоторые виды способны выживать в условиях где температура превышает 40°C. А вот низкая влажность снижает выживаемость личинок комаров, что уменьшает шансы на появление взрослых особей, и соответственно, риск передачи малярии."
    },
    {
         "question": "11. Какой из следующих симптомов является характерным для тяжелой формы малярии?",
         "options": ["Легкая лихорадка", "Головная боль", "Желтуха", "Сыпь"],
         "correct": 2,
         "explanation": "Желтуха может указывать на поражение печени и является признаком тяжелой малярии. [Источник](https://ru.wikipedia.org/wiki/Малярия#Этиология_и_патогенез)"
    },
    {
         "question": "12. Какой из следующих методов контроля популяции малярийных комаров считается экологически безопасным?",
         "options": ["Массовое распыление инсектицидов", "Осушение болот", "Введение стерильных самцов"],
         "correct": 2,
         "explanation": "Введение стерильных самцов снижает популяцию комаров без использования химических веществ, что минимизирует воздействие на окружающую среду. Кажется, логично?"
    },
    {
         "question": "13. Была ли когда-нибудь малярия в России, или это болезнь распространена только в жарких странах?",
         "options": ["Да, была", "Нет, она только в Африке бывает"],
         "correct": 0,
         "explanation": "Да, малярия была распространена как массовое заболевание на территории России с 1920х годов. В 50-60х годах угроза массового распространения была ликвидирована, однако после распада СССР ситуация вновь осложнилась на территории Москвы и МО. Ситуацию удалось стабилизировать в начале нулевых. Почитать [здесь](https://doi.org/10.1186/s12936-020-03187-8)"
    },
    {
         "question": "14. Правда ли, что вакцину от малярии изобрели?",
         "options": ["Да", "К сожалению, нет", "Не вакцину, а сыворотку"],
         "correct": 0,
         "explanation": "Да, действительно, в 2021 году ВОЗ анонсировала первую вакцину на основе рекомбинантного белка RTS,S/AS01 для детей. Эта вакцина доказала свою способность значительно снижать заболеваемость малярией и, в частности, развитие ее смертельной тяжелой формы среди детей младшего возраста. В октябре 2023 г. ВОЗ рекомендовала вторую безопасную и эффективную вакцину против малярии R21/Matrix-M. Если не верите, смотрите сами [тут](https://ggsel.net/catalog/product/4026100)"
    },
    {
         "question": "15. Какой факт про малярийных комаров является правдой? 1. Малярийные комары боятся красного света; 2. Комары предпочитают кусать только тех, кто съел что-то вкусное; 3. Малярийные комары - самые смертоносные животные на планете; 4. После укуса человека комары впрыскивают паразита и сразу же погибают",
         "options": ["1", "2", "3", "4"],
         "correct": 2,
         "explanation": "Возможно, вы сейчас удивитесь, но да, малярийные комары САМЫЕ смертоносные существа, ведь от них погибает более 600 тысяч целовек в год. Для сравнения: от акул погибает 6-15 чел/год, а от собак 58 тыс. чел/год [Вот так вот.](https://journal.tinkoff.ru/short/dangerous-meow/)"
    },
    {
         "question": "16. Ну и финальный вопрос: кто все-таки нас кусает? Самки или самцы?",
         "options": ["Самки", "И те, и другие. По настроению", "Женщин кусают самцы, а мужчин самки", "Самцы"],
         "correct": 0,
         "explanation": "Давайте уже наконец закроем этот вопрос раз и навсегда: нас кусают только самки! У самцов недоразвит ротовой аппарат, по этому они спокойно пасутся на лугу и пьют цветочный нектар. Их роль - только осеменять самок. [Закрепляем](https://ru.wikipedia.org/wiki/Кровососущие_комары)"
    }
    # Добавь сюда больше вопросов
]

# Состояние пользователей
user_states = {}

# Команда /start
@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Играть", callback_data="play_game")],
        [InlineKeyboardButton(text="🧠 Викторина", callback_data="start_quiz")]
    ])
    await message.answer("Добро пожаловать! Выберите действие:", reply_markup=keyboard)

# запуск игры
@dp.callback_query(lambda call: call.data == "play_game")
async def play_game(callback: types.CallbackQuery):
    await callback.answer()  # Закрыть уведомление
    game_url = "https://taptosurvive.vercel.app"  # Ссылка на опубликованную игру
    web_app = WebAppInfo(url=game_url)
    await callback.message.answer(
        "Нажми на кнопку ниже, чтобы открыть игру прямо в Telegram:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎮 Играть", web_app=web_app)]
        ])
    )


# Запуск викторины
@dp.callback_query(lambda call: call.data == "start_quiz")
async def start_quiz(callback: types.CallbackQuery):
    logger.info(f"Пользователь {callback.from_user.id} начал викторину.")
    user_id = callback.from_user.id
    user_states[user_id] = {"current_question": 0, "score": 0}
    await callback.answer()  # Закрываем уведомление
    await send_question(user_id)

# Отправка вопроса
async def send_question(user_id):
    try:
        state = user_states.get(user_id, {"current_question": 0, "score": 0})
        user_states[user_id] = state  # Убедимся, что состояние сохраняется

        current_question = state["current_question"]
        logger.info(f"Пользователь {user_id}, текущий вопрос: {current_question}")

        if current_question >= len(quiz_data):
            score = state["score"]
            total = len(quiz_data)
            logger.info(f"Викторина завершена для пользователя {user_id}. Баллы: {score}/{total}")

            if score <= 1:
                message = f"Ты набрал {score}/{total} баллов. Пу-пу-пууу... ну как бы сказать, чтобы не обидеть... эм... может еще раз пройдем тестик? :)"
            elif score <= 5:
                message = f"Ты набрал {score}/{total} баллов. Давай так, если собирешься в отпуск в Африку, обещай что в одиночку не поедешь. Мало ли... или лучше перепройти тест"
            elif score <= 10:
                message = f"Ты набрал {score}/{total} баллов. Это весьма не плохо! Для новичка :) Скинь друзьям, проверим на сколько они хороши в этом?"
            elif score <= 15:
                message = f"Ты набрал {score}/{total} баллов. Это было впечатляюще! Возможно, стоит задуматься о просветительской карьере. Такие знания не должны пропадать!"
            else:
                message = f"Ты набрал {score}/{total} баллов. Чтобы ответить про малярийных комаров нужно думать как малярийный комар - этим вы руководствовались? Отличный результат, кажется, у нас появился новый эксперт!"

            await bot.send_message(user_id, message)
            user_states.pop(user_id, None)
            return

        question = quiz_data[current_question]
        options = question.get("options", [])
        if not options:  # Если список вариантов пуст
            logger.error(f"Ошибка: пустые варианты ответа для вопроса {current_question}.")
            await bot.send_message(user_id, "Ошибка в данных викторины.")
            user_states.pop(user_id, None)
            return

        # Создаём клавиатуру с вариантами ответов
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=opt, callback_data=f"answer_{i}")]
            for i, opt in enumerate(options)
        ])

        # Отправляем вопрос
        await bot.send_message(user_id, question["question"], reply_markup=keyboard)
    except Exception as e:
        logger.error(f"Ошибка в send_question для пользователя {user_id}: {e}")
        await bot.send_message(user_id, "Произошла ошибка. Попробуйте снова с /start.")

# Обработка ответа
@dp.callback_query(lambda call: call.data.startswith("answer_"))
async def process_answer(callback: types.CallbackQuery):
    try:
        user_id = callback.from_user.id
        state = user_states.get(user_id)

        if not state:  # Если состояние отсутствует
            logger.warning(f"Пользователь {user_id} пытается ответить без активной викторины.")
            await callback.answer("Викторина не активна. Начните с /start.")
            return

        current_question = state["current_question"]
        question = quiz_data[current_question]
        options = question.get("options", [])
        correct_answer = question.get("correct", -1)

        # Проверяем корректность индекса правильного ответа
        if correct_answer < 0 or correct_answer >= len(options):
            logger.error(f"Индекс правильного ответа выходит за пределы. Вопрос: {current_question}.")
            await callback.message.answer("Ошибка: данные викторины некорректны.")
            user_states.pop(user_id, None)
            return

        # Проверяем ответ пользователя
        user_answer = int(callback.data.split("_")[1])
        logger.info(f"Пользователь {user_id} ответил {user_answer} на вопрос {current_question}.")

        if user_answer == correct_answer:
            state["score"] += 1
            response = "✅ Правильно!"
        else:
            correct_option = options[correct_answer]
            response = f"❌ Неправильно. Правильный ответ: {correct_option}."

        response += f"\n\n{question.get('explanation', '')}"
        await callback.message.answer(response, parse_mode="Markdown")
        await callback.answer()

        # Переходим к следующему вопросу
        state["current_question"] += 1
        await send_question(user_id)
    except Exception as e:
        logger.error(f"Ошибка в process_answer для пользователя {callback.from_user.id}: {e}")
        await callback.message.answer("Произошла ошибка. Попробуйте снова с /start.")

# Запуск бота
async def main():
    try:
        logger.info("Бот запускается...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка в главном цикле: {e}")

if __name__ == "__main__":
    asyncio.run(main())
