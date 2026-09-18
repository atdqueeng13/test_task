-- Задание г) - дополнительное
-- Дополнить таблицу orders данными из clients и tickets,
-- вернуть только 1000 записей.
--
-- Связи:
--   orders.order_client_id -> clients.client_id (клиент, сделавший заказ)
--   orders.order_id -> tickets.ticket_order_id  (тикет по этому заказу)
--
-- LEFT JOIN - чтобы заказы без тикетов тоже попали в результат.
-- Если по одному заказу несколько тикетов, заказ будет в нескольких строках.

SELECT
    o.order_id,
    o.price,
    o.order_client_id,
    o.place,
    c.username,
    c.name,
    c.age,
    c.city,
    t.ticket_id,
    t.csat,
    t.text,
    t.date
FROM orders o
LEFT JOIN clients c ON o.order_client_id = c.client_id
LEFT JOIN tickets t ON o.order_id = t.ticket_order_id
LIMIT 1000;
