Tobacco_Legislation_Smokefree_Indoor_Air.csv

tar -czf archiveTobacco_Legislation_Smokefree_Indoor_Air.csv.gz Tobacco_Legislation_Smokefree_Indoor_Air.csv;

create or replace stage tobacco_stage
file_format = (type = 'CSV' field_optionally_enclosed_by = '"' skip_header = 1 null_if = ('NULL', 'null', ''));


list @tobacco_stage;

PUT 'file:///C:/Users/user/Desktop/DE/Projects/DataWar/1_SnowFlake/5_Data/archive/Tobacco_Legislation_Smokefree_Indoor_Air.csv.gz' @tobacco_stage;

CREATE OR REPLACE TRANSIENT TABLE RAHUL_DB.PUBLIC.TOBACCO (
  Year NUMBER,
  Quarter NUMBER(1,0),
  LocationAbbr VARCHAR(2),
  LocationDesc VARCHAR(100),
  TopicDesc VARCHAR(100),
  MeasureDesc VARCHAR(100),
  DataSource VARCHAR(3),
  ProvisionGroupDesc VARCHAR(50),
  ProvisionDesc VARCHAR(1000),
  ProvisionValue VARCHAR(1000),
  Citation VARCHAR(100),
  ProvisionAltValue NUMBER,
  DataType VARCHAR(50),
  Comments STRING,
  Enacted_Date DATE,
  Effective_Date DATE,
  GeoLocation VARCHAR(100),
  DisplayOrder NUMBER,
  TopicTypeId VARCHAR(3),
  TopicId VARCHAR(100),
  MeasureId VARCHAR(20),
  ProvisionGroupID VARCHAR(10),
  ProvisionID NUMBER
);

COPY INTO RAHUL_DB.PUBLIC.TOBACCO
FROM @tobacco_stage/Tobacco_Legislation_Smokefree_Indoor_Air.csv.gz;