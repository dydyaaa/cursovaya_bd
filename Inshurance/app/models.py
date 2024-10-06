from app.utils import execute_query


def initialize_database():
    query = ''' CREATE TABLE IF NOT EXISTS Policies (
                policy_id               SERIAL          PRIMARY KEY,
                policy_type             VARCHAR(255)    NOT NULL,
                client_id               INTEGER         NOT NULL,
                car_id                  INTEGER         NOT NULL,
                date_start              DATE            NOT NULL,
                date_stop               DATE            NOT NULL,
                policy_cost             INTEGER         NOT NULL,
                sum_insurance           INTEGER         NOT NULL,
                drivers                 VARCHAR(255)    NOT NULL,
                status                  VARCHAR(255)    DEFAULT 'Действующий'
    );'''

    execute_query(query)

    # =============================================

    query = ''' CREATE TABLE IF NOT EXISTS Clients (
                client_id                   SERIAL          PRIMARY KEY,
                client_first_name           VARCHAR(255)    NOT NULL,
                client_last_name            VARCHAR(255)    NOT NULL,
                client_surname              VARCHAR(255)    NOT NULL,
                birth_day                   DATE            NOT NULL,
                passport_series             INTEGER         NOT NULL,
                passport_number             INTEGER         NOT NULL,
                contact_number              VARCHAR(20)     NOT NULL,
                address                     VARCHAR(255)    NOT NULL,
                email                       VARCHAR         NOT NULL,
                user_id                     INTEGER         NOT NULL,
    );'''

    execute_query(query)

    # =============================================

    query = ''' CREATE TABLE IF NOT EXISTS Agents (
                agent_id                SERIAL          PRIMARY KEY,
                agent_first_name        VARCHAR(255)    NOT NULL,
                agent_last_name         VARCHAR(255)    NOT NULL,
                agent_surname           VARCHAR(255)    NOT NULL,
                agent_role              VARCHAR(255)    NOT NULL,
                hiring date             DATE            NOT NULL,
                user_id                 INTEGER         NOT NULL
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

    query = ''' CREATE TABLE IF NOT EXISTS Users (
                user_id             SERIAL          PRIMARY KEY,
                user_login          VARCHAR(255)    NOT NULL        UNIQUE,
                password_hash       VARCHAR(255)    NOT NULL,
                user_role           VARCHAR(255)    NOT NULL        DEFAULT 'Guest'
    );'''

    execute_query(query)
    
    # =============================================
    
    query = ''' CREATE TABLE IF NOT EXISTS Cars (
                car_id                  SERIAL          PRIMARY KEY,
                car_brand               VARCHAR(255)    NOT NULL,
                car_model               VARCHAR(255)    NOT NULL,    
                year_of_manufacture     INTEGER         NOT NULL,
                car_number              VARCHAR(255)    NOT NULL,
                damage_description      TEXT,
                photo_url               TEXT
    );'''
    
    execute_query(query)
    
    # =============================================
    
    query = ''' CREATE TABLE IF NOT EXISTS Drivers (
                driver_id               SERIAL              PRIMARY KEY,
                driver_first_name       VARCHAR(255)        NOT NUL,
                driver_last_name        VARCHAR(255)        NOT NULL,
                driver_surname          VARCHAR(255)        NOT NULL,
                dirver_licence          VARCHAR(255)        NOT NULL,
                date_of_issue           DATE                NOT NULL,
                region                  VARCHAR(255)        NOT NULL
                
    );'''    
    
    # =============================================
    
    query = ''' CREATE TABLE IF NOT EXISTS insurance_payments (
                payment_id              SERIAL              PRIMARY KEY,
                payment_sum             INTEGER             NOT NULL,
                payment_date            DATE,
                status                  VARCHAR(255)        DEFAULT ''
    );'''