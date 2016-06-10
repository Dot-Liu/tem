use oletter;
drop table if exists letter_detail;
create table letter_detail(
  letter_id int PRIMARY KEY AUTO_INCREMENT not null,
  user_id int,
  sender_id int not null,
  sender_name varchar(20) not null,
  add_time bigint not null,
  title text not null,
  content text not null
)engine=InnoDB default charset=utf8;

insert into letter_detail(letter_id,sender_id,add_time,title,content) values(1,3,1465300000,'text','text');
insert into letter_detail( letter_id,sender_id,add_time,title,content) values(2,4,1465300050,'text','text');
