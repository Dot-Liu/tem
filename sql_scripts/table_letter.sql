use oletter;
drop table if exists letter;
create table letter(
  user_id int not null,
  sender_id int not null,
  letter_id int not null,
  title text not null,
  add_time bigint not null,
  have_read enum('0','1') not null
)engine=InnoDB default charset=utf8;

insert into letter(user_id, sender_id,letter_id,title,add_time,have_read) values(3,2,1,'test',1465300000,'0');
insert into letter(user_id, sender_id,letter_id,title,add_time,have_read) values(3,2,1,'test',1465300050,'1');
