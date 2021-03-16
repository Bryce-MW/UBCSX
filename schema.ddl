create table owners
(
    owner      varchar(8) primary key comment 'CWL of the user. This is used for authentication.',
    owner_name varchar(255) not null,
    constraint owners_pk
        unique (owner_name)
);

create table accounts
(
    id           serial primary key,
    balance      bigint unsigned default 1000000 not null comment 'Stored as hundredths of a penny which is standard in finance.',
    owner        varchar(8)                      not null comment 'CWL of the user. This is used for authentication.',
    account_name varchar(255)                    not null,
    constraint owner_fk
        foreign key (owner) references owners (owner)
            on update cascade on delete cascade
);

create table ceos
(
    ceo       varchar(255) primary key,
    ceo_quote varchar(255)
);

create table stocks
(
    last_price bigint default 0 not null comment 'Measured in hundredths of a cent.',
    name       varchar(255)     not null,
    symbol     varchar(16) primary key comment 'Symbols may have a 1 to 6 character root and a 0 to 10 character suffix according to the NYSE Symbology guide.',
    ceo        varchar(255)     not null,
    constraint ceo_fk
        foreign key (ceo) references ceos (ceo)
            on update cascade on delete cascade
);

create
    unique index stocks_name_uindex
    on stocks (name);

create table shares
(
    id                  serial comment 'This ID technically doesnt have to be unique because of the foreign key that is part of the primary key. But making it unique is simply much easier.',
    symbol              varchar(16),
    owned_by_account_id bigint unsigned not null,
    constraint shares_pk
        primary key (symbol, id),
    constraint shares_accounts_id_fk
        foreign key (owned_by_account_id) references accounts (id)
            on update cascade on delete cascade,
    constraint shares_stocks_symbol_fk
        foreign key (symbol) references stocks (symbol)
            on update cascade on delete cascade
);

create table lendables
(
    id             serial primary key,
    input_datetime datetime default current_timestamp not null comment 'Datetime when the share was offered to be lent.',
    premium        double   default 0                 not null comment 'Percentage in decimal form (i.e. 12% is 0.12) of the APR premium of this share. The actual fees will be calculated daily based on the daily compounding equivalent percentage.',
    symbol         varchar(16)                        not null,
    share_id       bigint unsigned                    not null,
    account_id     bigint unsigned                    not null,
    constraint lendables_pk
        unique (symbol, share_id),
    constraint lendables_accounts_id_fk
        foreign key (account_id) references accounts (id)
            on update cascade on delete cascade,
    constraint lendables_shares_symbol_id_fk
        foreign key (symbol, share_id) references shares (symbol, id)
            on update cascade on delete cascade
);

create table lent
(
    premium       int             not null comment 'Percentage in decimal form (i.e. 12% is 0.12) of the APR premium of this share. The actual fees will be calculated daily based on the daily compounding equivalent percentage.',
    id            serial primary key,
    share_id      bigint unsigned not null,
    symbol        varchar(16)     not null,
    by_account_id bigint unsigned not null,
    to_account_id bigint unsigned not null,
    constraint lent_accounts_id_fk
        foreign key (by_account_id) references accounts (id)
            on update cascade on delete cascade,
    constraint lent_accounts_id_fk_2
        foreign key (to_account_id) references accounts (id)
            on update cascade on delete cascade,
    constraint lent_shares_id_symbol_fk
        foreign key (share_id, symbol) references shares (id, symbol)
            on update cascade on delete cascade
);

create table etfs
(
    symbol              varchar(16) primary key comment 'Symbols may have a 1 to 6 character root and a 0 to 10 character suffix according to the NYSE Symbology guide.',
    controls_account_id bigint unsigned not null,
    constraint etfs_accounts_id_fk
        foreign key (controls_account_id) references accounts (id)
            on update cascade
);

create
    unique index etfs_controls_account_id_uindex
    on etfs (controls_account_id);

create table owns
(
    symbol     varchar(16),
    account_id bigint unsigned,
    units      bigint unsigned default 1 not null,
    constraint owns_pk
        primary key (symbol, account_id),
    constraint owns_accounts_id_fk
        foreign key (account_id) references accounts (id)
            on update cascade on delete cascade,
    constraint owns_etfs_symbol_fk
        foreign key (symbol) references etfs (symbol)
            on update cascade on delete cascade
);

create table orders
(
    id                 serial primary key,
    input_datetime     datetime        default current_timestamp not null,
    valid_until        datetime                                  not null,
    quantity           bigint unsigned default 1                 not null comment 'If quantity is positive, it is a buy order, otherwise it is a sell order.',
    symbol             varchar(16)                               not null,
    made_by_account_id bigint unsigned                           not null,
    constraint orders_accounts_id_fk
        foreign key (made_by_account_id) references accounts (id)
            on update cascade on delete cascade,
    constraint orders_stocks_symbol_fk
        foreign key (symbol) references stocks (symbol)
            on update cascade on delete cascade
) comment 'Is an OptionOrder if there exists an option_order referencing this id, otherwise it is a StockOrder. Order is Market if neither limit nor stop exist otherwise it is a Limit or Stop order (both entities cant exist at the same time).';

create table contracts
(
    strike_price          bigint unsigned not null comment 'Measured in hundredths of a cent as per standard.',
    expiration            datetime        not null,
    id                    serial          primary key,
    symbol                varchar(16)     not null,
    written_by_account_id bigint unsigned not null,
    owned_by_account_id   bigint unsigned not null,
    constraint contracts_accounts_id_fk
        foreign key (written_by_account_id) references accounts (id)
            on update cascade on delete cascade,
    constraint contracts_accounts_id_fk_2
        foreign key (owned_by_account_id) references accounts (id)
            on update cascade on delete cascade,
    constraint contracts_stocks_symbol_fk
        foreign key (symbol) references stocks (symbol)
            on update cascade on delete cascade
);

create table option_order
(
    strike_price bigint unsigned not null comment 'Measured in hundredths of a cent as is standard.',
    expiration   datetime        not null,
    order_id     bigint unsigned not null,
    constraint option_order_orders_id_fk
        foreign key (order_id) references orders (id)
            on update cascade on delete cascade
);

create
    unique index option_order_order_id_uindex
    on option_order (order_id);

create table `limit`
(
    price    bigint unsigned not null,
    order_id bigint unsigned not null,
    constraint limit_orders_id_fk
        foreign key (order_id) references orders (id)
            on update cascade on delete cascade
);

create
    unique index limit_order_id_uindex
    on `limit` (order_id);

create table stop
(
    price       bigint unsigned not null comment 'Measured in hundredths of a cent as is standard.',
    limit_price bigint unsigned not null comment 'Measured in hundredths of a cent as is standard.',
    order_id    bigint unsigned not null,
    constraint stop_orders_id_fk
        foreign key (order_id) references orders (id)
            on update cascade on delete cascade
);

create
    unique index stop_order_id_uindex
    on stop (order_id);
