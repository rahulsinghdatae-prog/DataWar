-- Databricks Unity Catalog setup
-- Target: catalog `development` -> create schema/database `data`
-- Run this against the DATABRICKS connection (not Snowflake).
--   VS Code: Command Palette -> "Databricks: Configure workspace", then run
--   this file on the Databricks SQL warehouse / cluster.
--
-- NOTE: Do NOT use backticks here and do NOT run it on a Snowflake
-- connection, otherwise you get:
--   "SQL compilation error: syntax error ... unexpected ';'"
--
-- In Databricks, CREATE DATABASE is an alias of CREATE SCHEMA.

CREATE DATABASE IF NOT EXISTS development.data;

-- (Optional) confirm it exists:
-- SHOW SCHEMAS IN development;
