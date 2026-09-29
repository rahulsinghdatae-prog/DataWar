create or replace database rahul_db;

create table rahul_test(
id number, name varchar
);

/**************************************************************************/

--- Fix: SQL compilation error
--- Integration 'AWS_S3_INTEGRATION' does not exist or not authorized.
--- Working through the storage integration setup for DATA_STAGE.
--- Steps are order dependent: AWS IAM -> Snowflake integration -> trust
--- policy -> bucket policy -> enable -> grant -> stage -> verify.

/**************************************************************************/

--- STEP 0: confirm which account and region the session is connected to.
--- A storage integration is an account level object. If the session is
--- pointed at a different account than the one the integration was built
--- in, the name can never resolve and SHOW INTEGRATIONS comes back empty.

select current_account(), current_region(), current_role();

SHOW INTEGRATIONS;
SHOW INTEGRATIONS LIKE 'AWS_S3_INTEGRATION';

/**************************************************************************/

--- STEP 1 (AWS): create the IAM role used to read the bucket.
--- No permissions attached to the role. Authorization lives in the
--- bucket policy added in STEP 3.
---
--- Trust policy -- placeholders come from STEP 2:
---   <snowflake-aws-account-id>  account hosting the bucket
---   <storage-username>          STORAGE_AWS_IAM_USER_ARN from STEP 2
---   <storage-integration-id>    STORAGE_INTEGRATION_ID from STEP 2
---
--- {
---   "Version": "2012-10-17",
---   "Statement": [
---     {
---       "Effect": "Allow",
---       "Principal": {
---         "AWS": "arn:aws:iam::<snowflake-aws-account-id>:user/<storage-username>"
---       },
---       "Action": "sts:AssumeRole",
---       "Condition": {
---         "StringEquals": {
---           "sts:ExternalId": "<storage-integration-id>"
---         }
---       }
---     }
---   ]
--- }

/**************************************************************************/

--- STEP 2: create the integration disabled so it can return the ids
--- that the AWS trust policy needs.
---
--- TYPE = EXTERNAL_STAGE is required. An integration created with any
--- other type still shows up in SHOW INTEGRATIONS but can never be
--- attached to a stage.
---
--- ENABLED = FALSE is deliberate here. Flip it in STEP 4 once the AWS
--- side is in place.
---
--- STORAGE_AWS_ROLE_ARN must be an IAM role in the same AWS account as
--- the bucket. It cannot be an IAM user.

USE ROLE ACCOUNTADMIN;

create or replace storage integration AWS_S3_INTEGRATION
  type = external_stage
  storage_provider = s3
  enabled = false
  storage_aws_role_arn = 'arn:aws:iam::470451076022:role/amz-EDPRP-Snowflake-S3-Role-Thailand'
  storage_allowed_locations = ('s3://amz-s3-practice-snow-data/data/');

-- capture from the output:
--   STORAGE_AWS_IAM_USER_ARN  -> <storage-username> for STEP 1 and STEP 3
--   STORAGE_AWS_ROLE_ARN      -> confirm it matches what was passed above
--   STORAGE_INTEGRATION_ID    -> <storage-integration-id> for STEP 1
--
-- enabled should read false at this point.

DESC INTEGRATION AWS_S3_INTEGRATION;

#STORAGE_AWS_IAM_USER_ARN='arn:aws:iam::556675846235:user/9kza2000-s'
#STORAGE_AWS_ROLE_ARN='arn:aws:iam::470451076022:role/amz-EDPRP-Snowflake-S3-Role-Thailand'
#STORAGE_AWS_EXTERNAL_ID='SZ87465_SFCRole=3_EbKoMd7gkXN1eWuFhKpXh4FTeGY='
/**************************************************************************/

--- STEP 3 (AWS): bucket policy on amz-s3-practice-snow-data.
--- Merge into any existing policy rather than replacing it.
---
--- s3:GetObject targets bucket/data/* because it is object level.
--- s3:ListBucket targets the bare bucket because it is bucket level.
--- Scoping both to data/* makes LIST fail with a permission error.
---
--- The principal is the storage user, not the role ARN. Snowflake
--- assumes the role, the role authorizes, but the policy matches the user.
---
--- {
---   "Version": "2012-10-17",
---   "Statement": [
---     {
---       "Sid": "AllowSnowflakeStageRead",
---       "Effect": "Allow",
---       "Principal": {
---         "AWS": "arn:aws:iam::<snowflake-aws-account-id>:user/<storage-username>"
---       },
---       "Action": "s3:GetObject",
---       "Resource": "arn:aws:s3:::amz-s3-practice-snow-data/data/*"
---     },
---     {
---       "Sid": "AllowSnowflakeStageList",
---       "Effect": "Allow",
---       "Principal": {
---         "AWS": "arn:aws:iam::<snowflake-aws-account-id>:user/<storage-username>"
---       },
---       "Action": "s3:ListBucket",
---       "Resource": "arn:aws:s3:::amz-s3-practice-snow-data"
---     }
---   ]
--- }

/**************************************************************************/

--- STEP 4: enable the integration. This is the handshake. If enabled
--- stays false Snowflake declined it silently, recheck in this order:
---   1. ExternalId matches STORAGE_INTEGRATION_ID character for character
---   2. trust policy principal matches STORAGE_AWS_IAM_USER_ARN exactly
---   3. the IAM role is assumable, not just created
---   4. bucket policy present and valid json
---   5. role and bucket are in the same AWS account

ALTER STORAGE INTEGRATION AWS_S3_INTEGRATION SET ENABLED = TRUE;

DESC INTEGRATION AWS_S3_INTEGRATION;

/**************************************************************************/

--- STEP 5: grant usage to the role that runs the scripts.
--- Grant the role used day to day, not PUBLIC, unless this is a throwaway
--- practice account. PUBLIC hands stage access to every user.
--- A CI service user is a different principal than the interactive user
--- and needs its own grant.
---
--- grantor must hold USAGE on the integration or have APPLY INTEGRATION
--- on the account, otherwise this fails even under ACCOUNTADMIN.

GRANT USAGE ON INTEGRATION AWS_S3_INTEGRATION TO ROLE <your_role>;

SHOW GRANTS ON INTEGRATION AWS_S3_INTEGRATION;

-- shows role memberships and direct grants, this is the one that confirms
-- usage is reachable from the principal actually running the script.
SHOW GRANTS TO USER <your_user>;

/**************************************************************************/

--- STEP 6: create the stage as the granted role, not ACCOUNTADMIN, so the
--- permission model used in practice is the one proven to work.
---
--- The STORAGE_INTEGRATION reference is resolved at compile time, which is
--- why the original error was a compilation error and why the integration
--- must exist and be usable before this statement can run at all.

USE ROLE <your_role>;

CREATE STAGE DATA_STAGE
  URL = 's3://amz-s3-practice-snow-data/data/'
  STORAGE_INTEGRATION = AWS_S3_INTEGRATION;

/**************************************************************************/

--- STEP 7: verify.
--- DESC proves the reference bound. LIST proves the whole chain, which
--- includes the parts SQL cannot check: credentials, trust, bucket
--- policy, prefix.
---
--- S3 access denied on LIST means the compile error is behind you and the
--- problem is now IAM only, go back to STEP 3.
--- Empty result with no error means the prefix has no objects.

DESC STAGE DATA_STAGE;

LIST @DATA_STAGE;

-- write and read round trip. A permissions error on PUT is expected and
-- correct if the bucket is intentionally read only here.
PUT file:///tmp/test.csv @DATA_STAGE;
GET @DATA_STAGE file:///tmp/;

/**************************************************************************/

--- Failure modes
---
--- integration does not exist on stage create   -> integration absent from
---                                                this account, STEP 2
--- does not exist after STEP 2                  -> session on wrong account
---                                                or region, STEP 0
--- integration exists, stage create fails       -> TYPE not EXTERNAL_STAGE,
---                                                STEP 2
--- enabled stays false after STEP 4             -> ExternalId or principal
---                                                mismatch, STEP 1 and 3
--- LIST returns access denied                   -> bucket policy scope or
---                                                principal, STEP 3
--- LIST empty with no error                     -> prefix has no objects,
---                                                not a fault
--- stage create fails on permission            -> USAGE grant missing for
---                                                the executing role, STEP 5

