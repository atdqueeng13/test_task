-- Задание а)
-- Вывести ники клиентов, поставивших csat меньше 3
--
-- DISTINCT - один клиент мог поставить низкую оценку несколько раз,
-- а ник нужен один

SELECT DISTINCT ticket_client
FROM tickets
WHERE csat < 3;
