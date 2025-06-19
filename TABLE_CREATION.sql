CREATE TABLE user_profiles (
    ID BIGSERIAL PRIMARY KEY,
    title VARCHAR(255),
    permissions JSON,
    created_at TIMESTAMP,
    status BOOLEAN
);

CREATE TABLE bank (
    ID BIGSERIAL PRIMARY KEY,
    name VARCHAR(255),
    document VARCHAR(255),
    created_at TIMESTAMP
);

INSERT INTO bank (name, document, created_at)
VALUES ('Banco Exemplo', '1234567890129', CURRENT_TIMESTAMP)

CREATE TABLE bank_users (
    ID BIGSERIAL PRIMARY KEY,
    username VARCHAR(255),
    password VARCHAR(255),
    bank_id BIGINT REFERENCES bank(ID),
    created_at TIMESTAMP,
    status BOOLEAN,
    profileId BIGINT REFERENCES user_profiles(ID)
);

CREATE TABLE account_types (
    ID BIGSERIAL PRIMARY KEY,
    title VARCHAR(255),
    created_at TIMESTAMP,
    status BOOLEAN
);

CREATE TABLE account_status (
    ID BIGSERIAL PRIMARY KEY,
    title VARCHAR(255),
    created_at TIMESTAMP,
    status BOOLEAN
);

CREATE TABLE accounts (
    ID BIGSERIAL PRIMARY KEY,
    account_number VARCHAR(255),
    client_id BIGINT,
    balance DOUBLE PRECISION,
    account_type_id BIGINT REFERENCES account_types(ID),
    created_at TIMESTAMP,
    closed_at TIMESTAMP,
    bank_id BIGINT REFERENCES bank(ID),
    account_status_id BIGINT REFERENCES account_status(ID)
);

CREATE TABLE account_logs (
    ID BIGSERIAL PRIMARY KEY,
    account_id BIGINT REFERENCES accounts(ID),
    action INT,
    performed_by BIGINT,
    description TEXT,
    created_at TIMESTAMP
);

CREATE TABLE transaction_types (
    ID BIGSERIAL PRIMARY KEY,
    title VARCHAR(255),
    created_at TIMESTAMP,
    status BOOLEAN
);

CREATE TABLE transactions (
    ID BIGSERIAL PRIMARY KEY,
    from_account_id BIGINT REFERENCES accounts(ID),
    to_account_id BIGINT REFERENCES accounts(ID),
    transaction_type_id BIGINT REFERENCES transaction_types(ID),
    amount DOUBLE PRECISION,
    created_at TIMESTAMP,
    status INT,
    description TEXT
);

CREATE TABLE client_users (
    ID BIGSERIAL PRIMARY KEY,
    username VARCHAR(255),
    password VARCHAR(255),
    created_at TIMESTAMP,
    status BOOLEAN,
    description TEXT
);

CREATE TABLE clients (
    ID BIGSERIAL PRIMARY KEY,
    name VARCHAR(255),
    document VARCHAR(255),
    created_at TIMESTAMP,
    client_user_id BIGINT REFERENCES client_users(ID)
);

CREATE TABLE code_cities (
    code_city BIGINT PRIMARY KEY,
    state VARCHAR(100),
    city VARCHAR(100),
    country VARCHAR(100)
);

CREATE TABLE client_addresses (
    ID BIGSERIAL PRIMARY KEY,
    client_id BIGINT REFERENCES clients(ID),
    title VARCHAR(255),
    street VARCHAR(255),
    code_city_id BIGINT REFERENCES code_cities(code_city)
);

CREATE TABLE session_tokens (
    ID BIGSERIAL PRIMARY KEY,
    client_user_id BIGINT REFERENCES client_users(ID),
    token VARCHAR(255),
    ip_address VARCHAR(100),
    user_agent TEXT,
    created_at TIMESTAMP,
    expires_at TIMESTAMP,
    revoked BOOLEAN
);
