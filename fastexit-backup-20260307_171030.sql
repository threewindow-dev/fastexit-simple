--
-- PostgreSQL database dump
--

\restrict KOnq45ap4lixrxLwidlZqxyVbbCfSPwcWfECwEDmvgIwfhRtj5CxjsQMfFq1X1D

-- Dumped from database version 17.9 (Debian 17.9-1.pgdg12+1)
-- Dumped by pg_dump version 17.9 (Debian 17.9-1.pgdg12+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.weekly_snapshots DROP CONSTRAINT IF EXISTS weekly_snapshots_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.weekly_snapshots DROP CONSTRAINT IF EXISTS weekly_snapshots_source_snapshot_id_fkey;
ALTER TABLE IF EXISTS ONLY public.weekly_snapshot_holdings DROP CONSTRAINT IF EXISTS weekly_snapshot_holdings_weekly_snapshot_id_fkey;
ALTER TABLE IF EXISTS ONLY public.weekly_snapshot_holdings DROP CONSTRAINT IF EXISTS weekly_snapshot_holdings_holding_id_fkey;
ALTER TABLE IF EXISTS ONLY public.target_allocations DROP CONSTRAINT IF EXISTS target_allocations_account_group_id_fkey;
ALTER TABLE IF EXISTS ONLY public.target_allocation_accounts DROP CONSTRAINT IF EXISTS target_allocation_accounts_account_id_fkey;
ALTER TABLE IF EXISTS ONLY public.snapshots DROP CONSTRAINT IF EXISTS snapshots_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.snapshot_holdings DROP CONSTRAINT IF EXISTS snapshot_holdings_snapshot_id_fkey;
ALTER TABLE IF EXISTS ONLY public.snapshot_holdings DROP CONSTRAINT IF EXISTS snapshot_holdings_holding_id_fkey;
ALTER TABLE IF EXISTS ONLY public.holdings DROP CONSTRAINT IF EXISTS holdings_product_id_fkey;
ALTER TABLE IF EXISTS ONLY public.holdings DROP CONSTRAINT IF EXISTS holdings_account_id_fkey;
ALTER TABLE IF EXISTS ONLY public.annual_snapshots DROP CONSTRAINT IF EXISTS annual_snapshots_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.annual_snapshots DROP CONSTRAINT IF EXISTS annual_snapshots_source_snapshot_id_fkey;
ALTER TABLE IF EXISTS ONLY public.annual_snapshot_holdings DROP CONSTRAINT IF EXISTS annual_snapshot_holdings_holding_id_fkey;
ALTER TABLE IF EXISTS ONLY public.annual_snapshot_holdings DROP CONSTRAINT IF EXISTS annual_snapshot_holdings_annual_snapshot_id_fkey;
ALTER TABLE IF EXISTS ONLY public.accounts DROP CONSTRAINT IF EXISTS accounts_institution_id_fkey;
ALTER TABLE IF EXISTS ONLY public.account_group_accounts DROP CONSTRAINT IF EXISTS account_group_accounts_account_id_fkey;
ALTER TABLE IF EXISTS ONLY public.account_group_accounts DROP CONSTRAINT IF EXISTS account_group_accounts_account_group_id_fkey;
DROP INDEX IF EXISTS public.ix_users_username;
DROP INDEX IF EXISTS public.ix_users_email;
DROP INDEX IF EXISTS public.idx_weekly_snapshots_user;
DROP INDEX IF EXISTS public.idx_weekly_snapshot_holdings_snap;
DROP INDEX IF EXISTS public.idx_target_allocations_year;
DROP INDEX IF EXISTS public.idx_target_allocations_account_group;
DROP INDEX IF EXISTS public.idx_target_allocation_totals_year;
DROP INDEX IF EXISTS public.idx_target_allocation_accounts_year;
DROP INDEX IF EXISTS public.idx_target_allocation_accounts_account;
DROP INDEX IF EXISTS public.idx_snapshots_user;
DROP INDEX IF EXISTS public.idx_snapshots_status;
DROP INDEX IF EXISTS public.idx_snapshot_holdings_snapshot;
DROP INDEX IF EXISTS public.idx_snapshot_holdings_holding;
DROP INDEX IF EXISTS public.idx_holdings_product;
DROP INDEX IF EXISTS public.idx_holdings_account;
DROP INDEX IF EXISTS public.idx_annual_snapshots_user;
DROP INDEX IF EXISTS public.idx_annual_snapshot_holdings_snap;
DROP INDEX IF EXISTS public.idx_accounts_institution;
DROP INDEX IF EXISTS public.idx_account_group_accounts_account;
ALTER TABLE IF EXISTS ONLY public.weekly_snapshots DROP CONSTRAINT IF EXISTS weekly_snapshots_pkey;
ALTER TABLE IF EXISTS ONLY public.weekly_snapshot_holdings DROP CONSTRAINT IF EXISTS weekly_snapshot_holdings_pkey;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_pkey;
ALTER TABLE IF EXISTS ONLY public.weekly_snapshots DROP CONSTRAINT IF EXISTS uq_weekly_snapshot_user_reference;
ALTER TABLE IF EXISTS ONLY public.weekly_snapshot_holdings DROP CONSTRAINT IF EXISTS uq_weekly_snapshot_holding;
ALTER TABLE IF EXISTS ONLY public.target_allocations DROP CONSTRAINT IF EXISTS uq_target_allocation_year_group;
ALTER TABLE IF EXISTS ONLY public.target_allocation_accounts DROP CONSTRAINT IF EXISTS uq_target_allocation_account_year_account;
ALTER TABLE IF EXISTS ONLY public.snapshots DROP CONSTRAINT IF EXISTS uq_snapshot_user_reference;
ALTER TABLE IF EXISTS ONLY public.snapshot_holdings DROP CONSTRAINT IF EXISTS uq_snapshot_holding;
ALTER TABLE IF EXISTS ONLY public.products DROP CONSTRAINT IF EXISTS uq_product_identity;
ALTER TABLE IF EXISTS ONLY public.holdings DROP CONSTRAINT IF EXISTS uq_holding_account_product;
ALTER TABLE IF EXISTS ONLY public.annual_snapshots DROP CONSTRAINT IF EXISTS uq_annual_snapshot_user_reference;
ALTER TABLE IF EXISTS ONLY public.annual_snapshot_holdings DROP CONSTRAINT IF EXISTS uq_annual_snapshot_holding;
ALTER TABLE IF EXISTS ONLY public.accounts DROP CONSTRAINT IF EXISTS uq_account_name_per_institution;
ALTER TABLE IF EXISTS ONLY public.target_allocations DROP CONSTRAINT IF EXISTS target_allocations_pkey;
ALTER TABLE IF EXISTS ONLY public.target_allocation_totals DROP CONSTRAINT IF EXISTS target_allocation_totals_year_key;
ALTER TABLE IF EXISTS ONLY public.target_allocation_totals DROP CONSTRAINT IF EXISTS target_allocation_totals_pkey;
ALTER TABLE IF EXISTS ONLY public.target_allocation_accounts DROP CONSTRAINT IF EXISTS target_allocation_accounts_pkey;
ALTER TABLE IF EXISTS ONLY public.snapshots DROP CONSTRAINT IF EXISTS snapshots_pkey;
ALTER TABLE IF EXISTS ONLY public.snapshot_holdings DROP CONSTRAINT IF EXISTS snapshot_holdings_pkey;
ALTER TABLE IF EXISTS ONLY public.products DROP CONSTRAINT IF EXISTS products_pkey;
ALTER TABLE IF EXISTS ONLY public.institutions DROP CONSTRAINT IF EXISTS institutions_pkey;
ALTER TABLE IF EXISTS ONLY public.institutions DROP CONSTRAINT IF EXISTS institutions_name_key;
ALTER TABLE IF EXISTS ONLY public.holdings DROP CONSTRAINT IF EXISTS holdings_pkey;
ALTER TABLE IF EXISTS ONLY public.annual_snapshots DROP CONSTRAINT IF EXISTS annual_snapshots_pkey;
ALTER TABLE IF EXISTS ONLY public.annual_snapshot_holdings DROP CONSTRAINT IF EXISTS annual_snapshot_holdings_pkey;
ALTER TABLE IF EXISTS ONLY public.accounts DROP CONSTRAINT IF EXISTS accounts_pkey;
ALTER TABLE IF EXISTS ONLY public.account_groups DROP CONSTRAINT IF EXISTS account_groups_pkey;
ALTER TABLE IF EXISTS ONLY public.account_groups DROP CONSTRAINT IF EXISTS account_groups_name_key;
ALTER TABLE IF EXISTS ONLY public.account_group_accounts DROP CONSTRAINT IF EXISTS account_group_accounts_pkey;
ALTER TABLE IF EXISTS public.weekly_snapshots ALTER COLUMN weekly_snapshot_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.weekly_snapshot_holdings ALTER COLUMN weekly_snapshot_holding_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.users ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.target_allocations ALTER COLUMN target_allocation_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.target_allocation_totals ALTER COLUMN target_allocation_total_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.target_allocation_accounts ALTER COLUMN target_allocation_account_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.snapshots ALTER COLUMN snapshot_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.snapshot_holdings ALTER COLUMN snapshot_holding_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.products ALTER COLUMN product_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.institutions ALTER COLUMN institution_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.holdings ALTER COLUMN holding_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.annual_snapshots ALTER COLUMN annual_snapshot_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.annual_snapshot_holdings ALTER COLUMN annual_snapshot_holding_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.accounts ALTER COLUMN account_id DROP DEFAULT;
ALTER TABLE IF EXISTS public.account_groups ALTER COLUMN account_group_id DROP DEFAULT;
DROP SEQUENCE IF EXISTS public.weekly_snapshots_weekly_snapshot_id_seq;
DROP TABLE IF EXISTS public.weekly_snapshots;
DROP SEQUENCE IF EXISTS public.weekly_snapshot_holdings_weekly_snapshot_holding_id_seq;
DROP TABLE IF EXISTS public.weekly_snapshot_holdings;
DROP SEQUENCE IF EXISTS public.users_id_seq;
DROP TABLE IF EXISTS public.users;
DROP SEQUENCE IF EXISTS public.target_allocations_target_allocation_id_seq;
DROP TABLE IF EXISTS public.target_allocations;
DROP SEQUENCE IF EXISTS public.target_allocation_totals_target_allocation_total_id_seq;
DROP TABLE IF EXISTS public.target_allocation_totals;
DROP SEQUENCE IF EXISTS public.target_allocation_accounts_target_allocation_account_id_seq;
DROP TABLE IF EXISTS public.target_allocation_accounts;
DROP SEQUENCE IF EXISTS public.snapshots_snapshot_id_seq;
DROP TABLE IF EXISTS public.snapshots;
DROP SEQUENCE IF EXISTS public.snapshot_holdings_snapshot_holding_id_seq;
DROP TABLE IF EXISTS public.snapshot_holdings;
DROP SEQUENCE IF EXISTS public.products_product_id_seq;
DROP TABLE IF EXISTS public.products;
DROP SEQUENCE IF EXISTS public.institutions_institution_id_seq;
DROP TABLE IF EXISTS public.institutions;
DROP SEQUENCE IF EXISTS public.holdings_holding_id_seq;
DROP TABLE IF EXISTS public.holdings;
DROP SEQUENCE IF EXISTS public.annual_snapshots_annual_snapshot_id_seq;
DROP TABLE IF EXISTS public.annual_snapshots;
DROP SEQUENCE IF EXISTS public.annual_snapshot_holdings_annual_snapshot_holding_id_seq;
DROP TABLE IF EXISTS public.annual_snapshot_holdings;
DROP SEQUENCE IF EXISTS public.accounts_account_id_seq;
DROP TABLE IF EXISTS public.accounts;
DROP SEQUENCE IF EXISTS public.account_groups_account_group_id_seq;
DROP TABLE IF EXISTS public.account_groups;
DROP TABLE IF EXISTS public.account_group_accounts;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: account_group_accounts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account_group_accounts (
    account_group_id integer NOT NULL,
    account_id integer NOT NULL,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.account_group_accounts OWNER TO postgres;

--
-- Name: account_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.account_groups (
    account_group_id integer NOT NULL,
    name character varying(255) NOT NULL,
    include_in_report boolean NOT NULL,
    display_order integer NOT NULL,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.account_groups OWNER TO postgres;

--
-- Name: account_groups_account_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.account_groups_account_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.account_groups_account_group_id_seq OWNER TO postgres;

--
-- Name: account_groups_account_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.account_groups_account_group_id_seq OWNED BY public.account_groups.account_group_id;


--
-- Name: accounts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts (
    account_id integer NOT NULL,
    institution_id integer NOT NULL,
    name character varying(255) NOT NULL,
    type character varying(100) NOT NULL,
    display_order integer NOT NULL,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.accounts OWNER TO postgres;

--
-- Name: accounts_account_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.accounts_account_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.accounts_account_id_seq OWNER TO postgres;

--
-- Name: accounts_account_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.accounts_account_id_seq OWNED BY public.accounts.account_id;


--
-- Name: annual_snapshot_holdings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.annual_snapshot_holdings (
    annual_snapshot_holding_id integer NOT NULL,
    annual_snapshot_id integer NOT NULL,
    holding_id integer NOT NULL,
    valuation_amount numeric(20,4) NOT NULL,
    data_source character varying(10) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    CONSTRAINT chk_annual_snapshot_data_source CHECK (((data_source)::text = ANY ((ARRAY['auto'::character varying, 'manual'::character varying, 'missing'::character varying])::text[])))
);


ALTER TABLE public.annual_snapshot_holdings OWNER TO postgres;

--
-- Name: annual_snapshot_holdings_annual_snapshot_holding_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.annual_snapshot_holdings_annual_snapshot_holding_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.annual_snapshot_holdings_annual_snapshot_holding_id_seq OWNER TO postgres;

--
-- Name: annual_snapshot_holdings_annual_snapshot_holding_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.annual_snapshot_holdings_annual_snapshot_holding_id_seq OWNED BY public.annual_snapshot_holdings.annual_snapshot_holding_id;


--
-- Name: annual_snapshots; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.annual_snapshots (
    annual_snapshot_id integer NOT NULL,
    user_id integer NOT NULL,
    reference_date date NOT NULL,
    source_snapshot_id integer NOT NULL,
    status character varying(20) NOT NULL,
    editable_until timestamp without time zone,
    created_at timestamp without time zone NOT NULL,
    CONSTRAINT chk_annual_snapshot_status CHECK (((status)::text = 'locked'::text))
);


ALTER TABLE public.annual_snapshots OWNER TO postgres;

--
-- Name: annual_snapshots_annual_snapshot_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.annual_snapshots_annual_snapshot_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.annual_snapshots_annual_snapshot_id_seq OWNER TO postgres;

--
-- Name: annual_snapshots_annual_snapshot_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.annual_snapshots_annual_snapshot_id_seq OWNED BY public.annual_snapshots.annual_snapshot_id;


--
-- Name: holdings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.holdings (
    holding_id integer NOT NULL,
    account_id integer NOT NULL,
    product_id integer NOT NULL,
    is_visible boolean NOT NULL,
    deleted_at timestamp without time zone,
    deletion_reason text,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.holdings OWNER TO postgres;

--
-- Name: holdings_holding_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.holdings_holding_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.holdings_holding_id_seq OWNER TO postgres;

--
-- Name: holdings_holding_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.holdings_holding_id_seq OWNED BY public.holdings.holding_id;


--
-- Name: institutions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.institutions (
    institution_id integer NOT NULL,
    name character varying(255) NOT NULL,
    type character varying(50) NOT NULL,
    display_order integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    CONSTRAINT chk_institution_type CHECK (((type)::text = ANY ((ARRAY['증권사'::character varying, '은행'::character varying, '기타기관'::character varying])::text[])))
);


ALTER TABLE public.institutions OWNER TO postgres;

--
-- Name: institutions_institution_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.institutions_institution_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.institutions_institution_id_seq OWNER TO postgres;

--
-- Name: institutions_institution_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.institutions_institution_id_seq OWNED BY public.institutions.institution_id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    product_id integer NOT NULL,
    product_name character varying(255) NOT NULL,
    asset_class character varying(50) NOT NULL,
    region character varying(50) NOT NULL,
    currency character varying(10) NOT NULL,
    investment_type character varying(50) NOT NULL,
    characteristics character varying[],
    risk_level character varying(20) NOT NULL,
    allow_snapshot_input boolean NOT NULL,
    display_order integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    CONSTRAINT chk_product_asset_class CHECK (((asset_class)::text = ANY ((ARRAY['주식'::character varying, '채권'::character varying, '통화'::character varying, '금'::character varying, '부동산'::character varying, '가상자산'::character varying, '기타자산'::character varying])::text[]))),
    CONSTRAINT chk_product_currency CHECK (((currency)::text = ANY ((ARRAY['KRW'::character varying, 'USD'::character varying])::text[]))),
    CONSTRAINT chk_product_investment_type CHECK (((investment_type)::text = ANY ((ARRAY['직접'::character varying, 'ETF'::character varying])::text[]))),
    CONSTRAINT chk_product_region CHECK (((region)::text = ANY ((ARRAY['대한민국'::character varying, '미국'::character varying])::text[]))),
    CONSTRAINT chk_product_risk_level CHECK (((risk_level)::text = ANY ((ARRAY['안전'::character varying, '위험'::character varying])::text[])))
);


ALTER TABLE public.products OWNER TO postgres;

--
-- Name: products_product_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.products_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.products_product_id_seq OWNER TO postgres;

--
-- Name: products_product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.products_product_id_seq OWNED BY public.products.product_id;


--
-- Name: snapshot_holdings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.snapshot_holdings (
    snapshot_holding_id integer NOT NULL,
    snapshot_id integer NOT NULL,
    holding_id integer NOT NULL,
    valuation_amount numeric(20,4) NOT NULL,
    data_source character varying(10) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    CONSTRAINT chk_snapshot_data_source CHECK (((data_source)::text = ANY ((ARRAY['auto'::character varying, 'manual'::character varying, 'missing'::character varying])::text[])))
);


ALTER TABLE public.snapshot_holdings OWNER TO postgres;

--
-- Name: snapshot_holdings_snapshot_holding_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.snapshot_holdings_snapshot_holding_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.snapshot_holdings_snapshot_holding_id_seq OWNER TO postgres;

--
-- Name: snapshot_holdings_snapshot_holding_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.snapshot_holdings_snapshot_holding_id_seq OWNED BY public.snapshot_holdings.snapshot_holding_id;


--
-- Name: snapshots; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.snapshots (
    snapshot_id integer NOT NULL,
    user_id integer NOT NULL,
    reference_date date NOT NULL,
    status character varying(20) NOT NULL,
    locked_at timestamp without time zone,
    editable_until timestamp without time zone,
    created_at timestamp without time zone NOT NULL,
    CONSTRAINT chk_snapshot_status CHECK (((status)::text = ANY ((ARRAY['in_progress'::character varying, 'locked'::character varying])::text[])))
);


ALTER TABLE public.snapshots OWNER TO postgres;

--
-- Name: snapshots_snapshot_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.snapshots_snapshot_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.snapshots_snapshot_id_seq OWNER TO postgres;

--
-- Name: snapshots_snapshot_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.snapshots_snapshot_id_seq OWNED BY public.snapshots.snapshot_id;


--
-- Name: target_allocation_accounts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.target_allocation_accounts (
    target_allocation_account_id integer NOT NULL,
    year integer NOT NULL,
    account_id integer NOT NULL,
    target_amount numeric(15,2) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.target_allocation_accounts OWNER TO postgres;

--
-- Name: target_allocation_accounts_target_allocation_account_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.target_allocation_accounts_target_allocation_account_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.target_allocation_accounts_target_allocation_account_id_seq OWNER TO postgres;

--
-- Name: target_allocation_accounts_target_allocation_account_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.target_allocation_accounts_target_allocation_account_id_seq OWNED BY public.target_allocation_accounts.target_allocation_account_id;


--
-- Name: target_allocation_totals; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.target_allocation_totals (
    target_allocation_total_id integer NOT NULL,
    year integer NOT NULL,
    target_amount numeric(15,2) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.target_allocation_totals OWNER TO postgres;

--
-- Name: target_allocation_totals_target_allocation_total_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.target_allocation_totals_target_allocation_total_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.target_allocation_totals_target_allocation_total_id_seq OWNER TO postgres;

--
-- Name: target_allocation_totals_target_allocation_total_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.target_allocation_totals_target_allocation_total_id_seq OWNED BY public.target_allocation_totals.target_allocation_total_id;


--
-- Name: target_allocations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.target_allocations (
    target_allocation_id integer NOT NULL,
    year integer NOT NULL,
    account_group_id integer NOT NULL,
    target_amount numeric(15,2) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.target_allocations OWNER TO postgres;

--
-- Name: target_allocations_target_allocation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.target_allocations_target_allocation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.target_allocations_target_allocation_id_seq OWNER TO postgres;

--
-- Name: target_allocations_target_allocation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.target_allocations_target_allocation_id_seq OWNED BY public.target_allocations.target_allocation_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(100) NOT NULL,
    email character varying(255) NOT NULL,
    full_name character varying(255),
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: weekly_snapshot_holdings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.weekly_snapshot_holdings (
    weekly_snapshot_holding_id integer NOT NULL,
    weekly_snapshot_id integer NOT NULL,
    holding_id integer NOT NULL,
    valuation_amount numeric(20,4) NOT NULL,
    data_source character varying(10) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    CONSTRAINT chk_weekly_snapshot_data_source CHECK (((data_source)::text = ANY ((ARRAY['auto'::character varying, 'manual'::character varying, 'missing'::character varying])::text[])))
);


ALTER TABLE public.weekly_snapshot_holdings OWNER TO postgres;

--
-- Name: weekly_snapshot_holdings_weekly_snapshot_holding_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.weekly_snapshot_holdings_weekly_snapshot_holding_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.weekly_snapshot_holdings_weekly_snapshot_holding_id_seq OWNER TO postgres;

--
-- Name: weekly_snapshot_holdings_weekly_snapshot_holding_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.weekly_snapshot_holdings_weekly_snapshot_holding_id_seq OWNED BY public.weekly_snapshot_holdings.weekly_snapshot_holding_id;


--
-- Name: weekly_snapshots; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.weekly_snapshots (
    weekly_snapshot_id integer NOT NULL,
    user_id integer NOT NULL,
    reference_date date NOT NULL,
    source_snapshot_id integer NOT NULL,
    status character varying(20) NOT NULL,
    editable_until timestamp without time zone,
    created_at timestamp without time zone NOT NULL,
    CONSTRAINT chk_weekly_snapshot_status CHECK (((status)::text = ANY ((ARRAY['in_progress'::character varying, 'locked'::character varying])::text[])))
);


ALTER TABLE public.weekly_snapshots OWNER TO postgres;

--
-- Name: weekly_snapshots_weekly_snapshot_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.weekly_snapshots_weekly_snapshot_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.weekly_snapshots_weekly_snapshot_id_seq OWNER TO postgres;

--
-- Name: weekly_snapshots_weekly_snapshot_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.weekly_snapshots_weekly_snapshot_id_seq OWNED BY public.weekly_snapshots.weekly_snapshot_id;


--
-- Name: account_groups account_group_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_groups ALTER COLUMN account_group_id SET DEFAULT nextval('public.account_groups_account_group_id_seq'::regclass);


--
-- Name: accounts account_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts ALTER COLUMN account_id SET DEFAULT nextval('public.accounts_account_id_seq'::regclass);


--
-- Name: annual_snapshot_holdings annual_snapshot_holding_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.annual_snapshot_holdings ALTER COLUMN annual_snapshot_holding_id SET DEFAULT nextval('public.annual_snapshot_holdings_annual_snapshot_holding_id_seq'::regclass);


--
-- Name: annual_snapshots annual_snapshot_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.annual_snapshots ALTER COLUMN annual_snapshot_id SET DEFAULT nextval('public.annual_snapshots_annual_snapshot_id_seq'::regclass);


--
-- Name: holdings holding_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.holdings ALTER COLUMN holding_id SET DEFAULT nextval('public.holdings_holding_id_seq'::regclass);


--
-- Name: institutions institution_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.institutions ALTER COLUMN institution_id SET DEFAULT nextval('public.institutions_institution_id_seq'::regclass);


--
-- Name: products product_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products ALTER COLUMN product_id SET DEFAULT nextval('public.products_product_id_seq'::regclass);


--
-- Name: snapshot_holdings snapshot_holding_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.snapshot_holdings ALTER COLUMN snapshot_holding_id SET DEFAULT nextval('public.snapshot_holdings_snapshot_holding_id_seq'::regclass);


--
-- Name: snapshots snapshot_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.snapshots ALTER COLUMN snapshot_id SET DEFAULT nextval('public.snapshots_snapshot_id_seq'::regclass);


--
-- Name: target_allocation_accounts target_allocation_account_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.target_allocation_accounts ALTER COLUMN target_allocation_account_id SET DEFAULT nextval('public.target_allocation_accounts_target_allocation_account_id_seq'::regclass);


--
-- Name: target_allocation_totals target_allocation_total_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.target_allocation_totals ALTER COLUMN target_allocation_total_id SET DEFAULT nextval('public.target_allocation_totals_target_allocation_total_id_seq'::regclass);


--
-- Name: target_allocations target_allocation_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.target_allocations ALTER COLUMN target_allocation_id SET DEFAULT nextval('public.target_allocations_target_allocation_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: weekly_snapshot_holdings weekly_snapshot_holding_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.weekly_snapshot_holdings ALTER COLUMN weekly_snapshot_holding_id SET DEFAULT nextval('public.weekly_snapshot_holdings_weekly_snapshot_holding_id_seq'::regclass);


--
-- Name: weekly_snapshots weekly_snapshot_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.weekly_snapshots ALTER COLUMN weekly_snapshot_id SET DEFAULT nextval('public.weekly_snapshots_weekly_snapshot_id_seq'::regclass);


--
-- Data for Name: account_group_accounts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account_group_accounts (account_group_id, account_id, created_at) FROM stdin;
1	1	2026-03-07 06:45:51.211311
1	2	2026-03-07 06:45:51.211317
1	3	2026-03-07 06:45:51.211318
2	4	2026-03-07 06:46:10.571704
2	5	2026-03-07 06:46:10.571708
2	7	2026-03-07 06:46:10.571708
2	8	2026-03-07 06:46:10.571709
2	9	2026-03-07 06:46:10.57171
2	12	2026-03-07 06:46:10.57171
4	19	2026-03-07 06:49:35.01345
4	20	2026-03-07 06:49:35.013453
3	6	2026-03-07 06:49:42.066806
3	10	2026-03-07 06:49:42.06681
3	11	2026-03-07 06:49:42.066811
3	13	2026-03-07 06:49:42.066811
3	14	2026-03-07 06:49:42.066812
3	16	2026-03-07 06:49:42.066813
3	17	2026-03-07 06:49:42.066813
3	18	2026-03-07 06:49:42.066814
3	21	2026-03-07 06:49:42.066814
3	22	2026-03-07 06:49:42.066815
\.


--
-- Data for Name: account_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.account_groups (account_group_id, name, include_in_report, display_order, created_at) FROM stdin;
1	세금우대계좌	t	0	2026-03-07 06:45:44.392511
2	투자계좌	t	0	2026-03-07 06:46:10.570958
4	기타	t	0	2026-03-07 06:49:35.013013
3	예적금계좌	t	0	2026-03-07 06:47:03.285463
\.


--
-- Data for Name: accounts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts (account_id, institution_id, name, type, display_order, created_at) FROM stdin;
1	1	IRP	연금계좌	1	2026-03-07 06:36:15.999645
2	1	연금저축	연금계좌	2	2026-03-07 06:36:24.906288
3	1	ISA	ISA계좌	3	2026-03-07 06:36:41.372019
4	1	종합투자	위탁계좌	4	2026-03-07 06:36:54.065387
5	1	금현물	금현물계좌	5	2026-03-07 06:37:03.7267
6	1	CMA	CMA	6	2026-03-07 06:37:24.14998
7	2	고위험 미국 금융상품	위탁계좌	1	2026-03-07 06:37:53.313599
8	2	배당 미국 금융상품	위탁계좌	2	2026-03-07 06:38:02.220299
9	2	월적립	위탁계좌	3	2026-03-07 06:38:10.029483
10	2	CMA	CMA	4	2026-03-07 06:38:17.351439
11	3	CMA	CMA	1	2026-03-07 06:38:49.049363
12	4	국내주식	위탁계좌	1	2026-03-07 06:39:18.286574
13	5	예금	예금계좌	1	2026-03-07 06:42:03.609231
22	9	예금	예금계좌	1	2026-03-07 06:48:18.289189
14	6	예금	예금계좌	1	2026-03-07 06:42:18.868531
18	6	신한쏠편한적금	예금계좌	2	2026-03-07 06:43:23.070758
21	7	예금	예금계좌	1	2026-03-07 06:47:17.258179
17	8	예금	예금계좌	1	2026-03-07 06:42:58.626614
19	8	주택청약저축	예금계좌	2	2026-03-07 06:43:41.23424
16	10	예금	예금계좌	1	2026-03-07 06:42:42.545694
20	11	보증금	기타계좌	1	2026-03-07 06:44:00.018291
\.


--
-- Data for Name: annual_snapshot_holdings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.annual_snapshot_holdings (annual_snapshot_holding_id, annual_snapshot_id, holding_id, valuation_amount, data_source, created_at) FROM stdin;
\.


--
-- Data for Name: annual_snapshots; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.annual_snapshots (annual_snapshot_id, user_id, reference_date, source_snapshot_id, status, editable_until, created_at) FROM stdin;
\.


--
-- Data for Name: holdings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.holdings (holding_id, account_id, product_id, is_visible, deleted_at, deletion_reason, created_at) FROM stdin;
1	1	1	t	\N	\N	2026-03-07 07:21:40.006311
2	1	3	t	\N	\N	2026-03-07 07:21:56.756582
3	1	4	t	\N	\N	2026-03-07 07:22:20.630842
4	2	5	t	\N	\N	2026-03-07 07:22:33.889826
5	2	6	t	\N	\N	2026-03-07 07:22:50.799451
6	2	7	t	\N	\N	2026-03-07 07:22:59.512893
7	2	4	t	\N	\N	2026-03-07 07:23:09.651188
8	3	8	t	\N	\N	2026-03-07 07:23:18.854363
9	3	9	t	\N	\N	2026-03-07 07:23:24.959523
10	3	4	t	\N	\N	2026-03-07 07:23:38.23705
11	4	10	t	\N	\N	2026-03-07 07:24:03.569683
12	4	11	t	\N	\N	2026-03-07 07:24:09.881393
13	4	4	t	\N	\N	2026-03-07 07:24:17.670552
14	5	12	t	\N	\N	2026-03-07 07:24:32.767583
15	5	4	t	\N	\N	2026-03-07 07:24:38.643921
16	6	13	t	\N	\N	2026-03-07 07:24:54.114288
17	7	14	t	\N	\N	2026-03-07 07:25:04.382535
18	7	15	t	\N	\N	2026-03-07 07:25:11.219985
19	7	16	t	\N	\N	2026-03-07 07:25:16.447878
20	7	17	t	\N	\N	2026-03-07 07:25:23.046765
21	7	18	t	\N	\N	2026-03-07 07:25:28.405825
22	7	19	t	\N	\N	2026-03-07 07:25:36.940414
23	7	20	t	\N	\N	2026-03-07 07:25:42.559414
24	7	11	t	\N	\N	2026-03-07 07:25:48.299889
25	7	4	t	\N	\N	2026-03-07 07:25:56.39815
26	8	21	t	\N	\N	2026-03-07 07:26:13.676206
27	8	22	t	\N	\N	2026-03-07 07:26:18.4398
28	8	23	t	\N	\N	2026-03-07 07:26:24.021711
29	8	24	t	\N	\N	2026-03-07 07:26:29.59409
30	8	11	t	\N	\N	2026-03-07 07:26:35.426435
31	8	4	t	\N	\N	2026-03-07 07:26:41.988698
32	9	25	t	\N	\N	2026-03-07 07:26:48.280289
33	9	26	t	\N	\N	2026-03-07 07:26:54.239846
34	9	27	t	\N	\N	2026-03-07 07:27:04.237552
35	9	28	t	\N	\N	2026-03-07 07:27:11.876412
36	9	11	t	\N	\N	2026-03-07 07:27:20.726275
37	9	4	t	\N	\N	2026-03-07 07:27:27.946017
38	10	13	t	\N	\N	2026-03-07 07:27:38.147413
39	11	29	t	\N	\N	2026-03-07 07:27:51.209281
40	12	31	t	\N	\N	2026-03-07 07:28:59.098645
41	12	32	t	\N	\N	2026-03-07 07:29:07.465319
42	12	4	t	\N	\N	2026-03-07 07:29:12.417749
43	13	4	t	\N	\N	2026-03-07 07:29:25.135077
44	14	4	t	\N	\N	2026-03-07 07:29:34.296066
45	18	4	t	\N	\N	2026-03-07 07:29:43.534085
46	21	4	t	\N	\N	2026-03-07 07:29:49.844128
47	17	4	t	\N	\N	2026-03-07 07:29:57.096042
48	19	33	t	\N	\N	2026-03-07 07:31:02.767414
49	22	4	t	\N	\N	2026-03-07 07:31:19.845163
50	16	4	t	\N	\N	2026-03-07 07:31:28.835419
51	20	30	t	\N	\N	2026-03-07 07:31:38.558745
52	1	2	t	\N	\N	2026-03-07 07:56:18.945209
53	2	2	t	\N	\N	2026-03-07 07:56:26.159493
54	3	2	t	\N	\N	2026-03-07 07:56:34.004972
55	4	2	t	\N	\N	2026-03-07 07:56:48.927063
56	5	2	t	\N	\N	2026-03-07 07:56:56.14511
57	7	2	t	\N	\N	2026-03-07 07:57:11.867416
58	8	2	t	\N	\N	2026-03-07 07:57:17.173001
59	9	2	t	\N	\N	2026-03-07 07:57:26.98627
60	12	2	t	\N	\N	2026-03-07 07:57:43.709588
\.


--
-- Data for Name: institutions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.institutions (institution_id, name, type, display_order, created_at) FROM stdin;
1	한국투자증권	증권사	1	2026-03-07 06:26:17.738763
2	미래에셋증권	증권사	2	2026-03-07 06:28:11.087919
3	우리투자증권	증권사	3	2026-03-07 06:28:52.926806
4	토스증권	증권사	4	2026-03-07 06:28:59.823461
5	기업은행	은행	5	2026-03-07 06:29:11.391007
6	신한은행	은행	6	2026-03-07 06:29:21.85474
7	우리은행	은행	7	2026-03-07 06:29:34.830293
8	하나은행	은행	8	2026-03-07 06:30:18.683815
9	토스뱅크	은행	9	2026-03-07 06:30:39.324194
10	새마을금고	기타기관	10	2026-03-07 06:30:49.781333
11	기관아님	기타기관	11	2026-03-07 06:32:35.351069
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.products (product_id, product_name, asset_class, region, currency, investment_type, characteristics, risk_level, allow_snapshot_input, display_order, created_at) FROM stdin;
5	ACE 미국빅테크 TOP7 Plus	주식	미국	KRW	ETF	\N	위험	t	3	2026-03-07 07:08:37.779457
6	KODEX iShares 미국하이일드액티브	채권	미국	KRW	ETF	\N	안전	t	4	2026-03-07 07:08:56.923919
7	SOL 미국AI소프트웨어	주식	미국	KRW	ETF	\N	위험	t	5	2026-03-07 07:09:20.747259
8	ACE 미국빅테크 TOP7 Plus 레버리지	주식	미국	KRW	ETF	\N	위험	t	6	2026-03-07 07:10:09.343713
9	ACE KRX 금현물	주식	대한민국	KRW	ETF	\N	안전	t	7	2026-03-07 07:10:42.183999
10	VOO	주식	미국	USD	직접	\N	위험	t	8	2026-03-07 07:11:31.634923
12	금	금	대한민국	KRW	직접	\N	안전	t	9	2026-03-07 07:12:44.053143
14	FNGU	주식	미국	USD	ETF	\N	위험	t	10	2026-03-07 07:13:49.795957
15	NVDU	주식	미국	USD	ETF	\N	위험	t	11	2026-03-07 07:14:07.427538
16	FNGO	주식	미국	USD	ETF	\N	위험	t	12	2026-03-07 07:14:22.108924
17	QLD	주식	미국	USD	ETF	\N	위험	t	13	2026-03-07 07:14:36.002874
18	USHY	채권	미국	USD	ETF	\N	안전	t	14	2026-03-07 07:14:53.094921
19	SGOV	통화	미국	USD	ETF	\N	안전	t	15	2026-03-07 07:15:12.535175
20	UUUU	주식	미국	USD	직접	\N	위험	t	16	2026-03-07 07:16:17.123924
21	O	부동산	미국	USD	ETF	\N	안전	t	17	2026-03-07 07:16:43.718406
22	DGRW	주식	미국	USD	ETF	\N	위험	t	18	2026-03-07 07:16:57.407463
23	TLT	채권	미국	USD	ETF	\N	안전	t	19	2026-03-07 07:17:09.853506
24	BITO	가상자산	미국	USD	ETF	\N	위험	t	20	2026-03-07 07:17:23.124308
25	아마존	주식	미국	USD	직접	{소수점투자}	위험	t	21	2026-03-07 07:18:05.588085
26	알파벳 A	주식	미국	USD	직접	{소주점투자}	위험	t	22	2026-03-07 07:18:22.01694
27	마이크로소프트	주식	미국	USD	직접	{소수점투자}	위험	t	23	2026-03-07 07:18:42.705279
28	엔비디아	주식	미국	USD	직접	{소수점투자}	위험	t	24	2026-03-07 07:18:58.948855
31	아이스크림에듀	주식	대한민국	KRW	직접	\N	위험	t	25	2026-03-07 07:28:23.586739
32	명신산업	주식	대한민국	KRW	직접	\N	위험	t	26	2026-03-07 07:28:34.433574
33	청약저축	부동산	대한민국	KRW	직접	\N	안전	t	27	2026-03-07 07:30:42.11388
11	달러	통화	미국	USD	직접	\N	안전	t	28	2026-03-07 07:11:49.727338
1	TIGER 미국테크TOP10 INDXX	주식	미국	KRW	ETF	\N	위험	t	1	2026-03-07 04:26:18.078291
13	발행어음	통화	대한민국	KRW	직접	\N	안전	t	29	2026-03-07 07:13:14.228028
29	RP	통화	대한민국	KRW	직접	\N	안전	t	30	2026-03-07 07:20:23.471946
4	현금	통화	대한민국	KRW	직접	\N	안전	t	31	2026-03-07 07:08:11.720914
30	월세보증금	부동산	대한민국	KRW	직접	\N	안전	t	32	2026-03-07 07:20:48.084582
2	평가금액 보정	기타자산	대한민국	KRW	직접	{보정}	안전	f	33	2026-03-07 04:26:25.178218
3	ACE 엔비디아채권혼합블룸버그	채권	미국	KRW	ETF	\N	안전	t	2	2026-03-07 07:07:48.89984
\.


--
-- Data for Name: snapshot_holdings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.snapshot_holdings (snapshot_holding_id, snapshot_id, holding_id, valuation_amount, data_source, created_at) FROM stdin;
1	7	1	81538000.0000	manual	2026-03-07 07:58:53.246553
5	7	3	7476.0000	manual	2026-03-07 07:58:53.254014
2	7	2	35170860.0000	manual	2026-03-07 07:58:53.254413
3	7	4	384715420.0000	manual	2026-03-07 07:58:53.260216
4	7	5	45819400.0000	manual	2026-03-07 07:58:53.259913
6	7	7	261054.0000	manual	2026-03-07 07:58:53.265625
7	7	8	54448800.0000	manual	2026-03-07 07:58:53.273175
9	7	9	16915000.0000	manual	2026-03-07 07:58:53.273941
10	7	10	13764.0000	manual	2026-03-07 07:58:53.280916
11	7	11	79689900.0000	manual	2026-03-07 07:58:53.282106
12	7	12	196268.0000	manual	2026-03-07 07:58:53.284372
8	7	6	37924150.0000	manual	2026-03-07 07:58:53.286913
13	7	13	0.0000	manual	2026-03-07 07:58:53.292194
14	7	14	43997525.0000	manual	2026-03-07 07:58:53.29397
15	7	15	11765.0000	manual	2026-03-07 07:58:53.302779
17	7	17	75447999.0000	manual	2026-03-07 07:58:53.303254
16	7	16	9475410.0000	manual	2026-03-07 07:58:53.303928
19	7	19	0.0000	manual	2026-03-07 07:58:53.310766
20	7	20	33535018.0000	manual	2026-03-07 07:58:53.312991
18	7	18	47391659.0000	manual	2026-03-07 07:58:53.313289
21	7	21	23084455.0000	manual	2026-03-07 07:58:53.319505
23	7	22	0.0000	manual	2026-03-07 07:58:53.325774
22	7	23	5545260.0000	manual	2026-03-07 07:58:53.326692
24	7	24	128025.0000	manual	2026-03-07 07:58:53.334795
26	7	26	3997539.0000	manual	2026-03-07 07:58:53.335176
25	7	25	69655.0000	manual	2026-03-07 07:58:53.336233
27	7	27	5567649.0000	manual	2026-03-07 07:58:53.341343
28	7	28	5440343.0000	manual	2026-03-07 07:58:53.349431
29	7	29	577491.0000	manual	2026-03-07 07:58:53.350815
30	7	30	35558.0000	manual	2026-03-07 07:58:53.356198
32	7	32	212480.0000	manual	2026-03-07 07:58:53.359827
31	7	31	14534.0000	manual	2026-03-07 07:58:53.362054
33	7	33	358981.0000	manual	2026-03-07 07:58:53.364997
34	7	34	205992.0000	manual	2026-03-07 07:58:53.371366
35	7	35	297620.0000	manual	2026-03-07 07:58:53.372541
37	7	37	47612.0000	manual	2026-03-07 07:58:53.378802
36	7	36	0.0000	manual	2026-03-07 07:58:53.379281
38	7	38	1422138.0000	manual	2026-03-07 07:58:53.384105
39	7	39	20909032.0000	manual	2026-03-07 07:58:53.386675
40	7	40	20124.0000	manual	2026-03-07 07:58:53.394925
41	7	41	18340.0000	manual	2026-03-07 07:58:53.396483
42	7	42	133.0000	manual	2026-03-07 07:58:53.398593
43	7	43	2933513.0000	manual	2026-03-07 07:58:53.402305
44	7	44	134294.0000	manual	2026-03-07 07:58:53.407766
46	7	46	196354.0000	manual	2026-03-07 07:58:53.410814
45	7	47	99056.0000	manual	2026-03-07 07:58:53.420504
48	7	49	12432.0000	manual	2026-03-07 07:58:53.420971
47	7	48	18500000.0000	manual	2026-03-07 07:58:53.421251
49	7	50	400606.0000	manual	2026-03-07 07:58:53.424706
50	7	51	0.0000	manual	2026-03-07 07:58:53.427418
\.


--
-- Data for Name: snapshots; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.snapshots (snapshot_id, user_id, reference_date, status, locked_at, editable_until, created_at) FROM stdin;
7	1	2026-03-07	locked	2026-03-07 07:59:48.034275	\N	2026-03-07 07:50:16.023909
\.


--
-- Data for Name: target_allocation_accounts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.target_allocation_accounts (target_allocation_account_id, year, account_id, target_amount, created_at, updated_at) FROM stdin;
1	2026	1	140000000.00	2026-03-07 07:35:30.949534	2026-03-07 07:59:06.04058
2	2026	2	570000000.00	2026-03-07 07:35:30.966177	2026-03-07 07:59:06.041068
5	2026	4	120000000.00	2026-03-07 07:35:30.974214	2026-03-07 07:59:06.048066
4	2026	5	60000000.00	2026-03-07 07:35:30.972865	2026-03-07 07:59:06.048829
3	2026	3	90000000.00	2026-03-07 07:35:30.97022	2026-03-07 07:59:06.049176
7	2026	7	280000000.00	2026-03-07 07:35:30.982142	2026-03-07 07:59:06.060188
8	2026	8	16000000.00	2026-03-07 07:35:30.986163	2026-03-07 07:59:06.063777
6	2026	6	0.00	2026-03-07 07:35:30.980229	2026-03-07 07:59:06.063122
9	2026	9	1000000.00	2026-03-07 07:35:30.98682	2026-03-07 07:59:06.067505
10	2026	10	0.00	2026-03-07 07:35:30.993505	2026-03-07 07:59:06.069699
11	2026	11	10000000.00	2026-03-07 07:35:30.994275	2026-03-07 07:59:06.071305
12	2026	12	0.00	2026-03-07 07:35:30.997487	2026-03-07 07:59:06.078344
13	2026	13	1000000.00	2026-03-07 07:35:30.998035	2026-03-07 07:59:06.081026
14	2026	14	0.00	2026-03-07 07:35:31.002981	2026-03-07 07:59:06.086064
15	2026	16	0.00	2026-03-07 07:35:31.00454	2026-03-07 07:59:06.086598
17	2026	18	0.00	2026-03-07 07:35:31.010741	2026-03-07 07:59:06.092081
16	2026	17	0.00	2026-03-07 07:35:31.010302	2026-03-07 07:59:06.092533
18	2026	19	19000000.00	2026-03-07 07:35:31.015019	2026-03-07 07:59:06.093842
19	2026	20	20000000.00	2026-03-07 07:35:31.01873	2026-03-07 07:59:06.102698
20	2026	21	0.00	2026-03-07 07:35:31.02037	2026-03-07 07:59:06.106956
21	2026	22	0.00	2026-03-07 07:35:31.022228	2026-03-07 07:59:06.107824
\.


--
-- Data for Name: target_allocation_totals; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.target_allocation_totals (target_allocation_total_id, year, target_amount, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: target_allocations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.target_allocations (target_allocation_id, year, account_group_id, target_amount, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, email, full_name, created_at) FROM stdin;
1	admin	admin@test.com	admin	2026-03-07 07:50:08.615987
\.


--
-- Data for Name: weekly_snapshot_holdings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.weekly_snapshot_holdings (weekly_snapshot_holding_id, weekly_snapshot_id, holding_id, valuation_amount, data_source, created_at) FROM stdin;
1	1	1	81538000.0000	manual	2026-03-07 07:59:56.749208
2	1	3	7476.0000	manual	2026-03-07 07:59:56.749208
3	1	2	35170860.0000	manual	2026-03-07 07:59:56.749208
4	1	4	384715420.0000	manual	2026-03-07 07:59:56.749208
5	1	5	45819400.0000	manual	2026-03-07 07:59:56.749208
6	1	7	261054.0000	manual	2026-03-07 07:59:56.749208
7	1	8	54448800.0000	manual	2026-03-07 07:59:56.749208
8	1	9	16915000.0000	manual	2026-03-07 07:59:56.749208
9	1	10	13764.0000	manual	2026-03-07 07:59:56.749208
10	1	11	79689900.0000	manual	2026-03-07 07:59:56.749208
11	1	12	196268.0000	manual	2026-03-07 07:59:56.749208
12	1	6	37924150.0000	manual	2026-03-07 07:59:56.749208
13	1	13	0.0000	manual	2026-03-07 07:59:56.749208
14	1	14	43997525.0000	manual	2026-03-07 07:59:56.749208
15	1	15	11765.0000	manual	2026-03-07 07:59:56.749208
16	1	17	75447999.0000	manual	2026-03-07 07:59:56.749208
17	1	16	9475410.0000	manual	2026-03-07 07:59:56.749208
18	1	19	0.0000	manual	2026-03-07 07:59:56.749208
19	1	20	33535018.0000	manual	2026-03-07 07:59:56.749208
20	1	18	47391659.0000	manual	2026-03-07 07:59:56.749208
21	1	21	23084455.0000	manual	2026-03-07 07:59:56.749208
22	1	22	0.0000	manual	2026-03-07 07:59:56.749208
23	1	23	5545260.0000	manual	2026-03-07 07:59:56.749208
24	1	24	128025.0000	manual	2026-03-07 07:59:56.749208
25	1	26	3997539.0000	manual	2026-03-07 07:59:56.749208
26	1	25	69655.0000	manual	2026-03-07 07:59:56.749208
27	1	27	5567649.0000	manual	2026-03-07 07:59:56.749208
28	1	28	5440343.0000	manual	2026-03-07 07:59:56.749208
29	1	29	577491.0000	manual	2026-03-07 07:59:56.749208
30	1	30	35558.0000	manual	2026-03-07 07:59:56.749208
31	1	32	212480.0000	manual	2026-03-07 07:59:56.749208
32	1	31	14534.0000	manual	2026-03-07 07:59:56.749208
33	1	33	358981.0000	manual	2026-03-07 07:59:56.749208
34	1	34	205992.0000	manual	2026-03-07 07:59:56.749208
35	1	35	297620.0000	manual	2026-03-07 07:59:56.749208
36	1	37	47612.0000	manual	2026-03-07 07:59:56.749208
37	1	36	0.0000	manual	2026-03-07 07:59:56.749208
38	1	38	1422138.0000	manual	2026-03-07 07:59:56.749208
39	1	39	20909032.0000	manual	2026-03-07 07:59:56.749208
40	1	40	20124.0000	manual	2026-03-07 07:59:56.749208
41	1	41	18340.0000	manual	2026-03-07 07:59:56.749208
42	1	42	133.0000	manual	2026-03-07 07:59:56.749208
43	1	43	2933513.0000	manual	2026-03-07 07:59:56.749208
44	1	44	134294.0000	manual	2026-03-07 07:59:56.749208
45	1	46	196354.0000	manual	2026-03-07 07:59:56.749208
46	1	47	99056.0000	manual	2026-03-07 07:59:56.749208
47	1	49	12432.0000	manual	2026-03-07 07:59:56.749208
48	1	48	18500000.0000	manual	2026-03-07 07:59:56.749208
49	1	50	400606.0000	manual	2026-03-07 07:59:56.749208
50	1	51	0.0000	manual	2026-03-07 07:59:56.749208
\.


--
-- Data for Name: weekly_snapshots; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.weekly_snapshots (weekly_snapshot_id, user_id, reference_date, source_snapshot_id, status, editable_until, created_at) FROM stdin;
1	1	2026-03-07	7	in_progress	2026-03-14 00:00:00	2026-03-07 07:59:56.748099
\.


--
-- Name: account_groups_account_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.account_groups_account_group_id_seq', 4, true);


--
-- Name: accounts_account_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_account_id_seq', 22, true);


--
-- Name: annual_snapshot_holdings_annual_snapshot_holding_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.annual_snapshot_holdings_annual_snapshot_holding_id_seq', 1, false);


--
-- Name: annual_snapshots_annual_snapshot_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.annual_snapshots_annual_snapshot_id_seq', 1, false);


--
-- Name: holdings_holding_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.holdings_holding_id_seq', 60, true);


--
-- Name: institutions_institution_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.institutions_institution_id_seq', 11, true);


--
-- Name: products_product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.products_product_id_seq', 33, true);


--
-- Name: snapshot_holdings_snapshot_holding_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.snapshot_holdings_snapshot_holding_id_seq', 100, true);


--
-- Name: snapshots_snapshot_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.snapshots_snapshot_id_seq', 7, true);


--
-- Name: target_allocation_accounts_target_allocation_account_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.target_allocation_accounts_target_allocation_account_id_seq', 21, true);


--
-- Name: target_allocation_totals_target_allocation_total_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.target_allocation_totals_target_allocation_total_id_seq', 1, false);


--
-- Name: target_allocations_target_allocation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.target_allocations_target_allocation_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);


--
-- Name: weekly_snapshot_holdings_weekly_snapshot_holding_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.weekly_snapshot_holdings_weekly_snapshot_holding_id_seq', 50, true);


--
-- Name: weekly_snapshots_weekly_snapshot_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.weekly_snapshots_weekly_snapshot_id_seq', 1, true);


--
-- Name: account_group_accounts account_group_accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_group_accounts
    ADD CONSTRAINT account_group_accounts_pkey PRIMARY KEY (account_group_id, account_id);


--
-- Name: account_groups account_groups_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_groups
    ADD CONSTRAINT account_groups_name_key UNIQUE (name);


--
-- Name: account_groups account_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_groups
    ADD CONSTRAINT account_groups_pkey PRIMARY KEY (account_group_id);


--
-- Name: accounts accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_pkey PRIMARY KEY (account_id);


--
-- Name: annual_snapshot_holdings annual_snapshot_holdings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.annual_snapshot_holdings
    ADD CONSTRAINT annual_snapshot_holdings_pkey PRIMARY KEY (annual_snapshot_holding_id);


--
-- Name: annual_snapshots annual_snapshots_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.annual_snapshots
    ADD CONSTRAINT annual_snapshots_pkey PRIMARY KEY (annual_snapshot_id);


--
-- Name: holdings holdings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.holdings
    ADD CONSTRAINT holdings_pkey PRIMARY KEY (holding_id);


--
-- Name: institutions institutions_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.institutions
    ADD CONSTRAINT institutions_name_key UNIQUE (name);


--
-- Name: institutions institutions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.institutions
    ADD CONSTRAINT institutions_pkey PRIMARY KEY (institution_id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (product_id);


--
-- Name: snapshot_holdings snapshot_holdings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.snapshot_holdings
    ADD CONSTRAINT snapshot_holdings_pkey PRIMARY KEY (snapshot_holding_id);


--
-- Name: snapshots snapshots_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.snapshots
    ADD CONSTRAINT snapshots_pkey PRIMARY KEY (snapshot_id);


--
-- Name: target_allocation_accounts target_allocation_accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.target_allocation_accounts
    ADD CONSTRAINT target_allocation_accounts_pkey PRIMARY KEY (target_allocation_account_id);


--
-- Name: target_allocation_totals target_allocation_totals_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.target_allocation_totals
    ADD CONSTRAINT target_allocation_totals_pkey PRIMARY KEY (target_allocation_total_id);


--
-- Name: target_allocation_totals target_allocation_totals_year_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.target_allocation_totals
    ADD CONSTRAINT target_allocation_totals_year_key UNIQUE (year);


--
-- Name: target_allocations target_allocations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.target_allocations
    ADD CONSTRAINT target_allocations_pkey PRIMARY KEY (target_allocation_id);


--
-- Name: accounts uq_account_name_per_institution; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT uq_account_name_per_institution UNIQUE (institution_id, name);


--
-- Name: annual_snapshot_holdings uq_annual_snapshot_holding; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.annual_snapshot_holdings
    ADD CONSTRAINT uq_annual_snapshot_holding UNIQUE (annual_snapshot_id, holding_id);


--
-- Name: annual_snapshots uq_annual_snapshot_user_reference; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.annual_snapshots
    ADD CONSTRAINT uq_annual_snapshot_user_reference UNIQUE (user_id, reference_date);


--
-- Name: holdings uq_holding_account_product; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.holdings
    ADD CONSTRAINT uq_holding_account_product UNIQUE (account_id, product_id);


--
-- Name: products uq_product_identity; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT uq_product_identity UNIQUE (product_name, asset_class, region, currency, investment_type);


--
-- Name: snapshot_holdings uq_snapshot_holding; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.snapshot_holdings
    ADD CONSTRAINT uq_snapshot_holding UNIQUE (snapshot_id, holding_id);


--
-- Name: snapshots uq_snapshot_user_reference; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.snapshots
    ADD CONSTRAINT uq_snapshot_user_reference UNIQUE (user_id, reference_date);


--
-- Name: target_allocation_accounts uq_target_allocation_account_year_account; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.target_allocation_accounts
    ADD CONSTRAINT uq_target_allocation_account_year_account UNIQUE (year, account_id);


--
-- Name: target_allocations uq_target_allocation_year_group; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.target_allocations
    ADD CONSTRAINT uq_target_allocation_year_group UNIQUE (year, account_group_id);


--
-- Name: weekly_snapshot_holdings uq_weekly_snapshot_holding; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.weekly_snapshot_holdings
    ADD CONSTRAINT uq_weekly_snapshot_holding UNIQUE (weekly_snapshot_id, holding_id);


--
-- Name: weekly_snapshots uq_weekly_snapshot_user_reference; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.weekly_snapshots
    ADD CONSTRAINT uq_weekly_snapshot_user_reference UNIQUE (user_id, reference_date);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: weekly_snapshot_holdings weekly_snapshot_holdings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.weekly_snapshot_holdings
    ADD CONSTRAINT weekly_snapshot_holdings_pkey PRIMARY KEY (weekly_snapshot_holding_id);


--
-- Name: weekly_snapshots weekly_snapshots_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.weekly_snapshots
    ADD CONSTRAINT weekly_snapshots_pkey PRIMARY KEY (weekly_snapshot_id);


--
-- Name: idx_account_group_accounts_account; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_account_group_accounts_account ON public.account_group_accounts USING btree (account_id);


--
-- Name: idx_accounts_institution; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_accounts_institution ON public.accounts USING btree (institution_id);


--
-- Name: idx_annual_snapshot_holdings_snap; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_annual_snapshot_holdings_snap ON public.annual_snapshot_holdings USING btree (annual_snapshot_id);


--
-- Name: idx_annual_snapshots_user; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_annual_snapshots_user ON public.annual_snapshots USING btree (user_id);


--
-- Name: idx_holdings_account; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_holdings_account ON public.holdings USING btree (account_id);


--
-- Name: idx_holdings_product; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_holdings_product ON public.holdings USING btree (product_id);


--
-- Name: idx_snapshot_holdings_holding; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_snapshot_holdings_holding ON public.snapshot_holdings USING btree (holding_id);


--
-- Name: idx_snapshot_holdings_snapshot; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_snapshot_holdings_snapshot ON public.snapshot_holdings USING btree (snapshot_id);


--
-- Name: idx_snapshots_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_snapshots_status ON public.snapshots USING btree (status);


--
-- Name: idx_snapshots_user; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_snapshots_user ON public.snapshots USING btree (user_id);


--
-- Name: idx_target_allocation_accounts_account; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_target_allocation_accounts_account ON public.target_allocation_accounts USING btree (account_id);


--
-- Name: idx_target_allocation_accounts_year; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_target_allocation_accounts_year ON public.target_allocation_accounts USING btree (year);


--
-- Name: idx_target_allocation_totals_year; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_target_allocation_totals_year ON public.target_allocation_totals USING btree (year);


--
-- Name: idx_target_allocations_account_group; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_target_allocations_account_group ON public.target_allocations USING btree (account_group_id);


--
-- Name: idx_target_allocations_year; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_target_allocations_year ON public.target_allocations USING btree (year);


--
-- Name: idx_weekly_snapshot_holdings_snap; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_weekly_snapshot_holdings_snap ON public.weekly_snapshot_holdings USING btree (weekly_snapshot_id);


--
-- Name: idx_weekly_snapshots_user; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_weekly_snapshots_user ON public.weekly_snapshots USING btree (user_id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);


--
-- Name: account_group_accounts account_group_accounts_account_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_group_accounts
    ADD CONSTRAINT account_group_accounts_account_group_id_fkey FOREIGN KEY (account_group_id) REFERENCES public.account_groups(account_group_id) ON DELETE CASCADE;


--
-- Name: account_group_accounts account_group_accounts_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.account_group_accounts
    ADD CONSTRAINT account_group_accounts_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.accounts(account_id) ON DELETE CASCADE;


--
-- Name: accounts accounts_institution_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_institution_id_fkey FOREIGN KEY (institution_id) REFERENCES public.institutions(institution_id) ON DELETE CASCADE;


--
-- Name: annual_snapshot_holdings annual_snapshot_holdings_annual_snapshot_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.annual_snapshot_holdings
    ADD CONSTRAINT annual_snapshot_holdings_annual_snapshot_id_fkey FOREIGN KEY (annual_snapshot_id) REFERENCES public.annual_snapshots(annual_snapshot_id) ON DELETE CASCADE;


--
-- Name: annual_snapshot_holdings annual_snapshot_holdings_holding_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.annual_snapshot_holdings
    ADD CONSTRAINT annual_snapshot_holdings_holding_id_fkey FOREIGN KEY (holding_id) REFERENCES public.holdings(holding_id) ON DELETE CASCADE;


--
-- Name: annual_snapshots annual_snapshots_source_snapshot_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.annual_snapshots
    ADD CONSTRAINT annual_snapshots_source_snapshot_id_fkey FOREIGN KEY (source_snapshot_id) REFERENCES public.snapshots(snapshot_id) ON DELETE CASCADE;


--
-- Name: annual_snapshots annual_snapshots_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.annual_snapshots
    ADD CONSTRAINT annual_snapshots_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: holdings holdings_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.holdings
    ADD CONSTRAINT holdings_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.accounts(account_id) ON DELETE CASCADE;


--
-- Name: holdings holdings_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.holdings
    ADD CONSTRAINT holdings_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(product_id) ON DELETE CASCADE;


--
-- Name: snapshot_holdings snapshot_holdings_holding_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.snapshot_holdings
    ADD CONSTRAINT snapshot_holdings_holding_id_fkey FOREIGN KEY (holding_id) REFERENCES public.holdings(holding_id) ON DELETE CASCADE;


--
-- Name: snapshot_holdings snapshot_holdings_snapshot_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.snapshot_holdings
    ADD CONSTRAINT snapshot_holdings_snapshot_id_fkey FOREIGN KEY (snapshot_id) REFERENCES public.snapshots(snapshot_id) ON DELETE CASCADE;


--
-- Name: snapshots snapshots_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.snapshots
    ADD CONSTRAINT snapshots_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: target_allocation_accounts target_allocation_accounts_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.target_allocation_accounts
    ADD CONSTRAINT target_allocation_accounts_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.accounts(account_id) ON DELETE CASCADE;


--
-- Name: target_allocations target_allocations_account_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.target_allocations
    ADD CONSTRAINT target_allocations_account_group_id_fkey FOREIGN KEY (account_group_id) REFERENCES public.account_groups(account_group_id) ON DELETE CASCADE;


--
-- Name: weekly_snapshot_holdings weekly_snapshot_holdings_holding_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.weekly_snapshot_holdings
    ADD CONSTRAINT weekly_snapshot_holdings_holding_id_fkey FOREIGN KEY (holding_id) REFERENCES public.holdings(holding_id) ON DELETE CASCADE;


--
-- Name: weekly_snapshot_holdings weekly_snapshot_holdings_weekly_snapshot_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.weekly_snapshot_holdings
    ADD CONSTRAINT weekly_snapshot_holdings_weekly_snapshot_id_fkey FOREIGN KEY (weekly_snapshot_id) REFERENCES public.weekly_snapshots(weekly_snapshot_id) ON DELETE CASCADE;


--
-- Name: weekly_snapshots weekly_snapshots_source_snapshot_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.weekly_snapshots
    ADD CONSTRAINT weekly_snapshots_source_snapshot_id_fkey FOREIGN KEY (source_snapshot_id) REFERENCES public.snapshots(snapshot_id) ON DELETE CASCADE;


--
-- Name: weekly_snapshots weekly_snapshots_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.weekly_snapshots
    ADD CONSTRAINT weekly_snapshots_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict KOnq45ap4lixrxLwidlZqxyVbbCfSPwcWfECwEDmvgIwfhRtj5CxjsQMfFq1X1D

