
```

CREATE SCHEMA batch_jobs;
CREATE SCHEMA random_schema;  -- Replace 'random_schema' with your preferred name


CREATE EXTENSION "uuid-ossp";
 
 
CREATE TABLE batch_jobs.runs (
    run_id SERIAL PRIMARY KEY,
    client_name VARCHAR(255) NOT NULL,
    run_uuid UUID DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE batch_jobs.runs ADD CONSTRAINT unique_run_uuid UNIQUE(run_uuid);

-- INSERT INTO batch_jobs.runs (client_name) VALUES ('ClientB');


CREATE TABLE batch_jobs.checkpoints (
    batch_id SERIAL PRIMARY KEY,
    status VARCHAR(50) NOT NULL,
    run_uuid_fk UUID REFERENCES batch_jobs.runs(run_uuid),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


```