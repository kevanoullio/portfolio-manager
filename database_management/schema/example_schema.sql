create sequence portfolio_ids start with 1;

create TABLE portfolio_users (
  email VARCHAR(32) NOT NULL primary key,
    constraint email_valid CHECK (REGEXP_LIKE (email, '[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+\.[a-zA-Z]{2,4}')),
  name VARCHAR(32) NOT NULL,
  password VARCHAR(64) NOT NULL,
      constraint long_pw CHECK (password LIKE '________%')
);

create TABLE portfolio_portfolios (
  id number primary key,
  name VARCHAR(32) NOT NULL,
  description VARCHAR(255),
  owner NOT NULL references portfolio_users(email) ON DELETE CASCADE,
  creation_date number,
  cash_balance number default '0' NOT NULL,
    constraint cash_balance_nonnegative CHECK( cash_balance >=0 )
);

create TABLE portfolio_stocksDaily (
  symbol varchar(16) NOT NULL,
  time number NOT NULL,
    constraint stock_time_unique UNIQUE(symbol, time),
  open number NOT NULL,
  close number NOT NULL,
  high number NOT NULL,
  low number NOT NULL,
  volume number NOT NULL
);

create TABLE stocks_stats (
  symbol VARCHAR(16) NOT NULL,
  from_date number,
  to_date number,
  field VARCHAR(32),
  count number NOT NULL,
  average number NOT NULL,
  std_dev number NOT NULL,
  min number NOT NULL,
  max number NOT NULL,
  volatility number NOT NULL,
  beta number NOT NULL,
    constraint stock_stats_cache_unique UNIQUE(symbol, from_date, to_date, field)
);

create TABLE covar_corr (
  symbol1 VARCHAR(16) NOT NULL,
  symbol2 VARCHAR(16) NOT NULL,
  covar number NOT NULL,
  corr number NOT NULL,
    constraint covar_corr_unique UNIQUE(symbol1, symbol2)
);

create TABLE portfolio_stocks (
  symbol VARCHAR(16) NOT NULL,
  shares number default '0' NOT NULL,
  cost_basis number NOT NULL,
  holder number references portfolio_portfolios(id) ON DELETE CASCADE,
    constraint stock_portfolio_unique UNIQUE(symbol, holder)
);

create TABLE averagesDaily (
  time number NOT NULL,
  average number NOT NULL,
    constraint time_ave_unique UNIQUE(time, average)
);

  

quit;