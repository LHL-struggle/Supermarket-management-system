-- 数据库设计(库名：W_Surper)：
-- 库存表(kucun):
-- 商品ID, 商品名TradeName, 生产日期ProducData，入库日期RDate, 保质期ShelfLife, 进价Pprice，售价Price, 库存Inventory
create table kucun (
    ID int(12) auto_increment primary key,
    TradeName char(100) Not Null,
    ProducData Date Not Null,
    RDate  Date  Not Null,
    ShelfLife  char(20),
    Pprice float(7),
    Price float(7),
    Inventory  int((7)
    );
-- 在库存表中添加了销售数量 sellnum 这一属性
alter table kucun add sellnum int(7) default 0;
-- 在库存表中添加了出售金额 SaleAmount 这一属性
alter table kucun add SaleAmount float(10) default 0;

--+------------+-----------+------+-----+---------+----------------+
--| Field      | Type      | Null | Key | Default | Extra          |
--+------------+-----------+------+-----+---------+----------------+
--| ID         | int(12)   | NO   | PRI | NULL    | auto_increment |
--| TradeName  | char(100) | NO   |     | NULL    |                |
--| ProducData | date      | NO   |     | NULL    |                |
--| RDate      | date      | NO   |     | NULL    |                |
--| ShelfLife  | char(20)  | YES  |     | NULL    |                |
--| Pprice     | float     | YES  |     | NULL    |                |
--| Price      | float     | YES  |     | NULL    |                |
--| Inventory  | int(7)    | YES  |     | NULL    |                |
--+------------+-----------+------+-----+---------+----------------+

-- 进货表(jh)：
-- 商品ID，商品名TradeName，生产日期ProducData，入库日期RDate, 保质期ShelfLife, 进价Pprice，进货数量QuantityIn

-- 出售表(sell):
-- 商品ID，商品名TradeName，售价Price，出售数量SellQuantity
