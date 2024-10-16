from app.utils import execute_query


def initialize_database():
    
    query = ''' CREATE TABLE IF NOT EXISTS Users (
                user_id             SERIAL          PRIMARY KEY,
                user_login          VARCHAR(255)    NOT NULL        UNIQUE,
                password_hash       VARCHAR(255)    NOT NULL,
                user_role           VARCHAR(255)    NOT NULL        DEFAULT 'Guest'
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
                contact_number              VARCHAR(20)     NOT NULL        UNIQUE,
                address                     VARCHAR(255)    NOT NULL,
                client_email                VARCHAR(255)    NOT NULL        UNIQUE,
                user_id                     INTEGER         NOT NULL
    );'''

    execute_query(query)

    # =============================================

    query = ''' CREATE TABLE IF NOT EXISTS Policies (
                policy_id                   SERIAL          PRIMARY KEY,
                policy_type                 VARCHAR(255)    NOT NULL,
                date_start                  DATE            NOT NULL,
                date_stop                   DATE            NOT NULL,
                policy_cost                 INTEGER         NOT NULL,
                car_id                      INTEGER         NOT NULL,
                client_id                   INTEGER         NOT NULL,
                agent_id                    INTEGER         NOT NULL
    );'''
    
    execute_query(query)
    
    # =============================================
    
    query = ''' CREATE TABLE IF NOT EXISTS Drivers (
                driver_id                   SERIAL          PRIMARY KEY,
                policy_id                   INTEGER         NOT NULL,
                driver_first_name           VARCHAR(255)    NOT NULL,
                driver_last_name            VARCHAR(255)    NOT NULL,
                driver_surname              VARCHAR(255)    NOT NULL,
                license_number              VARCHAR(255)    NOT NULL,
                first_license_date          DATE            NOT NULL,
                driver_birth                DATE            NOT NULL
    );'''
    
    execute_query(query)
    
    # =============================================
    
    query = ''' CREATE TABLE IF NOT EXISTS Cars (
                car_id                      SERIAL          PRIMARY KEY,
                brand_id                    INTEGER         NOT NULL,
                year_manufacture            INTEGER         NOT NULL,
                state_number                VARCHAR(255)    NOT NULL,
                damage_description          TEXT
    );'''
    
    execute_query(query)
    
    # =============================================
    
    query = ''' CREATE TABLE IF NOT EXISTS Brands (
                brand_id                    SERIAL          PRIMARY KEY,
                brand                       VARCHAR(255)    NOT NULL,
                model                       VARCHAR         NOT NULL,
                coefficient                 DECIMAL(3,2)    NOT NULL
    );'''
    
    execute_query(query)
    
    # =============================================
    
    query = ''' CREATE TABLE IF NOT EXISTS Agents (
                agent_id                    SERIAL          PRIMARY KEY,
                agent_first_name            VARCHAR(255)    NOT NULL,
                agent_last_name             VARCHAR(255)    NOT NULL,
                agent_surname               VARCHAR(255)    NOT NULL,
                hiring_date                 DATE            NOT NULL,
                agent_number                VARCHAR(255)    NOT NULL,
                agent_email                 VARCHAR(255)    NOT NULL,
                user_id                     INTEGER         NOT NULL
    );'''
    
    execute_query(query)
    
    # =============================================
    
    query = ''' CREATE TABLE IF NOT EXISTS Insurance_cases (
                case_id                     SERIAL          PRIMARY KEY,
                payment_id                  INTEGER         NOT NULL,
                case_date                   DATE            NOT NULL,
                agent_id                    INTEGER         NOT NULL,    
                policy_id                   INTEGER         NOT NULL,
                case_description          TEXT            NOT NULL,
                case_status                 VARCHAR(255)    NOT NULL
    );'''
    
    execute_query(query)
    
    # =============================================
    
    query = ''' CREATE TABLE IF NOT EXISTS Insurance_payments (
                payment_id                  SERIAL          PRIMARY KEY,
                payment_sum                 INTEGER         NOT NULL,
                payment_date                DATE            NOT NULL,
                payment_details             VARCHAR(255)    NOT NULL
    );'''
    
    execute_query(query)
    
    # =============================================