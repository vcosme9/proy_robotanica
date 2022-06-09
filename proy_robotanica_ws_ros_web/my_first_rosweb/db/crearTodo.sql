create table Rol(
	id_rol 				INTEGER 		PRIMARY KEY,
	rol 				varchar(255) 	not null
);

create table Invernadero(
	id_invernadero		INTEGER 		PRIMARY KEY,
	mapa			 	varchar(255) 	not null
);

create table Coleccion(
	url 				varchar(255) 	PRIMARY KEY,
	id_invernadero 		INTEGER		 	not null,
	seccion				varchar(255)	not null,
	fecha				varchar(255)	not null,
	
	foreign key(id_invernadero) references Invernadero(id_invernadero)
);

create table Usuario(
	email 				varchar(255) 	not null,
	id_invernadero		int				not null,
	id_rol 				int 			not null,
	nombre 				varchar(255) 	not null,
	contrasenya 		varchar(255) 	not null,
	
	foreign key(id_rol) references Rol(id_rol),
	foreign key(id_invernadero) references Invernadero(id_invernadero),
	primary key (email)
);