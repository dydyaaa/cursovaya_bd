from app.utils import execute_query


def initialize_database():
    query = ''' CREATE TABLE IF NOT EXISTS Policies (
                policy_id               SERIAL          PRIMARY KEY,
                policy_type             VARCHAR(255)    NOT NULL,
                agent_id                INTEGER,
                client_id               INTEGER,
                date_start              DATE            NOT NULL,
                date_stop               DATE            NOT NULL,
                car_brand               VARCHAR(255)    NOT NULL,
                year_of_manufacture     INTEGER         NOT NULL,
                policy_cost             INTEGER         NOT NULL,
                sum_insurance           INTEGER         NOT NULL,
                status                  VARCHAR(255)    DEFAULT 'На проверке'
    );'''

    execute_query(query)

    # =============================================

    query = ''' CREATE TABLE IF NOT EXISTS Clients (
                client_id           SERIAL          PRIMARY KEY,
                client_name         VARCHAR(255)    NOT NULL,
                birth_day           DATE            NOT NULL,
                passport_series     INTEGER         NOT NULL,
                passport_number     INTEGER         NOT NULL,
                contact_number      VARCHAR(20)     NOT NULL,
                address             VARCHAR(255)    NOT NULL,
                user_id             INTEGER         NOT NULL,
                status              VARCHAR(255)    DEFAULT 'На проверке'
    );'''

    execute_query(query)

    # =============================================

    query = ''' CREATE TABLE IF NOT EXISTS Agents (
                agent_id        SERIAL          PRIMARY KEY,
                agent_name      VARCHAR(255)    NOT NULL,
                agent_role      VARCHAR(255)    NOT NULL,
                user_id         INTEGER         NOT NULL
    );'''

    execute_query(query)

    # =============================================

    query = ''' CREATE TABLE IF NOT EXISTS Cases (
                case_id         SERIAL          PRIMARY KEY,
                policy_id       INTEGER,
                agent_id        INTEGER,
                date            DATE            NOT NULL,
                description     TEXT            NOT NULL,
                status          VARCHAR(255)    DEFAULT 'На проверке',
                sum_payment     INTEGER         DEFAULT 0
    );'''

    execute_query(query)

    # =============================================

    query = ''' CREATE TABLE Users (
                user_id             SERIAL          PRIMARY KEY,
                user_login          VARCHAR(255)    NOT NULL        UNIQUE,
                password_hash       VARCHAR(255)    NOT NULL,
                user_role           VARCHAR(255)    NOT NULL        DEFAULT 'guest'
    );'''

    execute_query(query)