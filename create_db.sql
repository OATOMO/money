-- ֤ȯ�����
create table stock_code
(
    code         text not null
        constraint stock_code_pk
            unique,
    code_name    text not null,
    trade_status text
);
-- ֤ȯ��ҵ��
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

comment on table stock_industry is '֤ȯ��ҵ';

comment on column stock_industry.industryclassification is '����';

comment on column stock_industry.industry is '��ҵ';
-- k �������ݱ�
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

comment on table stock_d_k_line is '��k��
';

comment on column stock_d_k_line.preclose is '�������̼�';

comment on column stock_d_k_line.volume is '�ɽ���';

comment on column stock_d_k_line.amount is '�ɽ����';

comment on column stock_d_k_line.adjustflag is '��Ȩ״̬';

comment on column stock_d_k_line.close is '�����̼�
';

