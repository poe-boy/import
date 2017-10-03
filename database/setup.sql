select
    pg_terminate_backend(pg_stat_activity.pid)
from
    pg_stat_activity
where
    pg_stat_activity.datname = 'poeboy' and
    pid != pg_backend_pid();

drop database if exists poeboy;
create database poeboy;

\c poeboy

create extension if not exists "uuid-ossp";
create extension if not exists "citext";

begin;

create table next_change_id (
    id          text not null,
    previous_id text not null,
    created_on  timestamptz not null default now(),
    updated_on  timestamptz not null default now()
);

create table accounts (
    id                  uuid not null default uuid_generate_v4() primary key,
    name                citext unique not null,
    last_character_name citext,
    created_on          timestamptz not null default now()
);

create table stashes (
    id          uuid not null default uuid_generate_v4() primary key,
    account_id  uuid not null references accounts(id),
    stash_id    text not null unique,
    stash       text not null,
    type        text not null,
    public      boolean not null,
    created_on  timestamptz not null default now()
);

create table frame_types (
    id      smallint not null primary key,
    name    text not null unique
);

create table items (
    id                  uuid not null default uuid_generate_v4() primary key,
    stash_id            uuid not null references stashes(id),
    verified            boolean not null,
    dimensions          json not null default '{"w":0,"h":0}',
    ilvl                smallint not null,
    icon                text,
    league              citext,
    item_id             text not null unique,
    name                citext,
    type_line           text not null,
    identified          boolean not null,
    corrupted           boolean not null,
    locked_to_character boolean not null,
    note                text,
    -- properties          jsonb not null,
    -- requirements        jsonb not null,
    explicit_mods       text,
    enchant_mods        text,
    crafted_mods        text,
    flavour_text        text,
    frame_type          smallint not null references frame_types(id),
    stash_position      json not null default '{"x":0,"h":0}',
    inventory_id        citext,
    created_on          timestamptz not null default now()
);

-- bridge table for the `socketedItems` property on `items`
-- id is the item and socketedItemId is the item that is socketed
create table socketed_items (
    id                  uuid not null references items(id),
    socketed_item_id    uuid not null references items(id),
    unique(id, socketed_item_id)
);

create table property_types (
    id      smallint not null primary key,
    name    citext not null unique
);

create table value_types (
    id      smallint not null primary key,
    name    citext not null unique
);

create table properties (
    id              uuid not null default uuid_generate_v4() primary key,
    item_id         uuid not null references items(id),
    name            text not null,
    value_1         citext,
    value_type_1     smallint references value_types(id),
    value_2         citext,
    value_type_2    smallint references value_types(id),
    display_mode    smallint not null,
    type            text not null check(type in('property', 'requirement')),
    progress        numeric not null,
    property_type   smallint references property_types(id),
    is_additional   boolean not null default false,
    created_on      timestamptz not null default now()
);

insert into frame_types
    (id, name)
values
    (0,	'normal'),
    (1,	'magic'),
    (2,	'rare'),
    (3,	'unique'),
    (4,	'gem'),
    (5,	'currency'),
    (6,	'divination card'),
    (7,	'quest item'),
    (8,	'prophecy'),
    (9,	'relic');

insert into property_types
    (id, name) 
values
    (5, 'Level'),
    (6, 'Quality'),
    (9, 'Physical Damage'),
    (10, 'Elemental Damage'),
    (12, 'Critical Strike Chance'),
    (13, 'Attacks per Second'),
    (14, 'Weapon Range'),
    (15, 'Chance to Block'),
    (16, 'Armour'),
    (17, 'Evasion Rating'),
    (18, 'Energy Shield');

insert into value_types
    (id, name)
values
    (0,	'white, or physical'),
    (1,	'blue for modified value'),
    (4,	'fire'),
    (5,	'cold'),
    (6,	'lightning'),
    (7,	'chaos');

end;