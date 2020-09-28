-- 证券代码表
create table stock_code
(
    code         text not null
        constraint stock_code_pk
            unique,
    code_name    text not null,
    trade_status text
);
-- 证券行业表
create table stock_industry
(
    code                   text
        constraint stock_industry_pk
            unique,
    code_name              text,
    industryclassification text,
    industry               text,
    updatedate             date
);

comment on table stock_industry is '证券行业';

comment on column stock_industry.industryclassification is '分类';

comment on column stock_industry.industry is '行业';
-- k 日线数据表
create table stock_d_k_line
(
    date       date,
    code       text,
    open       double precision,
    high       double precision,
    low        double precision,
    close      double precision,
    preclose   double precision,
    volume     int8,
    amount     double precision,
    adjustflag text,
    turn	   double precision,
    tradestatus text,
    pctChg      double precision,
    peTTM       double precision,
    psTTM       double precision,
    pcfNcfTTM   double precision,
    pbMRQ       double precision,
    isST        text,
    constraint stock_d_k_line_pk
        primary key (date, code)
);

comment on table stock_d_k_line is '日k线
';

comment on column stock_d_k_line.preclose is '昨日收盘价';

comment on column stock_d_k_line.volume is '成交量';

comment on column stock_d_k_line.amount is '成交金额';

comment on column stock_d_k_line.adjustflag is '复权状态';

comment on column stock_d_k_line.close is '今收盘价
';

