-- Tables for DuckDB. Stocks are joined on security_id, never on ticker.

CREATE TABLE IF NOT EXISTS securities (
    security_id      VARCHAR PRIMARY KEY,
    name             VARCHAR NOT NULL,
    sector           VARCHAR,
    security_type    VARCHAR NOT NULL,
    listed_date      DATE,
    delisted_date    DATE,
    delisting_reason VARCHAR  -- bankruptcy, merger, acquisition, voluntary, other
);

CREATE TABLE IF NOT EXISTS ticker_history (
    security_id VARCHAR NOT NULL REFERENCES securities (security_id),
    ticker      VARCHAR NOT NULL,
    exchange    VARCHAR,
    start_date  DATE NOT NULL,
    end_date    DATE,
    PRIMARY KEY (security_id, ticker, start_date)
);

CREATE TABLE IF NOT EXISTS prices (
    security_id    VARCHAR NOT NULL REFERENCES securities (security_id),
    date           DATE NOT NULL,
    open           DOUBLE,
    high           DOUBLE,
    low            DOUBLE,
    close          DOUBLE,
    volume         DOUBLE,
    adjusted_close DOUBLE,
    total_return   DOUBLE,
    PRIMARY KEY (security_id, date)
);

CREATE TABLE IF NOT EXISTS corporate_actions (
    security_id VARCHAR NOT NULL REFERENCES securities (security_id),
    date        DATE NOT NULL,
    action_type VARCHAR NOT NULL,  -- split, dividend, merger, delisting
    value       DOUBLE,
    PRIMARY KEY (security_id, date, action_type)
);

-- Each row is one version of a report, so restatements keep the original figures.
CREATE TABLE IF NOT EXISTS fundamentals (
    security_id        VARCHAR NOT NULL REFERENCES securities (security_id),
    period_end         DATE NOT NULL,
    published_date     DATE NOT NULL,
    revenue            DOUBLE,
    gross_profit       DOUBLE,
    operating_income   DOUBLE,
    net_income         DOUBLE,
    interest_expense   DOUBLE,
    free_cash_flow     DOUBLE,
    total_debt         DOUBLE,
    cash               DOUBLE,
    book_equity        DOUBLE,
    shares_outstanding DOUBLE,
    PRIMARY KEY (security_id, period_end, published_date)
);

CREATE TABLE IF NOT EXISTS macro (
    date   DATE NOT NULL,
    series VARCHAR NOT NULL,  -- e.g. treasury_10y, cpi, market_return
    value  DOUBLE,
    PRIMARY KEY (date, series)
);

-- Long format, so indicators can change without altering the table.
CREATE TABLE IF NOT EXISTS features (
    security_id VARCHAR NOT NULL REFERENCES securities (security_id),
    month       DATE NOT NULL,
    feature     VARCHAR NOT NULL,
    value       DOUBLE,  -- NULL marks a missing value; never fill it with zero.
    PRIMARY KEY (security_id, month, feature)
);
