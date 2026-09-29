/****************************************************/

create  or replace table emp
(
emp_id number,
first_name varchar(20),
last_name varchar(20),
city varchar(20),
salary number,
hire_date date
);

INSERT INTO emp
(emp_id, first_name, last_name, city, salary, hire_date)
VALUES
(101, 'Rahul', 'Sharma', 'Delhi', 55000, '2020-01-15'),
(102, 'Amit', 'Verma', 'Mumbai', 62000, '2019-06-20'),
(103, 'Priya', 'Singh', 'Noida', 58000, '2021-03-10'),
(104, 'Neha', 'Gupta', 'Pune', 67000, '2018-11-05'),
(105, 'Ravi', 'Kumar', 'Bangalore', 72000, '2022-07-18'),
(106, 'Anjali', 'Mehta', 'Chennai', 61000, '2020-09-25'),
(107, 'Vikas', 'Yadav', 'Hyderabad', 75000, '2017-04-12'),
(108, 'Sneha', 'Patel', 'Ahmedabad', 54000, '2023-01-09'),
(109, 'Arjun', 'Malhotra', 'Jaipur', 69000, '2019-12-16'),
(110, 'Pooja', 'Agarwal', 'Kolkata', 63000, '2021-08-23');

commit;
-- Time travel

select * from emp;      -- Assume its a production table

update emp set first_name='phc';    -- first wrong update

update emp set city='Bangalore';    -- second wrong update.

select * from emp at(offset => -60*8);    -- after 2 mins you realised you did wrong
                                          -- if you realise after 5 hrs you need to travel back by 5 hrs
                                          -- How long you can travel back depends on table retention period.
                                          

-- Recovery

   create or replace table emp
   as
   select * from emp at(offset => -60*11);
   
-- Big mistake

  -- you realised you need to undo name update also. Try it
  
  select * from emp at(offset => -60*12);   -- not seeing any records
  
  -- Why ?
  
  
-- What you should have been done ?

   -- i will recreate the same table from backup
   
      create or replace table emp
        as
      select * from emp_1
      
update emp set first_name='phc';    -- first wrong update

update emp set city='Bangalore';    -- second wrong update.

-- create backup table
create or replace table emp_bkp
as select * from emp at(offset => -60*7.8);

truncate table emp;

insert into emp
select * from emp_bkp

select * from emp at(offset => -60*16.9);

    -- if you now realise 




create or replace table emp
as select * from emp at(offset => -60*2);

insert into emp
select * from emp_bkp

drop table emp

undrop table emp



-- Time travel

select * from emp

truncate table emp

select * from emp at(offset => -60*5);

create or replace table emp_bkp
as select * from emp at(offset => -60*2);

insert into emp
select * from emp_bkp

create or replace table emp
as
select * from emp_bkp

emp_bkp--- Only 5 min back version.
emp -- you loose all previous version.

drop table emp

undrop table emp


/*********************************************************/