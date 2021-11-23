                                     Спецификация Duty_Rescuer_Bot

 
 
 Общие сведения:

1. Duty_Rescuer_Bot- это бот, созданный для того чтобы каждый член группы всегда знал дату своего дежурства. Больше никакой путаницы и споров:
- "Я в прошлый раз дежурил!!! Теперь твоя очередь!"
- "Не ври!!! Нет, твоя!"
- Теперь эти конфликты решатся сами собой- за вас все сделает бот!


2. Что может этот бот:
- Рассчитать даты всех ваших рабочих дней на несколько лет вперед
- Создать базу данных с именами людей, добавлять и удалять новых дежурных
- Контролировать очередь кто когда дежурит, следить за соблюдением очереди даже если человек находится в отпуске или болеет 
- Назвать дату когда дежурит определенный человек
 
 
 3. Этот бот масштабируется! Для каждого пользователя создаются отдельные таблицы в базе данных,
 а количество дней отдыха между сменами можно легко изменить (подходит для разных рабочих графиков). 
 При его создании были использованы библиотека PyTelegramBotAPI, вебфреймворк Flask, база данных MySQL, вебхуки,
 и хостинг Heroku в паре с сервисом для баз данных ClearDB.
 Для деплоя на Heroku использовался репозиторий GitHub и бесплатные Dino часы (ну от куда у спасателя деньги?).
 
 
 4. Чего не будет в программе, но планируется в следующей версии:
 - Календарь с отмеченными датами дежурств
 - Рейтинг количества и качества дежурств, присвоение званий (сержант вантуз, лейтенант мыла, генерал очка)
 
 
Взаимодействие с ботом:

1. Пользователь нажимает клавишу "Start" и перед ним появляется сообщение с фирменной картинкой. 
В сообщении говорится, что нужно отправить ответ "начать" боту для старта программы.
Затем в базе данных создается таблица с датами дежурств.
Список дат создается в зависимости от даты отправки сообщения "начать". По этой причине сообщение должно быть отправлено в день дежурства.
Если пользователь вводит любой другой текст, ему приходит сообщение: "Следуйте указаниям выше!!!". 
Такое сообщение приходит во всех случаях, когда пользователь пишет боту не тогда, когда это необходимо.

2.После того, как пользователь отправил "начать" нашему боту, на экране появляется главное меню с кнопками Телеграм (InLineButton)
В меню есть такие кнопки: 
- "Добавить в список дежурных"
- "Удалить из списка дежурных"
- "Узнать когда дежуришь"
- "Сегодня дежурит"

Примечание: Если пользователь пользуется ботом не в первый раз, то вводить "начать" ему не нужно. 
Он просто продолжает с того места, где остановился в прошлый раз. 

3. Если пользователь пользуется ботом впервые, то списки с именами дежурных будут пусты (no paint, no gained)
Если он выберет любую кнопку кроме "Добавить в список дежурных", он получит сообщение:
"Список дежурных пока еще пуст! Добавьте людей в список дежурных!!!"

4. Когда пользователь нажимает кнопку "Добавить в список дежурных", ему приходит сообщение:
"Введите имя человека, которого хотите добавить в список дежурных"
После ввода имени и отправки этого сообщения приходит еще одно сообщение от бота:
"Повторно введите имя человека"
Это делается для того, чтобы пользователь по ошибке не добавил неправильно написанное имя дежурного
Если имена совпадают, пользователь получает сообщение, что имя, которое он ввел, добавлено в базу данных
Если они не совпадают, то присылается предупреждение: "Имена не совпадают!!!"
В обоих случаях кроме уведомлений появляются кнопки: "В главное меню" и "Ввести имя"
При нажатии кнопки "В главное меню" на экране появляется главное меню. А при "Ввести имя" повторяется алгоритм  добавления в базу

Примечание: Дважды добавить в список одно и то же имя нельзя!!! 
Нельзя втайне смеяться как некто по имени Витя дежурит вдвое чаще, чем все остальные!!! 
По этой причине при добавлении имени бот проверяет есть ли оно в базе данных.

5. Если вам кто-то "надоел", и вы решили его "выкинуть" из списка, воспользуйтесь кнопкой "Удалить из списка дежурных"
При нажатии этой кнопки вам приходит сообщение: "Введите имя человека, которого вы хотите удалить из списка дежурных"
Отправьте боту сообщение с именем и он проверит есть ли человек с таким именем в базе.
Если человек с таким именем есть в базе, пользователя попросят подтвердить его удаление нажатием на кнопку "Подтвердить".
При нажатии кнопки "Подтвердить" приходит сообщение: "введенное_имя удален из списка дежурных!".
После этого сообщения появляются кнопки главного меню.
Если пользователь вдруг понял, что этот человек все таки полезен, ошибся, и передумал... Следует нажать кнопку "Отмена".
Если человека с таким именем нет в базе, приходит сообщение: "введенное_имя нет в базе дежурных! Попробуйте ввести имя еще раз!"
В таком случае появляются две кнопки: "В главное меню" и "Попробовать еще".

6. Кнопка "Узнать когда дежуришь"- это кнопка чтобы узнать когда ты дежуришь!
При ее нажатии приходит сообщение: "Введите имя человека чтобы узнать дату его дежурства:"
Нужно отправить сообщение с именем человека, и тогда программа выведет дату его дежурства согласно очереди.
Если пальцы пользователя слишком толстые чтобы попасть по нужным кнопкам, или он изрядно пьян - "введенное_имя нет в списке дежурных!"
Попробуйте ввести имя еще раз, нажав на кнопку "Попробовать еще".

7. О боже, это последняя кнопка из главного меню!!! Самая важная кнопка!!! Кнопка "Сегодня дежурит"
Когда нажимаешь эту кнопку, на экране появляется сообщение с именем человека, который стоит первым в очереди на дежурство.
Если этот человек на работе - ему не очень повезло!!! Нажмите кнопку "Подтвердить", и он будет назначен дежурным сегодня!
После подтверждения сменить дежурного на эту дату уже нельзя!!! Будьте внимательны!
Если человек заболел, в отпуске, кормит ребенка грудью или просто лентяй- нажмите кнопку "Не дежурит"
Кнопка "Не дежурит" делает этого человека первым в очереди на следующий раз, а на экране появляется имя второго в очереди. 
Очередь сдвигается до тех пор, пока дежурный не будет назначен (кнопка "Подтвердить"!!!)
После назначения дежурного его имя прикрепляется к этой дате. Данные заносятся в отдельную таблицу "Архив".

Примечание: Назначить дежурного можно только в день дежурства!!!
Во все остальные дни нажав на кнопку "Сегодня дежурит" будет получено сообщение:
"Дождитесь следующей смены!!! Назначить нового дежурного можно будет только в день смены!!!"



 
