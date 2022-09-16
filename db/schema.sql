BEGIN;

DO $create_type_if_not_exists$ BEGIN
CREATE TYPE status AS ENUM (
        'queued',
        'in_progress',
        'completed'
    );
EXCEPTION
      WHEN duplicate_object THEN null;
END $create_type_if_not_exists$;

DO $create_type_if_not_exists$ BEGIN
CREATE TYPE conclusion AS ENUM (
        'success',
        'failure',
        'neutral',
        'cancelled',
        'skipped',  -- 'skipped' is not documented, but has been encountered in 'workflow_job.steps[].conclusion'
        'timed_out',
        'action_required',
        'stale'
    );
EXCEPTION
      WHEN duplicate_object THEN null;
END $create_type_if_not_exists$;

CREATE TABLE IF NOT EXISTS runners
(
    id                       BIGINT                       PRIMARY KEY,
    name                     VARCHAR(255)                 NOT NULL
);

CREATE TABLE IF NOT EXISTS organizations
(
    id                       BIGINT                       PRIMARY KEY,
    name                     VARCHAR(255)                 NOT NULL
);

CREATE TABLE IF NOT EXISTS repositories
(
    id                       BIGINT                       PRIMARY KEY,
    org_id                   BIGINT                       REFERENCES organizations,
    name                     VARCHAR(255)                 NOT NULL,
    data                     JSONB
);

CREATE TABLE IF NOT EXISTS workflows
(
    id                       BIGINT                       PRIMARY KEY,
    repo_id                  BIGINT                       NOT NULL REFERENCES repositories,
    name                     VARCHAR(255)                 NOT NULL,
    path                     VARCHAR(255)                 NOT NULL,
    created_at               TIMESTAMP WITH TIME ZONE     ,
    updated_at               TIMESTAMP WITH TIME ZONE,
    data                     JSONB
);

CREATE TABLE IF NOT EXISTS runs
(
    id                       BIGINT                       PRIMARY KEY,
    workflow_id              BIGINT                       REFERENCES workflows,
    event                    VARCHAR(255)                 ,
    status                   status            ,
    conclusion               conclusion        ,
    start_time               TIMESTAMP WITH TIME ZONE     ,
    end_time                 TIMESTAMP WITH TIME ZONE     ,
    action_url               VARCHAR(255)                 ,
    run_number               INTEGER                      ,
    run_attempt              INTEGER                      ,
    branch                   VARCHAR(255)                 ,
    source_hash              VARCHAR(40)                  ,
    target_ref               VARCHAR(255)
    );

CREATE TABLE IF NOT EXISTS jobs
(
    id                       BIGINT                       PRIMARY KEY,
    run_id                   BIGINT                       NOT NULL REFERENCES runs ON DELETE CASCADE,
    runner_id                BIGINT                       REFERENCES runners,
    name                     VARCHAR(255)                 NOT NULL,
    status                   status                       NOT NULL,
    conclusion               conclusion        ,
    start_time               TIMESTAMP WITH TIME ZONE     ,
    end_time                 TIMESTAMP WITH TIME ZONE,
    data                     JSONB
);

CREATE TABLE IF NOT EXISTS steps
(
    job_id                   BIGINT                       NOT NULL REFERENCES jobs ON DELETE CASCADE,
    step_nr                  INTEGER                      NOT NULL,
    name                     VARCHAR(255)                 NOT NULL,
    status                   status                       NOT NULL,
    conclusion               conclusion        ,
    start_time               TIMESTAMP WITH TIME ZONE     ,
    end_time                 TIMESTAMP WITH TIME ZONE     ,
    PRIMARY KEY (job_id, step_nr)
);

END;