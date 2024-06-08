drop database if exists ai_starter_test;
drop database if exists ai_starter_development;
drop user ai_starter;
drop user ai_starter_test;

create database ai_starter_development;
create database ai_starter_test;
create user ai_starter with password 'ai_starter';
grant all privileges on database ai_starter_development to ai_starter;
grant all privileges on database ai_starter_test to ai_starter;

\connect ai_starter_development
create extension if not exists vector;
grant usage, create on schema public to ai_starter;

\connect ai_starter_test
create extension if not exists vector;
grant usage, create on schema public to ai_starter;
