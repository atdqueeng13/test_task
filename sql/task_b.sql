-- Задание б)
-- Вывести id тикетов, в тексте которых есть слово "отлично",
-- отсортировать по убыванию csat
--
-- LOWER - чтобы найти и "Отлично" в начале предложения

SELECT ticket_id
FROM tickets
WHERE LOWER(text) LIKE '%отлично%'
ORDER BY csat DESC;
