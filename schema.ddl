create table lendables
(
	id serial not null,
	input_datetime datetime default CURRENT_TIMESTAMP not null comment 'Datetime when the share was offered to be lent.',
	premium double default 0 not null comment 'Percentage in decimal form (i.e. 12% is 0.12) of the APR premium of this share. The actual fees will be calculated daily based on the daily compounding equivalent percentage.',
	constraint lendables_pk
		primary key (id)
);

create table lent
(
	premium int not null comment 'Percentage in decimal form (i.e. 12% is 0.12) of the APR premium of this share. The actual fees will be calculated daily based on the daily compounding equivalent percentage.',
	id serial not null,
	constraint lent_pk
		primary key (id)
);

create table shares
(
	id serial not null comment 'This ID technically doesn\'t have to be unique because of the foreign key that is part of the primary key. But making it unique is simply much easier.',
	constraint shares_pk
		primary key (id)
);

create table accounts
(
	id serial not null,
	balance bigint unsigned default 1000000 not null comment 'Stored as hundredths of a penny which is standard in finance.',
	owner varchar(8) not null comment 'CWL of the user. This is used for authentication.',
	constraint accounts_pk
		primary key (id)
);

create table etfs
(
	symbol varchar(16) not null comment 'Symbols may have a 1 to 6 character root and a 0 to 10 character suffix according to the NYSE Symbology guide.',
	constraint etfs_pk
		primary key (symbol)
);

create table stocks
(
	last_price bigint default 0 not null comment 'Measured in hundredths of a cent.',
	name varchar(255) not null,
	symbol varchar(16) not null comment 'Symbols may have a 1 to 6 character root and a 0 to 10 character suffix according to the NYSE Symbology guide.',
	constraint stocks_pk
		primary key (symbol)
);

create unique index stocks_name_uindex
	on stocks (name);

create table orders
(
	id SERIAL not null,
	input_datetime DATETIME default CURRENT_TIMESTAMP not null,
	valid_until DATETIME not null,
	quantity bigint unsigned default 1 not null,
	constraint orders_pk
		primary key (id)
) comment 'Is an OptionOrder if there exists an option_order referencing this id, otherwise it is a StockOrder. Order is Market if neither limit nor stop exist otherwise it is a Limit or Stop order (both entities can\'t exist at the same time).';

create table contracts
(
	strike_price bigint unsigned not null comment 'Measured in hundredths of a cent as per standard.',
	expiration datetime not null,
	id serial not null,
	constraint contracts_pk
		primary key (id)
);

create table option_order
(
	strike_price bigint unsigned not null comment 'Measured in hundredths of a cent as is standard.',
	expiration datetime not null
);

create table `limit`
(
	price bigint unsigned not null
);

create table stop
(
	price bigint unsigned not null comment 'Measured in hundredths of a cent as is standard.',
	limit_price bigint unsigned not null comment 'Measured in hundredths of a cent as is standard.'
);