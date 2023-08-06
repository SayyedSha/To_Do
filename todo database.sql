create database TODO;
use TODO;

create table User_registry(id bigint primary key auto_increment,First_name varchar(200),Last_name varchar(200),Email varchar(255),Password varchar(255),created_at datetime);
create table TodoSP_user_registry_get_by_email(id bigint primary key auto_increment, user_id bigint, foreign key(user_id) references User_registry(id),Title Varchar(200),category varchar(200), Descbribe Text, Status varchar(200));

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_user_registry_get_by_email`(
in email_in varchar(200)
)
BEGIN
SELECT `id`,
    `First_name`,
    `Last_name`,
    `Email`,
    `Password`,
    `created_at`
FROM `user_registry`
Where `Email`=email_in;
END

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_user_registry_insert`(
in First_name_in varchar(200),
in Last_name_in varchar(200),
in Email_in varchar(200),
in Password_in varchar(255)
)
BEGIN
INSERT INTO `user_registry`
(
`First_name`,
`Last_name`,
`Email`,
`Password`,
`created_at`)
VALUES
(
First_name_in,
Last_name_in,
Email_in,
Password_in,
now());
END

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_todo_get_all`()
BEGIN
SELECT `id`,
    `user_id`,
    `Title`,
    `category`,
    `Descbribe`,
    `Status`
FROM `todo`;
END

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_todo_insert`(
in user_id_in bigint,
in Title_in varchar(200),
in category_in varchar(200),
in Descbribe_in text,
in Status_in varchar(200)
)
BEGIN
INSERT INTO `todo`
(
`user_id`,
`Title`,
`category`,
`Descbribe`,
`Status`)
VALUES
(
user_id_in,
Title_in,
category_in,
Descbribe_in,
Status_in);
END

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_user_registry_get_all`()
BEGIN
SELECT `id`,
    `First_name`,
    `Last_name`,
    `Email`,
    `Password`,
    `created_at`
FROM `user_registry`;
END