use oletter;

drop table if exists userinfo;
create table userinfo(
  user_id int primary key not null,
  name varchar(20) not null,
  gender enum('male', 'female') not null,
  have_connect enum('0','1') NOT NULL
)engine=InnoDB default charset=utf8;

insert into userinfo(user_id, name, gender,have_connect) values(2, 'ch_oosy', 'male','0');
insert into userinfo(user_id, name, gender,have_connect) values(3, 'scar', 'male','1');
insert into userinfo(user_id, name, gender,have_connect) values(4, 'snail','male','1');

