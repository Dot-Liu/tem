use oletter;

drop table if exists verify;
create table verify(
  user_id int primary key,
  add_time bigint NOT NULL ,
  verify_code varchar(64) not null
)engine=InnoDB default charset=utf8;
