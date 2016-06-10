use oletter;

drop table if exists mate;
create table mate(
  user_id int primary key not null,
  mate_id int not null,
  add_time bigint not null,
)engine=InnoDB default charset=utf8;

insert into mate(user_id, mate_id,add_time) values(3,4,1465282867);
insert into mate(user_id, mate_id,add_time) values(4,3,1465282867);

