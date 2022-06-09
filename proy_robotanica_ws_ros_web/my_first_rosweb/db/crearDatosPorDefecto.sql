-- crearDatosPorDefecto.sql
insert into Rol(rol) values ("usuario");
insert into Rol(rol) values ("administrador");

insert into Invernadero(mapa) values ("https://m.media-amazon.com/images/I/71YhL1zcPdL._AC_SL1050_.jpg");
insert into Invernadero(mapa) values ("https://m.media-amazon.com/images/I/61zSkwAvlXL._AC_SX679_.jpg");

insert into Usuario values ("luisInvernadero@gmail.com", 1, 1, "Luis", "123456");
insert into Usuario values ("joanBancals@gmail.com", 2, 1, "Joan", "xoanet12");

insert into Coleccion values ("https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Bright_red_tomato_and_cross_section02.jpg/1200px-Bright_red_tomato_and_cross_section02.jpg", 1, "Tomates", "2022-05-13");
insert into Coleccion values ("https://d2ke0ff4uknkae.cloudfront.net/hortalizas/wp-content/uploads/2019/01/tomatoes-1280859_1280-1024x674.jpg", 1, "Tomates", "2022-05-14");
insert into Coleccion values ("https://www.ahorramas.com/wp-content/uploads/2021/07/variedades-de-tomate.jpg", 1, "Tomates", "2022-05-14");
insert into Coleccion values ("https://statics-cuidateplus.marca.com/cms/styles/ratio_43/azblob/tomate-chef.jpg.webp?itok=snpH5Vpk", 1, "Tomates", "2022-05-15");
insert into Coleccion values ("https://www.gastronomiavasca.net/uploads/image/file/3406/w700_pepino.jpg", 1, "Pepinos", "2022-05-15");

insert into Coleccion values ("https://www.casi.es/wp-content/uploads/2020/10/img-apariencia-sabor-perfectos.jpg", 2, "Pepinos", "2022-04-28");
insert into Coleccion values ("https://sgfm.elcorteingles.es/SGFM/dctm/MEDIA03/201811/26/00118109100018____2__600x600.jpg", 2, "Pepinos", "2022-05-19");
insert into Coleccion values ("https://www.sportlife.es/uploads/s1/10/73/25/16/tomate.jpeg", 2, "Tomates", "2022-05-19");