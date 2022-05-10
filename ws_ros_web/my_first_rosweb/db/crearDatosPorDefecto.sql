-- crearDatosPorDefecto.sql
insert into Rol(rol) values ("usuario");
insert into Rol(rol) values ("administrador");

insert into Invernadero(mapa) values ("https://m.media-amazon.com/images/I/71YhL1zcPdL._AC_SL1050_.jpg");
insert into Invernadero(mapa) values ("https://m.media-amazon.com/images/I/61zSkwAvlXL._AC_SX679_.jpg");

insert into Usuario values ("luisInvernadero@gmail.com", 1, 1, "Luis", "123456");
insert into Usuario values ("joanBancals@gmail.com", 2, 1, "Joan", "xoanet12");