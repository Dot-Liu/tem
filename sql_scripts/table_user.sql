use oletter;

drop table if exists user;
create table user(
  user_id int primary key auto_increment not null,
  login_name varchar(16) not null unique,
  password varchar(64),
  type enum('0','1','2') not null
)engine=InnoDB default charset=utf8;

insert into user(login_name, password,type) values('admin', '21232f297a57a5a743894a0e4a801fc3','0');
insert into user(login_name, password,type) values('824010343@qq.com', 'e10adc3949ba59abbe56e057f20f883e','1');
insert into user(login_name, password,type) values('1054139596@qq.com', 'e10adc3949ba59abbe56e057f20f883e','1');
insert into user(login_name, password,type) values('1776177006@qq.com', 'e10adc3949ba59abbe56e057f20f883e','1');
insert into user(login_name, password,type) values('384157031@qq.com', 'e10adc3949ba59abbe56e057f20f883e','1');