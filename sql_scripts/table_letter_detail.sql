use oletter;
drop table if exists letter_detail;
create table letter_detail(
  letter_id int PRIMARY KEY AUTO_INCREMENT not null,
  user_id int default 0,
  sender_id int not null,
  sender_name varchar(20) not null,
  add_time bigint not null,
  title text not null,
  content text not null
)engine=InnoDB default charset=utf8;

insert into letter_detail(user_id,sender_id,sender_name,add_time,title,content) values(4,3,'scar',1465300000,'text','text');
insert into letter_detail(user_id,sender_id,sender_name,add_time,title,content) values(3,4,'snail',1465300050,'text','text');
insert into letter_detail(sender_id,sender_name,add_time,title,content) values(2,'choosy',1465300060,'text','text');
insert into letter_detail(sender_id,sender_name,add_time,title,content) values(5,'123456',1465300070,'text','text');                                                  
