SELECT * FROM suppliers;
SELECT * FROM products;
SELECT * FROM stock_entries;
SELECT * FROM shipments;
SELECT * FROM reorders;

-- 1.Total supliers
SELECT count(*) AS total_supliers FROM suppliers;

-- 2.Total Product
SELECT count(*) AS total_products FROM products;

-- 3.Total category deeling
SELECT COUNT(Distinct category) AS total_categories FROM products;

-- 4.Total sales value made by last 3 months
SELECT round(sum( t1.price*abs(t2.change_quantity)),2)  as total_sales 
FROM products t1
JOIN stock_entries t2
ON t1.product_id=t2.product_id
WHERE t2.change_type='Sale' 
AND t2.entry_date >= (SELECT date_sub(max(entry_date),interval 3 month) FROM stock_entries);


-- 5.Total Restock value in last 3 month
SELECT round(sum( t1.price*abs(t2.change_quantity)),2)  as total_restock 
FROM products t1
JOIN stock_entries t2
ON t1.product_id=t2.product_id
WHERE t2.change_type='Restock'
AND t2.entry_date >= (SELECT date_sub(max(entry_date),interval 3 month) FROM stock_entries);

-- 6.Below reorder and pending order
SELECT * FROM products t1
WHERE t1.stock_quantity < t1.reorder_level
AND t1.product_id NOT IN(
SELECT distinct product_id FROM reorders
WHERE status = 'Pending');

-- 7.supplier and their contact details

SELECT supplier_name,contact_name,email,phone FROM suppliers;

-- 8.product with their supplier and current stock

select t1.product_name,t2.supplier_name,
t1.stock_quantity,
t1.reorder_level
 from products t1
join suppliers t2
on t1.supplier_id=t2.supplier_id
order by t1.product_name ASC;

-- 9.Reorder prouct needed
select product_name,stock_quantity,reorder_level
from products
where stock_quantity < reorder_level;

-- 10. Add New Product

delimiter $$

create procedure add_new_product(
in input_product_name varchar(255),
in input_category varchar(255),
in input_price decimal(10,2),
in input_stock_quantity int,
in input_reorder_level int,
in input_supplier_id int
)
BEGIN
	declare new_prod_id int;
    declare new_shipment_id int;
    declare new_entry_id int;
    
    -- change in product table
   SELECT max(product_id) + 1 into new_prod_id FROM products;
   INSERT INTO products (product_id,product_name,category,price,stock_quantity,reorder_level,supplier_id)
   VALUES (new_prod_id,input_product_name,input_category,input_price,
   input_stock_quantity,input_reorder_level,input_supplier_id);
   
   -- change shipment table
   SELECT max(shipment_id) + 1 into new_shipment_id FROM shipments;
   insert into shipments (shipment_id,product_id,supplier_id,quantity_received,shipment_date)
   values(new_shipment_id,new_prod_id,input_supplier_id,input_stock_quantity,curdate());
   
   -- change stock Entry
   SELECT max(entry_id) + 1 into new_entry_id FROM stock_entries;
   insert into stock_entries (entry_id,product_id,change_quantity,change_type,entry_date)
   values (new_entry_id,new_prod_id,input_stock_quantity,'Restock',curdate());
    
END ;



-- 11.product history ..shipments,sales,purchase

select * FRom shipments;
create or replace view  product_history as(
select t1.product_id,t1.record_type,t1.quantity,t1.record_date,t1.change_type,t2.supplier_id from
(SELECT product_id,
"Shipment" as record_type,
quantity_received as quantity,
shipment_date as record_date,
null change_type
FROM shipments
union all
SELECT product_id,
"Stock Entry" as record_type,
change_quantity as quantity,
entry_date as record_date,
change_type
FROM stock_entries
) t1
join products t2
on t1.product_id=t2.product_id
)

-- show view

select * from product_history;

select product_id,product_name from products
group by product_id,product_name;


-- 12.place reorder
INSERT INTO reorders(reorder_id,product_id,reorder_quantity,reorder_date,status)
SELECT max(reorder_id)+1,101,200,curdate(),"ordered" from reorders

select * from reorders;

-- 13. Receive order
delimiter $$
create procedure receive_order(
in in_reorder_id int)
begin
declare prod_id int;
declare ship_id int;
declare qnty int;
declare entry_id_input int;
declare sup_id int;

start transaction;
-- fetch product_id and quantity
select product_id,reorder_quantity into prod_id,qnty from reorders where reorder_id=in_reorder_id;
-- fetch supplier_id
select supplier_id into sup_id from products where product_id=prod_id;
-- update reorder status to Received
update reorders set status='Recevied' where reorder_id=in_reorder_id;
-- update stock_quantity into products
update products set stock_quantity=stock_quantity+qnty where product_id=prod_id;
-- get new shipment id
select max(shipment_id) + 1 into ship_id from shipments;
-- update shipment table
insert into shipments values (ship_id,prod_id,sup_id,qnty,curdate());
-- get new entry id
select max(entry_id)+1 into entry_id_input from stock_entries;
-- update stock entries table
insert into stock_entries values (entry_id_input,prod_id,qnty,"Restock",curdate());
commit;
end;


