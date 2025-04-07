# My CSV file is located in 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\'
# So that inline csv imports excluding the AccountID line is possible

use bankdb;
drop table if exists Accounts;
create table if not exists Accounts  (
	AccountID int unique not null auto_increment,
    Username varchar(24) unique not null,
    Password_hash varchar(255) not null,
    fname varchar(40) not null,
    lname varchar(40) not null,
    SSN decimal(9,0) not null unique,
    address varchar(255) not null,
    phone varchar(24) not null,
    balance float default 0,
    approved bool default False,
    PRIMARY KEY (AccountID)
);
create table if not exists Admins (
	Username varchar(24) unique not null,
    Password_hash varchar(255) not null,
    fname varchar(40) not null,
    lname varchar(40) not null,
    CONSTRAINT AdminPK primary key (Username, Password_hash)
);
create table if not exists Transactions (
	TransactionID int unique not null primary key auto_increment,
    trans_date date,
    fromID int not null,
    toID int not null,
    amount float not null
);
drop table if exists Login;
create table if not exists Login (
	Username varchar(24) not null primary key,
    Password_Hash varchar(255) not null,
    AdminAccount bool not null
);
# The sole admin account is created here to be more secure
truncate table Admins;
insert into Admins values ("AdminAccount", "$2b$12$kj/bR0ob6gKnysfyJIdFsugJRUyEPY8VinmQ8H8ig7LcS4QPoCC4K","Joe", "Smith");
# For simplicity the passwords are the same as the username for testing
truncate table Accounts;
INSERT INTO Accounts (Username, Password_hash, fname, lname, SSN, address, phone, balance) VALUES
('jdoe123', '$2b$12$2y.v8f2baeBl8HHU1FTGXey0NhHzlabPPE.7sszrYlmG34Lrs6ipm', 'John', 'Doe', 123456789, '123 Elm Street', '555-123-4567', 1000.50),
('asmith456', '$2b$12$P1f23vhNx1SGgMVBwz5Tb.efKarSA7d11CIBsAQMgYZ5RVx35R/iy', 'Alice', 'Smith', 987654321, '456 Oak Avenue', '555-987-6543', 250.75),
('bwayne', '$2b$12$vBqbnSvjoGAX5sR0snovKuYqOB3ViRr91u42HhRjv.CL9jYhPVoE2', 'Bruce', 'Wayne', 111223333, '1007 Mountain Dr', '555-000-0001', 1000000000),
('ckent88', '$2b$12$SAoVYR60hUySQmOlDWMlhuF4N8JoNTj7OemhjHlRRqfVF10U9VSRK', 'Clark', 'Kent', 222334444, '344 Clinton St', '555-111-2222', 5000.00),
('pparker', '$2b$12$yHtPHZ20to5iEgo9Lvo6xOCnQp99DDov3R0x/T3pulK.nxOori2lS', 'Peter', 'Parker', 333445555, '20 Ingram Street', '555-333-4444', 125.25),
('tswiftie13', '$2b$12$qwgkXMB.QeWScnXYFsOjC..Ffk/E9EZ9GUFsCB7xXneIyvTR5X7WO', 'Taylor', 'Swift', 444556666, '13 Swift Blvd', '555-123-1313', 1300.13),
('lskywalker', '$2b$12$jQQig7D3IqE8VxgJjThz0u2mh2LP7w7ZVsGV25Cbq3Oto9miMa186', 'Luke', 'Skywalker', 555667777, 'Anchorhead', '555-456-7890', 999.99),
('srogers', '$2b$12$neQQEEcPcTPOKOzjyhwhSebYRKsu9YwFARK.6w66h8r1C6KAkJm5u', 'Steve', 'Rogers', 666778888, 'Brooklyn NY', '555-987-0000', 1776.00),
('mbolton99', '$2b$12$U06IeLG9c/CeGP5bq4NR/OimDxD2RC2QhFBcYjg2ptKmvuFV/CKSe', 'Mike', 'Bolton', 777889999, 'Initech Office 4B', '555-321-7654', 0.01),
('eexample', '$2b$12$.ZlNy7I84AQmtr665HkQ3emn0Tdanc.iRYALDGKAjLkJBQIN7efAe', 'Emily', 'Example', 888990000, '999 Sample Rd', '555-999-9999', 42.42);
select * from Accounts;