--
-- PostgreSQL database dump
--

\restrict 6mZHKf6oKaKfXz3TYhmhfdVlM4gIrsdu17B4zWbuft3PlOitfosd9yTyDZ9BS0N

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
ALTER TABLE IF EXISTS ONLY public.target_allocation_asset_classes DROP CONSTRAINT IF EXISTS target_allocation_asset_classes_pkey;
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
ALTER TABLE IF EXISTS public.target_allocation_asset_classes ALTER COLUMN target_allocation_asset_class_id DROP DEFAULT;
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
DROP SEQUENCE IF EXISTS public.target_allocation_asset_class_target_allocation_asset_class_seq;
DROP TABLE IF EXISTS public.target_allocation_asset_classes;
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
    CONSTRAINT chk_annual_snapshot_data_source CHECK (((data_source)::text = ANY (ARRAY[('auto'::character varying)::text, ('manual'::character varying)::text, ('missing'::character varying)::text])))
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
    CONSTRAINT chk_institution_type CHECK (((type)::text = ANY (ARRAY[('증권사'::character varying)::text, ('은행'::character varying)::text, ('기타기관'::character varying)::text])))
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
    CONSTRAINT chk_product_asset_class CHECK (((asset_class)::text = ANY (ARRAY[('주식'::character varying)::text, ('채권'::character varying)::text, ('통화'::character varying)::text, ('금'::character varying)::text, ('부동산'::character varying)::text, ('가상자산'::character varying)::text, ('기타자산'::character varying)::text]))),
    CONSTRAINT chk_product_currency CHECK (((currency)::text = ANY (ARRAY[('KRW'::character varying)::text, ('USD'::character varying)::text]))),
    CONSTRAINT chk_product_investment_type CHECK (((investment_type)::text = ANY (ARRAY[('직접'::character varying)::text, ('ETF'::character varying)::text]))),
    CONSTRAINT chk_product_region CHECK (((region)::text = ANY (ARRAY[('대한민국'::character varying)::text, ('미국'::character varying)::text]))),
    CONSTRAINT chk_product_risk_level CHECK (((risk_level)::text = ANY (ARRAY[('안전'::character varying)::text, ('위험'::character varying)::text])))
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
    CONSTRAINT chk_snapshot_data_source CHECK (((data_source)::text = ANY (ARRAY[('auto'::character varying)::text, ('manual'::character varying)::text, ('missing'::character varying)::text])))
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
    CONSTRAINT chk_snapshot_status CHECK (((status)::text = ANY (ARRAY[('in_progress'::character varying)::text, ('locked'::character varying)::text])))
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
-- Name: target_allocation_asset_classes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.target_allocation_asset_classes (
    target_allocation_asset_class_id integer NOT NULL,
    year integer NOT NULL,
    asset_class character varying(100) NOT NULL,
    target_percentage numeric(5,2) NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.target_allocation_asset_classes OWNER TO postgres;

--
-- Name: target_allocation_asset_class_target_allocation_asset_class_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.target_allocation_asset_class_target_allocation_asset_class_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.target_allocation_asset_class_target_allocation_asset_class_seq OWNER TO postgres;

--
-- Name: target_allocation_asset_class_target_allocation_asset_class_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.target_allocation_asset_class_target_allocation_asset_class_seq OWNED BY public.target_allocation_asset_classes.target_allocation_asset_class_id;


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
    CONSTRAINT chk_weekly_snapshot_data_source CHECK (((data_source)::text = ANY (ARRAY[('auto'::character varying)::text, ('manual'::character varying)::text, ('missing'::character varying)::text])))
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
    CONSTRAINT chk_weekly_snapshot_status CHECK (((status)::text = ANY (ARRAY[('in_progress'::character varying)::text, ('locked'::character varying)::text])))
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
-- Name: target_allocation_asset_classes target_allocation_asset_class_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.target_allocation_asset_classes ALTER COLUMN target_allocation_asset_class_id SET DEFAULT nextval('public.target_allocation_asset_class_target_allocation_asset_class_seq'::regclass);


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
1	세금우대계좌	t	1	2026-03-07 06:45:44.392511
2	투자계좌	t	2	2026-03-07 06:46:10.570958
3	예적금계좌	t	3	2026-03-07 06:47:03.285463
4	기타	t	4	2026-03-07 06:49:35.013013
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
23	7	정기예금	예금계좌	2	2026-03-07 15:38:31.119826
\.


--
-- Data for Name: annual_snapshot_holdings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.annual_snapshot_holdings (annual_snapshot_holding_id, annual_snapshot_id, holding_id, valuation_amount, data_source, created_at) FROM stdin;
1	1	52	7730892.0000	auto	2026-03-07 15:15:48.914086
2	1	53	22055739.0000	auto	2026-03-07 15:15:48.914086
3	1	54	13401530.0000	auto	2026-03-07 15:15:48.914086
4	1	60	25293088.0000	auto	2026-03-07 15:15:48.914086
5	1	55	83891706.0000	auto	2026-03-07 15:15:48.914086
6	1	57	18297741.0000	auto	2026-03-07 15:15:48.914086
7	1	58	105020.0000	auto	2026-03-07 15:15:48.914086
8	1	16	94517.0000	auto	2026-03-07 15:15:48.914086
9	1	38	1504782.0000	auto	2026-03-07 15:15:48.914086
10	1	39	500000.0000	auto	2026-03-07 15:15:48.914086
11	1	43	10779760.0000	auto	2026-03-07 15:15:48.914086
12	1	44	1500344.0000	auto	2026-03-07 15:15:48.914086
13	1	51	20000000.0000	auto	2026-03-07 15:15:48.914086
14	1	48	13900000.0000	auto	2026-03-07 15:15:48.914086
15	2	52	7678606.0000	auto	2026-03-07 15:15:49.819734
16	2	53	26426764.0000	auto	2026-03-07 15:15:49.819734
17	2	54	23779137.0000	auto	2026-03-07 15:15:49.819734
18	2	60	28866624.0000	auto	2026-03-07 15:15:49.819734
19	2	55	68361900.0000	auto	2026-03-07 15:15:49.819734
20	2	56	879193.0000	auto	2026-03-07 15:15:49.819734
21	2	57	6400079.0000	auto	2026-03-07 15:15:49.819734
22	2	58	1933504.0000	auto	2026-03-07 15:15:49.819734
23	2	16	1044.0000	auto	2026-03-07 15:15:49.819734
24	2	39	1895199.0000	auto	2026-03-07 15:15:49.819734
25	2	43	3155306.0000	auto	2026-03-07 15:15:49.819734
26	2	44	1000000.0000	auto	2026-03-07 15:15:49.819734
27	2	46	20000.0000	auto	2026-03-07 15:15:49.819734
28	2	51	20000000.0000	auto	2026-03-07 15:15:49.819734
29	2	48	15100000.0000	auto	2026-03-07 15:15:49.819734
30	3	52	58927012.0000	auto	2026-03-07 15:15:50.731946
31	3	53	65051348.0000	auto	2026-03-07 15:15:50.731946
32	3	54	92501218.0000	auto	2026-03-07 15:15:50.731946
33	3	60	46343865.0000	auto	2026-03-07 15:15:50.731946
34	3	55	114913190.0000	auto	2026-03-07 15:15:50.731946
35	3	56	4763034.0000	auto	2026-03-07 15:15:50.731946
36	3	57	31597310.0000	auto	2026-03-07 15:15:50.731946
37	3	58	5639402.0000	auto	2026-03-07 15:15:50.731946
38	3	16	11280540.0000	auto	2026-03-07 15:15:50.731946
39	3	39	37171690.0000	auto	2026-03-07 15:15:50.731946
40	3	43	2759356.0000	auto	2026-03-07 15:15:50.731946
41	3	44	1434638.0000	auto	2026-03-07 15:15:50.731946
42	3	46	237599.0000	auto	2026-03-07 15:15:50.731946
43	3	49	12889.0000	auto	2026-03-07 15:15:50.731946
44	3	50	190095.0000	auto	2026-03-07 15:15:50.731946
45	3	48	16300000.0000	auto	2026-03-07 15:15:50.731946
46	4	52	96816283.0000	auto	2026-03-07 15:15:51.635706
47	4	53	387098279.0000	auto	2026-03-07 15:15:51.635706
48	4	54	16398641.0000	auto	2026-03-07 15:15:51.635706
49	4	60	269038.0000	auto	2026-03-07 15:15:51.635706
50	4	55	155285077.0000	auto	2026-03-07 15:15:51.635706
51	4	56	13045393.0000	auto	2026-03-07 15:15:51.635706
52	4	57	199900535.1000	auto	2026-03-07 15:15:51.635706
53	4	58	12599926.8800	auto	2026-03-07 15:15:51.635706
54	4	59	524616.5680	auto	2026-03-07 15:15:51.635706
55	4	39	17124244.0000	auto	2026-03-07 15:15:51.635706
56	4	43	2543272.0000	auto	2026-03-07 15:15:51.635706
57	4	44	8591.0000	auto	2026-03-07 15:15:51.635706
58	4	46	106229.0000	auto	2026-03-07 15:15:51.635706
59	4	49	12853.0000	auto	2026-03-07 15:15:51.635706
60	4	50	310316.0000	auto	2026-03-07 15:15:51.635706
61	4	48	17500000.0000	auto	2026-03-07 15:15:51.635706
62	5	52	116259904.0000	auto	2026-03-07 15:15:52.499863
63	5	53	467669203.0000	auto	2026-03-07 15:15:52.499863
64	5	54	52692243.0000	auto	2026-03-07 15:15:52.499863
65	5	60	41598.0000	auto	2026-03-07 15:15:52.499863
66	5	55	100797090.5650	auto	2026-03-07 15:15:52.499863
67	5	56	37152060.0000	auto	2026-03-07 15:15:52.499863
68	5	57	208911633.9450	auto	2026-03-07 15:15:52.499863
69	5	58	14489308.7450	auto	2026-03-07 15:15:52.499863
70	5	59	1104982.3200	auto	2026-03-07 15:15:52.499863
71	5	16	20002250.0000	auto	2026-03-07 15:15:52.499863
72	5	39	18800585.0000	auto	2026-03-07 15:15:52.499863
73	5	43	428877.0000	auto	2026-03-07 15:15:52.499863
74	5	44	134294.0000	auto	2026-03-07 15:15:52.499863
75	5	46	176354.0000	auto	2026-03-07 15:15:52.499863
76	5	49	103878.0000	auto	2026-03-07 15:15:52.499863
77	5	50	380606.0000	auto	2026-03-07 15:15:52.499863
78	5	47	79056.0000	auto	2026-03-07 15:15:52.499863
79	5	48	18300000.0000	auto	2026-03-07 15:15:52.499863
80	1	45	1000000.0000	auto	2026-03-07 15:33:23.239291
81	2	45	900000.0000	auto	2026-03-07 15:33:23.239291
82	3	45	1420000.0000	auto	2026-03-07 15:33:23.239291
83	4	45	1375000.0000	auto	2026-03-07 15:33:23.239291
84	5	45	0.0000	auto	2026-03-07 15:33:23.239291
85	1	61	93110000.0000	auto	2026-03-07 15:38:31.119826
86	2	61	95110000.0000	auto	2026-03-07 15:38:31.119826
87	3	61	50000000.0000	auto	2026-03-07 15:38:31.119826
88	4	61	0.0000	auto	2026-03-07 15:38:31.119826
89	5	61	0.0000	auto	2026-03-07 15:38:31.119826
\.


--
-- Data for Name: annual_snapshots; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.annual_snapshots (annual_snapshot_id, user_id, reference_date, source_snapshot_id, status, editable_until, created_at) FROM stdin;
1	1	2022-01-01	116	locked	\N	2026-03-07 15:15:48.731054
2	1	2023-01-01	117	locked	\N	2026-03-07 15:15:49.66439
3	1	2024-01-01	118	locked	\N	2026-03-07 15:15:50.587595
4	1	2025-01-01	119	locked	\N	2026-03-07 15:15:51.48779
5	1	2026-01-01	120	locked	\N	2026-03-07 15:15:52.350149
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
61	23	4	t	\N	\N	2026-03-07 15:38:31.119826
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
12	7	12	196268.0000	manual	2026-03-07 07:58:53.284372
8	7	6	37924150.0000	manual	2026-03-07 07:58:53.286913
13	7	13	0.0000	manual	2026-03-07 07:58:53.292194
19	7	19	0.0000	manual	2026-03-07 07:58:53.310766
23	7	22	0.0000	manual	2026-03-07 07:58:53.325774
24	7	24	128025.0000	manual	2026-03-07 07:58:53.334795
30	7	30	35558.0000	manual	2026-03-07 07:58:53.356198
36	7	36	0.0000	manual	2026-03-07 07:58:53.379281
50	7	51	0.0000	manual	2026-03-07 07:58:53.427418
2255	100	52	115040924.0000	auto	2026-03-07 15:02:55.303985
2256	100	53	463998635.0000	auto	2026-03-07 15:02:55.303985
2257	100	54	51948453.0000	auto	2026-03-07 15:02:55.303985
2258	100	60	42176.0000	auto	2026-03-07 15:02:55.303985
2259	100	55	101530584.0000	auto	2026-03-07 15:02:55.303985
2260	100	56	29767186.0000	auto	2026-03-07 15:02:55.303985
2261	100	57	224263672.6400	auto	2026-03-07 15:02:55.303985
2262	100	58	14730327.6640	auto	2026-03-07 15:02:55.303985
2263	100	59	1079663.0000	auto	2026-03-07 15:02:55.303985
2264	100	16	23964135.0000	auto	2026-03-07 15:02:55.303985
2265	100	39	16983303.0000	auto	2026-03-07 15:02:55.303985
2266	100	43	4007595.0000	auto	2026-03-07 15:02:55.303985
2267	100	44	134263.0000	auto	2026-03-07 15:02:55.303985
2268	100	46	166315.0000	auto	2026-03-07 15:02:55.303985
2269	100	49	4653.0000	auto	2026-03-07 15:02:55.303985
2270	100	50	370453.0000	auto	2026-03-07 15:02:55.303985
2271	100	48	18200000.0000	auto	2026-03-07 15:02:55.303985
40	7	40	20124.0000	manual	2026-03-07 07:58:53.394925
41	7	41	18340.0000	manual	2026-03-07 07:58:53.396483
42	7	42	133.0000	manual	2026-03-07 07:58:53.398593
11	7	11	79689900.0000	manual	2026-03-07 07:58:53.282106
14	7	14	43997525.0000	manual	2026-03-07 07:58:53.29397
15	7	15	11765.0000	manual	2026-03-07 07:58:53.302779
17	7	17	75447999.0000	manual	2026-03-07 07:58:53.303254
18	7	18	47391659.0000	manual	2026-03-07 07:58:53.313289
20	7	20	33535018.0000	manual	2026-03-07 07:58:53.312991
21	7	21	23084455.0000	manual	2026-03-07 07:58:53.319505
22	7	23	5545260.0000	manual	2026-03-07 07:58:53.326692
25	7	25	69655.0000	manual	2026-03-07 07:58:53.336233
26	7	26	3997539.0000	manual	2026-03-07 07:58:53.335176
27	7	27	5567649.0000	manual	2026-03-07 07:58:53.341343
28	7	28	5440343.0000	manual	2026-03-07 07:58:53.349431
29	7	29	577491.0000	manual	2026-03-07 07:58:53.350815
31	7	31	14534.0000	manual	2026-03-07 07:58:53.362054
32	7	32	212480.0000	manual	2026-03-07 07:58:53.359827
33	7	33	358981.0000	manual	2026-03-07 07:58:53.364997
34	7	34	205992.0000	manual	2026-03-07 07:58:53.371366
35	7	35	297620.0000	manual	2026-03-07 07:58:53.372541
37	7	37	47612.0000	manual	2026-03-07 07:58:53.378802
178	14	52	66895260.0000	auto	2026-03-07 14:59:05.280178
179	14	53	81915953.0000	auto	2026-03-07 14:59:05.431259
180	14	54	121949588.0000	auto	2026-03-07 14:59:05.582045
181	14	60	43502070.0000	auto	2026-03-07 14:59:05.73566
182	14	55	122209286.7100	auto	2026-03-07 14:59:05.889405
183	14	56	6360999.0000	auto	2026-03-07 14:59:06.039468
184	14	57	41294821.0000	auto	2026-03-07 14:59:06.174377
185	14	58	6948548.0000	auto	2026-03-07 14:59:06.326675
186	14	59	101827.0000	auto	2026-03-07 14:59:06.47107
187	14	16	4585352.0000	auto	2026-03-07 14:59:06.632469
188	14	39	44630781.0000	auto	2026-03-07 14:59:06.815464
189	14	43	2731084.0000	auto	2026-03-07 14:59:06.987831
190	14	44	114638.0000	auto	2026-03-07 14:59:07.132993
191	14	46	267599.0000	auto	2026-03-07 14:59:07.288299
192	14	49	12910.0000	auto	2026-03-07 14:59:07.436902
193	14	50	220095.0000	auto	2026-03-07 14:59:07.569652
195	15	52	68681848.0000	auto	2026-03-07 14:59:08.60244
196	15	53	84332291.0000	auto	2026-03-07 14:59:08.755963
197	15	54	128008380.0000	auto	2026-03-07 14:59:08.901323
198	15	60	47510530.0000	auto	2026-03-07 14:59:09.056147
199	15	55	124210752.8480	auto	2026-03-07 14:59:09.225613
200	15	56	6425749.0000	auto	2026-03-07 14:59:09.391685
201	15	57	47252663.5600	auto	2026-03-07 14:59:09.54495
202	15	58	7303437.6800	auto	2026-03-07 14:59:09.684792
203	15	59	104465.3840	auto	2026-03-07 14:59:09.840191
204	15	16	24340170.0000	auto	2026-03-07 14:59:10.013345
205	15	38	9402317.0000	auto	2026-03-07 14:59:10.165539
206	15	39	45079991.0000	auto	2026-03-07 14:59:10.319062
207	15	43	2595974.0000	auto	2026-03-07 14:59:10.474284
208	15	44	18764.0000	auto	2026-03-07 14:59:10.637888
209	15	46	21815841.0000	auto	2026-03-07 14:59:10.795964
213	16	52	69178625.0000	auto	2026-03-07 14:59:12.285418
214	16	53	84879328.0000	auto	2026-03-07 14:59:12.454038
215	16	54	127533166.0000	auto	2026-03-07 14:59:12.640482
216	16	60	50594122.0000	auto	2026-03-07 14:59:12.794323
217	16	55	127688885.6960	auto	2026-03-07 14:59:12.959976
218	16	56	6738579.0000	auto	2026-03-07 14:59:13.113951
219	16	57	46802962.7760	auto	2026-03-07 14:59:13.263534
220	16	58	7945546.8960	auto	2026-03-07 14:59:13.415195
221	16	59	105629.3840	auto	2026-03-07 14:59:13.561235
222	16	16	32357095.0000	auto	2026-03-07 14:59:13.695396
223	16	38	20057980.0000	auto	2026-03-07 14:59:13.849786
224	16	39	45154872.0000	auto	2026-03-07 14:59:14.001673
225	16	43	1524069.0000	auto	2026-03-07 14:59:14.158351
226	16	44	157800.0000	auto	2026-03-07 14:59:14.308364
227	16	46	1815841.0000	auto	2026-03-07 14:59:14.487363
228	16	49	12961.0000	auto	2026-03-07 14:59:14.657485
229	16	50	220095.0000	auto	2026-03-07 14:59:14.821952
231	17	52	68739755.0000	auto	2026-03-07 14:59:15.920258
232	17	53	84971172.0000	auto	2026-03-07 14:59:16.061829
233	17	54	124264339.0000	auto	2026-03-07 14:59:16.20338
234	17	60	52875045.0000	auto	2026-03-07 14:59:16.338274
235	17	55	129052950.6960	auto	2026-03-07 14:59:16.470495
236	17	56	6828719.0000	auto	2026-03-07 14:59:16.618167
2272	100	47	69041.0000	auto	2026-03-07 15:02:55.303985
2310	103	52	119489504.0000	auto	2026-03-07 15:02:57.913689
2311	103	53	483736431.0000	auto	2026-03-07 15:02:57.913689
2312	103	54	55852173.0000	auto	2026-03-07 15:02:57.913689
2313	103	60	42458.0000	auto	2026-03-07 15:02:57.913689
2314	103	55	103531076.0000	auto	2026-03-07 15:02:57.913689
2315	103	56	32785903.0000	auto	2026-03-07 15:02:57.913689
2316	103	57	224540882.7360	auto	2026-03-07 15:02:57.913689
2317	103	58	14818575.0320	auto	2026-03-07 15:02:57.913689
2318	103	59	1103141.0000	auto	2026-03-07 15:02:57.913689
2319	103	16	21053216.0000	auto	2026-03-07 15:02:57.913689
2320	103	39	16983303.0000	auto	2026-03-07 15:02:57.913689
2321	103	43	1556824.0000	auto	2026-03-07 15:02:57.913689
2322	103	44	134263.0000	auto	2026-03-07 15:02:57.913689
2323	103	46	166315.0000	auto	2026-03-07 15:02:57.913689
2324	103	49	4656.0000	auto	2026-03-07 15:02:57.913689
2325	103	50	370453.0000	auto	2026-03-07 15:02:57.913689
249	18	52	71327369.0000	auto	2026-03-07 14:59:19.343752
250	18	53	89582818.0000	auto	2026-03-07 14:59:19.482474
251	18	54	135276325.0000	auto	2026-03-07 14:59:19.620075
252	18	60	53291281.0000	auto	2026-03-07 14:59:19.764813
253	18	55	126889997.4760	auto	2026-03-07 14:59:19.898218
254	18	56	7671349.0000	auto	2026-03-07 14:59:20.046934
255	18	57	50154259.0000	auto	2026-03-07 14:59:20.194873
256	18	58	8434064.0000	auto	2026-03-07 14:59:20.372116
257	18	59	155455.4320	auto	2026-03-07 14:59:20.524117
258	18	16	29139722.0000	auto	2026-03-07 14:59:20.663363
259	18	38	17678822.0000	auto	2026-03-07 14:59:20.807321
267	19	52	68091681.0000	auto	2026-03-07 14:59:21.687357
268	19	53	84190331.0000	auto	2026-03-07 14:59:21.8319
269	19	54	119391940.0000	auto	2026-03-07 14:59:21.978635
270	19	60	50539991.0000	auto	2026-03-07 14:59:22.116191
271	19	55	127258891.0000	auto	2026-03-07 14:59:22.264635
272	19	56	7820799.0000	auto	2026-03-07 14:59:22.438651
273	19	57	39690535.0000	auto	2026-03-07 14:59:22.58442
274	19	58	8775216.0000	auto	2026-03-07 14:59:22.732993
275	19	59	145836.0000	auto	2026-03-07 14:59:22.884478
276	19	16	27454766.0000	auto	2026-03-07 14:59:23.062962
277	19	38	16687853.0000	auto	2026-03-07 14:59:23.260183
278	19	39	49217420.0000	auto	2026-03-07 14:59:23.427523
279	19	43	286462.0000	auto	2026-03-07 14:59:23.583438
280	19	44	17800.0000	auto	2026-03-07 14:59:23.744619
281	19	46	25841.0000	auto	2026-03-07 14:59:23.890934
282	19	49	12983.0000	auto	2026-03-07 14:59:24.048817
283	19	50	230095.0000	auto	2026-03-07 14:59:24.222209
285	20	52	69406665.0000	auto	2026-03-07 14:59:25.316706
286	20	53	86067164.0000	auto	2026-03-07 14:59:25.469331
287	20	54	124603765.0000	auto	2026-03-07 14:59:25.624774
288	20	60	50781592.0000	auto	2026-03-07 14:59:25.772709
289	20	55	130134328.0000	auto	2026-03-07 14:59:25.93684
290	20	56	7573469.0000	auto	2026-03-07 14:59:26.080506
291	20	57	47346529.0000	auto	2026-03-07 14:59:26.223459
292	20	58	9155239.0000	auto	2026-03-07 14:59:26.389176
293	20	59	194704.0000	auto	2026-03-07 14:59:26.542707
294	20	16	25968974.0000	auto	2026-03-07 14:59:26.684632
295	20	38	15606254.0000	auto	2026-03-07 14:59:26.835979
296	20	39	47856302.0000	auto	2026-03-07 14:59:26.989272
297	20	43	251430.0000	auto	2026-03-07 14:59:27.120327
298	20	44	52800.0000	auto	2026-03-07 14:59:27.27597
299	20	46	25841.0000	auto	2026-03-07 14:59:27.426521
300	20	49	12983.0000	auto	2026-03-07 14:59:27.584737
301	20	50	230095.0000	auto	2026-03-07 14:59:27.728542
303	21	52	69419814.0000	auto	2026-03-07 14:59:28.712633
304	21	53	86359882.0000	auto	2026-03-07 14:59:28.856393
305	21	54	124458187.0000	auto	2026-03-07 14:59:29.007814
306	21	60	52377950.0000	auto	2026-03-07 14:59:29.156961
307	21	55	132631210.0000	auto	2026-03-07 14:59:29.305104
308	21	56	7340889.0000	auto	2026-03-07 14:59:29.493082
309	21	57	50123176.0000	auto	2026-03-07 14:59:29.646925
310	21	58	9462256.0000	auto	2026-03-07 14:59:29.796141
311	21	59	196084.0000	auto	2026-03-07 14:59:29.934898
312	21	16	24082200.0000	auto	2026-03-07 14:59:30.077254
313	21	38	14864254.0000	auto	2026-03-07 14:59:30.230917
314	21	39	46884554.0000	auto	2026-03-07 14:59:30.37316
315	21	43	260889.0000	auto	2026-03-07 14:59:30.515803
316	21	44	37800.0000	auto	2026-03-07 14:59:30.680537
317	21	46	25841.0000	auto	2026-03-07 14:59:30.822147
318	21	49	13004.0000	auto	2026-03-07 14:59:30.96039
319	21	50	230095.0000	auto	2026-03-07 14:59:31.108052
321	22	52	71501447.0000	auto	2026-03-07 14:59:32.179402
322	22	53	90612335.0000	auto	2026-03-07 14:59:32.33991
323	22	54	133930055.0000	auto	2026-03-07 14:59:32.528687
324	22	60	53461544.0000	auto	2026-03-07 14:59:32.688103
325	22	55	135702590.0000	auto	2026-03-07 14:59:32.89784
326	22	56	7913689.0000	auto	2026-03-07 14:59:33.039278
327	22	57	51419541.0000	auto	2026-03-07 14:59:33.192143
328	22	58	9835566.0000	auto	2026-03-07 14:59:33.349467
329	22	59	196432.6880	auto	2026-03-07 14:59:33.515882
330	22	16	22194567.0000	auto	2026-03-07 14:59:33.663142
331	22	38	14172796.0000	auto	2026-03-07 14:59:33.828852
332	22	39	46790362.0000	auto	2026-03-07 14:59:33.980382
333	22	43	1208920.0000	auto	2026-03-07 14:59:34.131346
334	22	44	122800.0000	auto	2026-03-07 14:59:34.319325
335	22	46	35841.0000	auto	2026-03-07 14:59:34.487308
336	22	49	12704.0000	auto	2026-03-07 14:59:34.654755
339	23	52	72303188.0000	auto	2026-03-07 14:59:35.949738
340	23	53	91940153.0000	auto	2026-03-07 14:59:36.085794
341	23	54	138818974.0000	auto	2026-03-07 14:59:36.234464
342	23	60	52334379.0000	auto	2026-03-07 14:59:36.371876
343	23	55	137871409.0000	auto	2026-03-07 14:59:36.515622
344	23	56	7922619.0000	auto	2026-03-07 14:59:36.65202
345	23	57	54797072.0000	auto	2026-03-07 14:59:36.823622
346	23	58	10173674.7900	auto	2026-03-07 14:59:36.985749
347	23	59	199594.0000	auto	2026-03-07 14:59:37.129757
348	23	16	20205759.0000	auto	2026-03-07 14:59:37.276067
349	23	38	13439096.0000	auto	2026-03-07 14:59:37.429056
350	23	39	46767226.0000	auto	2026-03-07 14:59:37.578974
351	23	43	259413.0000	auto	2026-03-07 14:59:37.732026
352	23	44	7800.0000	auto	2026-03-07 14:59:37.88259
353	23	46	35841.0000	auto	2026-03-07 14:59:38.041891
354	23	49	12704.0000	auto	2026-03-07 14:59:38.180752
355	23	50	240095.0000	auto	2026-03-07 14:59:38.328289
357	24	52	73636415.0000	auto	2026-03-07 14:59:39.377351
358	24	53	93767131.0000	auto	2026-03-07 14:59:39.520539
359	24	54	142259098.0000	auto	2026-03-07 14:59:39.66461
360	24	60	51503861.0000	auto	2026-03-07 14:59:39.821591
361	24	55	138705705.0000	auto	2026-03-07 14:59:39.967514
362	24	56	7841359.0000	auto	2026-03-07 14:59:40.118007
363	24	57	58632092.0000	auto	2026-03-07 14:59:40.264431
364	24	58	10499306.0000	auto	2026-03-07 14:59:40.42043
365	24	59	208272.0000	auto	2026-03-07 14:59:40.565944
366	24	16	20216656.0000	auto	2026-03-07 14:59:40.728914
367	24	38	12565850.0000	auto	2026-03-07 14:59:40.874979
368	24	39	46767226.0000	auto	2026-03-07 14:59:41.030721
369	24	43	170313.0000	auto	2026-03-07 14:59:41.196697
2273	101	52	114633204.0000	auto	2026-03-07 15:02:56.184319
2274	101	53	457868886.0000	auto	2026-03-07 15:02:56.184319
2275	101	54	50332373.0000	auto	2026-03-07 15:02:56.184319
2276	101	60	40813.0000	auto	2026-03-07 15:02:56.184319
2277	101	55	100195809.0000	auto	2026-03-07 15:02:56.184319
2278	101	56	29469573.0000	auto	2026-03-07 15:02:56.184319
2279	101	57	206895395.0000	auto	2026-03-07 15:02:56.184319
2280	101	58	14616305.3600	auto	2026-03-07 15:02:56.184319
2281	101	59	1057233.0000	auto	2026-03-07 15:02:56.184319
2282	101	16	22973205.0000	auto	2026-03-07 15:02:56.184319
2283	101	38	1000342.0000	auto	2026-03-07 15:02:56.184319
2284	101	39	16983303.0000	auto	2026-03-07 15:02:56.184319
2285	101	43	1789933.0000	auto	2026-03-07 15:02:56.184319
2286	101	44	134263.0000	auto	2026-03-07 15:02:56.184319
2287	101	46	166315.0000	auto	2026-03-07 15:02:56.184319
2288	101	49	4653.0000	auto	2026-03-07 15:02:56.184319
2289	101	50	370453.0000	auto	2026-03-07 15:02:56.184319
2290	101	48	18200000.0000	auto	2026-03-07 15:02:56.184319
375	25	52	74314061.0000	auto	2026-03-07 14:59:42.868762
376	25	53	95334967.0000	auto	2026-03-07 14:59:43.016115
377	25	54	145027608.0000	auto	2026-03-07 14:59:43.160393
378	25	60	40103150.0000	auto	2026-03-07 14:59:43.292351
393	26	52	75693972.0000	auto	2026-03-07 14:59:46.222641
394	26	53	97786144.0000	auto	2026-03-07 14:59:46.382751
395	26	54	158344412.0000	auto	2026-03-07 14:59:46.536368
396	26	60	32003942.0000	auto	2026-03-07 14:59:46.675889
397	26	55	139975092.0000	auto	2026-03-07 14:59:46.82757
398	26	56	7933516.0000	auto	2026-03-07 14:59:46.994074
399	26	57	83181289.3900	auto	2026-03-07 14:59:47.150259
400	26	58	10914234.5400	auto	2026-03-07 14:59:47.303894
401	26	59	266183.0000	auto	2026-03-07 14:59:47.455298
402	26	16	14729302.0000	auto	2026-03-07 14:59:47.596044
403	26	38	10774969.0000	auto	2026-03-07 14:59:47.727348
404	26	39	46475587.0000	auto	2026-03-07 14:59:47.877891
405	26	43	254995.0000	auto	2026-03-07 14:59:48.032945
406	26	44	47800.0000	auto	2026-03-07 14:59:48.172109
407	26	46	35841.0000	auto	2026-03-07 14:59:48.308729
408	26	49	12704.0000	auto	2026-03-07 14:59:48.45302
409	26	50	240095.0000	auto	2026-03-07 14:59:48.599968
411	27	52	79910477.0000	auto	2026-03-07 14:59:49.665951
412	27	53	105664393.0000	auto	2026-03-07 14:59:49.804195
413	27	54	179535567.0000	auto	2026-03-07 14:59:49.958811
414	27	60	22549672.0000	auto	2026-03-07 14:59:50.11495
415	27	55	141426167.0000	auto	2026-03-07 14:59:49.794288
416	27	56	8198766.0000	auto	2026-03-07 14:59:49.331844
417	27	57	109190945.1220	auto	2026-03-07 14:59:49.463161
418	27	58	11119279.4510	auto	2026-03-07 14:59:49.604219
419	27	59	271275.1720	auto	2026-03-07 14:59:49.735055
420	27	16	14873195.0000	auto	2026-03-07 14:59:49.871162
421	27	38	11478268.0000	auto	2026-03-07 14:59:50.00642
422	27	39	46469992.0000	auto	2026-03-07 14:59:50.144742
423	27	43	3279473.0000	auto	2026-03-07 14:59:50.294956
424	27	44	32800.0000	auto	2026-03-07 14:59:50.434934
425	27	46	45841.0000	auto	2026-03-07 14:59:50.58507
426	27	49	12704.0000	auto	2026-03-07 14:59:50.735879
427	27	50	250193.0000	auto	2026-03-07 14:59:50.877683
429	28	52	80648842.0000	auto	2026-03-07 14:59:51.886546
430	28	53	107922526.0000	auto	2026-03-07 14:59:52.055666
431	28	54	182229145.0000	auto	2026-03-07 14:59:52.196892
432	28	60	12448601.0000	auto	2026-03-07 14:59:52.349678
433	28	55	142561959.0000	auto	2026-03-07 14:59:52.487404
434	28	56	8416356.0000	auto	2026-03-07 14:59:52.630602
435	28	57	115155635.2040	auto	2026-03-07 14:59:52.772811
436	28	58	11188763.4510	auto	2026-03-07 14:59:52.911348
437	28	59	274767.1720	auto	2026-03-07 14:59:53.039439
438	28	16	13594473.0000	auto	2026-03-07 14:59:53.180122
439	28	38	11483176.0000	auto	2026-03-07 14:59:53.33149
440	28	39	46469992.0000	auto	2026-03-07 14:59:53.47633
441	28	43	2951712.0000	auto	2026-03-07 14:59:53.624276
442	28	44	22821.0000	auto	2026-03-07 14:59:53.796648
443	28	46	45841.0000	auto	2026-03-07 14:59:53.942688
444	28	49	12704.0000	auto	2026-03-07 14:59:54.07541
445	28	50	250193.0000	auto	2026-03-07 14:59:54.206565
447	29	52	80902349.0000	auto	2026-03-07 14:59:55.283384
448	29	53	108135314.0000	auto	2026-03-07 14:59:55.444679
449	29	54	182390644.0000	auto	2026-03-07 14:59:55.578776
450	29	60	352714.0000	auto	2026-03-07 14:59:55.710888
451	29	55	142222227.0000	auto	2026-03-07 14:59:55.851619
452	29	56	8257136.0000	auto	2026-03-07 14:59:56.002512
453	29	57	125124834.0650	auto	2026-03-07 14:59:56.142929
454	29	58	11024714.2990	auto	2026-03-07 14:59:56.286759
455	29	59	276240.3690	auto	2026-03-07 14:59:56.435429
456	29	16	13601754.0000	auto	2026-03-07 14:59:56.580571
457	29	38	14488071.0000	auto	2026-03-07 14:59:56.73699
458	29	39	45548718.0000	auto	2026-03-07 14:59:56.872569
459	29	43	2720920.0000	auto	2026-03-07 14:59:57.023988
460	29	44	7821.0000	auto	2026-03-07 14:59:57.175232
461	29	46	46192.0000	auto	2026-03-07 14:59:57.331306
462	29	49	12704.0000	auto	2026-03-07 14:59:57.479921
465	30	52	82876154.0000	auto	2026-03-07 14:59:58.669253
466	30	53	110685301.0000	auto	2026-03-07 14:59:58.828121
467	30	54	190496891.0000	auto	2026-03-07 14:59:58.963471
468	30	60	352212.0000	auto	2026-03-07 14:59:59.112558
469	30	55	143666284.0000	auto	2026-03-07 14:59:59.258658
470	30	56	8415306.0000	auto	2026-03-07 14:59:59.394127
471	30	57	146526588.0140	auto	2026-03-07 14:59:59.53516
472	30	58	10930471.0000	auto	2026-03-07 14:59:59.668012
473	30	59	285260.6910	auto	2026-03-07 14:59:59.824277
474	30	16	13338899.0000	auto	2026-03-07 14:59:59.955892
475	30	38	10003722.0000	auto	2026-03-07 15:00:00.100521
476	30	39	45548718.0000	auto	2026-03-07 15:00:00.243167
477	30	43	16071505.0000	auto	2026-03-07 15:00:00.395565
478	30	44	1263.0000	auto	2026-03-07 15:00:00.547678
479	30	46	46192.0000	auto	2026-03-07 15:00:00.697212
480	30	49	12743.0000	auto	2026-03-07 15:00:00.841965
481	30	50	250193.0000	auto	2026-03-07 15:00:00.98379
483	31	52	83173289.0000	auto	2026-03-07 15:00:02.075858
484	31	53	111451036.0000	auto	2026-03-07 15:00:02.23954
485	31	54	189814973.0000	auto	2026-03-07 15:00:02.395919
486	31	60	349012.0000	auto	2026-03-07 15:00:02.542625
487	31	55	144504196.0000	auto	2026-03-07 15:00:02.68674
488	31	56	9039956.0000	auto	2026-03-07 15:00:02.855536
489	31	57	148035168.0000	auto	2026-03-07 15:00:02.989671
490	31	58	11545668.0000	auto	2026-03-07 15:00:03.14217
491	31	59	320296.3060	auto	2026-03-07 15:00:03.294957
492	31	16	23597452.0000	auto	2026-03-07 15:00:03.441055
493	31	38	14703528.0000	auto	2026-03-07 15:00:03.58142
494	31	39	47579617.0000	auto	2026-03-07 15:00:03.727719
495	31	43	2117717.0000	auto	2026-03-07 15:00:03.862405
496	31	44	1263.0000	auto	2026-03-07 15:00:03.997751
497	31	46	56192.0000	auto	2026-03-07 15:00:04.146568
498	31	49	12743.0000	auto	2026-03-07 15:00:04.276595
499	31	50	260193.0000	auto	2026-03-07 15:00:04.432312
2291	101	47	69041.0000	auto	2026-03-07 15:02:56.184319
2326	103	48	18200000.0000	auto	2026-03-07 15:02:57.913689
2327	103	47	69041.0000	auto	2026-03-07 15:02:57.913689
2346	105	52	116745644.0000	auto	2026-03-07 15:02:59.581271
2347	105	53	471338163.0000	auto	2026-03-07 15:02:59.581271
2348	105	54	53514113.0000	auto	2026-03-07 15:02:59.581271
2349	105	60	42280.0000	auto	2026-03-07 15:02:59.581271
2350	105	55	103531266.0000	auto	2026-03-07 15:02:59.581271
2351	105	56	35762345.0000	auto	2026-03-07 15:02:59.581271
2352	105	57	209493571.4800	auto	2026-03-07 15:02:59.581271
2353	105	58	14955132.4800	auto	2026-03-07 15:02:59.581271
2354	105	59	1119040.0000	auto	2026-03-07 15:02:59.581271
2355	105	16	25372293.0000	auto	2026-03-07 15:02:59.581271
2356	105	39	18800585.0000	auto	2026-03-07 15:02:59.581271
2357	105	43	834535.0000	auto	2026-03-07 15:02:59.581271
2358	105	44	134294.0000	auto	2026-03-07 15:02:59.581271
519	33	52	77484606.0000	auto	2026-03-07 15:00:08.847215
520	33	53	102456144.0000	auto	2026-03-07 15:00:08.987824
521	33	54	158544792.0000	auto	2026-03-07 15:00:09.130257
522	33	60	331311.0000	auto	2026-03-07 15:00:09.287114
523	33	55	142936436.0000	auto	2026-03-07 15:00:09.446297
524	33	56	8981506.0000	auto	2026-03-07 15:00:09.615234
525	33	57	121592332.0000	auto	2026-03-07 15:00:09.772337
526	33	58	11771646.1700	auto	2026-03-07 15:00:09.91407
527	33	59	281325.0000	auto	2026-03-07 15:00:10.056994
528	33	16	23622222.0000	auto	2026-03-07 15:00:10.213863
529	33	38	5007035.0000	auto	2026-03-07 15:00:10.374203
530	33	39	47574013.0000	auto	2026-03-07 15:00:10.511071
531	33	43	1582780.0000	auto	2026-03-07 15:00:10.654224
532	33	44	16263.0000	auto	2026-03-07 15:00:10.792134
533	33	46	56192.0000	auto	2026-03-07 15:00:10.942644
534	33	49	12743.0000	auto	2026-03-07 15:00:11.074714
535	33	50	260193.0000	auto	2026-03-07 15:00:11.219733
537	34	52	75273366.0000	auto	2026-03-07 15:00:12.225935
538	34	53	98973248.0000	auto	2026-03-07 15:00:12.366813
539	34	54	153556516.0000	auto	2026-03-07 15:00:12.505795
540	34	60	319011.0000	auto	2026-03-07 15:00:12.641281
541	34	55	141006892.0000	auto	2026-03-07 15:00:12.794144
542	34	56	9294216.0000	auto	2026-03-07 15:00:12.937242
543	34	57	111355514.0000	auto	2026-03-07 15:00:13.083671
544	34	58	11707117.9540	auto	2026-03-07 15:00:13.223161
545	34	59	266046.0000	auto	2026-03-07 15:00:13.363178
546	34	16	18132930.0000	auto	2026-03-07 15:00:13.5035
547	34	39	45631114.0000	auto	2026-03-07 15:00:13.641748
548	34	43	3582780.0000	auto	2026-03-07 15:00:13.779511
549	34	44	11263.0000	auto	2026-03-07 15:00:13.939323
550	34	46	56192.0000	auto	2026-03-07 15:00:14.064317
551	34	49	12743.0000	auto	2026-03-07 15:00:14.21305
552	34	50	260193.0000	auto	2026-03-07 15:00:14.356013
554	35	52	74419277.0000	auto	2026-03-07 15:00:15.407348
555	35	53	97007286.0000	auto	2026-03-07 15:00:15.577945
556	35	54	146521149.0000	auto	2026-03-07 15:00:15.735391
557	35	60	297531.0000	auto	2026-03-07 15:00:15.88658
558	35	55	141353369.0000	auto	2026-03-07 15:00:16.027503
559	35	56	9639596.0000	auto	2026-03-07 15:00:16.194202
560	35	57	109887218.0000	auto	2026-03-07 15:00:16.342968
561	35	58	11807288.2280	auto	2026-03-07 15:00:16.504426
562	35	59	305869.0000	auto	2026-03-07 15:00:16.651331
563	35	16	17642188.0000	auto	2026-03-07 15:00:16.808911
564	35	39	44660051.0000	auto	2026-03-07 15:00:16.952181
565	35	43	3592780.0000	auto	2026-03-07 15:00:17.088537
566	35	44	101263.0000	auto	2026-03-07 15:00:17.269886
567	35	46	56192.0000	auto	2026-03-07 15:00:17.426419
568	35	49	12743.0000	auto	2026-03-07 15:00:17.563187
569	35	50	260193.0000	auto	2026-03-07 15:00:17.730894
571	36	52	79348771.0000	auto	2026-03-07 15:00:18.778372
572	36	53	104675633.0000	auto	2026-03-07 15:00:18.940498
573	36	54	167146674.0000	auto	2026-03-07 15:00:19.094325
574	36	60	319111.0000	auto	2026-03-07 15:00:18.792438
575	36	55	143411061.0000	auto	2026-03-07 15:00:18.36711
576	36	56	9642406.0000	auto	2026-03-07 15:00:18.498233
577	36	57	140186954.0000	auto	2026-03-07 15:00:18.657472
578	36	58	11936306.2720	auto	2026-03-07 15:00:18.803499
579	36	59	324137.0000	auto	2026-03-07 15:00:18.971166
580	36	16	14650190.0000	auto	2026-03-07 15:00:19.119761
581	36	39	43683337.0000	auto	2026-03-07 15:00:19.262255
582	36	43	2174652.0000	auto	2026-03-07 15:00:19.414777
583	36	44	16263.0000	auto	2026-03-07 15:00:19.569722
584	36	46	66192.0000	auto	2026-03-07 15:00:19.718846
585	36	49	12743.0000	auto	2026-03-07 15:00:19.879811
586	36	50	270193.0000	auto	2026-03-07 15:00:20.032696
588	37	52	78508402.0000	auto	2026-03-07 15:00:21.079537
589	37	53	103040736.0000	auto	2026-03-07 15:00:21.219093
590	37	54	161748633.0000	auto	2026-03-07 15:00:21.358899
591	37	60	302011.0000	auto	2026-03-07 15:00:21.503306
592	37	55	142877710.0000	auto	2026-03-07 15:00:21.637858
593	37	56	9669126.0000	auto	2026-03-07 15:00:21.78306
594	37	57	142909908.0000	auto	2026-03-07 15:00:21.930015
595	37	58	11915156.5940	auto	2026-03-07 15:00:22.078956
596	37	59	324250.0000	auto	2026-03-07 15:00:22.218294
597	37	16	14657778.0000	auto	2026-03-07 15:00:22.355244
598	37	39	43683337.0000	auto	2026-03-07 15:00:22.519628
599	37	43	1512152.0000	auto	2026-03-07 15:00:22.660125
600	37	44	6263.0000	auto	2026-03-07 15:00:22.813809
601	37	46	66192.0000	auto	2026-03-07 15:00:22.962215
602	37	49	12743.0000	auto	2026-03-07 15:00:23.108044
603	37	50	270193.0000	auto	2026-03-07 15:00:23.256964
605	38	52	77112213.0000	auto	2026-03-07 15:00:24.338446
606	38	53	100983004.0000	auto	2026-03-07 15:00:24.509124
607	38	54	155411801.0000	auto	2026-03-07 15:00:24.651017
608	38	60	302011.0000	auto	2026-03-07 15:00:24.791317
609	38	55	142892602.0000	auto	2026-03-07 15:00:24.926873
610	38	56	9675696.0000	auto	2026-03-07 15:00:25.069934
611	38	57	129311816.0000	auto	2026-03-07 15:00:25.23237
612	38	58	11839375.0330	auto	2026-03-07 15:00:25.388089
613	38	59	315191.0000	auto	2026-03-07 15:00:25.555389
614	38	16	14665372.0000	auto	2026-03-07 15:00:25.711637
615	38	39	42710880.0000	auto	2026-03-07 15:00:25.858788
616	38	43	962097.0000	auto	2026-03-07 15:00:26.005801
617	38	44	26263.0000	auto	2026-03-07 15:00:26.167157
618	38	46	66192.0000	auto	2026-03-07 15:00:26.33195
619	38	49	12743.0000	auto	2026-03-07 15:00:26.477717
620	38	50	270193.0000	auto	2026-03-07 15:00:26.638182
622	39	52	73939123.0000	auto	2026-03-07 15:00:27.59501
623	39	53	98006699.0000	auto	2026-03-07 15:00:27.759009
624	39	54	145718362.0000	auto	2026-03-07 15:00:27.919525
625	39	60	282871.0000	auto	2026-03-07 15:00:28.055073
626	39	55	140529479.0000	auto	2026-03-07 15:00:28.207302
627	39	56	9648533.0000	auto	2026-03-07 15:00:28.358731
628	39	57	102234626.0000	auto	2026-03-07 15:00:28.51362
629	39	58	11783857.3520	auto	2026-03-07 15:00:28.641643
630	39	59	289930.0000	auto	2026-03-07 15:00:28.770509
631	39	16	14672970.0000	auto	2026-03-07 15:00:28.910658
2292	102	52	119129584.0000	auto	2026-03-07 15:02:57.056068
2293	102	53	482629306.0000	auto	2026-03-07 15:02:57.056068
2294	102	54	55499183.0000	auto	2026-03-07 15:02:57.056068
2295	102	60	41687.0000	auto	2026-03-07 15:02:57.056068
2296	102	55	102856277.0000	auto	2026-03-07 15:02:57.056068
2297	102	56	31453583.0000	auto	2026-03-07 15:02:57.056068
2298	102	57	220661316.2920	auto	2026-03-07 15:02:57.056068
2299	102	58	14860109.5800	auto	2026-03-07 15:02:57.056068
2300	102	59	1095858.0000	auto	2026-03-07 15:02:57.056068
2301	102	16	21981945.0000	auto	2026-03-07 15:02:57.056068
2302	102	39	16983303.0000	auto	2026-03-07 15:02:57.056068
2303	102	43	1556824.0000	auto	2026-03-07 15:02:57.056068
2304	102	44	134263.0000	auto	2026-03-07 15:02:57.056068
2305	102	46	166315.0000	auto	2026-03-07 15:02:57.056068
2306	102	49	4653.0000	auto	2026-03-07 15:02:57.056068
2307	102	50	370453.0000	auto	2026-03-07 15:02:57.056068
161	13	52	66480745.0000	auto	2026-03-07 14:59:01.743679
162	13	53	82357410.0000	auto	2026-03-07 14:59:01.883106
163	13	54	124814930.0000	auto	2026-03-07 14:59:02.047795
164	13	60	44029994.0000	auto	2026-03-07 14:59:02.226572
165	13	55	122892553.0680	auto	2026-03-07 14:59:02.396359
166	13	56	6292319.0000	auto	2026-03-07 14:59:02.550537
167	13	57	43438857.6220	auto	2026-03-07 14:59:02.7198
168	13	58	7112684.7420	auto	2026-03-07 14:59:02.883266
169	13	59	102331.0000	auto	2026-03-07 14:59:03.062064
170	13	16	4832740.0000	auto	2026-03-07 14:59:03.228185
171	13	39	44630781.0000	auto	2026-03-07 14:59:03.408201
172	13	43	3152700.0000	auto	2026-03-07 14:59:03.556663
173	13	44	114638.0000	auto	2026-03-07 14:59:03.70691
174	13	46	267599.0000	auto	2026-03-07 14:59:03.862759
175	13	49	12910.0000	auto	2026-03-07 14:59:04.015405
176	13	50	220095.0000	auto	2026-03-07 14:59:04.182042
177	13	48	16600000.0000	auto	2026-03-07 14:59:04.333696
194	14	48	16600000.0000	auto	2026-03-07 14:59:07.710177
210	15	49	12910.0000	auto	2026-03-07 14:59:10.953783
211	15	50	220095.0000	auto	2026-03-07 14:59:11.146805
212	15	48	16600000.0000	auto	2026-03-07 14:59:11.295361
230	16	48	16600000.0000	auto	2026-03-07 14:59:14.999365
237	17	57	47951277.0000	auto	2026-03-07 14:59:16.776431
238	17	58	8037070.0960	auto	2026-03-07 14:59:16.94788
239	17	59	154983.3840	auto	2026-03-07 14:59:17.094809
240	17	16	30373740.0000	auto	2026-03-07 14:59:17.251109
241	17	38	18668117.0000	auto	2026-03-07 14:59:17.416708
242	17	39	45190818.0000	auto	2026-03-07 14:59:17.566914
243	17	43	511586.0000	auto	2026-03-07 14:59:17.735857
244	17	44	147800.0000	auto	2026-03-07 14:59:17.876194
245	17	46	1815841.0000	auto	2026-03-07 14:59:18.031778
246	17	49	12983.0000	auto	2026-03-07 14:59:18.167435
247	17	50	220095.0000	auto	2026-03-07 14:59:18.334139
248	17	48	16600000.0000	auto	2026-03-07 14:59:18.487736
260	18	39	49217420.0000	auto	2026-03-07 14:59:20.966125
261	18	43	1474582.0000	auto	2026-03-07 14:59:21.107208
262	18	44	32800.0000	auto	2026-03-07 14:59:20.795647
263	18	46	25841.0000	auto	2026-03-07 14:59:20.947104
264	18	49	12983.0000	auto	2026-03-07 14:59:20.507491
265	18	50	230095.0000	auto	2026-03-07 14:59:20.651848
266	18	48	16700000.0000	auto	2026-03-07 14:59:20.794952
284	19	48	16700000.0000	auto	2026-03-07 14:59:24.400181
302	20	48	16700000.0000	auto	2026-03-07 14:59:27.869449
320	21	48	16700000.0000	auto	2026-03-07 14:59:31.244689
337	22	50	240095.0000	auto	2026-03-07 14:59:34.84803
338	22	48	16800000.0000	auto	2026-03-07 14:59:35.027667
356	23	48	16800000.0000	auto	2026-03-07 14:59:38.472468
639	40	52	77734636.0000	auto	2026-03-07 15:00:30.747416
640	40	53	103339448.0000	auto	2026-03-07 15:00:30.903626
641	40	54	159533506.0000	auto	2026-03-07 15:00:31.051112
642	40	60	283081.0000	auto	2026-03-07 15:00:31.18172
643	40	55	143505811.0000	auto	2026-03-07 15:00:31.309379
644	40	56	10295273.0000	auto	2026-03-07 15:00:31.491219
656	41	52	78798567.0000	auto	2026-03-07 15:00:33.895108
657	41	53	106224208.0000	auto	2026-03-07 15:00:34.040461
658	41	54	167315891.0000	auto	2026-03-07 15:00:34.182909
659	41	60	272241.0000	auto	2026-03-07 15:00:34.3264
660	41	55	144110621.0000	auto	2026-03-07 15:00:34.467715
661	41	56	10446473.0000	auto	2026-03-07 15:00:34.618591
662	41	57	131871870.0000	auto	2026-03-07 15:00:34.777853
663	41	58	11966658.1400	auto	2026-03-07 15:00:34.938552
664	41	59	372363.9600	auto	2026-03-07 15:00:35.075609
665	41	16	11185296.0000	auto	2026-03-07 15:00:35.212746
666	41	39	37814834.0000	auto	2026-03-07 15:00:35.363894
667	41	43	1831773.0000	auto	2026-03-07 15:00:35.515147
668	41	44	3588.0000	auto	2026-03-07 15:00:35.676647
669	41	46	76207.0000	auto	2026-03-07 15:00:35.817203
670	41	49	12781.0000	auto	2026-03-07 15:00:35.964758
671	41	50	280193.0000	auto	2026-03-07 15:00:36.117257
673	42	52	79319396.0000	auto	2026-03-07 15:00:37.18324
674	42	53	106716505.0000	auto	2026-03-07 15:00:37.32736
675	42	54	168818235.0000	auto	2026-03-07 15:00:37.463901
676	42	60	289361.0000	auto	2026-03-07 15:00:37.621525
677	42	55	143757901.0000	auto	2026-03-07 15:00:37.7592
678	42	56	10626393.0000	auto	2026-03-07 15:00:37.907253
679	42	57	135933901.0000	auto	2026-03-07 15:00:38.051199
680	42	58	12033801.4770	auto	2026-03-07 15:00:38.207232
681	42	59	376172.2120	auto	2026-03-07 15:00:38.363115
682	42	16	11191071.0000	auto	2026-03-07 15:00:38.516407
683	42	39	36834352.0000	auto	2026-03-07 15:00:38.695012
684	42	43	1519218.0000	auto	2026-03-07 15:00:38.85606
685	42	44	3588.0000	auto	2026-03-07 15:00:39.01552
686	42	46	76207.0000	auto	2026-03-07 15:00:39.176458
687	42	49	12781.0000	auto	2026-03-07 15:00:39.358944
688	42	50	280193.0000	auto	2026-03-07 15:00:39.554426
690	43	52	79394387.0000	auto	2026-03-07 15:00:40.576572
691	43	53	106091697.0000	auto	2026-03-07 15:00:40.707298
692	43	54	167807890.0000	auto	2026-03-07 15:00:40.864648
693	43	60	274301.0000	auto	2026-03-07 15:00:41.019849
694	43	55	143990034.8630	auto	2026-03-07 15:00:41.159755
695	43	56	10709563.0000	auto	2026-03-07 15:00:41.305687
696	43	57	142736882.0000	auto	2026-03-07 15:00:41.443558
697	43	58	11704975.5430	auto	2026-03-07 15:00:41.599044
698	43	59	377381.9160	auto	2026-03-07 15:00:41.741721
699	43	16	10696750.0000	auto	2026-03-07 15:00:41.8978
700	43	39	35853388.0000	auto	2026-03-07 15:00:42.054968
701	43	43	1509218.0000	auto	2026-03-07 15:00:42.198725
702	43	44	8588.0000	auto	2026-03-07 15:00:42.354993
703	43	46	76207.0000	auto	2026-03-07 15:00:42.494395
704	43	49	12781.0000	auto	2026-03-07 15:00:42.651388
705	43	50	280193.0000	auto	2026-03-07 15:00:42.812636
707	44	52	82220231.0000	auto	2026-03-07 15:00:43.832747
708	44	53	109523551.0000	auto	2026-03-07 15:00:43.978805
709	44	54	177921037.0000	auto	2026-03-07 15:00:44.134013
710	44	60	283161.0000	auto	2026-03-07 15:00:44.283661
711	44	55	146281312.6830	auto	2026-03-07 15:00:44.431216
712	44	56	10771303.0000	auto	2026-03-07 15:00:44.574419
713	44	57	162913697.0000	auto	2026-03-07 15:00:44.714787
714	44	58	11968593.0520	auto	2026-03-07 15:00:44.87172
715	44	59	388541.1830	auto	2026-03-07 15:00:45.027431
370	24	44	42800.0000	auto	2026-03-07 14:59:41.36329
371	24	46	35841.0000	auto	2026-03-07 14:59:41.54402
372	24	49	12704.0000	auto	2026-03-07 14:59:41.696981
373	24	50	240095.0000	auto	2026-03-07 14:59:41.855025
374	24	48	16800000.0000	auto	2026-03-07 14:59:42.009181
379	25	55	139143296.0000	auto	2026-03-07 14:59:43.436113
380	25	56	7934409.0000	auto	2026-03-07 14:59:43.577438
381	25	57	65530553.7500	auto	2026-03-07 14:59:43.722459
382	25	58	10553019.4800	auto	2026-03-07 14:59:43.864136
383	25	59	208716.0000	auto	2026-03-07 14:59:44.009087
384	25	16	19727330.0000	auto	2026-03-07 14:59:44.137082
385	25	38	11371768.0000	auto	2026-03-07 14:59:44.277352
386	25	39	46475587.0000	auto	2026-03-07 14:59:44.431804
387	25	43	240259.0000	auto	2026-03-07 14:59:44.571789
388	25	44	17800.0000	auto	2026-03-07 14:59:44.724679
389	25	46	35841.0000	auto	2026-03-07 14:59:44.867461
390	25	49	12704.0000	auto	2026-03-07 14:59:45.028474
391	25	50	240095.0000	auto	2026-03-07 14:59:45.208622
392	25	48	16800000.0000	auto	2026-03-07 14:59:45.344692
410	26	48	16800000.0000	auto	2026-03-07 14:59:48.732683
428	27	48	16900000.0000	auto	2026-03-07 14:59:51.023641
446	28	48	16900000.0000	auto	2026-03-07 14:59:54.375815
463	29	50	250193.0000	auto	2026-03-07 14:59:57.627655
464	29	48	16900000.0000	auto	2026-03-07 14:59:57.773194
482	30	48	16900000.0000	auto	2026-03-07 15:00:01.140448
500	31	48	17000000.0000	auto	2026-03-07 15:00:04.571148
501	32	52	80796361.0000	auto	2026-03-07 15:00:05.44602
502	32	53	107748890.0000	auto	2026-03-07 15:00:05.580999
503	32	54	176645435.0000	auto	2026-03-07 15:00:05.732159
504	32	60	341211.0000	auto	2026-03-07 15:00:05.871238
505	32	55	143320313.0000	auto	2026-03-07 15:00:06.017995
506	32	56	9154126.0000	auto	2026-03-07 15:00:06.160831
507	32	57	129568577.0000	auto	2026-03-07 15:00:06.305796
508	32	58	11701494.9300	auto	2026-03-07 15:00:06.458371
509	32	59	292065.0000	auto	2026-03-07 15:00:06.596058
510	32	16	23609833.0000	auto	2026-03-07 15:00:06.752917
511	32	38	10003713.0000	auto	2026-03-07 15:00:06.912831
512	32	39	47574013.0000	auto	2026-03-07 15:00:07.064614
513	32	43	1875335.0000	auto	2026-03-07 15:00:07.200372
514	32	44	31263.0000	auto	2026-03-07 15:00:07.353694
515	32	46	56192.0000	auto	2026-03-07 15:00:07.491848
516	32	49	12743.0000	auto	2026-03-07 15:00:07.644014
517	32	50	260193.0000	auto	2026-03-07 15:00:07.798562
518	32	48	17000000.0000	auto	2026-03-07 15:00:07.942998
536	33	48	17000000.0000	auto	2026-03-07 15:00:11.366469
553	34	48	17000000.0000	auto	2026-03-07 15:00:14.479292
570	35	48	17000000.0000	auto	2026-03-07 15:00:17.867789
587	36	48	17100000.0000	auto	2026-03-07 15:00:20.194179
604	37	48	17100000.0000	auto	2026-03-07 15:00:23.400343
621	38	48	17100000.0000	auto	2026-03-07 15:00:26.793743
632	39	39	40758021.0000	auto	2026-03-07 15:00:29.050869
633	39	43	2162097.0000	auto	2026-03-07 15:00:29.201266
634	39	44	16263.0000	auto	2026-03-07 15:00:29.345273
635	39	46	66192.0000	auto	2026-03-07 15:00:29.477546
636	39	49	12743.0000	auto	2026-03-07 15:00:29.612848
637	39	50	270193.0000	auto	2026-03-07 15:00:29.762034
638	39	48	17100000.0000	auto	2026-03-07 15:00:29.907168
645	40	57	131862658.0000	auto	2026-03-07 15:00:31.644702
646	40	58	12070593.9680	auto	2026-03-07 15:00:31.781047
647	40	59	369883.0720	auto	2026-03-07 15:00:31.932165
648	40	16	11179524.0000	auto	2026-03-07 15:00:32.06864
649	40	39	38800977.0000	auto	2026-03-07 15:00:32.198537
650	40	43	1875255.0000	auto	2026-03-07 15:00:32.34168
651	40	44	6263.0000	auto	2026-03-07 15:00:32.500509
652	40	46	76192.0000	auto	2026-03-07 15:00:32.634906
653	40	49	12743.0000	auto	2026-03-07 15:00:32.781038
654	40	50	280193.0000	auto	2026-03-07 15:00:32.920169
655	40	48	17200000.0000	auto	2026-03-07 15:00:33.060189
672	41	48	17200000.0000	auto	2026-03-07 15:00:36.276082
689	42	48	17200000.0000	auto	2026-03-07 15:00:39.710263
706	43	48	17200000.0000	auto	2026-03-07 15:00:42.973195
1271	44	16	10452191.0000	auto	2026-03-07 15:02:09.23453
1272	44	39	34872723.0000	auto	2026-03-07 15:02:09.23453
1273	44	43	940278.0000	auto	2026-03-07 15:02:09.23453
1274	44	44	8588.0000	auto	2026-03-07 15:02:09.23453
1275	44	46	86207.0000	auto	2026-03-07 15:02:09.23453
1276	44	49	12799.0000	auto	2026-03-07 15:02:09.23453
1277	44	50	290193.0000	auto	2026-03-07 15:02:09.23453
1278	44	48	17300000.0000	auto	2026-03-07 15:02:09.23453
1279	45	52	83619331.0000	auto	2026-03-07 15:02:10.077758
1280	45	53	110837769.0000	auto	2026-03-07 15:02:10.077758
1281	45	54	182205463.0000	auto	2026-03-07 15:02:10.077758
1282	45	60	280661.0000	auto	2026-03-07 15:02:10.077758
1283	45	55	148115597.6830	auto	2026-03-07 15:02:10.077758
1284	45	56	11353383.0000	auto	2026-03-07 15:02:10.077758
1285	45	57	170129263.0000	auto	2026-03-07 15:02:10.077758
1286	45	58	12376683.9580	auto	2026-03-07 15:02:10.077758
1287	45	59	395283.0000	auto	2026-03-07 15:02:10.077758
1288	45	16	10407587.0000	auto	2026-03-07 15:02:10.077758
1289	45	39	33886043.0000	auto	2026-03-07 15:02:10.077758
1290	45	43	644713.0000	auto	2026-03-07 15:02:10.077758
1291	45	44	8588.0000	auto	2026-03-07 15:02:10.077758
1292	45	46	86207.0000	auto	2026-03-07 15:02:10.077758
1293	45	49	12799.0000	auto	2026-03-07 15:02:10.077758
1294	45	50	290193.0000	auto	2026-03-07 15:02:10.077758
1295	45	48	17300000.0000	auto	2026-03-07 15:02:10.077758
1296	46	52	85231357.0000	auto	2026-03-07 15:02:10.929489
1297	46	53	113864888.0000	auto	2026-03-07 15:02:10.929489
1298	46	54	194295171.0000	auto	2026-03-07 15:02:10.929489
1299	46	60	261281.0000	auto	2026-03-07 15:02:10.929489
1300	46	55	148407955.1720	auto	2026-03-07 15:02:10.929489
1301	46	56	12181423.0000	auto	2026-03-07 15:02:10.929489
1302	46	57	176284958.0000	auto	2026-03-07 15:02:10.929489
1303	46	58	12166886.2720	auto	2026-03-07 15:02:10.929489
1304	46	59	398856.0000	auto	2026-03-07 15:02:10.929489
1305	46	16	10287801.0000	auto	2026-03-07 15:02:10.929489
1306	46	39	32905263.0000	auto	2026-03-07 15:02:10.929489
1307	46	43	217213.0000	auto	2026-03-07 15:02:10.929489
1308	46	44	8588.0000	auto	2026-03-07 15:02:10.929489
1309	46	46	86207.0000	auto	2026-03-07 15:02:10.929489
1310	46	49	12799.0000	auto	2026-03-07 15:02:10.929489
1311	46	50	290193.0000	auto	2026-03-07 15:02:10.929489
1312	46	48	17300000.0000	auto	2026-03-07 15:02:10.929489
1313	47	52	83815977.0000	auto	2026-03-07 15:02:11.77819
1314	47	53	113145786.0000	auto	2026-03-07 15:02:11.77819
1315	47	54	187974598.0000	auto	2026-03-07 15:02:11.77819
1316	47	60	261281.0000	auto	2026-03-07 15:02:11.77819
1317	47	55	146989782.2530	auto	2026-03-07 15:02:11.77819
1318	47	56	11968933.0000	auto	2026-03-07 15:02:11.77819
1319	47	57	165229254.0000	auto	2026-03-07 15:02:11.77819
1320	47	58	11923080.0690	auto	2026-03-07 15:02:11.77819
1321	47	59	391216.0000	auto	2026-03-07 15:02:11.77819
1322	47	16	10162846.0000	auto	2026-03-07 15:02:11.77819
1323	47	39	31924870.0000	auto	2026-03-07 15:02:11.77819
1324	47	43	1112158.0000	auto	2026-03-07 15:02:11.77819
1325	47	44	8588.0000	auto	2026-03-07 15:02:11.77819
1326	47	46	86207.0000	auto	2026-03-07 15:02:11.77819
1327	47	49	12799.0000	auto	2026-03-07 15:02:11.77819
1328	47	50	290193.0000	auto	2026-03-07 15:02:11.77819
1329	47	48	17300000.0000	auto	2026-03-07 15:02:11.77819
1330	48	52	88482467.0000	auto	2026-03-07 15:02:12.650479
1331	48	53	121097836.0000	auto	2026-03-07 15:02:12.650479
1332	48	54	216014222.0000	auto	2026-03-07 15:02:12.650479
1333	48	60	261281.0000	auto	2026-03-07 15:02:12.650479
1334	48	55	151660587.2700	auto	2026-03-07 15:02:12.650479
1335	48	56	11761283.0000	auto	2026-03-07 15:02:12.650479
1336	48	57	198775281.0000	auto	2026-03-07 15:02:12.650479
1337	48	58	12385203.1000	auto	2026-03-07 15:02:12.650479
1338	48	59	467236.0000	auto	2026-03-07 15:02:12.650479
1339	48	16	10042821.0000	auto	2026-03-07 15:02:12.650479
1340	48	38	68.0000	auto	2026-03-07 15:02:12.650479
1341	48	39	30945040.0000	auto	2026-03-07 15:02:12.650479
1342	48	43	1262158.0000	auto	2026-03-07 15:02:12.650479
1343	48	44	8588.0000	auto	2026-03-07 15:02:12.650479
1344	48	46	86207.0000	auto	2026-03-07 15:02:12.650479
1345	48	49	12799.0000	auto	2026-03-07 15:02:12.650479
1346	48	50	290193.0000	auto	2026-03-07 15:02:12.650479
1347	48	48	17300000.0000	auto	2026-03-07 15:02:12.650479
1348	49	52	88389882.0000	auto	2026-03-07 15:02:13.476698
1349	49	53	120876079.0000	auto	2026-03-07 15:02:13.476698
1350	49	54	209895429.0000	auto	2026-03-07 15:02:13.476698
1351	49	60	270698.0000	auto	2026-03-07 15:02:13.476698
1352	49	55	150455625.5450	auto	2026-03-07 15:02:13.476698
1353	49	56	11354863.0000	auto	2026-03-07 15:02:13.476698
1354	49	57	185732299.0000	auto	2026-03-07 15:02:13.476698
1355	49	58	12410688.7550	auto	2026-03-07 15:02:13.476698
1356	49	59	451078.0000	auto	2026-03-07 15:02:13.476698
1357	49	16	8341168.0000	auto	2026-03-07 15:02:13.476698
1358	49	39	29870121.0000	auto	2026-03-07 15:02:13.476698
1359	49	43	684514.0000	auto	2026-03-07 15:02:13.476698
1360	49	44	8588.0000	auto	2026-03-07 15:02:13.476698
1361	49	46	96207.0000	auto	2026-03-07 15:02:13.476698
1362	49	49	12818.0000	auto	2026-03-07 15:02:13.476698
1363	49	50	300193.0000	auto	2026-03-07 15:02:13.476698
1364	49	48	17400000.0000	auto	2026-03-07 15:02:13.476698
1365	50	52	88107391.0000	auto	2026-03-07 15:02:14.383544
1366	50	53	119405672.0000	auto	2026-03-07 15:02:14.383544
1367	50	54	205293452.0000	auto	2026-03-07 15:02:14.383544
1368	50	60	279778.0000	auto	2026-03-07 15:02:14.383544
1369	50	55	151409580.0000	auto	2026-03-07 15:02:14.383544
1370	50	56	12071623.0000	auto	2026-03-07 15:02:14.383544
1371	50	57	190332102.0000	auto	2026-03-07 15:02:14.383544
1372	50	58	12557753.0000	auto	2026-03-07 15:02:14.383544
1373	50	59	444334.0000	auto	2026-03-07 15:02:14.383544
1374	50	16	8315358.0000	auto	2026-03-07 15:02:14.383544
1375	50	39	28890030.0000	auto	2026-03-07 15:02:14.383544
1376	50	43	637214.0000	auto	2026-03-07 15:02:14.383544
1377	50	44	8588.0000	auto	2026-03-07 15:02:14.383544
1378	50	46	96207.0000	auto	2026-03-07 15:02:14.383544
1379	50	49	12822.0000	auto	2026-03-07 15:02:14.383544
1380	50	50	300193.0000	auto	2026-03-07 15:02:14.383544
1381	50	48	17400000.0000	auto	2026-03-07 15:02:14.383544
1382	51	52	87287595.0000	auto	2026-03-07 15:02:14.171797
1383	51	53	119299115.0000	auto	2026-03-07 15:02:14.171797
1384	51	54	204678775.0000	auto	2026-03-07 15:02:14.171797
1385	51	60	270578.0000	auto	2026-03-07 15:02:14.171797
1386	51	55	152314929.0000	auto	2026-03-07 15:02:14.171797
1387	51	56	12003843.0000	auto	2026-03-07 15:02:14.171797
1388	51	57	185214287.0000	auto	2026-03-07 15:02:14.171797
1389	51	58	12741925.5500	auto	2026-03-07 15:02:14.171797
1390	51	59	447858.0000	auto	2026-03-07 15:02:14.171797
1391	51	16	8195479.0000	auto	2026-03-07 15:02:14.171797
1392	51	39	27908472.0000	auto	2026-03-07 15:02:14.171797
1393	51	43	727159.0000	auto	2026-03-07 15:02:14.171797
1394	51	44	8588.0000	auto	2026-03-07 15:02:14.171797
1395	51	46	96207.0000	auto	2026-03-07 15:02:14.171797
1396	51	49	12822.0000	auto	2026-03-07 15:02:14.171797
1397	51	50	300193.0000	auto	2026-03-07 15:02:14.171797
1398	51	48	17400000.0000	auto	2026-03-07 15:02:14.171797
1399	52	52	91926700.0000	auto	2026-03-07 15:02:15.183027
1400	52	53	126814405.0000	auto	2026-03-07 15:02:15.183027
1401	52	54	231640988.0000	auto	2026-03-07 15:02:15.183027
1402	52	60	275778.0000	auto	2026-03-07 15:02:15.183027
1403	52	55	154895009.0000	auto	2026-03-07 15:02:15.183027
1404	52	56	12280543.0000	auto	2026-03-07 15:02:15.183027
1405	52	57	209259368.0000	auto	2026-03-07 15:02:15.183027
1406	52	58	12856972.4400	auto	2026-03-07 15:02:15.183027
1407	52	59	473310.0000	auto	2026-03-07 15:02:15.183027
1408	52	16	8078530.0000	auto	2026-03-07 15:02:15.183027
1409	52	39	27908472.0000	auto	2026-03-07 15:02:15.183027
1410	52	43	847159.0000	auto	2026-03-07 15:02:15.183027
1411	52	44	8588.0000	auto	2026-03-07 15:02:15.183027
1412	52	46	96207.0000	auto	2026-03-07 15:02:15.183027
1413	52	49	12837.0000	auto	2026-03-07 15:02:15.183027
1414	52	50	300193.0000	auto	2026-03-07 15:02:15.183027
1415	52	48	17400000.0000	auto	2026-03-07 15:02:15.183027
1416	53	52	94707213.0000	auto	2026-03-07 15:02:16.045587
1417	53	53	133428940.0000	auto	2026-03-07 15:02:16.045587
1418	53	54	253031261.0000	auto	2026-03-07 15:02:16.045587
1419	53	60	294458.0000	auto	2026-03-07 15:02:16.045587
1420	53	55	155389616.0000	auto	2026-03-07 15:02:16.045587
1421	53	56	12703693.0000	auto	2026-03-07 15:02:16.045587
1422	53	57	196381216.8960	auto	2026-03-07 15:02:16.045587
1423	53	58	12742192.3360	auto	2026-03-07 15:02:16.045587
1424	53	59	524825.5200	auto	2026-03-07 15:02:16.045587
1425	53	16	7957514.0000	auto	2026-03-07 15:02:16.045587
1426	53	39	26927845.0000	auto	2026-03-07 15:02:16.045587
1427	53	43	747502.0000	auto	2026-03-07 15:02:16.045587
1428	53	44	8588.0000	auto	2026-03-07 15:02:16.045587
1429	53	46	106255.0000	auto	2026-03-07 15:02:16.045587
1430	53	49	12837.0000	auto	2026-03-07 15:02:16.045587
1431	53	50	310193.0000	auto	2026-03-07 15:02:16.045587
1432	53	48	17500000.0000	auto	2026-03-07 15:02:16.045587
1433	54	52	93558727.0000	auto	2026-03-07 15:02:16.909892
1434	54	53	372502625.0000	auto	2026-03-07 15:02:16.909892
1435	54	54	10812635.0000	auto	2026-03-07 15:02:16.909892
1436	54	60	278838.0000	auto	2026-03-07 15:02:16.909892
1437	54	55	154629545.0000	auto	2026-03-07 15:02:16.909892
1438	54	56	12514993.0000	auto	2026-03-07 15:02:16.909892
1439	54	57	205010822.2550	auto	2026-03-07 15:02:16.909892
1440	54	58	12516583.8450	auto	2026-03-07 15:02:16.909892
1441	54	59	524334.7600	auto	2026-03-07 15:02:16.909892
1442	54	39	22022475.0000	auto	2026-03-07 15:02:16.909892
1443	54	43	2695827.0000	auto	2026-03-07 15:02:16.909892
1444	54	44	8591.0000	auto	2026-03-07 15:02:16.909892
1445	54	46	106255.0000	auto	2026-03-07 15:02:16.909892
1446	54	49	12837.0000	auto	2026-03-07 15:02:16.909892
1447	54	50	310316.0000	auto	2026-03-07 15:02:16.909892
1448	54	48	17500000.0000	auto	2026-03-07 15:02:16.909892
1449	55	52	97776457.0000	auto	2026-03-07 15:02:17.738473
1450	55	53	388785979.0000	auto	2026-03-07 15:02:17.738473
1451	55	54	16572862.0000	auto	2026-03-07 15:02:17.738473
1452	55	60	279338.0000	auto	2026-03-07 15:02:17.738473
1453	55	55	155998273.0000	auto	2026-03-07 15:02:17.738473
1454	55	56	12918913.0000	auto	2026-03-07 15:02:17.738473
1455	55	57	210580350.3550	auto	2026-03-07 15:02:17.738473
1456	55	58	12544326.2550	auto	2026-03-07 15:02:17.738473
1457	55	59	533453.2800	auto	2026-03-07 15:02:17.738473
1458	55	39	17124244.0000	auto	2026-03-07 15:02:17.738473
1459	55	43	2543272.0000	auto	2026-03-07 15:02:17.738473
1460	55	44	8591.0000	auto	2026-03-07 15:02:17.738473
1461	55	46	106229.0000	auto	2026-03-07 15:02:17.738473
1462	55	49	12837.0000	auto	2026-03-07 15:02:17.738473
1463	55	50	310316.0000	auto	2026-03-07 15:02:17.738473
1464	55	48	17500000.0000	auto	2026-03-07 15:02:17.738473
1465	55	47	9000.0000	auto	2026-03-07 15:02:17.738473
1466	56	52	95415052.0000	auto	2026-03-07 15:02:18.591167
1467	56	53	380725214.0000	auto	2026-03-07 15:02:18.591167
1468	56	54	20939258.0000	auto	2026-03-07 15:02:18.591167
1469	56	60	276998.0000	auto	2026-03-07 15:02:18.591167
1470	56	55	156101725.3300	auto	2026-03-07 15:02:18.591167
1471	56	56	13271923.0000	auto	2026-03-07 15:02:18.591167
1472	56	57	212977427.6970	auto	2026-03-07 15:02:18.591167
1473	56	58	12709269.4240	auto	2026-03-07 15:02:18.591167
1474	56	59	539817.1520	auto	2026-03-07 15:02:18.591167
1475	56	39	17124244.0000	auto	2026-03-07 15:02:18.591167
1476	56	43	3043273.0000	auto	2026-03-07 15:02:18.591167
1477	56	44	8591.0000	auto	2026-03-07 15:02:18.591167
1478	56	46	106229.0000	auto	2026-03-07 15:02:18.591167
1479	56	49	12853.0000	auto	2026-03-07 15:02:18.591167
1480	56	50	310316.0000	auto	2026-03-07 15:02:18.591167
1481	56	48	17500000.0000	auto	2026-03-07 15:02:18.591167
1482	57	52	95099256.0000	auto	2026-03-07 15:02:19.470618
1483	57	53	378735067.0000	auto	2026-03-07 15:02:19.470618
1484	57	54	25528426.0000	auto	2026-03-07 15:02:19.470618
1485	57	60	277118.0000	auto	2026-03-07 15:02:19.470618
1486	57	55	148604340.0000	auto	2026-03-07 15:02:19.470618
1487	57	56	13309376.0000	auto	2026-03-07 15:02:19.470618
1488	57	57	190709699.3940	auto	2026-03-07 15:02:19.470618
1489	57	58	12338603.4240	auto	2026-03-07 15:02:19.470618
1490	57	59	581727.1520	auto	2026-03-07 15:02:19.470618
1491	57	16	535630.0000	auto	2026-03-07 15:02:19.470618
1492	57	39	17124244.0000	auto	2026-03-07 15:02:19.470618
1493	57	43	1856133.0000	auto	2026-03-07 15:02:19.470618
1494	57	44	8591.0000	auto	2026-03-07 15:02:19.470618
1495	57	46	106229.0000	auto	2026-03-07 15:02:19.470618
1496	57	49	12853.0000	auto	2026-03-07 15:02:19.470618
1497	57	50	310316.0000	auto	2026-03-07 15:02:19.470618
1498	57	48	17600000.0000	auto	2026-03-07 15:02:19.470618
1499	58	52	93992371.0000	auto	2026-03-07 15:02:20.325246
1500	58	53	375087341.0000	auto	2026-03-07 15:02:20.325246
1501	58	54	25044601.0000	auto	2026-03-07 15:02:20.325246
1502	58	60	277118.0000	auto	2026-03-07 15:02:20.325246
1503	58	55	150294177.0000	auto	2026-03-07 15:02:20.325246
1504	58	56	13408183.0000	auto	2026-03-07 15:02:20.325246
1505	58	57	198658398.0000	auto	2026-03-07 15:02:20.325246
1506	58	58	12797632.5450	auto	2026-03-07 15:02:20.325246
1507	58	59	556978.0000	auto	2026-03-07 15:02:20.325246
1508	58	16	392245.0000	auto	2026-03-07 15:02:20.325246
1509	58	39	17118600.0000	auto	2026-03-07 15:02:20.325246
1510	58	43	1499888.0000	auto	2026-03-07 15:02:20.325246
1511	58	44	8591.0000	auto	2026-03-07 15:02:20.325246
1512	58	46	106229.0000	auto	2026-03-07 15:02:20.325246
1513	58	49	12853.0000	auto	2026-03-07 15:02:20.325246
1514	58	50	310316.0000	auto	2026-03-07 15:02:20.325246
1515	58	48	17600000.0000	auto	2026-03-07 15:02:20.325246
1516	59	52	95805347.0000	auto	2026-03-07 15:02:21.19068
1517	59	53	382148852.0000	auto	2026-03-07 15:02:21.19068
1518	59	54	25817011.0000	auto	2026-03-07 15:02:21.19068
1519	59	60	260658.0000	auto	2026-03-07 15:02:21.19068
1520	59	55	148820750.0000	auto	2026-03-07 15:02:21.19068
1521	59	56	13691806.0000	auto	2026-03-07 15:02:21.19068
1522	59	57	215945791.0000	auto	2026-03-07 15:02:21.19068
1523	59	58	12700653.5450	auto	2026-03-07 15:02:21.19068
1524	59	59	566561.0000	auto	2026-03-07 15:02:21.19068
1525	59	16	367471.0000	auto	2026-03-07 15:02:21.19068
1526	59	39	17118600.0000	auto	2026-03-07 15:02:21.19068
1527	59	43	1417388.0000	auto	2026-03-07 15:02:21.19068
1528	59	44	8591.0000	auto	2026-03-07 15:02:21.19068
1529	59	46	106229.0000	auto	2026-03-07 15:02:21.19068
1530	59	49	12853.0000	auto	2026-03-07 15:02:21.19068
1531	59	50	310316.0000	auto	2026-03-07 15:02:21.19068
1532	59	48	17600000.0000	auto	2026-03-07 15:02:21.19068
1533	60	52	94366774.0000	auto	2026-03-07 15:02:22.019
1534	60	53	380823647.0000	auto	2026-03-07 15:02:22.019
1535	60	54	25585883.0000	auto	2026-03-07 15:02:22.019
1536	60	60	256258.0000	auto	2026-03-07 15:02:22.019
1537	60	55	148525998.0000	auto	2026-03-07 15:02:22.019
1538	60	56	13996112.0000	auto	2026-03-07 15:02:22.019
1539	60	57	178287255.6200	auto	2026-03-07 15:02:22.019
1540	60	58	12639915.6950	auto	2026-03-07 15:02:22.019
1541	60	59	537141.0000	auto	2026-03-07 15:02:22.019
1542	60	16	367633.0000	auto	2026-03-07 15:02:22.019
1543	60	39	15164545.0000	auto	2026-03-07 15:02:22.019
1544	60	43	1417388.0000	auto	2026-03-07 15:02:22.019
1545	60	44	8591.0000	auto	2026-03-07 15:02:22.019
1546	60	46	106229.0000	auto	2026-03-07 15:02:22.019
1547	60	49	12853.0000	auto	2026-03-07 15:02:22.019
1548	60	50	310316.0000	auto	2026-03-07 15:02:22.019
1549	60	48	17600000.0000	auto	2026-03-07 15:02:22.019
1550	61	52	93865191.0000	auto	2026-03-07 15:02:22.917156
1551	61	53	379206169.0000	auto	2026-03-07 15:02:22.917156
1552	61	54	30549068.0000	auto	2026-03-07 15:02:22.917156
1553	61	60	252925.0000	auto	2026-03-07 15:02:22.917156
1554	61	55	142106113.0000	auto	2026-03-07 15:02:22.917156
1555	61	56	15293056.0000	auto	2026-03-07 15:02:22.917156
1556	61	57	191091611.0000	auto	2026-03-07 15:02:22.917156
1557	61	58	12855945.9650	auto	2026-03-07 15:02:22.917156
1558	61	59	533637.9850	auto	2026-03-07 15:02:22.917156
1559	61	16	367822.0000	auto	2026-03-07 15:02:22.917156
1560	61	39	14188095.0000	auto	2026-03-07 15:02:22.917156
1561	61	43	1417388.0000	auto	2026-03-07 15:02:22.917156
1562	61	44	8591.0000	auto	2026-03-07 15:02:22.917156
1563	61	46	106229.0000	auto	2026-03-07 15:02:22.917156
1564	61	49	12853.0000	auto	2026-03-07 15:02:22.917156
1565	61	50	310316.0000	auto	2026-03-07 15:02:22.917156
1566	61	48	17600000.0000	auto	2026-03-07 15:02:22.917156
1567	61	47	9000.0000	auto	2026-03-07 15:02:22.917156
1568	62	52	94938939.0000	auto	2026-03-07 15:02:23.758431
1569	62	53	380665579.0000	auto	2026-03-07 15:02:23.758431
1570	62	54	30723181.0000	auto	2026-03-07 15:02:23.758431
1571	62	60	257965.0000	auto	2026-03-07 15:02:23.758431
1572	62	55	143290219.0000	auto	2026-03-07 15:02:23.758431
1573	62	56	17175706.0000	auto	2026-03-07 15:02:23.758431
1574	62	57	211830831.0000	auto	2026-03-07 15:02:23.758431
1575	62	58	12832796.8020	auto	2026-03-07 15:02:23.758431
1576	62	59	541894.4990	auto	2026-03-07 15:02:23.758431
1577	62	16	368011.0000	auto	2026-03-07 15:02:23.758431
1578	62	39	14165882.0000	auto	2026-03-07 15:02:23.758431
1579	62	43	1417388.0000	auto	2026-03-07 15:02:23.758431
1580	62	44	8591.0000	auto	2026-03-07 15:02:23.758431
1581	62	46	106229.0000	auto	2026-03-07 15:02:23.758431
1582	62	49	12869.0000	auto	2026-03-07 15:02:23.758431
1583	62	50	310316.0000	auto	2026-03-07 15:02:23.758431
1584	62	48	17600000.0000	auto	2026-03-07 15:02:23.758431
1585	62	47	9000.0000	auto	2026-03-07 15:02:23.758431
1586	63	52	94642727.0000	auto	2026-03-07 15:02:24.669917
1587	63	53	376580789.0000	auto	2026-03-07 15:02:24.669917
1588	63	54	30131400.0000	auto	2026-03-07 15:02:24.669917
1589	63	60	250185.0000	auto	2026-03-07 15:02:24.669917
1590	63	55	141242690.0000	auto	2026-03-07 15:02:24.669917
1591	63	56	15543256.0000	auto	2026-03-07 15:02:24.669917
1592	63	57	187594766.0000	auto	2026-03-07 15:02:24.669917
1593	63	58	12834799.7170	auto	2026-03-07 15:02:24.669917
1594	63	59	523196.4990	auto	2026-03-07 15:02:24.669917
1595	63	16	524744.0000	auto	2026-03-07 15:02:24.669917
1596	63	39	14165882.0000	auto	2026-03-07 15:02:24.669917
1597	63	43	1417388.0000	auto	2026-03-07 15:02:24.669917
1598	63	44	8591.0000	auto	2026-03-07 15:02:24.669917
1599	63	46	106229.0000	auto	2026-03-07 15:02:24.669917
1600	63	49	12869.0000	auto	2026-03-07 15:02:24.669917
1601	63	50	310316.0000	auto	2026-03-07 15:02:24.669917
1602	63	48	17600000.0000	auto	2026-03-07 15:02:24.669917
1603	63	47	9000.0000	auto	2026-03-07 15:02:24.669917
1604	64	52	89375935.0000	auto	2026-03-07 15:02:25.501168
1605	64	53	356048269.0000	auto	2026-03-07 15:02:25.501168
1606	64	54	30131400.0000	auto	2026-03-07 15:02:25.501168
1607	64	60	239425.0000	auto	2026-03-07 15:02:25.501168
1608	64	55	141267929.0000	auto	2026-03-07 15:02:25.501168
1609	64	56	14744016.0000	auto	2026-03-07 15:02:25.501168
1610	64	57	163367370.0000	auto	2026-03-07 15:02:25.501168
1611	64	58	12868330.0000	auto	2026-03-07 15:02:25.501168
1612	64	59	502393.6000	auto	2026-03-07 15:02:25.501168
1613	64	16	525010.0000	auto	2026-03-07 15:02:25.501168
1614	64	39	14165882.0000	auto	2026-03-07 15:02:25.501168
1615	64	43	1417388.0000	auto	2026-03-07 15:02:25.501168
1616	64	44	8591.0000	auto	2026-03-07 15:02:25.501168
1617	64	46	106229.0000	auto	2026-03-07 15:02:25.501168
1618	64	49	12883.0000	auto	2026-03-07 15:02:25.501168
1619	64	50	310316.0000	auto	2026-03-07 15:02:25.501168
1620	64	48	17600000.0000	auto	2026-03-07 15:02:25.501168
1621	64	47	9000.0000	auto	2026-03-07 15:02:25.501168
1622	65	52	86369623.0000	auto	2026-03-07 15:02:26.37263
1623	65	53	343965795.0000	auto	2026-03-07 15:02:26.37263
1624	65	54	25377578.0000	auto	2026-03-07 15:02:26.37263
1625	65	60	239425.0000	auto	2026-03-07 15:02:26.37263
1626	65	55	139049867.0000	auto	2026-03-07 15:02:26.37263
1627	65	56	14825646.0000	auto	2026-03-07 15:02:26.37263
1628	65	57	133162484.0000	auto	2026-03-07 15:02:26.37263
1629	65	58	12796832.6000	auto	2026-03-07 15:02:26.37263
1630	65	59	485364.6000	auto	2026-03-07 15:02:26.37263
1631	65	16	525273.0000	auto	2026-03-07 15:02:26.37263
1632	65	39	12217091.0000	auto	2026-03-07 15:02:26.37263
1633	65	43	1417388.0000	auto	2026-03-07 15:02:26.37263
1634	65	44	8591.0000	auto	2026-03-07 15:02:26.37263
1635	65	46	106229.0000	auto	2026-03-07 15:02:26.37263
1636	65	49	12883.0000	auto	2026-03-07 15:02:26.37263
1637	65	50	310316.0000	auto	2026-03-07 15:02:26.37263
1638	65	48	17600000.0000	auto	2026-03-07 15:02:26.37263
1639	65	47	9000.0000	auto	2026-03-07 15:02:26.37263
1640	66	52	84837691.0000	auto	2026-03-07 15:02:27.262704
1641	66	53	334014405.0000	auto	2026-03-07 15:02:27.262704
1642	66	54	23910633.0000	auto	2026-03-07 15:02:27.262704
1643	66	60	248240.0000	auto	2026-03-07 15:02:27.262704
1644	66	55	137939197.0000	auto	2026-03-07 15:02:27.262704
1645	66	56	14952846.0000	auto	2026-03-07 15:02:27.262704
1646	66	57	140008717.0000	auto	2026-03-07 15:02:27.262704
1647	66	58	12659133.8000	auto	2026-03-07 15:02:27.262704
1648	66	59	490802.0000	auto	2026-03-07 15:02:27.262704
1649	66	16	525518.0000	auto	2026-03-07 15:02:27.262704
1650	66	39	12217091.0000	auto	2026-03-07 15:02:27.262704
1651	66	43	1417388.0000	auto	2026-03-07 15:02:27.262704
1652	66	44	8591.0000	auto	2026-03-07 15:02:27.262704
1653	66	46	106229.0000	auto	2026-03-07 15:02:27.262704
1654	66	49	12883.0000	auto	2026-03-07 15:02:27.262704
1655	66	50	310316.0000	auto	2026-03-07 15:02:27.262704
1656	66	48	17600000.0000	auto	2026-03-07 15:02:27.262704
1657	66	47	9000.0000	auto	2026-03-07 15:02:27.262704
1658	67	52	85324919.0000	auto	2026-03-07 15:02:28.102307
1659	67	53	336685385.0000	auto	2026-03-07 15:02:28.102307
1660	67	54	24149810.0000	auto	2026-03-07 15:02:28.102307
1661	67	60	233390.0000	auto	2026-03-07 15:02:28.102307
1662	67	55	138958317.0000	auto	2026-03-07 15:02:28.102307
1663	67	56	15231626.0000	auto	2026-03-07 15:02:28.102307
1664	67	57	136011826.0000	auto	2026-03-07 15:02:28.102307
1665	67	58	12704978.8000	auto	2026-03-07 15:02:28.102307
1666	67	59	487941.6000	auto	2026-03-07 15:02:28.102307
1667	67	16	525763.0000	auto	2026-03-07 15:02:28.102307
1668	67	39	11841627.0000	auto	2026-03-07 15:02:28.102307
1669	67	43	1417388.0000	auto	2026-03-07 15:02:28.102307
1670	67	44	1614198.0000	auto	2026-03-07 15:02:28.102307
1671	67	46	106253.0000	auto	2026-03-07 15:02:28.102307
1672	67	49	12883.0000	auto	2026-03-07 15:02:28.102307
1673	67	50	310316.0000	auto	2026-03-07 15:02:28.102307
1674	67	48	17600000.0000	auto	2026-03-07 15:02:28.102307
1675	67	47	9029.0000	auto	2026-03-07 15:02:28.102307
1676	68	52	86066643.0000	auto	2026-03-07 15:02:28.930079
1677	68	53	342411515.0000	auto	2026-03-07 15:02:28.930079
1678	68	54	25014296.0000	auto	2026-03-07 15:02:28.930079
1679	68	60	220310.0000	auto	2026-03-07 15:02:28.930079
1680	68	55	137968497.0000	auto	2026-03-07 15:02:28.930079
1681	68	56	15435146.0000	auto	2026-03-07 15:02:28.930079
1682	68	57	118500172.8000	auto	2026-03-07 15:02:28.930079
1683	68	58	12757722.4000	auto	2026-03-07 15:02:28.930079
1684	68	59	508627.6000	auto	2026-03-07 15:02:28.930079
1685	68	16	275941.0000	auto	2026-03-07 15:02:28.930079
1686	68	39	11859072.0000	auto	2026-03-07 15:02:28.930079
1687	68	43	1417388.0000	auto	2026-03-07 15:02:28.930079
1688	68	44	114198.0000	auto	2026-03-07 15:02:28.930079
1689	68	46	116253.0000	auto	2026-03-07 15:02:28.930079
1690	68	49	12883.0000	auto	2026-03-07 15:02:28.930079
1691	68	50	320316.0000	auto	2026-03-07 15:02:28.930079
1692	68	48	17719029.0000	auto	2026-03-07 15:02:28.930079
1693	68	47	19029.0000	auto	2026-03-07 15:02:28.930079
1694	69	52	79059245.0000	auto	2026-03-07 15:02:29.802964
1695	69	53	311106485.0000	auto	2026-03-07 15:02:29.802964
1696	69	54	20529291.0000	auto	2026-03-07 15:02:29.802964
1697	69	60	222750.0000	auto	2026-03-07 15:02:29.802964
1698	69	55	132328755.5500	auto	2026-03-07 15:02:29.802964
1699	69	56	15269786.0000	auto	2026-03-07 15:02:29.802964
1700	69	57	85246690.6400	auto	2026-03-07 15:02:29.802964
1701	69	58	12513030.0600	auto	2026-03-07 15:02:29.802964
1702	69	59	466602.4200	auto	2026-03-07 15:02:29.802964
1703	69	16	276067.0000	auto	2026-03-07 15:02:29.802964
1704	69	39	11892956.0000	auto	2026-03-07 15:02:29.802964
1705	69	43	1417388.0000	auto	2026-03-07 15:02:29.802964
1706	69	44	114198.0000	auto	2026-03-07 15:02:29.802964
1707	69	46	116253.0000	auto	2026-03-07 15:02:29.802964
1708	69	49	12883.0000	auto	2026-03-07 15:02:29.802964
1709	69	50	320316.0000	auto	2026-03-07 15:02:29.802964
1710	69	48	17719029.0000	auto	2026-03-07 15:02:29.802964
1711	69	47	19029.0000	auto	2026-03-07 15:02:29.802964
1712	70	52	81810267.0000	auto	2026-03-07 15:02:30.657273
1713	70	53	319986780.0000	auto	2026-03-07 15:02:30.657273
1714	70	54	21428336.0000	auto	2026-03-07 15:02:30.657273
1715	70	60	355890.0000	auto	2026-03-07 15:02:30.657273
1716	70	55	134648497.5500	auto	2026-03-07 15:02:30.657273
1717	70	56	15816172.0000	auto	2026-03-07 15:02:30.657273
1718	70	57	110378343.0400	auto	2026-03-07 15:02:30.657273
1719	70	58	12290548.2000	auto	2026-03-07 15:02:30.657273
1720	70	59	544383.6200	auto	2026-03-07 15:02:30.657273
1721	70	16	276175.0000	auto	2026-03-07 15:02:30.657273
1722	70	39	11892956.0000	auto	2026-03-07 15:02:30.657273
1723	70	43	1417388.0000	auto	2026-03-07 15:02:30.657273
1724	70	44	114198.0000	auto	2026-03-07 15:02:30.657273
1725	70	46	116253.0000	auto	2026-03-07 15:02:30.657273
1726	70	49	12896.0000	auto	2026-03-07 15:02:30.657273
1727	70	50	320316.0000	auto	2026-03-07 15:02:30.657273
1728	70	48	17719029.0000	auto	2026-03-07 15:02:30.657273
1729	70	47	19029.0000	auto	2026-03-07 15:02:30.657273
1730	71	52	78036569.0000	auto	2026-03-07 15:02:31.516805
1731	71	53	303763505.0000	auto	2026-03-07 15:02:31.516805
1732	71	54	19230181.0000	auto	2026-03-07 15:02:31.516805
1733	71	60	528730.0000	auto	2026-03-07 15:02:31.516805
1734	71	55	122001453.5500	auto	2026-03-07 15:02:31.516805
1735	71	56	16146406.0000	auto	2026-03-07 15:02:31.516805
1736	71	57	93669558.0400	auto	2026-03-07 15:02:31.516805
1737	71	58	12151819.3700	auto	2026-03-07 15:02:31.516805
1738	71	59	465888.6200	auto	2026-03-07 15:02:31.516805
1739	71	16	276319.0000	auto	2026-03-07 15:02:31.516805
1740	71	39	12019541.0000	auto	2026-03-07 15:02:31.516805
1741	71	43	1417388.0000	auto	2026-03-07 15:02:31.516805
1742	71	44	114198.0000	auto	2026-03-07 15:02:31.516805
1743	71	46	116253.0000	auto	2026-03-07 15:02:31.516805
1744	71	49	12896.0000	auto	2026-03-07 15:02:31.516805
1745	71	50	320316.0000	auto	2026-03-07 15:02:31.516805
1746	71	48	17719029.0000	auto	2026-03-07 15:02:31.516805
1747	71	47	19029.0000	auto	2026-03-07 15:02:31.516805
1748	72	52	82810749.0000	auto	2026-03-07 15:02:32.381805
1749	72	53	325486480.0000	auto	2026-03-07 15:02:32.381805
1750	72	54	21765507.0000	auto	2026-03-07 15:02:32.381805
1751	72	60	473507.0000	auto	2026-03-07 15:02:32.381805
1752	72	55	135687107.5500	auto	2026-03-07 15:02:32.381805
1753	72	56	16225332.0000	auto	2026-03-07 15:02:32.381805
1754	72	57	119768930.0400	auto	2026-03-07 15:02:32.381805
1755	72	58	12442768.3700	auto	2026-03-07 15:02:32.381805
1756	72	59	506421.0000	auto	2026-03-07 15:02:32.381805
1757	72	16	276445.0000	auto	2026-03-07 15:02:32.381805
1758	72	39	12019541.0000	auto	2026-03-07 15:02:32.381805
1759	72	43	1202983.0000	auto	2026-03-07 15:02:32.381805
1760	72	44	114198.0000	auto	2026-03-07 15:02:32.381805
1761	72	46	116253.0000	auto	2026-03-07 15:02:32.381805
1762	72	49	12896.0000	auto	2026-03-07 15:02:32.381805
1763	72	50	320316.0000	auto	2026-03-07 15:02:32.381805
1764	72	48	17700000.0000	auto	2026-03-07 15:02:32.381805
1765	72	47	19029.0000	auto	2026-03-07 15:02:32.381805
1766	73	52	83692334.0000	auto	2026-03-07 15:02:33.241538
1767	73	53	327952816.0000	auto	2026-03-07 15:02:33.241538
1768	73	54	22290576.0000	auto	2026-03-07 15:02:33.241538
1769	73	60	601321.0000	auto	2026-03-07 15:02:33.241538
1770	73	55	136143858.0000	auto	2026-03-07 15:02:33.241538
1771	73	56	15878406.0000	auto	2026-03-07 15:02:33.241538
1772	73	57	130669563.5200	auto	2026-03-07 15:02:33.241538
1773	73	58	12440012.4600	auto	2026-03-07 15:02:33.241538
1774	73	59	567217.0000	auto	2026-03-07 15:02:33.241538
1775	73	16	917059.0000	auto	2026-03-07 15:02:33.241538
1776	73	39	12019541.0000	auto	2026-03-07 15:02:33.241538
1777	73	43	1202983.0000	auto	2026-03-07 15:02:33.241538
1778	73	44	114198.0000	auto	2026-03-07 15:02:33.241538
1779	73	46	116253.0000	auto	2026-03-07 15:02:33.241538
1780	73	49	12908.0000	auto	2026-03-07 15:02:33.241538
1781	73	50	320316.0000	auto	2026-03-07 15:02:33.241538
1782	73	48	17700000.0000	auto	2026-03-07 15:02:33.241538
1783	73	47	19029.0000	auto	2026-03-07 15:02:33.241538
1784	74	52	84111438.0000	auto	2026-03-07 15:02:34.11009
1785	74	53	328672252.0000	auto	2026-03-07 15:02:34.11009
1786	74	54	22340154.0000	auto	2026-03-07 15:02:34.11009
1787	74	60	65420.0000	auto	2026-03-07 15:02:34.11009
1788	74	55	134320559.0000	auto	2026-03-07 15:02:34.11009
1789	74	56	16057096.0000	auto	2026-03-07 15:02:34.11009
1790	74	57	127853252.5200	auto	2026-03-07 15:02:34.11009
1791	74	58	12199561.0800	auto	2026-03-07 15:02:34.11009
1792	74	59	552632.0000	auto	2026-03-07 15:02:34.11009
1793	74	16	917608.0000	auto	2026-03-07 15:02:34.11009
1794	74	39	11042809.0000	auto	2026-03-07 15:02:34.11009
1795	74	43	1018553.0000	auto	2026-03-07 15:02:34.11009
1796	74	44	114198.0000	auto	2026-03-07 15:02:34.11009
1797	74	46	116253.0000	auto	2026-03-07 15:02:34.11009
1798	74	49	517989.0000	auto	2026-03-07 15:02:34.11009
1799	74	50	320316.0000	auto	2026-03-07 15:02:34.11009
1800	74	48	17700000.0000	auto	2026-03-07 15:02:34.11009
1801	74	47	19029.0000	auto	2026-03-07 15:02:34.11009
1802	75	52	89322460.0000	auto	2026-03-07 15:02:34.967763
1803	75	53	350403728.0000	auto	2026-03-07 15:02:34.967763
1804	75	54	25565795.0000	auto	2026-03-07 15:02:34.967763
1805	75	60	43910.0000	auto	2026-03-07 15:02:34.967763
1806	75	55	137903673.0000	auto	2026-03-07 15:02:34.967763
1807	75	56	15482112.0000	auto	2026-03-07 15:02:34.967763
1808	75	57	144082164.7800	auto	2026-03-07 15:02:34.967763
1809	75	58	12350765.1000	auto	2026-03-07 15:02:34.967763
1810	75	59	599675.2800	auto	2026-03-07 15:02:34.967763
1811	75	16	917974.0000	auto	2026-03-07 15:02:34.967763
1812	75	39	10912610.0000	auto	2026-03-07 15:02:34.967763
1813	75	43	760041.0000	auto	2026-03-07 15:02:34.967763
1814	75	44	114198.0000	auto	2026-03-07 15:02:34.967763
1815	75	46	116253.0000	auto	2026-03-07 15:02:34.967763
1816	75	49	517989.0000	auto	2026-03-07 15:02:34.967763
1817	75	50	320316.0000	auto	2026-03-07 15:02:34.967763
1818	75	48	17700000.0000	auto	2026-03-07 15:02:34.967763
1819	75	47	19029.0000	auto	2026-03-07 15:02:34.967763
1820	76	52	87835922.0000	auto	2026-03-07 15:02:35.810019
1821	76	53	344632148.0000	auto	2026-03-07 15:02:35.810019
1822	76	54	24484109.0000	auto	2026-03-07 15:02:35.810019
1823	76	60	42640.0000	auto	2026-03-07 15:02:35.810019
1824	76	55	134850867.0000	auto	2026-03-07 15:02:35.810019
1825	76	56	15781036.0000	auto	2026-03-07 15:02:35.810019
1826	76	57	136839191.7050	auto	2026-03-07 15:02:35.810019
1827	76	58	11994712.1750	auto	2026-03-07 15:02:35.810019
1828	76	59	583342.6900	auto	2026-03-07 15:02:35.810019
1829	76	16	918462.0000	auto	2026-03-07 15:02:35.810019
1830	76	39	10912610.0000	auto	2026-03-07 15:02:35.810019
1831	76	43	697542.0000	auto	2026-03-07 15:02:35.810019
1832	76	44	114198.0000	auto	2026-03-07 15:02:35.810019
1833	76	46	116253.0000	auto	2026-03-07 15:02:35.810019
1834	76	49	517989.0000	auto	2026-03-07 15:02:35.810019
1835	76	50	320316.0000	auto	2026-03-07 15:02:35.810019
1836	76	48	17700000.0000	auto	2026-03-07 15:02:35.810019
1837	76	47	19029.0000	auto	2026-03-07 15:02:35.810019
1838	77	52	89450944.0000	auto	2026-03-07 15:02:36.641336
1839	77	53	351163278.0000	auto	2026-03-07 15:02:36.641336
1840	77	54	25715780.0000	auto	2026-03-07 15:02:36.641336
1841	77	60	42820.0000	auto	2026-03-07 15:02:36.641336
1842	77	55	136372374.0000	auto	2026-03-07 15:02:36.641336
1843	77	56	15672966.0000	auto	2026-03-07 15:02:36.641336
1844	77	57	143029572.8870	auto	2026-03-07 15:02:36.641336
1845	77	58	12173812.3450	auto	2026-03-07 15:02:36.641336
1846	77	59	653158.7660	auto	2026-03-07 15:02:36.641336
1847	77	16	918889.0000	auto	2026-03-07 15:02:36.641336
1848	77	39	10912610.0000	auto	2026-03-07 15:02:36.641336
1849	77	43	464433.0000	auto	2026-03-07 15:02:36.641336
1850	77	44	114198.0000	auto	2026-03-07 15:02:36.641336
1851	77	46	116253.0000	auto	2026-03-07 15:02:36.641336
1852	77	49	517989.0000	auto	2026-03-07 15:02:36.641336
1853	77	50	320316.0000	auto	2026-03-07 15:02:36.641336
1854	77	48	17700000.0000	auto	2026-03-07 15:02:36.641336
1855	77	47	19029.0000	auto	2026-03-07 15:02:36.641336
1856	78	52	89618167.0000	auto	2026-03-07 15:02:37.534624
1857	78	53	348203204.0000	auto	2026-03-07 15:02:37.534624
1858	78	54	25196811.0000	auto	2026-03-07 15:02:37.534624
1859	78	60	43305.0000	auto	2026-03-07 15:02:37.534624
1860	78	55	137032708.0000	auto	2026-03-07 15:02:37.534624
1861	78	56	15789248.0000	auto	2026-03-07 15:02:37.534624
1862	78	57	148898434.5050	auto	2026-03-07 15:02:37.534624
1863	78	58	12102532.1700	auto	2026-03-07 15:02:37.534624
1864	78	59	666931.0900	auto	2026-03-07 15:02:37.534624
1865	78	16	919255.0000	auto	2026-03-07 15:02:37.534624
1866	78	39	10912610.0000	auto	2026-03-07 15:02:37.534624
1867	78	43	384433.0000	auto	2026-03-07 15:02:37.534624
1868	78	44	114198.0000	auto	2026-03-07 15:02:37.534624
1869	78	46	116253.0000	auto	2026-03-07 15:02:37.534624
1870	78	49	517989.0000	auto	2026-03-07 15:02:37.534624
1871	78	50	320316.0000	auto	2026-03-07 15:02:37.534624
1872	78	48	17700000.0000	auto	2026-03-07 15:02:37.534624
1873	78	47	19029.0000	auto	2026-03-07 15:02:37.534624
1874	79	52	89866350.0000	auto	2026-03-07 15:02:38.369165
1875	79	53	349674819.0000	auto	2026-03-07 15:02:38.369165
1876	79	54	25036183.0000	auto	2026-03-07 15:02:38.369165
1877	79	60	42328.0000	auto	2026-03-07 15:02:38.369165
1878	79	55	136625003.0000	auto	2026-03-07 15:02:38.369165
1879	79	56	16120249.0000	auto	2026-03-07 15:02:38.369165
1880	79	57	147056684.3450	auto	2026-03-07 15:02:38.369165
1881	79	58	12177727.4750	auto	2026-03-07 15:02:38.369165
1882	79	59	663822.3400	auto	2026-03-07 15:02:38.369165
1883	79	16	919707.0000	auto	2026-03-07 15:02:38.369165
1884	79	39	10912610.0000	auto	2026-03-07 15:02:38.369165
1885	79	43	289727.0000	auto	2026-03-07 15:02:38.369165
1886	79	44	114198.0000	auto	2026-03-07 15:02:38.369165
1887	79	46	116253.0000	auto	2026-03-07 15:02:38.369165
1888	79	49	1280305.0000	auto	2026-03-07 15:02:38.369165
1889	79	50	320316.0000	auto	2026-03-07 15:02:38.369165
1890	79	48	17700000.0000	auto	2026-03-07 15:02:38.369165
1891	79	47	19029.0000	auto	2026-03-07 15:02:38.369165
1892	80	52	90832992.0000	auto	2026-03-07 15:02:39.18506
1893	80	53	353940039.0000	auto	2026-03-07 15:02:39.18506
1894	80	54	25828744.0000	auto	2026-03-07 15:02:39.18506
1895	80	60	43235.0000	auto	2026-03-07 15:02:39.18506
1896	80	55	137172505.0000	auto	2026-03-07 15:02:39.18506
1897	80	56	15846329.0000	auto	2026-03-07 15:02:39.18506
1898	80	57	149167768.6400	auto	2026-03-07 15:02:39.18506
1899	80	58	12284508.1600	auto	2026-03-07 15:02:39.18506
1900	80	59	666375.3000	auto	2026-03-07 15:02:39.18506
1901	80	16	920147.0000	auto	2026-03-07 15:02:39.18506
1902	80	39	10912610.0000	auto	2026-03-07 15:02:39.18506
1903	80	43	1029464.0000	auto	2026-03-07 15:02:39.18506
1904	80	44	114198.0000	auto	2026-03-07 15:02:39.18506
1905	80	46	116253.0000	auto	2026-03-07 15:02:39.18506
1906	80	49	280305.0000	auto	2026-03-07 15:02:39.18506
1907	80	50	320316.0000	auto	2026-03-07 15:02:39.18506
1908	80	48	17700000.0000	auto	2026-03-07 15:02:39.18506
1909	80	47	19029.0000	auto	2026-03-07 15:02:39.18506
1910	81	52	93627614.0000	auto	2026-03-07 15:02:40.033481
1911	81	53	362635649.0000	auto	2026-03-07 15:02:40.033481
1912	81	54	27279963.0000	auto	2026-03-07 15:02:40.033481
1913	81	60	43235.0000	auto	2026-03-07 15:02:40.033481
1914	81	55	138419588.0000	auto	2026-03-07 15:02:40.033481
1915	81	56	15464339.0000	auto	2026-03-07 15:02:40.033481
1916	81	57	164349197.6400	auto	2026-03-07 15:02:40.033481
1917	81	58	12259358.0600	auto	2026-03-07 15:02:40.033481
1918	81	59	699105.3000	auto	2026-03-07 15:02:40.033481
1919	81	16	920422.0000	auto	2026-03-07 15:02:40.033481
1920	81	39	10912610.0000	auto	2026-03-07 15:02:40.033481
1921	81	43	874855.0000	auto	2026-03-07 15:02:40.033481
1922	81	44	114198.0000	auto	2026-03-07 15:02:40.033481
1923	81	46	116253.0000	auto	2026-03-07 15:02:40.033481
1924	81	49	280305.0000	auto	2026-03-07 15:02:40.033481
1925	81	50	320316.0000	auto	2026-03-07 15:02:40.033481
1926	81	48	17700000.0000	auto	2026-03-07 15:02:40.033481
1927	81	47	19029.0000	auto	2026-03-07 15:02:40.033481
1928	82	52	95018396.0000	auto	2026-03-07 15:02:40.906176
1929	82	53	367656969.0000	auto	2026-03-07 15:02:40.906176
1930	82	54	27954715.0000	auto	2026-03-07 15:02:40.906176
1931	82	60	42279.0000	auto	2026-03-07 15:02:40.906176
1932	82	55	139876971.2600	auto	2026-03-07 15:02:40.906176
1933	82	56	15887679.0000	auto	2026-03-07 15:02:40.906176
1934	82	57	166959535.4400	auto	2026-03-07 15:02:40.906176
1935	82	58	12347693.0600	auto	2026-03-07 15:02:40.906176
1936	82	59	703211.3000	auto	2026-03-07 15:02:40.906176
1937	82	16	770844.0000	auto	2026-03-07 15:02:40.906176
1938	82	39	10912610.0000	auto	2026-03-07 15:02:40.906176
1939	82	43	649855.0000	auto	2026-03-07 15:02:40.906176
1940	82	44	114198.0000	auto	2026-03-07 15:02:40.906176
1941	82	46	116253.0000	auto	2026-03-07 15:02:40.906176
1942	82	49	280686.0000	auto	2026-03-07 15:02:40.906176
1943	82	50	320316.0000	auto	2026-03-07 15:02:40.906176
1944	82	48	17700000.0000	auto	2026-03-07 15:02:40.906176
1945	82	47	19029.0000	auto	2026-03-07 15:02:40.906176
1946	83	52	96324518.0000	auto	2026-03-07 15:02:41.781704
1947	83	53	372481688.0000	auto	2026-03-07 15:02:41.781704
1948	83	54	28677658.0000	auto	2026-03-07 15:02:41.781704
1949	83	60	42663.0000	auto	2026-03-07 15:02:41.781704
1950	83	55	139630606.0000	auto	2026-03-07 15:02:41.781704
1951	83	56	16162949.0000	auto	2026-03-07 15:02:41.781704
1952	83	57	167302092.0600	auto	2026-03-07 15:02:41.781704
1953	83	58	12520841.3800	auto	2026-03-07 15:02:41.781704
1954	83	59	721206.8200	auto	2026-03-07 15:02:41.781704
1955	83	16	1475891.0000	auto	2026-03-07 15:02:41.781704
1956	83	39	12996386.0000	auto	2026-03-07 15:02:41.781704
1957	83	43	7202715.0000	auto	2026-03-07 15:02:41.781704
1958	83	44	114234.0000	auto	2026-03-07 15:02:41.781704
1959	83	46	116253.0000	auto	2026-03-07 15:02:41.781704
1960	83	49	202186.0000	auto	2026-03-07 15:02:41.781704
1961	83	50	320316.0000	auto	2026-03-07 15:02:41.781704
1962	83	48	17700000.0000	auto	2026-03-07 15:02:41.781704
1963	83	47	19029.0000	auto	2026-03-07 15:02:41.781704
1964	84	52	99479440.0000	auto	2026-03-07 15:02:42.621885
1965	84	53	384363853.0000	auto	2026-03-07 15:02:42.621885
1966	84	54	30642787.0000	auto	2026-03-07 15:02:42.621885
1967	84	60	42722.0000	auto	2026-03-07 15:02:42.621885
1968	84	55	141175199.0000	auto	2026-03-07 15:02:42.621885
1969	84	56	16304649.0000	auto	2026-03-07 15:02:42.621885
1970	84	57	175367455.0600	auto	2026-03-07 15:02:42.621885
1971	84	58	12610015.4000	auto	2026-03-07 15:02:42.621885
1972	84	59	748056.0000	auto	2026-03-07 15:02:42.621885
1973	84	16	1476437.0000	auto	2026-03-07 15:02:42.621885
1974	84	39	12114375.0000	auto	2026-03-07 15:02:42.621885
1975	84	43	6797162.0000	auto	2026-03-07 15:02:42.621885
1976	84	44	114234.0000	auto	2026-03-07 15:02:42.621885
1977	84	46	116253.0000	auto	2026-03-07 15:02:42.621885
1978	84	49	202186.0000	auto	2026-03-07 15:02:42.621885
1979	84	50	320316.0000	auto	2026-03-07 15:02:42.621885
1980	84	48	17700000.0000	auto	2026-03-07 15:02:42.621885
1981	84	47	19029.0000	auto	2026-03-07 15:02:42.621885
1982	85	52	99376462.0000	auto	2026-03-07 15:02:43.469282
1983	85	53	384690878.0000	auto	2026-03-07 15:02:43.469282
1984	85	54	30584086.0000	auto	2026-03-07 15:02:43.469282
1985	85	60	41803.0000	auto	2026-03-07 15:02:43.469282
1986	85	55	141024220.0000	auto	2026-03-07 15:02:43.469282
1987	85	56	16216359.0000	auto	2026-03-07 15:02:43.469282
1988	85	57	175598473.0600	auto	2026-03-07 15:02:43.469282
1989	85	58	12600753.4000	auto	2026-03-07 15:02:43.469282
1990	85	59	750107.0000	auto	2026-03-07 15:02:43.469282
1991	85	16	1476988.0000	auto	2026-03-07 15:02:43.469282
1992	85	39	12114375.0000	auto	2026-03-07 15:02:43.469282
1993	85	43	6561553.0000	auto	2026-03-07 15:02:43.469282
1994	85	44	114234.0000	auto	2026-03-07 15:02:43.469282
1995	85	46	116253.0000	auto	2026-03-07 15:02:43.469282
1996	85	49	167186.0000	auto	2026-03-07 15:02:43.469282
1997	85	50	320316.0000	auto	2026-03-07 15:02:43.469282
1998	85	48	17700000.0000	auto	2026-03-07 15:02:43.469282
1999	85	47	19029.0000	auto	2026-03-07 15:02:43.469282
2000	86	52	101518204.0000	auto	2026-03-07 15:02:43.231691
2001	86	53	392405618.0000	auto	2026-03-07 15:02:43.231691
2002	86	54	31778859.0000	auto	2026-03-07 15:02:43.231691
2003	86	60	40287.0000	auto	2026-03-07 15:02:43.231691
2004	86	55	140739961.0000	auto	2026-03-07 15:02:43.231691
2005	86	56	16200009.0000	auto	2026-03-07 15:02:43.231691
2006	86	57	173142004.0600	auto	2026-03-07 15:02:43.231691
2007	86	58	12613584.6200	auto	2026-03-07 15:02:43.231691
2008	86	59	750451.0000	auto	2026-03-07 15:02:43.231691
2009	86	16	1477541.0000	auto	2026-03-07 15:02:43.231691
2010	86	39	12114375.0000	auto	2026-03-07 15:02:43.231691
2011	86	43	6661553.0000	auto	2026-03-07 15:02:43.231691
2012	86	44	114234.0000	auto	2026-03-07 15:02:43.231691
2013	86	46	116253.0000	auto	2026-03-07 15:02:43.231691
2014	86	49	167348.0000	auto	2026-03-07 15:02:43.231691
2015	86	50	320316.0000	auto	2026-03-07 15:02:43.231691
2016	86	48	17700000.0000	auto	2026-03-07 15:02:43.231691
2017	86	47	19029.0000	auto	2026-03-07 15:02:43.231691
2018	87	52	103600926.0000	auto	2026-03-07 15:02:44.09592
2019	87	53	398624410.0000	auto	2026-03-07 15:02:44.09592
2020	87	54	32374179.0000	auto	2026-03-07 15:02:44.09592
2021	87	60	41122.0000	auto	2026-03-07 15:02:44.09592
2022	87	55	141982591.0000	auto	2026-03-07 15:02:44.09592
2023	87	56	17009149.0000	auto	2026-03-07 15:02:44.09592
2024	87	57	184187811.0600	auto	2026-03-07 15:02:44.09592
2025	87	58	13293845.2600	auto	2026-03-07 15:02:44.09592
2026	87	59	825029.0000	auto	2026-03-07 15:02:44.09592
2027	87	16	724198.0000	auto	2026-03-07 15:02:44.09592
2028	87	39	14114375.0000	auto	2026-03-07 15:02:44.09592
2029	87	43	9091557.0000	auto	2026-03-07 15:02:44.09592
2030	87	44	124234.0000	auto	2026-03-07 15:02:44.09592
2031	87	46	136283.0000	auto	2026-03-07 15:02:44.09592
2032	87	49	167348.0000	auto	2026-03-07 15:02:44.09592
2033	87	50	340453.0000	auto	2026-03-07 15:02:44.09592
2034	87	48	17900000.0000	auto	2026-03-07 15:02:44.09592
2035	87	47	39033.0000	auto	2026-03-07 15:02:44.09592
2036	88	52	104691235.0000	auto	2026-03-07 15:02:44.951838
2037	88	53	403590340.0000	auto	2026-03-07 15:02:44.951838
2038	88	54	33159229.0000	auto	2026-03-07 15:02:44.951838
2039	88	60	41453.0000	auto	2026-03-07 15:02:44.951838
2040	88	55	142739351.0000	auto	2026-03-07 15:02:44.951838
2041	88	56	16632859.0000	auto	2026-03-07 15:02:44.951838
2042	88	57	184114707.5000	auto	2026-03-07 15:02:44.951838
2043	88	58	13115049.3600	auto	2026-03-07 15:02:44.951838
2044	88	59	855526.0000	auto	2026-03-07 15:02:44.951838
2045	88	16	724456.0000	auto	2026-03-07 15:02:44.951838
2046	88	39	14102915.0000	auto	2026-03-07 15:02:44.951838
2047	88	43	8952302.0000	auto	2026-03-07 15:02:44.951838
2048	88	44	124234.0000	auto	2026-03-07 15:02:44.951838
2049	88	46	136283.0000	auto	2026-03-07 15:02:44.951838
2050	88	49	167348.0000	auto	2026-03-07 15:02:44.951838
2051	88	50	340453.0000	auto	2026-03-07 15:02:44.951838
2052	88	48	17900000.0000	auto	2026-03-07 15:02:44.951838
2053	88	47	39033.0000	auto	2026-03-07 15:02:44.951838
2054	89	52	102031841.0000	auto	2026-03-07 15:02:45.771833
2055	89	53	392070040.0000	auto	2026-03-07 15:02:45.771833
2056	89	54	31418146.0000	auto	2026-03-07 15:02:45.771833
2057	89	60	42626.0000	auto	2026-03-07 15:02:45.771833
2058	89	55	142723913.0000	auto	2026-03-07 15:02:45.771833
2059	89	56	16587349.0000	auto	2026-03-07 15:02:45.771833
2060	89	57	180419130.0000	auto	2026-03-07 15:02:45.771833
2061	89	58	13352401.0000	auto	2026-03-07 15:02:45.771833
2062	89	59	856080.0000	auto	2026-03-07 15:02:45.771833
2063	89	16	724757.0000	auto	2026-03-07 15:02:45.771833
2064	89	39	14102915.0000	auto	2026-03-07 15:02:45.771833
2065	89	43	7679238.0000	auto	2026-03-07 15:02:45.771833
2066	89	44	124234.0000	auto	2026-03-07 15:02:45.771833
2067	89	46	136283.0000	auto	2026-03-07 15:02:45.771833
2068	89	49	87848.0000	auto	2026-03-07 15:02:45.771833
2069	89	50	340453.0000	auto	2026-03-07 15:02:45.771833
2070	89	48	17900000.0000	auto	2026-03-07 15:02:45.771833
2071	89	47	39033.0000	auto	2026-03-07 15:02:45.771833
2072	90	52	104843257.0000	auto	2026-03-07 15:02:46.660393
2073	90	53	404944540.0000	auto	2026-03-07 15:02:46.660393
2074	90	54	33369984.0000	auto	2026-03-07 15:02:46.660393
2075	90	60	41506.0000	auto	2026-03-07 15:02:46.660393
2076	90	55	143212856.0000	auto	2026-03-07 15:02:46.660393
2077	90	56	16972519.0000	auto	2026-03-07 15:02:46.660393
2078	90	57	177825536.0000	auto	2026-03-07 15:02:46.660393
2079	90	58	13134523.5800	auto	2026-03-07 15:02:46.660393
2080	90	59	851988.0000	auto	2026-03-07 15:02:46.660393
2081	90	16	725058.0000	auto	2026-03-07 15:02:46.660393
2082	90	39	14102915.0000	auto	2026-03-07 15:02:46.660393
2083	90	43	5664209.0000	auto	2026-03-07 15:02:46.660393
2084	90	44	124234.0000	auto	2026-03-07 15:02:46.660393
2085	90	46	136283.0000	auto	2026-03-07 15:02:46.660393
2086	90	49	87848.0000	auto	2026-03-07 15:02:46.660393
2087	90	50	340453.0000	auto	2026-03-07 15:02:46.660393
2088	90	48	17900000.0000	auto	2026-03-07 15:02:46.660393
2089	90	47	39033.0000	auto	2026-03-07 15:02:46.660393
2090	91	52	106515124.0000	auto	2026-03-07 15:02:47.536354
2091	91	53	422620189.0000	auto	2026-03-07 15:02:47.536354
2092	91	54	40571294.0000	auto	2026-03-07 15:02:47.536354
2093	91	60	42247.0000	auto	2026-03-07 15:02:47.536354
2094	91	55	144895135.0000	auto	2026-03-07 15:02:47.536354
2095	91	56	18331183.0000	auto	2026-03-07 15:02:47.536354
2096	91	57	189238243.0000	auto	2026-03-07 15:02:47.536354
2097	91	58	13543334.2800	auto	2026-03-07 15:02:47.536354
2098	91	59	885279.0000	auto	2026-03-07 15:02:47.536354
2099	91	16	28620.0000	auto	2026-03-07 15:02:47.536354
2100	91	39	16102915.0000	auto	2026-03-07 15:02:47.536354
2101	91	43	1194878.0000	auto	2026-03-07 15:02:47.536354
2102	91	44	124234.0000	auto	2026-03-07 15:02:47.536354
2103	91	46	146283.0000	auto	2026-03-07 15:02:47.536354
2104	91	49	87947.0000	auto	2026-03-07 15:02:47.536354
2105	91	50	350453.0000	auto	2026-03-07 15:02:47.536354
2106	91	48	18000000.0000	auto	2026-03-07 15:02:47.536354
2107	91	47	49033.0000	auto	2026-03-07 15:02:47.536354
2108	92	52	109295882.0000	auto	2026-03-07 15:02:48.398146
2109	92	53	436756073.0000	auto	2026-03-07 15:02:48.398146
2110	92	54	45618569.0000	auto	2026-03-07 15:02:48.398146
2111	92	60	41914.0000	auto	2026-03-07 15:02:48.398146
2112	92	55	95434571.0000	auto	2026-03-07 15:02:48.398146
2113	92	56	18849486.0000	auto	2026-03-07 15:02:48.398146
2114	92	57	204830088.5640	auto	2026-03-07 15:02:48.398146
2115	92	58	14107855.0000	auto	2026-03-07 15:02:48.398146
2116	92	59	950791.9980	auto	2026-03-07 15:02:48.398146
2117	92	16	30084644.0000	auto	2026-03-07 15:02:48.398146
2118	92	38	184753.0000	auto	2026-03-07 15:02:48.398146
2119	92	39	13632203.0000	auto	2026-03-07 15:02:48.398146
2120	92	43	1320453.0000	auto	2026-03-07 15:02:48.398146
2121	92	44	124263.0000	auto	2026-03-07 15:02:48.398146
2122	92	46	146315.0000	auto	2026-03-07 15:02:48.398146
2123	92	49	87948.0000	auto	2026-03-07 15:02:48.398146
2124	92	50	350453.0000	auto	2026-03-07 15:02:48.398146
2125	92	48	18000000.0000	auto	2026-03-07 15:02:48.398146
2126	92	47	49041.0000	auto	2026-03-07 15:02:48.398146
2127	93	52	110432162.0000	auto	2026-03-07 15:02:49.2999
2128	93	53	439669148.0000	auto	2026-03-07 15:02:49.2999
2129	93	54	46577844.0000	auto	2026-03-07 15:02:49.2999
2130	93	60	40605.0000	auto	2026-03-07 15:02:49.2999
2131	93	55	96176149.0000	auto	2026-03-07 15:02:49.2999
2132	93	56	21308066.0000	auto	2026-03-07 15:02:49.2999
2133	93	57	201361556.0000	auto	2026-03-07 15:02:49.2999
2134	93	58	14239366.0000	auto	2026-03-07 15:02:49.2999
2135	93	59	924811.9980	auto	2026-03-07 15:02:49.2999
2136	93	16	29095195.0000	auto	2026-03-07 15:02:49.2999
2137	93	38	185046.0000	auto	2026-03-07 15:02:49.2999
2138	93	39	13632203.0000	auto	2026-03-07 15:02:49.2999
2139	93	43	989054.0000	auto	2026-03-07 15:02:49.2999
2140	93	44	124263.0000	auto	2026-03-07 15:02:49.2999
2141	93	46	146315.0000	auto	2026-03-07 15:02:49.2999
2142	93	49	52005.0000	auto	2026-03-07 15:02:49.2999
2143	93	50	350453.0000	auto	2026-03-07 15:02:49.2999
2144	93	48	18000000.0000	auto	2026-03-07 15:02:49.2999
2145	93	47	49041.0000	auto	2026-03-07 15:02:49.2999
2146	94	52	111800102.0000	auto	2026-03-07 15:02:50.125296
2147	94	53	440536619.0000	auto	2026-03-07 15:02:50.125296
2148	94	54	47046094.0000	auto	2026-03-07 15:02:50.125296
2149	94	60	41020.0000	auto	2026-03-07 15:02:50.125296
2150	94	55	97342077.6900	auto	2026-03-07 15:02:50.125296
2151	94	56	23012963.0000	auto	2026-03-07 15:02:50.125296
2152	94	57	208113633.2900	auto	2026-03-07 15:02:50.125296
2153	94	58	14443005.3780	auto	2026-03-07 15:02:50.125296
2154	94	59	960717.9980	auto	2026-03-07 15:02:50.125296
2155	94	16	27105196.0000	auto	2026-03-07 15:02:50.125296
2156	94	38	185122.0000	auto	2026-03-07 15:02:50.125296
2157	94	39	13632203.0000	auto	2026-03-07 15:02:50.125296
2158	94	43	923054.0000	auto	2026-03-07 15:02:50.125296
2159	94	44	124263.0000	auto	2026-03-07 15:02:50.125296
2160	94	46	146315.0000	auto	2026-03-07 15:02:50.125296
2161	94	49	52005.0000	auto	2026-03-07 15:02:50.125296
2162	94	50	350453.0000	auto	2026-03-07 15:02:50.125296
2163	94	48	18000000.0000	auto	2026-03-07 15:02:50.125296
2164	94	47	49041.0000	auto	2026-03-07 15:02:50.125296
2165	95	52	113722084.0000	auto	2026-03-07 15:02:50.983503
2166	95	53	449092804.0000	auto	2026-03-07 15:02:50.983503
2167	95	54	49139064.0000	auto	2026-03-07 15:02:50.983503
2168	95	60	40129.0000	auto	2026-03-07 15:02:50.983503
2169	95	55	95482195.0500	auto	2026-03-07 15:02:50.983503
2170	95	56	25529193.0000	auto	2026-03-07 15:02:50.983503
2171	95	57	201555108.2900	auto	2026-03-07 15:02:50.983503
2172	95	58	14216843.6100	auto	2026-03-07 15:02:50.983503
2173	95	59	935653.0300	auto	2026-03-07 15:02:50.983503
2174	95	16	25114507.0000	auto	2026-03-07 15:02:50.983503
2175	95	39	15632203.0000	auto	2026-03-07 15:02:50.983503
2176	95	43	6500414.0000	auto	2026-03-07 15:02:50.983503
2177	95	44	124263.0000	auto	2026-03-07 15:02:50.983503
2178	95	46	156315.0000	auto	2026-03-07 15:02:50.983503
2179	95	49	52017.0000	auto	2026-03-07 15:02:50.983503
2180	95	50	360453.0000	auto	2026-03-07 15:02:50.983503
2181	95	48	18100000.0000	auto	2026-03-07 15:02:50.983503
2182	95	47	59041.0000	auto	2026-03-07 15:02:50.983503
2183	96	52	110495764.0000	auto	2026-03-07 15:02:51.856023
2184	96	53	439174554.0000	auto	2026-03-07 15:02:51.856023
2185	96	54	48359373.0000	auto	2026-03-07 15:02:51.856023
2186	96	60	42375.0000	auto	2026-03-07 15:02:51.856023
2187	96	55	97753457.0000	auto	2026-03-07 15:02:51.856023
2188	96	56	28316713.0000	auto	2026-03-07 15:02:51.856023
2189	96	57	210865472.0000	auto	2026-03-07 15:02:51.856023
2190	96	58	14623149.0000	auto	2026-03-07 15:02:51.856023
2191	96	59	993187.0000	auto	2026-03-07 15:02:51.856023
2192	96	16	25367610.0000	auto	2026-03-07 15:02:51.856023
2193	96	39	15546312.0000	auto	2026-03-07 15:02:51.856023
2194	96	43	2023204.0000	auto	2026-03-07 15:02:51.856023
2195	96	44	124263.0000	auto	2026-03-07 15:02:51.856023
2196	96	46	156315.0000	auto	2026-03-07 15:02:51.856023
2197	96	49	52017.0000	auto	2026-03-07 15:02:51.856023
2198	96	50	360453.0000	auto	2026-03-07 15:02:51.856023
2199	96	48	18100000.0000	auto	2026-03-07 15:02:51.856023
2200	96	47	59041.0000	auto	2026-03-07 15:02:51.856023
2201	97	52	114096064.0000	auto	2026-03-07 15:02:52.719208
2202	97	53	455705909.0000	auto	2026-03-07 15:02:52.719208
2203	97	54	50034113.0000	auto	2026-03-07 15:02:52.719208
2204	97	60	43842.0000	auto	2026-03-07 15:02:52.719208
2205	97	55	100392909.0000	auto	2026-03-07 15:02:52.719208
2206	97	56	25734873.0000	auto	2026-03-07 15:02:52.719208
2207	97	57	221608841.0000	auto	2026-03-07 15:02:52.719208
2208	97	58	14932509.0000	auto	2026-03-07 15:02:52.719208
2209	97	59	1030609.0000	auto	2026-03-07 15:02:52.719208
2210	97	16	24376451.0000	auto	2026-03-07 15:02:52.719208
2211	97	39	15546312.0000	auto	2026-03-07 15:02:52.719208
2212	97	43	1921704.0000	auto	2026-03-07 15:02:52.719208
2213	97	44	124263.0000	auto	2026-03-07 15:02:52.719208
2214	97	46	156315.0000	auto	2026-03-07 15:02:52.719208
2215	97	49	52017.0000	auto	2026-03-07 15:02:52.719208
2216	97	50	360453.0000	auto	2026-03-07 15:02:52.719208
2217	97	48	18100000.0000	auto	2026-03-07 15:02:52.719208
2218	97	47	59041.0000	auto	2026-03-07 15:02:52.719208
2219	98	52	119638644.0000	auto	2026-03-07 15:02:53.522234
2220	98	53	479016894.0000	auto	2026-03-07 15:02:53.522234
2221	98	54	54533173.0000	auto	2026-03-07 15:02:53.522234
2222	98	60	43995.0000	auto	2026-03-07 15:02:53.522234
2223	98	55	99786252.0000	auto	2026-03-07 15:02:53.522234
2224	98	56	25963893.0000	auto	2026-03-07 15:02:53.522234
2225	98	57	236744192.0000	auto	2026-03-07 15:02:53.522234
2226	98	58	14564563.1300	auto	2026-03-07 15:02:53.522234
2227	98	59	1083052.0000	auto	2026-03-07 15:02:53.522234
2228	98	16	23384994.0000	auto	2026-03-07 15:02:53.522234
2229	98	39	15546312.0000	auto	2026-03-07 15:02:53.522234
2230	98	43	1803595.0000	auto	2026-03-07 15:02:53.522234
2231	98	44	124263.0000	auto	2026-03-07 15:02:53.522234
2232	98	46	156315.0000	auto	2026-03-07 15:02:53.522234
2233	98	49	4653.0000	auto	2026-03-07 15:02:53.522234
2234	98	50	360453.0000	auto	2026-03-07 15:02:53.522234
2235	98	48	18100000.0000	auto	2026-03-07 15:02:53.522234
2236	98	47	59041.0000	auto	2026-03-07 15:02:53.522234
2237	99	52	117308784.0000	auto	2026-03-07 15:02:54.361331
2238	99	53	471174070.0000	auto	2026-03-07 15:02:54.361331
2239	99	54	52889233.0000	auto	2026-03-07 15:02:54.361331
2240	99	60	41355.0000	auto	2026-03-07 15:02:54.361331
2241	99	55	100200072.0000	auto	2026-03-07 15:02:54.361331
2242	99	56	27808563.0000	auto	2026-03-07 15:02:54.361331
2243	99	57	220097791.5600	auto	2026-03-07 15:02:54.361331
2244	99	58	14546842.0640	auto	2026-03-07 15:02:54.361331
2245	99	59	1066099.0000	auto	2026-03-07 15:02:54.361331
2246	99	16	22393393.0000	auto	2026-03-07 15:02:54.361331
2247	99	39	15546312.0000	auto	2026-03-07 15:02:54.361331
2248	99	43	1803595.0000	auto	2026-03-07 15:02:54.361331
2249	99	44	124263.0000	auto	2026-03-07 15:02:54.361331
2250	99	46	156315.0000	auto	2026-03-07 15:02:54.361331
2251	99	49	4653.0000	auto	2026-03-07 15:02:54.361331
2252	99	50	360453.0000	auto	2026-03-07 15:02:54.361331
2253	99	48	18100000.0000	auto	2026-03-07 15:02:54.361331
2254	99	47	59041.0000	auto	2026-03-07 15:02:54.361331
2308	102	48	18200000.0000	auto	2026-03-07 15:02:57.056068
2309	102	47	69041.0000	auto	2026-03-07 15:02:57.056068
2328	104	52	118891184.0000	auto	2026-03-07 15:02:58.751619
2329	104	53	483506093.0000	auto	2026-03-07 15:02:58.751619
2330	104	54	55630063.0000	auto	2026-03-07 15:02:58.751619
2331	104	60	42849.0000	auto	2026-03-07 15:02:58.751619
2332	104	55	102953383.0000	auto	2026-03-07 15:02:58.751619
2333	104	56	34191355.0000	auto	2026-03-07 15:02:58.751619
2334	104	57	209082436.8700	auto	2026-03-07 15:02:58.751619
2335	104	58	14970492.0000	auto	2026-03-07 15:02:58.751619
2336	104	59	1101315.0000	auto	2026-03-07 15:02:58.751619
2337	104	16	26362259.0000	auto	2026-03-07 15:02:58.751619
2338	104	39	18983303.0000	auto	2026-03-07 15:02:58.751619
2339	104	43	786111.0000	auto	2026-03-07 15:02:58.751619
2340	104	44	134263.0000	auto	2026-03-07 15:02:58.751619
2341	104	46	176315.0000	auto	2026-03-07 15:02:58.751619
2342	104	49	28657.0000	auto	2026-03-07 15:02:58.751619
2343	104	50	380453.0000	auto	2026-03-07 15:02:58.751619
2344	104	48	18300000.0000	auto	2026-03-07 15:02:58.751619
2345	104	47	79041.0000	auto	2026-03-07 15:02:58.751619
2359	105	46	176354.0000	auto	2026-03-07 15:02:59.581271
2360	105	49	28662.0000	auto	2026-03-07 15:02:59.581271
2361	105	50	380606.0000	auto	2026-03-07 15:02:59.581271
2362	105	48	18300000.0000	auto	2026-03-07 15:02:59.581271
2363	105	47	79056.0000	auto	2026-03-07 15:02:59.581271
2364	106	52	117616684.0000	auto	2026-03-07 15:03:00.447905
2365	106	53	470608233.0000	auto	2026-03-07 15:03:00.447905
2366	106	54	53315073.0000	auto	2026-03-07 15:03:00.447905
2367	106	60	41474.0000	auto	2026-03-07 15:03:00.447905
2368	106	55	103146923.0000	auto	2026-03-07 15:03:00.447905
2369	106	56	38085010.0000	auto	2026-03-07 15:03:00.447905
2370	106	57	219718490.0000	auto	2026-03-07 15:03:00.447905
2371	106	58	14847585.0000	auto	2026-03-07 15:03:00.447905
2372	106	59	1135183.0000	auto	2026-03-07 15:03:00.447905
2373	106	16	20381190.0000	auto	2026-03-07 15:03:00.447905
2374	106	39	18800585.0000	auto	2026-03-07 15:03:00.447905
2375	106	43	508877.0000	auto	2026-03-07 15:03:00.447905
2376	106	44	134294.0000	auto	2026-03-07 15:03:00.447905
2377	106	46	176354.0000	auto	2026-03-07 15:03:00.447905
2378	106	49	23862.0000	auto	2026-03-07 15:03:00.447905
2379	106	50	380606.0000	auto	2026-03-07 15:03:00.447905
2380	106	47	79056.0000	auto	2026-03-07 15:03:00.447905
2381	107	52	116643204.0000	auto	2026-03-07 15:03:01.267794
2382	107	53	469019343.0000	auto	2026-03-07 15:03:01.267794
2383	107	54	73022453.0000	auto	2026-03-07 15:03:01.267794
2384	107	60	41624.0000	auto	2026-03-07 15:03:01.267794
2385	107	55	100817987.5650	auto	2026-03-07 15:03:01.267794
2386	107	56	37497225.0000	auto	2026-03-07 15:03:01.267794
2387	107	57	205603846.8850	auto	2026-03-07 15:03:01.267794
2388	107	58	14610719.7950	auto	2026-03-07 15:03:01.267794
2389	107	59	1102119.3200	auto	2026-03-07 15:03:01.267794
2390	107	16	3375.0000	auto	2026-03-07 15:03:01.267794
2391	107	39	18800585.0000	auto	2026-03-07 15:03:01.267794
2392	107	43	428877.0000	auto	2026-03-07 15:03:01.267794
2393	107	44	134294.0000	auto	2026-03-07 15:03:01.267794
2394	107	46	176354.0000	auto	2026-03-07 15:03:01.267794
2395	107	49	53878.0000	auto	2026-03-07 15:03:01.267794
2396	107	50	380606.0000	auto	2026-03-07 15:03:01.267794
2397	107	47	79056.0000	auto	2026-03-07 15:03:01.267794
2398	107	48	18300000.0000	auto	2026-03-07 15:03:01.267794
2399	108	52	119763210.0000	auto	2026-03-07 15:03:02.131783
2400	108	53	487337704.0000	auto	2026-03-07 15:03:02.131783
2401	108	54	73967264.0000	auto	2026-03-07 15:03:02.131783
2402	108	60	38612.0000	auto	2026-03-07 15:03:02.131783
2403	108	55	81606655.0180	auto	2026-03-07 15:03:02.131783
2404	108	56	37861790.0000	auto	2026-03-07 15:03:02.131783
2405	108	57	210916433.4700	auto	2026-03-07 15:03:02.131783
2406	108	58	14958322.1620	auto	2026-03-07 15:03:02.131783
2407	108	59	1145209.9040	auto	2026-03-07 15:03:02.131783
2408	108	16	2928147.0000	auto	2026-03-07 15:03:02.131783
2409	108	38	25.0000	auto	2026-03-07 15:03:02.131783
2410	108	39	20800585.0000	auto	2026-03-07 15:03:02.131783
2411	108	43	7008877.0000	auto	2026-03-07 15:03:02.131783
2412	108	44	134294.0000	auto	2026-03-07 15:03:02.131783
2413	108	46	186354.0000	auto	2026-03-07 15:03:02.131783
2414	108	49	53891.0000	auto	2026-03-07 15:03:02.131783
2415	108	50	390606.0000	auto	2026-03-07 15:03:02.131783
2416	108	47	89056.0000	auto	2026-03-07 15:03:02.131783
2417	108	48	18400000.0000	auto	2026-03-07 15:03:02.131783
2418	109	52	120948476.0000	auto	2026-03-07 15:03:02.97659
2419	109	53	490020109.0000	auto	2026-03-07 15:03:02.97659
2420	109	54	75256414.0000	auto	2026-03-07 15:03:02.97659
2421	109	60	40367.0000	auto	2026-03-07 15:03:02.97659
2422	109	55	82463056.5330	auto	2026-03-07 15:03:02.97659
2423	109	56	39378895.0000	auto	2026-03-07 15:03:02.97659
2424	109	57	209258838.6950	auto	2026-03-07 15:03:02.97659
2425	109	58	15396721.6960	auto	2026-03-07 15:03:02.97659
2426	109	59	1187822.8240	auto	2026-03-07 15:03:02.97659
2427	109	16	8931026.0000	auto	2026-03-07 15:03:02.97659
2428	109	38	10025.0000	auto	2026-03-07 15:03:02.97659
2429	109	39	20268640.0000	auto	2026-03-07 15:03:02.97659
2430	109	43	454250.0000	auto	2026-03-07 15:03:02.97659
2431	109	44	134294.0000	auto	2026-03-07 15:03:02.97659
2432	109	46	186354.0000	auto	2026-03-07 15:03:02.97659
2433	109	49	75391.0000	auto	2026-03-07 15:03:02.97659
2434	109	50	390606.0000	auto	2026-03-07 15:03:02.97659
2435	109	47	89056.0000	auto	2026-03-07 15:03:02.97659
2436	109	48	18400000.0000	auto	2026-03-07 15:03:02.97659
2437	110	52	119051737.0000	auto	2026-03-07 15:03:03.864457
2438	110	53	480954459.0000	auto	2026-03-07 15:03:03.864457
2439	110	54	73876814.0000	auto	2026-03-07 15:03:03.864457
2440	110	60	40089.0000	auto	2026-03-07 15:03:03.864457
2441	110	55	82098557.2140	auto	2026-03-07 15:03:03.864457
2442	110	56	42147295.0000	auto	2026-03-07 15:03:03.864457
2443	110	57	207901749.8100	auto	2026-03-07 15:03:03.864457
2444	110	58	15291853.9680	auto	2026-03-07 15:03:03.864457
2445	110	59	1189702.1920	auto	2026-03-07 15:03:03.864457
2446	110	16	8934467.0000	auto	2026-03-07 15:03:03.864457
2447	110	38	10027.0000	auto	2026-03-07 15:03:03.864457
2448	110	39	20268640.0000	auto	2026-03-07 15:03:03.864457
2449	110	43	477700.0000	auto	2026-03-07 15:03:03.864457
2450	110	44	134294.0000	auto	2026-03-07 15:03:03.864457
2451	110	46	186354.0000	auto	2026-03-07 15:03:03.864457
2452	110	49	75391.0000	auto	2026-03-07 15:03:03.864457
2453	110	50	390606.0000	auto	2026-03-07 15:03:03.864457
2454	110	47	89056.0000	auto	2026-03-07 15:03:03.864457
2455	110	48	18400000.0000	auto	2026-03-07 15:03:03.864457
2456	111	52	118113168.0000	auto	2026-03-07 15:03:04.701177
2457	111	53	473308414.0000	auto	2026-03-07 15:03:04.701177
2458	111	54	74343464.0000	auto	2026-03-07 15:03:04.701177
2459	111	60	39253.0000	auto	2026-03-07 15:03:04.701177
2460	111	55	80274216.4450	auto	2026-03-07 15:03:04.701177
2461	111	56	45558590.0000	auto	2026-03-07 15:03:04.701177
2462	111	57	201841221.1750	auto	2026-03-07 15:03:04.701177
2463	111	58	14832841.5550	auto	2026-03-07 15:03:04.701177
2464	111	59	1157779.9600	auto	2026-03-07 15:03:04.701177
2465	111	16	8937827.0000	auto	2026-03-07 15:03:04.701177
2466	111	38	10032.0000	auto	2026-03-07 15:03:04.701177
2467	111	39	20268640.0000	auto	2026-03-07 15:03:04.701177
2468	111	43	284591.0000	auto	2026-03-07 15:03:04.701177
2469	111	44	134294.0000	auto	2026-03-07 15:03:04.701177
2470	111	46	186354.0000	auto	2026-03-07 15:03:04.701177
2471	111	49	12391.0000	auto	2026-03-07 15:03:04.701177
2472	111	50	390606.0000	auto	2026-03-07 15:03:04.701177
2473	111	47	89056.0000	auto	2026-03-07 15:03:04.701177
2474	111	48	18400000.0000	auto	2026-03-07 15:03:04.701177
2475	112	52	115015984.0000	auto	2026-03-07 15:03:05.608587
2476	112	53	456947619.0000	auto	2026-03-07 15:03:05.608587
2477	112	54	69301664.0000	auto	2026-03-07 15:03:05.608587
2478	112	60	38967.0000	auto	2026-03-07 15:03:05.608587
2479	112	55	82038632.6100	auto	2026-03-07 15:03:05.608587
2480	112	56	41684695.0000	auto	2026-03-07 15:03:05.608587
2481	112	57	189216442.2600	auto	2026-03-07 15:03:05.608587
2482	112	58	15356557.8200	auto	2026-03-07 15:03:05.608587
2483	112	59	1118015.0800	auto	2026-03-07 15:03:05.608587
2484	112	16	8941192.0000	auto	2026-03-07 15:03:05.608587
2485	112	38	10036.0000	auto	2026-03-07 15:03:05.608587
2486	112	39	19284363.0000	auto	2026-03-07 15:03:05.608587
2487	112	43	964791.0000	auto	2026-03-07 15:03:05.608587
2488	112	44	134294.0000	auto	2026-03-07 15:03:05.608587
2489	112	46	186354.0000	auto	2026-03-07 15:03:05.608587
2490	112	49	12423.0000	auto	2026-03-07 15:03:05.608587
2491	112	50	390606.0000	auto	2026-03-07 15:03:05.608587
2492	112	47	89056.0000	auto	2026-03-07 15:03:05.608587
2493	112	48	18400000.0000	auto	2026-03-07 15:03:05.608587
2494	113	52	113716880.0000	auto	2026-03-07 15:03:06.483369
2495	113	53	448436578.0000	auto	2026-03-07 15:03:06.483369
2496	113	54	66637414.0000	auto	2026-03-07 15:03:06.483369
2497	113	60	39323.0000	auto	2026-03-07 15:03:06.483369
2498	113	55	79818432.1620	auto	2026-03-07 15:03:06.483369
2499	113	56	41842295.0000	auto	2026-03-07 15:03:06.483369
2500	113	57	178452425.0000	auto	2026-03-07 15:03:06.483369
2501	113	58	15631736.0000	auto	2026-03-07 15:03:06.483369
2502	113	59	1106147.0000	auto	2026-03-07 15:03:06.483369
2503	113	16	9694718.0000	auto	2026-03-07 15:03:06.483369
2504	113	38	1420300.0000	auto	2026-03-07 15:03:06.483369
2505	113	39	21284363.0000	auto	2026-03-07 15:03:06.483369
2506	113	43	3215962.0000	auto	2026-03-07 15:03:06.483369
2507	113	44	134294.0000	auto	2026-03-07 15:03:06.483369
2508	113	46	196354.0000	auto	2026-03-07 15:03:06.483369
2509	113	49	12423.0000	auto	2026-03-07 15:03:06.483369
2510	113	50	400606.0000	auto	2026-03-07 15:03:06.483369
2511	113	47	99056.0000	auto	2026-03-07 15:03:06.483369
2512	113	48	18500000.0000	auto	2026-03-07 15:03:06.483369
2513	114	52	114407883.0000	auto	2026-03-07 15:03:07.345061
2514	114	53	453324483.0000	auto	2026-03-07 15:03:07.345061
2515	114	54	67396464.0000	auto	2026-03-07 15:03:07.345061
2516	114	60	39382.0000	auto	2026-03-07 15:03:07.345061
2517	114	55	81131638.1020	auto	2026-03-07 15:03:07.345061
2518	114	56	42383485.0000	auto	2026-03-07 15:03:07.345061
2519	114	57	187175352.0000	auto	2026-03-07 15:03:07.345061
2520	114	58	15755636.5060	auto	2026-03-07 15:03:07.345061
2521	114	59	1143292.0000	auto	2026-03-07 15:03:07.345061
2522	114	16	9698337.0000	auto	2026-03-07 15:03:07.345061
2523	114	38	1421000.0000	auto	2026-03-07 15:03:07.345061
2524	114	39	20909032.0000	auto	2026-03-07 15:03:07.345061
2525	114	43	3229172.0000	auto	2026-03-07 15:03:07.345061
2526	114	44	134294.0000	auto	2026-03-07 15:03:07.345061
2527	114	46	196354.0000	auto	2026-03-07 15:03:07.345061
2528	114	49	12423.0000	auto	2026-03-07 15:03:07.345061
2529	114	50	400606.0000	auto	2026-03-07 15:03:07.345061
2530	114	47	99056.0000	auto	2026-03-07 15:03:07.345061
2531	114	48	18500000.0000	auto	2026-03-07 15:03:07.345061
2532	115	52	114220379.0000	auto	2026-03-07 15:03:08.209308
2533	115	53	451269442.0000	auto	2026-03-07 15:03:08.209308
2534	115	54	67486414.0000	auto	2026-03-07 15:03:08.209308
2535	115	60	43013.0000	auto	2026-03-07 15:03:08.209308
2536	115	55	79295406.8000	auto	2026-03-07 15:03:08.209308
2537	115	56	43564365.0000	auto	2026-03-07 15:03:08.209308
2538	115	57	176159372.0000	auto	2026-03-07 15:03:08.209308
2539	115	58	15584490.8000	auto	2026-03-07 15:03:08.209308
2540	115	59	1096865.0000	auto	2026-03-07 15:03:08.209308
2541	115	16	9471886.0000	auto	2026-03-07 15:03:08.209308
2542	115	38	1421525.0000	auto	2026-03-07 15:03:08.209308
2543	115	39	20909032.0000	auto	2026-03-07 15:03:08.209308
2544	115	43	2933513.0000	auto	2026-03-07 15:03:08.209308
2545	115	44	134294.0000	auto	2026-03-07 15:03:08.209308
2546	115	46	196354.0000	auto	2026-03-07 15:03:08.209308
2547	115	49	12423.0000	auto	2026-03-07 15:03:08.209308
2548	115	50	400606.0000	auto	2026-03-07 15:03:08.209308
2549	115	47	99056.0000	auto	2026-03-07 15:03:08.209308
2550	115	48	18500000.0000	auto	2026-03-07 15:03:08.209308
2551	7	52	116716336.0000	auto	2026-03-07 15:03:08.928205
2552	7	53	468720024.0000	auto	2026-03-07 15:03:08.928205
2553	7	54	71377564.0000	auto	2026-03-07 15:03:08.928205
2554	7	60	38597.0000	auto	2026-03-07 15:03:08.928205
2555	7	55	79886167.5520	auto	2026-03-07 15:03:08.928205
2556	7	56	44009290.0000	auto	2026-03-07 15:03:08.928205
2557	7	57	185202071.0560	auto	2026-03-07 15:03:08.928205
2558	7	58	15633114.4000	auto	2026-03-07 15:03:08.928205
2559	7	59	1122685.0000	auto	2026-03-07 15:03:08.928205
16	7	16	9475410.0000	manual	2026-03-07 07:58:53.303928
38	7	38	1422138.0000	manual	2026-03-07 07:58:53.384105
39	7	39	20909032.0000	manual	2026-03-07 07:58:53.386675
43	7	43	2933513.0000	manual	2026-03-07 07:58:53.402305
44	7	44	134294.0000	manual	2026-03-07 07:58:53.407766
46	7	46	196354.0000	manual	2026-03-07 07:58:53.410814
48	7	49	12432.0000	manual	2026-03-07 07:58:53.420971
49	7	50	400606.0000	manual	2026-03-07 07:58:53.424706
45	7	47	99056.0000	manual	2026-03-07 07:58:53.420504
47	7	48	18500000.0000	manual	2026-03-07 07:58:53.421251
2570	116	52	7730892.0000	auto	2026-03-07 15:15:48.39961
2571	116	53	22055739.0000	auto	2026-03-07 15:15:48.39961
2572	116	54	13401530.0000	auto	2026-03-07 15:15:48.39961
2573	116	60	25293088.0000	auto	2026-03-07 15:15:48.39961
2574	116	55	83891706.0000	auto	2026-03-07 15:15:48.39961
2575	116	57	18297741.0000	auto	2026-03-07 15:15:48.39961
2576	116	58	105020.0000	auto	2026-03-07 15:15:48.39961
2577	116	16	94517.0000	auto	2026-03-07 15:15:48.39961
2578	116	38	1504782.0000	auto	2026-03-07 15:15:48.39961
2579	116	39	500000.0000	auto	2026-03-07 15:15:48.39961
2580	116	43	10779760.0000	auto	2026-03-07 15:15:48.39961
2581	116	44	1500344.0000	auto	2026-03-07 15:15:48.39961
2582	116	51	20000000.0000	auto	2026-03-07 15:15:48.39961
2583	116	48	13900000.0000	auto	2026-03-07 15:15:48.39961
2584	117	52	7678606.0000	auto	2026-03-07 15:15:49.369666
2585	117	53	26426764.0000	auto	2026-03-07 15:15:49.369666
2586	117	54	23779137.0000	auto	2026-03-07 15:15:49.369666
2587	117	60	28866624.0000	auto	2026-03-07 15:15:49.369666
2588	117	55	68361900.0000	auto	2026-03-07 15:15:49.369666
2589	117	56	879193.0000	auto	2026-03-07 15:15:49.369666
2590	117	57	6400079.0000	auto	2026-03-07 15:15:49.369666
2591	117	58	1933504.0000	auto	2026-03-07 15:15:49.369666
2592	117	16	1044.0000	auto	2026-03-07 15:15:49.369666
2593	117	39	1895199.0000	auto	2026-03-07 15:15:49.369666
2594	117	43	3155306.0000	auto	2026-03-07 15:15:49.369666
2595	117	44	1000000.0000	auto	2026-03-07 15:15:49.369666
2596	117	46	20000.0000	auto	2026-03-07 15:15:49.369666
2597	117	51	20000000.0000	auto	2026-03-07 15:15:49.369666
2598	117	48	15100000.0000	auto	2026-03-07 15:15:49.369666
2599	118	52	58927012.0000	auto	2026-03-07 15:15:50.272094
2600	118	53	65051348.0000	auto	2026-03-07 15:15:50.272094
2601	118	54	92501218.0000	auto	2026-03-07 15:15:50.272094
2602	118	60	46343865.0000	auto	2026-03-07 15:15:50.272094
2603	118	55	114913190.0000	auto	2026-03-07 15:15:50.272094
2604	118	56	4763034.0000	auto	2026-03-07 15:15:50.272094
2605	118	57	31597310.0000	auto	2026-03-07 15:15:50.272094
2606	118	58	5639402.0000	auto	2026-03-07 15:15:50.272094
2607	118	16	11280540.0000	auto	2026-03-07 15:15:50.272094
2608	118	39	37171690.0000	auto	2026-03-07 15:15:50.272094
2609	118	43	2759356.0000	auto	2026-03-07 15:15:50.272094
2610	118	44	1434638.0000	auto	2026-03-07 15:15:50.272094
2611	118	46	237599.0000	auto	2026-03-07 15:15:50.272094
2612	118	49	12889.0000	auto	2026-03-07 15:15:50.272094
2613	118	50	190095.0000	auto	2026-03-07 15:15:50.272094
2614	118	48	16300000.0000	auto	2026-03-07 15:15:50.272094
2615	119	52	96816283.0000	auto	2026-03-07 15:15:51.183919
2616	119	53	387098279.0000	auto	2026-03-07 15:15:51.183919
2617	119	54	16398641.0000	auto	2026-03-07 15:15:51.183919
2618	119	60	269038.0000	auto	2026-03-07 15:15:51.183919
2619	119	55	155285077.0000	auto	2026-03-07 15:15:51.183919
2620	119	56	13045393.0000	auto	2026-03-07 15:15:51.183919
2621	119	57	199900535.1000	auto	2026-03-07 15:15:51.183919
2622	119	58	12599926.8800	auto	2026-03-07 15:15:51.183919
2623	119	59	524616.5680	auto	2026-03-07 15:15:51.183919
2624	119	39	17124244.0000	auto	2026-03-07 15:15:51.183919
2625	119	43	2543272.0000	auto	2026-03-07 15:15:51.183919
2626	119	44	8591.0000	auto	2026-03-07 15:15:51.183919
2627	119	46	106229.0000	auto	2026-03-07 15:15:51.183919
2628	119	49	12853.0000	auto	2026-03-07 15:15:51.183919
2629	119	50	310316.0000	auto	2026-03-07 15:15:51.183919
2630	119	48	17500000.0000	auto	2026-03-07 15:15:51.183919
2631	120	52	116259904.0000	auto	2026-03-07 15:15:52.074213
2632	120	53	467669203.0000	auto	2026-03-07 15:15:52.074213
2633	120	54	52692243.0000	auto	2026-03-07 15:15:52.074213
2634	120	60	41598.0000	auto	2026-03-07 15:15:52.074213
2635	120	55	100797090.5650	auto	2026-03-07 15:15:52.074213
2636	120	56	37152060.0000	auto	2026-03-07 15:15:52.074213
2637	120	57	208911633.9450	auto	2026-03-07 15:15:52.074213
2638	120	58	14489308.7450	auto	2026-03-07 15:15:52.074213
2639	120	59	1104982.3200	auto	2026-03-07 15:15:52.074213
2640	120	16	20002250.0000	auto	2026-03-07 15:15:52.074213
2641	120	39	18800585.0000	auto	2026-03-07 15:15:52.074213
2642	120	43	428877.0000	auto	2026-03-07 15:15:52.074213
2643	120	44	134294.0000	auto	2026-03-07 15:15:52.074213
2644	120	46	176354.0000	auto	2026-03-07 15:15:52.074213
2645	120	49	103878.0000	auto	2026-03-07 15:15:52.074213
2646	120	50	380606.0000	auto	2026-03-07 15:15:52.074213
2647	120	47	79056.0000	auto	2026-03-07 15:15:52.074213
2648	120	48	18300000.0000	auto	2026-03-07 15:15:52.074213
2649	116	45	1000000.0000	auto	2026-03-07 15:33:23.239291
2650	117	45	900000.0000	auto	2026-03-07 15:33:23.239291
2651	118	45	1420000.0000	auto	2026-03-07 15:33:23.239291
2652	119	45	1375000.0000	auto	2026-03-07 15:33:23.239291
2653	120	45	0.0000	auto	2026-03-07 15:33:23.239291
2654	116	61	93110000.0000	auto	2026-03-07 15:38:31.119826
2655	117	61	95110000.0000	auto	2026-03-07 15:38:31.119826
2656	118	61	50000000.0000	auto	2026-03-07 15:38:31.119826
2657	119	61	0.0000	auto	2026-03-07 15:38:31.119826
2658	120	61	0.0000	auto	2026-03-07 15:38:31.119826
\.


--
-- Data for Name: snapshots; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.snapshots (snapshot_id, user_id, reference_date, status, locked_at, editable_until, created_at) FROM stdin;
7	1	2026-03-07	locked	2026-03-07 07:59:48.034275	\N	2026-03-07 07:50:16.023909
13	1	2024-03-09	in_progress	\N	\N	2026-03-07 14:59:01.594114
14	1	2024-03-16	in_progress	\N	\N	2026-03-07 14:59:05.115833
15	1	2024-03-23	in_progress	\N	\N	2026-03-07 14:59:08.451027
16	1	2024-03-30	in_progress	\N	\N	2026-03-07 14:59:12.120049
17	1	2024-04-06	in_progress	\N	\N	2026-03-07 14:59:15.767623
18	1	2024-04-13	in_progress	\N	\N	2026-03-07 14:59:19.199877
19	1	2024-04-20	in_progress	\N	\N	2026-03-07 14:59:21.535639
20	1	2024-04-27	in_progress	\N	\N	2026-03-07 14:59:25.158935
21	1	2024-05-04	in_progress	\N	\N	2026-03-07 14:59:28.569291
22	1	2024-05-11	in_progress	\N	\N	2026-03-07 14:59:32.033523
23	1	2024-05-18	in_progress	\N	\N	2026-03-07 14:59:35.810343
24	1	2024-05-25	in_progress	\N	\N	2026-03-07 14:59:39.230556
25	1	2024-06-01	in_progress	\N	\N	2026-03-07 14:59:42.736492
26	1	2024-06-08	in_progress	\N	\N	2026-03-07 14:59:46.069159
27	1	2024-06-15	in_progress	\N	\N	2026-03-07 14:59:49.50086
28	1	2024-06-22	in_progress	\N	\N	2026-03-07 14:59:51.746741
29	1	2024-06-29	in_progress	\N	\N	2026-03-07 14:59:55.14756
30	1	2024-07-06	in_progress	\N	\N	2026-03-07 14:59:58.524335
31	1	2024-07-13	in_progress	\N	\N	2026-03-07 15:00:01.926204
32	1	2024-07-20	in_progress	\N	\N	2026-03-07 15:00:05.315303
33	1	2024-07-27	in_progress	\N	\N	2026-03-07 15:00:08.709042
34	1	2024-08-03	in_progress	\N	\N	2026-03-07 15:00:12.093078
35	1	2024-08-10	in_progress	\N	\N	2026-03-07 15:00:15.253394
36	1	2024-08-17	in_progress	\N	\N	2026-03-07 15:00:18.639901
37	1	2024-08-24	in_progress	\N	\N	2026-03-07 15:00:20.926759
38	1	2024-08-31	in_progress	\N	\N	2026-03-07 15:00:24.184495
39	1	2024-09-07	in_progress	\N	\N	2026-03-07 15:00:27.451009
40	1	2024-09-14	in_progress	\N	\N	2026-03-07 15:00:30.615293
41	1	2024-09-21	in_progress	\N	\N	2026-03-07 15:00:33.764445
42	1	2024-09-28	in_progress	\N	\N	2026-03-07 15:00:37.038811
43	1	2024-10-05	in_progress	\N	\N	2026-03-07 15:00:40.424541
44	1	2024-10-12	in_progress	\N	\N	2026-03-07 15:00:43.694941
45	1	2024-10-19	in_progress	\N	\N	2026-03-07 15:02:09.945884
46	1	2024-10-26	in_progress	\N	\N	2026-03-07 15:02:10.793856
47	1	2024-11-02	in_progress	\N	\N	2026-03-07 15:02:11.643198
48	1	2024-11-09	in_progress	\N	\N	2026-03-07 15:02:12.505074
49	1	2024-11-16	in_progress	\N	\N	2026-03-07 15:02:13.334808
50	1	2024-11-23	in_progress	\N	\N	2026-03-07 15:02:14.228679
51	1	2024-11-30	in_progress	\N	\N	2026-03-07 15:02:14.656698
52	1	2024-12-07	in_progress	\N	\N	2026-03-07 15:02:15.007831
53	1	2024-12-14	in_progress	\N	\N	2026-03-07 15:02:15.899618
54	1	2024-12-21	in_progress	\N	\N	2026-03-07 15:02:16.761836
55	1	2024-12-28	in_progress	\N	\N	2026-03-07 15:02:17.603324
56	1	2025-01-04	in_progress	\N	\N	2026-03-07 15:02:18.4543
57	1	2025-01-11	in_progress	\N	\N	2026-03-07 15:02:19.310853
58	1	2025-01-18	in_progress	\N	\N	2026-03-07 15:02:20.177397
59	1	2025-01-25	in_progress	\N	\N	2026-03-07 15:02:21.046787
60	1	2025-02-01	in_progress	\N	\N	2026-03-07 15:02:21.885827
61	1	2025-02-08	in_progress	\N	\N	2026-03-07 15:02:22.770482
62	1	2025-02-15	in_progress	\N	\N	2026-03-07 15:02:23.609403
63	1	2025-02-22	in_progress	\N	\N	2026-03-07 15:02:24.510185
64	1	2025-03-01	in_progress	\N	\N	2026-03-07 15:02:25.357293
65	1	2025-03-08	in_progress	\N	\N	2026-03-07 15:02:26.224414
66	1	2025-03-15	in_progress	\N	\N	2026-03-07 15:02:27.123828
67	1	2025-03-22	in_progress	\N	\N	2026-03-07 15:02:27.97022
68	1	2025-03-29	in_progress	\N	\N	2026-03-07 15:02:28.782255
69	1	2025-04-05	in_progress	\N	\N	2026-03-07 15:02:29.662024
70	1	2025-04-12	in_progress	\N	\N	2026-03-07 15:02:30.505545
71	1	2025-04-19	in_progress	\N	\N	2026-03-07 15:02:31.364753
72	1	2025-04-26	in_progress	\N	\N	2026-03-07 15:02:32.231064
73	1	2025-05-03	in_progress	\N	\N	2026-03-07 15:02:33.102073
74	1	2025-05-10	in_progress	\N	\N	2026-03-07 15:02:33.979504
75	1	2025-05-17	in_progress	\N	\N	2026-03-07 15:02:34.822334
76	1	2025-05-24	in_progress	\N	\N	2026-03-07 15:02:35.666688
77	1	2025-05-31	in_progress	\N	\N	2026-03-07 15:02:36.500556
78	1	2025-06-07	in_progress	\N	\N	2026-03-07 15:02:37.38665
79	1	2025-06-14	in_progress	\N	\N	2026-03-07 15:02:38.22575
80	1	2025-06-21	in_progress	\N	\N	2026-03-07 15:02:39.053142
81	1	2025-06-28	in_progress	\N	\N	2026-03-07 15:02:39.898043
82	1	2025-07-05	in_progress	\N	\N	2026-03-07 15:02:40.757279
83	1	2025-07-12	in_progress	\N	\N	2026-03-07 15:02:41.630089
84	1	2025-07-19	in_progress	\N	\N	2026-03-07 15:02:42.479156
85	1	2025-07-26	in_progress	\N	\N	2026-03-07 15:02:43.334976
86	1	2025-08-02	in_progress	\N	\N	2026-03-07 15:02:43.100537
87	1	2025-08-09	in_progress	\N	\N	2026-03-07 15:02:43.945459
88	1	2025-08-16	in_progress	\N	\N	2026-03-07 15:02:44.820607
89	1	2025-08-23	in_progress	\N	\N	2026-03-07 15:02:45.618576
90	1	2025-08-30	in_progress	\N	\N	2026-03-07 15:02:46.528015
91	1	2025-09-13	in_progress	\N	\N	2026-03-07 15:02:47.376117
92	1	2025-09-20	in_progress	\N	\N	2026-03-07 15:02:48.248142
93	1	2025-09-27	in_progress	\N	\N	2026-03-07 15:02:49.159167
94	1	2025-10-04	in_progress	\N	\N	2026-03-07 15:02:49.983792
95	1	2025-10-11	in_progress	\N	\N	2026-03-07 15:02:50.836985
96	1	2025-10-18	in_progress	\N	\N	2026-03-07 15:02:51.703595
97	1	2025-10-25	in_progress	\N	\N	2026-03-07 15:02:52.56675
98	1	2025-11-01	in_progress	\N	\N	2026-03-07 15:02:53.388308
99	1	2025-11-08	in_progress	\N	\N	2026-03-07 15:02:54.22062
100	1	2025-11-15	in_progress	\N	\N	2026-03-07 15:02:55.157121
101	1	2025-11-22	in_progress	\N	\N	2026-03-07 15:02:56.039288
102	1	2025-11-29	in_progress	\N	\N	2026-03-07 15:02:56.921179
103	1	2025-12-06	in_progress	\N	\N	2026-03-07 15:02:57.756328
104	1	2025-12-13	in_progress	\N	\N	2026-03-07 15:02:58.616611
105	1	2025-12-20	in_progress	\N	\N	2026-03-07 15:02:59.443958
106	1	2025-12-27	in_progress	\N	\N	2026-03-07 15:03:00.300899
107	1	2026-01-03	in_progress	\N	\N	2026-03-07 15:03:01.128281
108	1	2026-01-10	in_progress	\N	\N	2026-03-07 15:03:01.985515
109	1	2026-01-17	in_progress	\N	\N	2026-03-07 15:03:02.837613
110	1	2026-01-24	in_progress	\N	\N	2026-03-07 15:03:03.709019
111	1	2026-01-31	in_progress	\N	\N	2026-03-07 15:03:04.548161
112	1	2026-02-07	in_progress	\N	\N	2026-03-07 15:03:05.452258
113	1	2026-02-14	in_progress	\N	\N	2026-03-07 15:03:06.328733
114	1	2026-02-21	in_progress	\N	\N	2026-03-07 15:03:07.202803
115	1	2026-02-28	in_progress	\N	\N	2026-03-07 15:03:08.068273
116	1	2022-01-01	in_progress	\N	\N	2026-03-07 15:15:48.247095
117	1	2023-01-01	in_progress	\N	\N	2026-03-07 15:15:49.205759
118	1	2024-01-01	in_progress	\N	\N	2026-03-07 15:15:50.128662
119	1	2025-01-01	in_progress	\N	\N	2026-03-07 15:15:51.028206
120	1	2026-01-01	in_progress	\N	\N	2026-03-07 15:15:51.927416
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
-- Data for Name: target_allocation_asset_classes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.target_allocation_asset_classes (target_allocation_asset_class_id, year, asset_class, target_percentage, created_at, updated_at) FROM stdin;
1	2026	주식	80.00	2026-03-07 14:12:59.169115	2026-03-07 14:19:37.84865
2	2026	채권	5.00	2026-03-07 14:12:59.181889	2026-03-07 14:19:37.855081
3	2026	금	5.00	2026-03-07 14:12:59.187478	2026-03-07 14:19:37.861378
4	2026	통화	5.00	2026-03-07 14:12:59.192245	2026-03-07 14:19:37.866448
5	2026	부동산	4.50	2026-03-07 14:12:59.198392	2026-03-07 14:19:37.870808
6	2026	가상자산	0.50	2026-03-07 14:12:59.202783	2026-03-07 14:19:37.875125
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
2118	88	52	117308784.0000	auto	2026-03-07 15:02:54.866463
2119	88	53	471174070.0000	auto	2026-03-07 15:02:54.866463
2120	88	54	52889233.0000	auto	2026-03-07 15:02:54.866463
2121	88	60	41355.0000	auto	2026-03-07 15:02:54.866463
2122	88	55	100200072.0000	auto	2026-03-07 15:02:54.866463
2123	88	56	27808563.0000	auto	2026-03-07 15:02:54.866463
2124	88	57	220097791.5600	auto	2026-03-07 15:02:54.866463
2125	88	58	14546842.0640	auto	2026-03-07 15:02:54.866463
2126	88	59	1066099.0000	auto	2026-03-07 15:02:54.866463
2127	88	16	22393393.0000	auto	2026-03-07 15:02:54.866463
2128	88	39	15546312.0000	auto	2026-03-07 15:02:54.866463
2129	88	43	1803595.0000	auto	2026-03-07 15:02:54.866463
2130	88	44	124263.0000	auto	2026-03-07 15:02:54.866463
2131	88	46	156315.0000	auto	2026-03-07 15:02:54.866463
2132	88	49	4653.0000	auto	2026-03-07 15:02:54.866463
2133	88	50	360453.0000	auto	2026-03-07 15:02:54.866463
2134	88	48	18100000.0000	auto	2026-03-07 15:02:54.866463
68	3	52	66895260.0000	auto	2026-03-07 14:59:08.172115
69	3	53	81915953.0000	auto	2026-03-07 14:59:08.172115
70	3	54	121949588.0000	auto	2026-03-07 14:59:08.172115
71	3	60	43502070.0000	auto	2026-03-07 14:59:08.172115
72	3	55	122209286.7100	auto	2026-03-07 14:59:08.172115
73	3	56	6360999.0000	auto	2026-03-07 14:59:08.172115
74	3	57	41294821.0000	auto	2026-03-07 14:59:08.172115
75	3	58	6948548.0000	auto	2026-03-07 14:59:08.172115
76	3	59	101827.0000	auto	2026-03-07 14:59:08.172115
77	3	16	4585352.0000	auto	2026-03-07 14:59:08.172115
78	3	39	44630781.0000	auto	2026-03-07 14:59:08.172115
79	3	43	2731084.0000	auto	2026-03-07 14:59:08.172115
80	3	44	114638.0000	auto	2026-03-07 14:59:08.172115
81	3	46	267599.0000	auto	2026-03-07 14:59:08.172115
82	3	49	12910.0000	auto	2026-03-07 14:59:08.172115
83	3	50	220095.0000	auto	2026-03-07 14:59:08.172115
85	4	52	68681848.0000	auto	2026-03-07 14:59:11.78781
86	4	53	84332291.0000	auto	2026-03-07 14:59:11.78781
87	4	54	128008380.0000	auto	2026-03-07 14:59:11.78781
88	4	60	47510530.0000	auto	2026-03-07 14:59:11.78781
89	4	55	124210752.8480	auto	2026-03-07 14:59:11.78781
90	4	56	6425749.0000	auto	2026-03-07 14:59:11.78781
91	4	57	47252663.5600	auto	2026-03-07 14:59:11.78781
92	4	58	7303437.6800	auto	2026-03-07 14:59:11.78781
93	4	59	104465.3840	auto	2026-03-07 14:59:11.78781
94	4	16	24340170.0000	auto	2026-03-07 14:59:11.78781
95	4	38	9402317.0000	auto	2026-03-07 14:59:11.78781
96	4	39	45079991.0000	auto	2026-03-07 14:59:11.78781
97	4	43	2595974.0000	auto	2026-03-07 14:59:11.78781
98	4	44	18764.0000	auto	2026-03-07 14:59:11.78781
99	4	46	21815841.0000	auto	2026-03-07 14:59:11.78781
103	5	52	69178625.0000	auto	2026-03-07 14:59:15.491622
104	5	53	84879328.0000	auto	2026-03-07 14:59:15.491622
105	5	54	127533166.0000	auto	2026-03-07 14:59:15.491622
106	5	60	50594122.0000	auto	2026-03-07 14:59:15.491622
107	5	55	127688885.6960	auto	2026-03-07 14:59:15.491622
108	5	56	6738579.0000	auto	2026-03-07 14:59:15.491622
109	5	57	46802962.7760	auto	2026-03-07 14:59:15.491622
110	5	58	7945546.8960	auto	2026-03-07 14:59:15.491622
111	5	59	105629.3840	auto	2026-03-07 14:59:15.491622
112	5	16	32357095.0000	auto	2026-03-07 14:59:15.491622
113	5	38	20057980.0000	auto	2026-03-07 14:59:15.491622
114	5	39	45154872.0000	auto	2026-03-07 14:59:15.491622
115	5	43	1524069.0000	auto	2026-03-07 14:59:15.491622
116	5	44	157800.0000	auto	2026-03-07 14:59:15.491622
117	5	46	1815841.0000	auto	2026-03-07 14:59:15.491622
118	5	49	12961.0000	auto	2026-03-07 14:59:15.491622
119	5	50	220095.0000	auto	2026-03-07 14:59:15.491622
121	6	52	68739755.0000	auto	2026-03-07 14:59:18.927249
122	6	53	84971172.0000	auto	2026-03-07 14:59:18.927249
123	6	54	124264339.0000	auto	2026-03-07 14:59:18.927249
124	6	60	52875045.0000	auto	2026-03-07 14:59:18.927249
125	6	55	129052950.6960	auto	2026-03-07 14:59:18.927249
126	6	56	6828719.0000	auto	2026-03-07 14:59:18.927249
127	6	57	47951277.0000	auto	2026-03-07 14:59:18.927249
128	6	58	8037070.0960	auto	2026-03-07 14:59:18.927249
2135	88	47	59041.0000	auto	2026-03-07 15:02:54.866463
2187	91	49	4653.0000	auto	2026-03-07 15:02:57.464384
2188	91	50	370453.0000	auto	2026-03-07 15:02:57.464384
2189	91	48	18200000.0000	auto	2026-03-07 15:02:57.464384
2190	91	47	69041.0000	auto	2026-03-07 15:02:57.464384
2205	92	49	4656.0000	auto	2026-03-07 15:02:58.333375
2206	92	50	370453.0000	auto	2026-03-07 15:02:58.333375
2207	92	48	18200000.0000	auto	2026-03-07 15:02:58.333375
2208	92	47	69041.0000	auto	2026-03-07 15:02:58.333375
2209	93	52	118891184.0000	auto	2026-03-07 15:02:59.157342
2210	93	53	483506093.0000	auto	2026-03-07 15:02:59.157342
2211	93	54	55630063.0000	auto	2026-03-07 15:02:59.157342
2212	93	60	42849.0000	auto	2026-03-07 15:02:59.157342
2213	93	55	102953383.0000	auto	2026-03-07 15:02:59.157342
2214	93	56	34191355.0000	auto	2026-03-07 15:02:59.157342
2215	93	57	209082436.8700	auto	2026-03-07 15:02:59.157342
2216	93	58	14970492.0000	auto	2026-03-07 15:02:59.157342
139	7	52	71327369.0000	auto	2026-03-07 14:59:21.236531
140	7	53	89582818.0000	auto	2026-03-07 14:59:21.236531
141	7	54	135276325.0000	auto	2026-03-07 14:59:21.236531
142	7	60	53291281.0000	auto	2026-03-07 14:59:21.236531
143	7	55	126889997.4760	auto	2026-03-07 14:59:21.236531
144	7	56	7671349.0000	auto	2026-03-07 14:59:21.236531
145	7	57	50154259.0000	auto	2026-03-07 14:59:21.236531
146	7	58	8434064.0000	auto	2026-03-07 14:59:21.236531
147	7	59	155455.4320	auto	2026-03-07 14:59:21.236531
157	8	52	68091681.0000	auto	2026-03-07 14:59:24.860833
158	8	53	84190331.0000	auto	2026-03-07 14:59:24.860833
159	8	54	119391940.0000	auto	2026-03-07 14:59:24.860833
160	8	60	50539991.0000	auto	2026-03-07 14:59:24.860833
161	8	55	127258891.0000	auto	2026-03-07 14:59:24.860833
162	8	56	7820799.0000	auto	2026-03-07 14:59:24.860833
163	8	57	39690535.0000	auto	2026-03-07 14:59:24.860833
164	8	58	8775216.0000	auto	2026-03-07 14:59:24.860833
165	8	59	145836.0000	auto	2026-03-07 14:59:24.860833
166	8	16	27454766.0000	auto	2026-03-07 14:59:24.860833
167	8	38	16687853.0000	auto	2026-03-07 14:59:24.860833
168	8	39	49217420.0000	auto	2026-03-07 14:59:24.860833
169	8	43	286462.0000	auto	2026-03-07 14:59:24.860833
170	8	44	17800.0000	auto	2026-03-07 14:59:24.860833
171	8	46	25841.0000	auto	2026-03-07 14:59:24.860833
172	8	49	12983.0000	auto	2026-03-07 14:59:24.860833
173	8	50	230095.0000	auto	2026-03-07 14:59:24.860833
175	9	52	69406665.0000	auto	2026-03-07 14:59:28.287629
176	9	53	86067164.0000	auto	2026-03-07 14:59:28.287629
177	9	54	124603765.0000	auto	2026-03-07 14:59:28.287629
178	9	60	50781592.0000	auto	2026-03-07 14:59:28.287629
179	9	55	130134328.0000	auto	2026-03-07 14:59:28.287629
180	9	56	7573469.0000	auto	2026-03-07 14:59:28.287629
181	9	57	47346529.0000	auto	2026-03-07 14:59:28.287629
182	9	58	9155239.0000	auto	2026-03-07 14:59:28.287629
183	9	59	194704.0000	auto	2026-03-07 14:59:28.287629
184	9	16	25968974.0000	auto	2026-03-07 14:59:28.287629
185	9	38	15606254.0000	auto	2026-03-07 14:59:28.287629
186	9	39	47856302.0000	auto	2026-03-07 14:59:28.287629
187	9	43	251430.0000	auto	2026-03-07 14:59:28.287629
188	9	44	52800.0000	auto	2026-03-07 14:59:28.287629
189	9	46	25841.0000	auto	2026-03-07 14:59:28.287629
190	9	49	12983.0000	auto	2026-03-07 14:59:28.287629
191	9	50	230095.0000	auto	2026-03-07 14:59:28.287629
193	10	52	69419814.0000	auto	2026-03-07 14:59:31.718371
194	10	53	86359882.0000	auto	2026-03-07 14:59:31.718371
195	10	54	124458187.0000	auto	2026-03-07 14:59:31.718371
196	10	60	52377950.0000	auto	2026-03-07 14:59:31.718371
197	10	55	132631210.0000	auto	2026-03-07 14:59:31.718371
198	10	56	7340889.0000	auto	2026-03-07 14:59:31.718371
199	10	57	50123176.0000	auto	2026-03-07 14:59:31.718371
200	10	58	9462256.0000	auto	2026-03-07 14:59:31.718371
201	10	59	196084.0000	auto	2026-03-07 14:59:31.718371
202	10	16	24082200.0000	auto	2026-03-07 14:59:31.718371
203	10	38	14864254.0000	auto	2026-03-07 14:59:31.718371
204	10	39	46884554.0000	auto	2026-03-07 14:59:31.718371
205	10	43	260889.0000	auto	2026-03-07 14:59:31.718371
206	10	44	37800.0000	auto	2026-03-07 14:59:31.718371
207	10	46	25841.0000	auto	2026-03-07 14:59:31.718371
208	10	49	13004.0000	auto	2026-03-07 14:59:31.718371
209	10	50	230095.0000	auto	2026-03-07 14:59:31.718371
211	11	52	71501447.0000	auto	2026-03-07 14:59:35.485553
212	11	53	90612335.0000	auto	2026-03-07 14:59:35.485553
213	11	54	133930055.0000	auto	2026-03-07 14:59:35.485553
214	11	60	53461544.0000	auto	2026-03-07 14:59:35.485553
215	11	55	135702590.0000	auto	2026-03-07 14:59:35.485553
216	11	56	7913689.0000	auto	2026-03-07 14:59:35.485553
217	11	57	51419541.0000	auto	2026-03-07 14:59:35.485553
218	11	58	9835566.0000	auto	2026-03-07 14:59:35.485553
219	11	59	196432.6880	auto	2026-03-07 14:59:35.485553
220	11	16	22194567.0000	auto	2026-03-07 14:59:35.485553
221	11	38	14172796.0000	auto	2026-03-07 14:59:35.485553
222	11	39	46790362.0000	auto	2026-03-07 14:59:35.485553
223	11	43	1208920.0000	auto	2026-03-07 14:59:35.485553
224	11	44	122800.0000	auto	2026-03-07 14:59:35.485553
225	11	46	35841.0000	auto	2026-03-07 14:59:35.485553
226	11	49	12704.0000	auto	2026-03-07 14:59:35.485553
227	11	50	240095.0000	auto	2026-03-07 14:59:35.485553
229	12	52	72303188.0000	auto	2026-03-07 14:59:38.926758
230	12	53	91940153.0000	auto	2026-03-07 14:59:38.926758
231	12	54	138818974.0000	auto	2026-03-07 14:59:38.926758
232	12	60	52334379.0000	auto	2026-03-07 14:59:38.926758
233	12	55	137871409.0000	auto	2026-03-07 14:59:38.926758
234	12	56	7922619.0000	auto	2026-03-07 14:59:38.926758
235	12	57	54797072.0000	auto	2026-03-07 14:59:38.926758
236	12	58	10173674.7900	auto	2026-03-07 14:59:38.926758
237	12	59	199594.0000	auto	2026-03-07 14:59:38.926758
238	12	16	20205759.0000	auto	2026-03-07 14:59:38.926758
239	12	38	13439096.0000	auto	2026-03-07 14:59:38.926758
240	12	39	46767226.0000	auto	2026-03-07 14:59:38.926758
241	12	43	259413.0000	auto	2026-03-07 14:59:38.926758
242	12	44	7800.0000	auto	2026-03-07 14:59:38.926758
243	12	46	35841.0000	auto	2026-03-07 14:59:38.926758
244	12	49	12704.0000	auto	2026-03-07 14:59:38.926758
247	13	52	73636415.0000	auto	2026-03-07 14:59:42.432613
248	13	53	93767131.0000	auto	2026-03-07 14:59:42.432613
249	13	54	142259098.0000	auto	2026-03-07 14:59:42.432613
250	13	60	51503861.0000	auto	2026-03-07 14:59:42.432613
251	13	55	138705705.0000	auto	2026-03-07 14:59:42.432613
252	13	56	7841359.0000	auto	2026-03-07 14:59:42.432613
253	13	57	58632092.0000	auto	2026-03-07 14:59:42.432613
254	13	58	10499306.0000	auto	2026-03-07 14:59:42.432613
255	13	59	208272.0000	auto	2026-03-07 14:59:42.432613
256	13	16	20216656.0000	auto	2026-03-07 14:59:42.432613
257	13	38	12565850.0000	auto	2026-03-07 14:59:42.432613
258	13	39	46767226.0000	auto	2026-03-07 14:59:42.432613
259	13	43	170313.0000	auto	2026-03-07 14:59:42.432613
260	13	44	42800.0000	auto	2026-03-07 14:59:42.432613
261	13	46	35841.0000	auto	2026-03-07 14:59:42.432613
2136	89	52	115040924.0000	auto	2026-03-07 15:02:55.733603
2137	89	53	463998635.0000	auto	2026-03-07 15:02:55.733603
2138	89	54	51948453.0000	auto	2026-03-07 15:02:55.733603
2139	89	60	42176.0000	auto	2026-03-07 15:02:55.733603
2140	89	55	101530584.0000	auto	2026-03-07 15:02:55.733603
2141	89	56	29767186.0000	auto	2026-03-07 15:02:55.733603
2142	89	57	224263672.6400	auto	2026-03-07 15:02:55.733603
2143	89	58	14730327.6640	auto	2026-03-07 15:02:55.733603
2144	89	59	1079663.0000	auto	2026-03-07 15:02:55.733603
2145	89	16	23964135.0000	auto	2026-03-07 15:02:55.733603
2146	89	39	16983303.0000	auto	2026-03-07 15:02:55.733603
2147	89	43	4007595.0000	auto	2026-03-07 15:02:55.733603
2148	89	44	134263.0000	auto	2026-03-07 15:02:55.733603
2149	89	46	166315.0000	auto	2026-03-07 15:02:55.733603
2150	89	49	4653.0000	auto	2026-03-07 15:02:55.733603
2151	89	50	370453.0000	auto	2026-03-07 15:02:55.733603
2152	89	48	18200000.0000	auto	2026-03-07 15:02:55.733603
2153	89	47	69041.0000	auto	2026-03-07 15:02:55.733603
265	14	52	74314061.0000	auto	2026-03-07 14:59:45.782252
266	14	53	95334967.0000	auto	2026-03-07 14:59:45.782252
268	14	60	40103150.0000	auto	2026-03-07 14:59:45.782252
283	15	52	75693972.0000	auto	2026-03-07 14:59:49.165025
284	15	53	97786144.0000	auto	2026-03-07 14:59:49.165025
285	15	54	158344412.0000	auto	2026-03-07 14:59:49.165025
286	15	60	32003942.0000	auto	2026-03-07 14:59:49.165025
287	15	55	139975092.0000	auto	2026-03-07 14:59:49.165025
288	15	56	7933516.0000	auto	2026-03-07 14:59:49.165025
289	15	57	83181289.3900	auto	2026-03-07 14:59:49.165025
290	15	58	10914234.5400	auto	2026-03-07 14:59:49.165025
291	15	59	266183.0000	auto	2026-03-07 14:59:49.165025
292	15	16	14729302.0000	auto	2026-03-07 14:59:49.165025
293	15	38	10774969.0000	auto	2026-03-07 14:59:49.165025
294	15	39	46475587.0000	auto	2026-03-07 14:59:49.165025
295	15	43	254995.0000	auto	2026-03-07 14:59:49.165025
296	15	44	47800.0000	auto	2026-03-07 14:59:49.165025
297	15	46	35841.0000	auto	2026-03-07 14:59:49.165025
298	15	49	12704.0000	auto	2026-03-07 14:59:49.165025
301	16	52	79910477.0000	auto	2026-03-07 14:59:51.450387
302	16	53	105664393.0000	auto	2026-03-07 14:59:51.450387
303	16	54	179535567.0000	auto	2026-03-07 14:59:51.450387
304	16	60	22549672.0000	auto	2026-03-07 14:59:51.450387
305	16	55	141426167.0000	auto	2026-03-07 14:59:51.450387
306	16	56	8198766.0000	auto	2026-03-07 14:59:51.450387
307	16	57	109190945.1220	auto	2026-03-07 14:59:51.450387
308	16	58	11119279.4510	auto	2026-03-07 14:59:51.450387
309	16	59	271275.1720	auto	2026-03-07 14:59:51.450387
310	16	16	14873195.0000	auto	2026-03-07 14:59:51.450387
311	16	38	11478268.0000	auto	2026-03-07 14:59:51.450387
312	16	39	46469992.0000	auto	2026-03-07 14:59:51.450387
313	16	43	3279473.0000	auto	2026-03-07 14:59:51.450387
314	16	44	32800.0000	auto	2026-03-07 14:59:51.450387
315	16	46	45841.0000	auto	2026-03-07 14:59:51.450387
316	16	49	12704.0000	auto	2026-03-07 14:59:51.450387
317	16	50	250193.0000	auto	2026-03-07 14:59:51.450387
319	17	52	80648842.0000	auto	2026-03-07 14:59:54.872424
320	17	53	107922526.0000	auto	2026-03-07 14:59:54.872424
321	17	54	182229145.0000	auto	2026-03-07 14:59:54.872424
322	17	60	12448601.0000	auto	2026-03-07 14:59:54.872424
323	17	55	142561959.0000	auto	2026-03-07 14:59:54.872424
324	17	56	8416356.0000	auto	2026-03-07 14:59:54.872424
325	17	57	115155635.2040	auto	2026-03-07 14:59:54.872424
326	17	58	11188763.4510	auto	2026-03-07 14:59:54.872424
327	17	59	274767.1720	auto	2026-03-07 14:59:54.872424
328	17	16	13594473.0000	auto	2026-03-07 14:59:54.872424
329	17	38	11483176.0000	auto	2026-03-07 14:59:54.872424
330	17	39	46469992.0000	auto	2026-03-07 14:59:54.872424
331	17	43	2951712.0000	auto	2026-03-07 14:59:54.872424
332	17	44	22821.0000	auto	2026-03-07 14:59:54.872424
333	17	46	45841.0000	auto	2026-03-07 14:59:54.872424
334	17	49	12704.0000	auto	2026-03-07 14:59:54.872424
335	17	50	250193.0000	auto	2026-03-07 14:59:54.872424
337	18	52	80902349.0000	auto	2026-03-07 14:59:58.204718
338	18	53	108135314.0000	auto	2026-03-07 14:59:58.204718
339	18	54	182390644.0000	auto	2026-03-07 14:59:58.204718
340	18	60	352714.0000	auto	2026-03-07 14:59:58.204718
341	18	55	142222227.0000	auto	2026-03-07 14:59:58.204718
342	18	56	8257136.0000	auto	2026-03-07 14:59:58.204718
343	18	57	125124834.0650	auto	2026-03-07 14:59:58.204718
344	18	58	11024714.2990	auto	2026-03-07 14:59:58.204718
345	18	59	276240.3690	auto	2026-03-07 14:59:58.204718
346	18	16	13601754.0000	auto	2026-03-07 14:59:58.204718
347	18	38	14488071.0000	auto	2026-03-07 14:59:58.204718
348	18	39	45548718.0000	auto	2026-03-07 14:59:58.204718
349	18	43	2720920.0000	auto	2026-03-07 14:59:58.204718
350	18	44	7821.0000	auto	2026-03-07 14:59:58.204718
351	18	46	46192.0000	auto	2026-03-07 14:59:58.204718
352	18	49	12704.0000	auto	2026-03-07 14:59:58.204718
355	19	52	82876154.0000	auto	2026-03-07 15:00:01.620129
356	19	53	110685301.0000	auto	2026-03-07 15:00:01.620129
357	19	54	190496891.0000	auto	2026-03-07 15:00:01.620129
358	19	60	352212.0000	auto	2026-03-07 15:00:01.620129
359	19	55	143666284.0000	auto	2026-03-07 15:00:01.620129
360	19	56	8415306.0000	auto	2026-03-07 15:00:01.620129
361	19	57	146526588.0140	auto	2026-03-07 15:00:01.620129
362	19	58	10930471.0000	auto	2026-03-07 15:00:01.620129
363	19	59	285260.6910	auto	2026-03-07 15:00:01.620129
364	19	16	13338899.0000	auto	2026-03-07 15:00:01.620129
365	19	38	10003722.0000	auto	2026-03-07 15:00:01.620129
366	19	39	45548718.0000	auto	2026-03-07 15:00:01.620129
367	19	43	16071505.0000	auto	2026-03-07 15:00:01.620129
368	19	44	1263.0000	auto	2026-03-07 15:00:01.620129
369	19	46	46192.0000	auto	2026-03-07 15:00:01.620129
370	19	49	12743.0000	auto	2026-03-07 15:00:01.620129
371	19	50	250193.0000	auto	2026-03-07 15:00:01.620129
373	20	52	83173289.0000	auto	2026-03-07 15:00:05.019718
374	20	53	111451036.0000	auto	2026-03-07 15:00:05.019718
375	20	54	189814973.0000	auto	2026-03-07 15:00:05.019718
376	20	60	349012.0000	auto	2026-03-07 15:00:05.019718
377	20	55	144504196.0000	auto	2026-03-07 15:00:05.019718
378	20	56	9039956.0000	auto	2026-03-07 15:00:05.019718
379	20	57	148035168.0000	auto	2026-03-07 15:00:05.019718
380	20	58	11545668.0000	auto	2026-03-07 15:00:05.019718
381	20	59	320296.3060	auto	2026-03-07 15:00:05.019718
382	20	16	23597452.0000	auto	2026-03-07 15:00:05.019718
383	20	38	14703528.0000	auto	2026-03-07 15:00:05.019718
384	20	39	47579617.0000	auto	2026-03-07 15:00:05.019718
385	20	43	2117717.0000	auto	2026-03-07 15:00:05.019718
386	20	44	1263.0000	auto	2026-03-07 15:00:05.019718
387	20	46	56192.0000	auto	2026-03-07 15:00:05.019718
388	20	49	12743.0000	auto	2026-03-07 15:00:05.019718
389	20	50	260193.0000	auto	2026-03-07 15:00:05.019718
391	21	52	80796361.0000	auto	2026-03-07 15:00:08.410765
392	21	53	107748890.0000	auto	2026-03-07 15:00:08.410765
2154	90	52	114633204.0000	auto	2026-03-07 15:02:56.612827
2155	90	53	457868886.0000	auto	2026-03-07 15:02:56.612827
2156	90	54	50332373.0000	auto	2026-03-07 15:02:56.612827
2157	90	60	40813.0000	auto	2026-03-07 15:02:56.612827
2158	90	55	100195809.0000	auto	2026-03-07 15:02:56.612827
2159	90	56	29469573.0000	auto	2026-03-07 15:02:56.612827
2160	90	57	206895395.0000	auto	2026-03-07 15:02:56.612827
2161	90	58	14616305.3600	auto	2026-03-07 15:02:56.612827
2162	90	59	1057233.0000	auto	2026-03-07 15:02:56.612827
2163	90	16	22973205.0000	auto	2026-03-07 15:02:56.612827
2164	90	38	1000342.0000	auto	2026-03-07 15:02:56.612827
2165	90	39	16983303.0000	auto	2026-03-07 15:02:56.612827
2166	90	43	1789933.0000	auto	2026-03-07 15:02:56.612827
2167	90	44	134263.0000	auto	2026-03-07 15:02:56.612827
2168	90	46	166315.0000	auto	2026-03-07 15:02:56.612827
2169	90	49	4653.0000	auto	2026-03-07 15:02:56.612827
409	22	52	77484606.0000	auto	2026-03-07 15:00:11.791789
410	22	53	102456144.0000	auto	2026-03-07 15:00:11.791789
411	22	54	158544792.0000	auto	2026-03-07 15:00:11.791789
412	22	60	331311.0000	auto	2026-03-07 15:00:11.791789
413	22	55	142936436.0000	auto	2026-03-07 15:00:11.791789
414	22	56	8981506.0000	auto	2026-03-07 15:00:11.791789
415	22	57	121592332.0000	auto	2026-03-07 15:00:11.791789
416	22	58	11771646.1700	auto	2026-03-07 15:00:11.791789
417	22	59	281325.0000	auto	2026-03-07 15:00:11.791789
418	22	16	23622222.0000	auto	2026-03-07 15:00:11.791789
419	22	38	5007035.0000	auto	2026-03-07 15:00:11.791789
420	22	39	47574013.0000	auto	2026-03-07 15:00:11.791789
421	22	43	1582780.0000	auto	2026-03-07 15:00:11.791789
422	22	44	16263.0000	auto	2026-03-07 15:00:11.791789
423	22	46	56192.0000	auto	2026-03-07 15:00:11.791789
427	23	52	75273366.0000	auto	2026-03-07 15:00:14.906054
428	23	53	98973248.0000	auto	2026-03-07 15:00:14.906054
429	23	54	153556516.0000	auto	2026-03-07 15:00:14.906054
430	23	60	319011.0000	auto	2026-03-07 15:00:14.906054
431	23	55	141006892.0000	auto	2026-03-07 15:00:14.906054
432	23	56	9294216.0000	auto	2026-03-07 15:00:14.906054
433	23	57	111355514.0000	auto	2026-03-07 15:00:14.906054
434	23	58	11707117.9540	auto	2026-03-07 15:00:14.906054
435	23	59	266046.0000	auto	2026-03-07 15:00:14.906054
436	23	16	18132930.0000	auto	2026-03-07 15:00:14.906054
437	23	39	45631114.0000	auto	2026-03-07 15:00:14.906054
438	23	43	3582780.0000	auto	2026-03-07 15:00:14.906054
439	23	44	11263.0000	auto	2026-03-07 15:00:14.906054
440	23	46	56192.0000	auto	2026-03-07 15:00:14.906054
441	23	49	12743.0000	auto	2026-03-07 15:00:14.906054
442	23	50	260193.0000	auto	2026-03-07 15:00:14.906054
443	23	48	17000000.0000	auto	2026-03-07 15:00:14.906054
444	24	52	74419277.0000	auto	2026-03-07 15:00:18.324355
445	24	53	97007286.0000	auto	2026-03-07 15:00:18.324355
446	24	54	146521149.0000	auto	2026-03-07 15:00:18.324355
447	24	60	297531.0000	auto	2026-03-07 15:00:18.324355
448	24	55	141353369.0000	auto	2026-03-07 15:00:18.324355
449	24	56	9639596.0000	auto	2026-03-07 15:00:18.324355
450	24	57	109887218.0000	auto	2026-03-07 15:00:18.324355
451	24	58	11807288.2280	auto	2026-03-07 15:00:18.324355
452	24	59	305869.0000	auto	2026-03-07 15:00:18.324355
453	24	16	17642188.0000	auto	2026-03-07 15:00:18.324355
454	24	39	44660051.0000	auto	2026-03-07 15:00:18.324355
455	24	43	3592780.0000	auto	2026-03-07 15:00:18.324355
456	24	44	101263.0000	auto	2026-03-07 15:00:18.324355
457	24	46	56192.0000	auto	2026-03-07 15:00:18.324355
458	24	49	12743.0000	auto	2026-03-07 15:00:18.324355
461	25	52	79348771.0000	auto	2026-03-07 15:00:20.623438
462	25	53	104675633.0000	auto	2026-03-07 15:00:20.623438
463	25	54	167146674.0000	auto	2026-03-07 15:00:20.623438
464	25	60	319111.0000	auto	2026-03-07 15:00:20.623438
465	25	55	143411061.0000	auto	2026-03-07 15:00:20.623438
466	25	56	9642406.0000	auto	2026-03-07 15:00:20.623438
467	25	57	140186954.0000	auto	2026-03-07 15:00:20.623438
468	25	58	11936306.2720	auto	2026-03-07 15:00:20.623438
469	25	59	324137.0000	auto	2026-03-07 15:00:20.623438
470	25	16	14650190.0000	auto	2026-03-07 15:00:20.623438
471	25	39	43683337.0000	auto	2026-03-07 15:00:20.623438
472	25	43	2174652.0000	auto	2026-03-07 15:00:20.623438
473	25	44	16263.0000	auto	2026-03-07 15:00:20.623438
474	25	46	66192.0000	auto	2026-03-07 15:00:20.623438
475	25	49	12743.0000	auto	2026-03-07 15:00:20.623438
476	25	50	270193.0000	auto	2026-03-07 15:00:20.623438
478	26	52	78508402.0000	auto	2026-03-07 15:00:23.869381
479	26	53	103040736.0000	auto	2026-03-07 15:00:23.869381
480	26	54	161748633.0000	auto	2026-03-07 15:00:23.869381
481	26	60	302011.0000	auto	2026-03-07 15:00:23.869381
482	26	55	142877710.0000	auto	2026-03-07 15:00:23.869381
483	26	56	9669126.0000	auto	2026-03-07 15:00:23.869381
484	26	57	142909908.0000	auto	2026-03-07 15:00:23.869381
485	26	58	11915156.5940	auto	2026-03-07 15:00:23.869381
486	26	59	324250.0000	auto	2026-03-07 15:00:23.869381
487	26	16	14657778.0000	auto	2026-03-07 15:00:23.869381
488	26	39	43683337.0000	auto	2026-03-07 15:00:23.869381
489	26	43	1512152.0000	auto	2026-03-07 15:00:23.869381
490	26	44	6263.0000	auto	2026-03-07 15:00:23.869381
491	26	46	66192.0000	auto	2026-03-07 15:00:23.869381
492	26	49	12743.0000	auto	2026-03-07 15:00:23.869381
493	26	50	270193.0000	auto	2026-03-07 15:00:23.869381
495	27	52	77112213.0000	auto	2026-03-07 15:00:27.195691
496	27	53	100983004.0000	auto	2026-03-07 15:00:27.195691
497	27	54	155411801.0000	auto	2026-03-07 15:00:27.195691
498	27	60	302011.0000	auto	2026-03-07 15:00:27.195691
499	27	55	142892602.0000	auto	2026-03-07 15:00:27.195691
500	27	56	9675696.0000	auto	2026-03-07 15:00:27.195691
501	27	57	129311816.0000	auto	2026-03-07 15:00:27.195691
502	27	58	11839375.0330	auto	2026-03-07 15:00:27.195691
503	27	59	315191.0000	auto	2026-03-07 15:00:27.195691
504	27	16	14665372.0000	auto	2026-03-07 15:00:27.195691
505	27	39	42710880.0000	auto	2026-03-07 15:00:27.195691
506	27	43	962097.0000	auto	2026-03-07 15:00:27.195691
507	27	44	26263.0000	auto	2026-03-07 15:00:27.195691
508	27	46	66192.0000	auto	2026-03-07 15:00:27.195691
509	27	49	12743.0000	auto	2026-03-07 15:00:27.195691
510	27	50	270193.0000	auto	2026-03-07 15:00:27.195691
512	28	52	73939123.0000	auto	2026-03-07 15:00:30.318252
513	28	53	98006699.0000	auto	2026-03-07 15:00:30.318252
514	28	54	145718362.0000	auto	2026-03-07 15:00:30.318252
515	28	60	282871.0000	auto	2026-03-07 15:00:30.318252
516	28	55	140529479.0000	auto	2026-03-07 15:00:30.318252
517	28	56	9648533.0000	auto	2026-03-07 15:00:30.318252
518	28	57	102234626.0000	auto	2026-03-07 15:00:30.318252
519	28	58	11783857.3520	auto	2026-03-07 15:00:30.318252
520	28	59	289930.0000	auto	2026-03-07 15:00:30.318252
521	28	16	14672970.0000	auto	2026-03-07 15:00:30.318252
522	28	39	40758021.0000	auto	2026-03-07 15:00:30.318252
523	28	43	2162097.0000	auto	2026-03-07 15:00:30.318252
2170	90	50	370453.0000	auto	2026-03-07 15:02:56.612827
2171	90	48	18200000.0000	auto	2026-03-07 15:02:56.612827
2172	90	47	69041.0000	auto	2026-03-07 15:02:56.612827
2191	92	52	119489504.0000	auto	2026-03-07 15:02:58.333375
2192	92	53	483736431.0000	auto	2026-03-07 15:02:58.333375
2193	92	54	55852173.0000	auto	2026-03-07 15:02:58.333375
2194	92	60	42458.0000	auto	2026-03-07 15:02:58.333375
2195	92	55	103531076.0000	auto	2026-03-07 15:02:58.333375
2196	92	56	32785903.0000	auto	2026-03-07 15:02:58.333375
2197	92	57	224540882.7360	auto	2026-03-07 15:02:58.333375
2198	92	58	14818575.0320	auto	2026-03-07 15:02:58.333375
2199	92	59	1103141.0000	auto	2026-03-07 15:02:58.333375
2200	92	16	21053216.0000	auto	2026-03-07 15:02:58.333375
2201	92	39	16983303.0000	auto	2026-03-07 15:02:58.333375
2202	92	43	1556824.0000	auto	2026-03-07 15:02:58.333375
2203	92	44	134263.0000	auto	2026-03-07 15:02:58.333375
2204	92	46	166315.0000	auto	2026-03-07 15:02:58.333375
51	2	52	66480745.0000	auto	2026-03-07 14:59:04.824882
52	2	53	82357410.0000	auto	2026-03-07 14:59:04.824882
53	2	54	124814930.0000	auto	2026-03-07 14:59:04.824882
54	2	60	44029994.0000	auto	2026-03-07 14:59:04.824882
55	2	55	122892553.0680	auto	2026-03-07 14:59:04.824882
56	2	56	6292319.0000	auto	2026-03-07 14:59:04.824882
57	2	57	43438857.6220	auto	2026-03-07 14:59:04.824882
58	2	58	7112684.7420	auto	2026-03-07 14:59:04.824882
59	2	59	102331.0000	auto	2026-03-07 14:59:04.824882
60	2	16	4832740.0000	auto	2026-03-07 14:59:04.824882
61	2	39	44630781.0000	auto	2026-03-07 14:59:04.824882
62	2	43	3152700.0000	auto	2026-03-07 14:59:04.824882
63	2	44	114638.0000	auto	2026-03-07 14:59:04.824882
64	2	46	267599.0000	auto	2026-03-07 14:59:04.824882
65	2	49	12910.0000	auto	2026-03-07 14:59:04.824882
66	2	50	220095.0000	auto	2026-03-07 14:59:04.824882
67	2	48	16600000.0000	auto	2026-03-07 14:59:04.824882
84	3	48	16600000.0000	auto	2026-03-07 14:59:08.172115
100	4	49	12910.0000	auto	2026-03-07 14:59:11.78781
101	4	50	220095.0000	auto	2026-03-07 14:59:11.78781
102	4	48	16600000.0000	auto	2026-03-07 14:59:11.78781
120	5	48	16600000.0000	auto	2026-03-07 14:59:15.491622
129	6	59	154983.3840	auto	2026-03-07 14:59:18.927249
130	6	16	30373740.0000	auto	2026-03-07 14:59:18.927249
131	6	38	18668117.0000	auto	2026-03-07 14:59:18.927249
132	6	39	45190818.0000	auto	2026-03-07 14:59:18.927249
133	6	43	511586.0000	auto	2026-03-07 14:59:18.927249
134	6	44	147800.0000	auto	2026-03-07 14:59:18.927249
135	6	46	1815841.0000	auto	2026-03-07 14:59:18.927249
136	6	49	12983.0000	auto	2026-03-07 14:59:18.927249
137	6	50	220095.0000	auto	2026-03-07 14:59:18.927249
138	6	48	16600000.0000	auto	2026-03-07 14:59:18.927249
148	7	16	29139722.0000	auto	2026-03-07 14:59:21.236531
149	7	38	17678822.0000	auto	2026-03-07 14:59:21.236531
150	7	39	49217420.0000	auto	2026-03-07 14:59:21.236531
151	7	43	1474582.0000	auto	2026-03-07 14:59:21.236531
152	7	44	32800.0000	auto	2026-03-07 14:59:21.236531
153	7	46	25841.0000	auto	2026-03-07 14:59:21.236531
154	7	49	12983.0000	auto	2026-03-07 14:59:21.236531
155	7	50	230095.0000	auto	2026-03-07 14:59:21.236531
156	7	48	16700000.0000	auto	2026-03-07 14:59:21.236531
174	8	48	16700000.0000	auto	2026-03-07 14:59:24.860833
192	9	48	16700000.0000	auto	2026-03-07 14:59:28.287629
210	10	48	16700000.0000	auto	2026-03-07 14:59:31.718371
228	11	48	16800000.0000	auto	2026-03-07 14:59:35.485553
245	12	50	240095.0000	auto	2026-03-07 14:59:38.926758
246	12	48	16800000.0000	auto	2026-03-07 14:59:38.926758
262	13	49	12704.0000	auto	2026-03-07 14:59:42.432613
263	13	50	240095.0000	auto	2026-03-07 14:59:42.432613
264	13	48	16800000.0000	auto	2026-03-07 14:59:42.432613
267	14	54	145027608.0000	auto	2026-03-07 14:59:45.782252
269	14	55	139143296.0000	auto	2026-03-07 14:59:45.782252
270	14	56	7934409.0000	auto	2026-03-07 14:59:45.782252
271	14	57	65530553.7500	auto	2026-03-07 14:59:45.782252
272	14	58	10553019.4800	auto	2026-03-07 14:59:45.782252
273	14	59	208716.0000	auto	2026-03-07 14:59:45.782252
274	14	16	19727330.0000	auto	2026-03-07 14:59:45.782252
275	14	38	11371768.0000	auto	2026-03-07 14:59:45.782252
529	29	52	77734636.0000	auto	2026-03-07 15:00:33.482896
530	29	53	103339448.0000	auto	2026-03-07 15:00:33.482896
531	29	54	159533506.0000	auto	2026-03-07 15:00:33.482896
532	29	60	283081.0000	auto	2026-03-07 15:00:33.482896
533	29	55	143505811.0000	auto	2026-03-07 15:00:33.482896
546	30	52	78798567.0000	auto	2026-03-07 15:00:36.706481
547	30	53	106224208.0000	auto	2026-03-07 15:00:36.706481
548	30	54	167315891.0000	auto	2026-03-07 15:00:36.706481
549	30	60	272241.0000	auto	2026-03-07 15:00:36.706481
550	30	55	144110621.0000	auto	2026-03-07 15:00:36.706481
551	30	56	10446473.0000	auto	2026-03-07 15:00:36.706481
552	30	57	131871870.0000	auto	2026-03-07 15:00:36.706481
553	30	58	11966658.1400	auto	2026-03-07 15:00:36.706481
554	30	59	372363.9600	auto	2026-03-07 15:00:36.706481
555	30	16	11185296.0000	auto	2026-03-07 15:00:36.706481
556	30	39	37814834.0000	auto	2026-03-07 15:00:36.706481
557	30	43	1831773.0000	auto	2026-03-07 15:00:36.706481
558	30	44	3588.0000	auto	2026-03-07 15:00:36.706481
559	30	46	76207.0000	auto	2026-03-07 15:00:36.706481
560	30	49	12781.0000	auto	2026-03-07 15:00:36.706481
563	31	52	79319396.0000	auto	2026-03-07 15:00:40.142782
564	31	53	106716505.0000	auto	2026-03-07 15:00:40.142782
565	31	54	168818235.0000	auto	2026-03-07 15:00:40.142782
566	31	60	289361.0000	auto	2026-03-07 15:00:40.142782
567	31	55	143757901.0000	auto	2026-03-07 15:00:40.142782
568	31	56	10626393.0000	auto	2026-03-07 15:00:40.142782
569	31	57	135933901.0000	auto	2026-03-07 15:00:40.142782
570	31	58	12033801.4770	auto	2026-03-07 15:00:40.142782
571	31	59	376172.2120	auto	2026-03-07 15:00:40.142782
572	31	16	11191071.0000	auto	2026-03-07 15:00:40.142782
573	31	39	36834352.0000	auto	2026-03-07 15:00:40.142782
574	31	43	1519218.0000	auto	2026-03-07 15:00:40.142782
575	31	44	3588.0000	auto	2026-03-07 15:00:40.142782
576	31	46	76207.0000	auto	2026-03-07 15:00:40.142782
577	31	49	12781.0000	auto	2026-03-07 15:00:40.142782
578	31	50	280193.0000	auto	2026-03-07 15:00:40.142782
580	32	52	79394387.0000	auto	2026-03-07 15:00:43.414153
581	32	53	106091697.0000	auto	2026-03-07 15:00:43.414153
582	32	54	167807890.0000	auto	2026-03-07 15:00:43.414153
583	32	60	274301.0000	auto	2026-03-07 15:00:43.414153
584	32	55	143990034.8630	auto	2026-03-07 15:00:43.414153
585	32	56	10709563.0000	auto	2026-03-07 15:00:43.414153
586	32	57	142736882.0000	auto	2026-03-07 15:00:43.414153
587	32	58	11704975.5430	auto	2026-03-07 15:00:43.414153
588	32	59	377381.9160	auto	2026-03-07 15:00:43.414153
589	32	16	10696750.0000	auto	2026-03-07 15:00:43.414153
590	32	39	35853388.0000	auto	2026-03-07 15:00:43.414153
591	32	43	1509218.0000	auto	2026-03-07 15:00:43.414153
592	32	44	8588.0000	auto	2026-03-07 15:00:43.414153
593	32	46	76207.0000	auto	2026-03-07 15:00:43.414153
594	32	49	12781.0000	auto	2026-03-07 15:00:43.414153
595	32	50	280193.0000	auto	2026-03-07 15:00:43.414153
276	14	39	46475587.0000	auto	2026-03-07 14:59:45.782252
277	14	43	240259.0000	auto	2026-03-07 14:59:45.782252
278	14	44	17800.0000	auto	2026-03-07 14:59:45.782252
279	14	46	35841.0000	auto	2026-03-07 14:59:45.782252
280	14	49	12704.0000	auto	2026-03-07 14:59:45.782252
281	14	50	240095.0000	auto	2026-03-07 14:59:45.782252
282	14	48	16800000.0000	auto	2026-03-07 14:59:45.782252
299	15	50	240095.0000	auto	2026-03-07 14:59:49.165025
300	15	48	16800000.0000	auto	2026-03-07 14:59:49.165025
318	16	48	16900000.0000	auto	2026-03-07 14:59:51.450387
336	17	48	16900000.0000	auto	2026-03-07 14:59:54.872424
353	18	50	250193.0000	auto	2026-03-07 14:59:58.204718
354	18	48	16900000.0000	auto	2026-03-07 14:59:58.204718
372	19	48	16900000.0000	auto	2026-03-07 15:00:01.620129
390	20	48	17000000.0000	auto	2026-03-07 15:00:05.019718
393	21	54	176645435.0000	auto	2026-03-07 15:00:08.410765
394	21	60	341211.0000	auto	2026-03-07 15:00:08.410765
395	21	55	143320313.0000	auto	2026-03-07 15:00:08.410765
396	21	56	9154126.0000	auto	2026-03-07 15:00:08.410765
397	21	57	129568577.0000	auto	2026-03-07 15:00:08.410765
398	21	58	11701494.9300	auto	2026-03-07 15:00:08.410765
399	21	59	292065.0000	auto	2026-03-07 15:00:08.410765
400	21	16	23609833.0000	auto	2026-03-07 15:00:08.410765
401	21	38	10003713.0000	auto	2026-03-07 15:00:08.410765
402	21	39	47574013.0000	auto	2026-03-07 15:00:08.410765
403	21	43	1875335.0000	auto	2026-03-07 15:00:08.410765
404	21	44	31263.0000	auto	2026-03-07 15:00:08.410765
405	21	46	56192.0000	auto	2026-03-07 15:00:08.410765
406	21	49	12743.0000	auto	2026-03-07 15:00:08.410765
407	21	50	260193.0000	auto	2026-03-07 15:00:08.410765
408	21	48	17000000.0000	auto	2026-03-07 15:00:08.410765
424	22	49	12743.0000	auto	2026-03-07 15:00:11.791789
425	22	50	260193.0000	auto	2026-03-07 15:00:11.791789
426	22	48	17000000.0000	auto	2026-03-07 15:00:11.791789
459	24	50	260193.0000	auto	2026-03-07 15:00:18.324355
460	24	48	17000000.0000	auto	2026-03-07 15:00:18.324355
477	25	48	17100000.0000	auto	2026-03-07 15:00:20.623438
494	26	48	17100000.0000	auto	2026-03-07 15:00:23.869381
511	27	48	17100000.0000	auto	2026-03-07 15:00:27.195691
524	28	44	16263.0000	auto	2026-03-07 15:00:30.318252
525	28	46	66192.0000	auto	2026-03-07 15:00:30.318252
526	28	49	12743.0000	auto	2026-03-07 15:00:30.318252
527	28	50	270193.0000	auto	2026-03-07 15:00:30.318252
528	28	48	17100000.0000	auto	2026-03-07 15:00:30.318252
534	29	56	10295273.0000	auto	2026-03-07 15:00:33.482896
535	29	57	131862658.0000	auto	2026-03-07 15:00:33.482896
536	29	58	12070593.9680	auto	2026-03-07 15:00:33.482896
537	29	59	369883.0720	auto	2026-03-07 15:00:33.482896
538	29	16	11179524.0000	auto	2026-03-07 15:00:33.482896
539	29	39	38800977.0000	auto	2026-03-07 15:00:33.482896
540	29	43	1875255.0000	auto	2026-03-07 15:00:33.482896
541	29	44	6263.0000	auto	2026-03-07 15:00:33.482896
542	29	46	76192.0000	auto	2026-03-07 15:00:33.482896
543	29	49	12743.0000	auto	2026-03-07 15:00:33.482896
544	29	50	280193.0000	auto	2026-03-07 15:00:33.482896
545	29	48	17200000.0000	auto	2026-03-07 15:00:33.482896
561	30	50	280193.0000	auto	2026-03-07 15:00:36.706481
562	30	48	17200000.0000	auto	2026-03-07 15:00:36.706481
579	31	48	17200000.0000	auto	2026-03-07 15:00:40.142782
596	32	48	17200000.0000	auto	2026-03-07 15:00:43.414153
1143	33	52	82220231.0000	auto	2026-03-07 15:02:09.663334
1144	33	53	109523551.0000	auto	2026-03-07 15:02:09.663334
1145	33	54	177921037.0000	auto	2026-03-07 15:02:09.663334
1146	33	60	283161.0000	auto	2026-03-07 15:02:09.663334
1147	33	55	146281312.6830	auto	2026-03-07 15:02:09.663334
1148	33	56	10771303.0000	auto	2026-03-07 15:02:09.663334
1149	33	57	162913697.0000	auto	2026-03-07 15:02:09.663334
1150	33	58	11968593.0520	auto	2026-03-07 15:02:09.663334
1151	33	59	388541.1830	auto	2026-03-07 15:02:09.663334
1152	33	16	10452191.0000	auto	2026-03-07 15:02:09.663334
1153	33	39	34872723.0000	auto	2026-03-07 15:02:09.663334
1154	33	43	940278.0000	auto	2026-03-07 15:02:09.663334
1155	33	44	8588.0000	auto	2026-03-07 15:02:09.663334
1156	33	46	86207.0000	auto	2026-03-07 15:02:09.663334
1157	33	49	12799.0000	auto	2026-03-07 15:02:09.663334
1158	33	50	290193.0000	auto	2026-03-07 15:02:09.663334
1159	33	48	17300000.0000	auto	2026-03-07 15:02:09.663334
1160	34	52	83619331.0000	auto	2026-03-07 15:02:10.518372
1161	34	53	110837769.0000	auto	2026-03-07 15:02:10.518372
1162	34	54	182205463.0000	auto	2026-03-07 15:02:10.518372
1163	34	60	280661.0000	auto	2026-03-07 15:02:10.518372
1164	34	55	148115597.6830	auto	2026-03-07 15:02:10.518372
1165	34	56	11353383.0000	auto	2026-03-07 15:02:10.518372
1166	34	57	170129263.0000	auto	2026-03-07 15:02:10.518372
1167	34	58	12376683.9580	auto	2026-03-07 15:02:10.518372
1168	34	59	395283.0000	auto	2026-03-07 15:02:10.518372
1169	34	16	10407587.0000	auto	2026-03-07 15:02:10.518372
1170	34	39	33886043.0000	auto	2026-03-07 15:02:10.518372
1171	34	43	644713.0000	auto	2026-03-07 15:02:10.518372
1172	34	44	8588.0000	auto	2026-03-07 15:02:10.518372
1173	34	46	86207.0000	auto	2026-03-07 15:02:10.518372
1174	34	49	12799.0000	auto	2026-03-07 15:02:10.518372
1175	34	50	290193.0000	auto	2026-03-07 15:02:10.518372
1176	34	48	17300000.0000	auto	2026-03-07 15:02:10.518372
1177	35	52	85231357.0000	auto	2026-03-07 15:02:11.363802
1178	35	53	113864888.0000	auto	2026-03-07 15:02:11.363802
1179	35	54	194295171.0000	auto	2026-03-07 15:02:11.363802
1180	35	60	261281.0000	auto	2026-03-07 15:02:11.363802
1181	35	55	148407955.1720	auto	2026-03-07 15:02:11.363802
1182	35	56	12181423.0000	auto	2026-03-07 15:02:11.363802
1183	35	57	176284958.0000	auto	2026-03-07 15:02:11.363802
1184	35	58	12166886.2720	auto	2026-03-07 15:02:11.363802
1185	35	59	398856.0000	auto	2026-03-07 15:02:11.363802
1186	35	16	10287801.0000	auto	2026-03-07 15:02:11.363802
1187	35	39	32905263.0000	auto	2026-03-07 15:02:11.363802
1188	35	43	217213.0000	auto	2026-03-07 15:02:11.363802
1189	35	44	8588.0000	auto	2026-03-07 15:02:11.363802
1190	35	46	86207.0000	auto	2026-03-07 15:02:11.363802
1191	35	49	12799.0000	auto	2026-03-07 15:02:11.363802
1192	35	50	290193.0000	auto	2026-03-07 15:02:11.363802
1193	35	48	17300000.0000	auto	2026-03-07 15:02:11.363802
1194	36	52	83815977.0000	auto	2026-03-07 15:02:12.2191
1195	36	53	113145786.0000	auto	2026-03-07 15:02:12.2191
1196	36	54	187974598.0000	auto	2026-03-07 15:02:12.2191
1197	36	60	261281.0000	auto	2026-03-07 15:02:12.2191
1198	36	55	146989782.2530	auto	2026-03-07 15:02:12.2191
1199	36	56	11968933.0000	auto	2026-03-07 15:02:12.2191
1200	36	57	165229254.0000	auto	2026-03-07 15:02:12.2191
1201	36	58	11923080.0690	auto	2026-03-07 15:02:12.2191
1202	36	59	391216.0000	auto	2026-03-07 15:02:12.2191
1203	36	16	10162846.0000	auto	2026-03-07 15:02:12.2191
1204	36	39	31924870.0000	auto	2026-03-07 15:02:12.2191
1205	36	43	1112158.0000	auto	2026-03-07 15:02:12.2191
1206	36	44	8588.0000	auto	2026-03-07 15:02:12.2191
1207	36	46	86207.0000	auto	2026-03-07 15:02:12.2191
1208	36	49	12799.0000	auto	2026-03-07 15:02:12.2191
1209	36	50	290193.0000	auto	2026-03-07 15:02:12.2191
1210	36	48	17300000.0000	auto	2026-03-07 15:02:12.2191
1211	37	52	88482467.0000	auto	2026-03-07 15:02:13.056551
1212	37	53	121097836.0000	auto	2026-03-07 15:02:13.056551
1213	37	54	216014222.0000	auto	2026-03-07 15:02:13.056551
1214	37	60	261281.0000	auto	2026-03-07 15:02:13.056551
1215	37	55	151660587.2700	auto	2026-03-07 15:02:13.056551
1216	37	56	11761283.0000	auto	2026-03-07 15:02:13.056551
1217	37	57	198775281.0000	auto	2026-03-07 15:02:13.056551
1218	37	58	12385203.1000	auto	2026-03-07 15:02:13.056551
1219	37	59	467236.0000	auto	2026-03-07 15:02:13.056551
1220	37	16	10042821.0000	auto	2026-03-07 15:02:13.056551
1221	37	38	68.0000	auto	2026-03-07 15:02:13.056551
1222	37	39	30945040.0000	auto	2026-03-07 15:02:13.056551
1223	37	43	1262158.0000	auto	2026-03-07 15:02:13.056551
1224	37	44	8588.0000	auto	2026-03-07 15:02:13.056551
1225	37	46	86207.0000	auto	2026-03-07 15:02:13.056551
1226	37	49	12799.0000	auto	2026-03-07 15:02:13.056551
1227	37	50	290193.0000	auto	2026-03-07 15:02:13.056551
1228	37	48	17300000.0000	auto	2026-03-07 15:02:13.056551
1229	38	52	88389882.0000	auto	2026-03-07 15:02:13.9394
1230	38	53	120876079.0000	auto	2026-03-07 15:02:13.9394
1231	38	54	209895429.0000	auto	2026-03-07 15:02:13.9394
1232	38	60	270698.0000	auto	2026-03-07 15:02:13.9394
1233	38	55	150455625.5450	auto	2026-03-07 15:02:13.9394
1234	38	56	11354863.0000	auto	2026-03-07 15:02:13.9394
1235	38	57	185732299.0000	auto	2026-03-07 15:02:13.9394
1236	38	58	12410688.7550	auto	2026-03-07 15:02:13.9394
1237	38	59	451078.0000	auto	2026-03-07 15:02:13.9394
1238	38	16	8341168.0000	auto	2026-03-07 15:02:13.9394
1239	38	39	29870121.0000	auto	2026-03-07 15:02:13.9394
1240	38	43	684514.0000	auto	2026-03-07 15:02:13.9394
1241	38	44	8588.0000	auto	2026-03-07 15:02:13.9394
1242	38	46	96207.0000	auto	2026-03-07 15:02:13.9394
1243	38	49	12818.0000	auto	2026-03-07 15:02:13.9394
1244	38	50	300193.0000	auto	2026-03-07 15:02:13.9394
1245	38	48	17400000.0000	auto	2026-03-07 15:02:13.9394
1246	39	52	88107391.0000	auto	2026-03-07 15:02:14.854911
1247	39	53	119405672.0000	auto	2026-03-07 15:02:14.854911
1248	39	54	205293452.0000	auto	2026-03-07 15:02:14.854911
1249	39	60	279778.0000	auto	2026-03-07 15:02:14.854911
1250	39	55	151409580.0000	auto	2026-03-07 15:02:14.854911
1251	39	56	12071623.0000	auto	2026-03-07 15:02:14.854911
1252	39	57	190332102.0000	auto	2026-03-07 15:02:14.854911
1253	39	58	12557753.0000	auto	2026-03-07 15:02:14.854911
1254	39	59	444334.0000	auto	2026-03-07 15:02:14.854911
1255	39	16	8315358.0000	auto	2026-03-07 15:02:14.854911
1256	39	39	28890030.0000	auto	2026-03-07 15:02:14.854911
1257	39	43	637214.0000	auto	2026-03-07 15:02:14.854911
1258	39	44	8588.0000	auto	2026-03-07 15:02:14.854911
1259	39	46	96207.0000	auto	2026-03-07 15:02:14.854911
1260	39	49	12822.0000	auto	2026-03-07 15:02:14.854911
1261	39	50	300193.0000	auto	2026-03-07 15:02:14.854911
1262	39	48	17400000.0000	auto	2026-03-07 15:02:14.854911
1263	40	52	87287595.0000	auto	2026-03-07 15:02:14.682515
1264	40	53	119299115.0000	auto	2026-03-07 15:02:14.682515
1265	40	54	204678775.0000	auto	2026-03-07 15:02:14.682515
1266	40	60	270578.0000	auto	2026-03-07 15:02:14.682515
1267	40	55	152314929.0000	auto	2026-03-07 15:02:14.682515
1268	40	56	12003843.0000	auto	2026-03-07 15:02:14.682515
1269	40	57	185214287.0000	auto	2026-03-07 15:02:14.682515
1270	40	58	12741925.5500	auto	2026-03-07 15:02:14.682515
1271	40	59	447858.0000	auto	2026-03-07 15:02:14.682515
1272	40	16	8195479.0000	auto	2026-03-07 15:02:14.682515
1273	40	39	27908472.0000	auto	2026-03-07 15:02:14.682515
1274	40	43	727159.0000	auto	2026-03-07 15:02:14.682515
1275	40	44	8588.0000	auto	2026-03-07 15:02:14.682515
1276	40	46	96207.0000	auto	2026-03-07 15:02:14.682515
1277	40	49	12822.0000	auto	2026-03-07 15:02:14.682515
1278	40	50	300193.0000	auto	2026-03-07 15:02:14.682515
1279	40	48	17400000.0000	auto	2026-03-07 15:02:14.682515
1280	41	52	91926700.0000	auto	2026-03-07 15:02:15.614171
1281	41	53	126814405.0000	auto	2026-03-07 15:02:15.614171
1282	41	54	231640988.0000	auto	2026-03-07 15:02:15.614171
1283	41	60	275778.0000	auto	2026-03-07 15:02:15.614171
1284	41	55	154895009.0000	auto	2026-03-07 15:02:15.614171
1285	41	56	12280543.0000	auto	2026-03-07 15:02:15.614171
1286	41	57	209259368.0000	auto	2026-03-07 15:02:15.614171
1287	41	58	12856972.4400	auto	2026-03-07 15:02:15.614171
1288	41	59	473310.0000	auto	2026-03-07 15:02:15.614171
1289	41	16	8078530.0000	auto	2026-03-07 15:02:15.614171
1290	41	39	27908472.0000	auto	2026-03-07 15:02:15.614171
1291	41	43	847159.0000	auto	2026-03-07 15:02:15.614171
1292	41	44	8588.0000	auto	2026-03-07 15:02:15.614171
1293	41	46	96207.0000	auto	2026-03-07 15:02:15.614171
1294	41	49	12837.0000	auto	2026-03-07 15:02:15.614171
1295	41	50	300193.0000	auto	2026-03-07 15:02:15.614171
1296	41	48	17400000.0000	auto	2026-03-07 15:02:15.614171
1297	42	52	94707213.0000	auto	2026-03-07 15:02:16.479995
1298	42	53	133428940.0000	auto	2026-03-07 15:02:16.479995
1299	42	54	253031261.0000	auto	2026-03-07 15:02:16.479995
1300	42	60	294458.0000	auto	2026-03-07 15:02:16.479995
1301	42	55	155389616.0000	auto	2026-03-07 15:02:16.479995
1302	42	56	12703693.0000	auto	2026-03-07 15:02:16.479995
1303	42	57	196381216.8960	auto	2026-03-07 15:02:16.479995
1304	42	58	12742192.3360	auto	2026-03-07 15:02:16.479995
1305	42	59	524825.5200	auto	2026-03-07 15:02:16.479995
1306	42	16	7957514.0000	auto	2026-03-07 15:02:16.479995
1307	42	39	26927845.0000	auto	2026-03-07 15:02:16.479995
1308	42	43	747502.0000	auto	2026-03-07 15:02:16.479995
1309	42	44	8588.0000	auto	2026-03-07 15:02:16.479995
1310	42	46	106255.0000	auto	2026-03-07 15:02:16.479995
1311	42	49	12837.0000	auto	2026-03-07 15:02:16.479995
1312	42	50	310193.0000	auto	2026-03-07 15:02:16.479995
1313	42	48	17500000.0000	auto	2026-03-07 15:02:16.479995
1314	43	52	93558727.0000	auto	2026-03-07 15:02:17.33009
1315	43	53	372502625.0000	auto	2026-03-07 15:02:17.33009
1316	43	54	10812635.0000	auto	2026-03-07 15:02:17.33009
1317	43	60	278838.0000	auto	2026-03-07 15:02:17.33009
1318	43	55	154629545.0000	auto	2026-03-07 15:02:17.33009
1319	43	56	12514993.0000	auto	2026-03-07 15:02:17.33009
1320	43	57	205010822.2550	auto	2026-03-07 15:02:17.33009
1321	43	58	12516583.8450	auto	2026-03-07 15:02:17.33009
1322	43	59	524334.7600	auto	2026-03-07 15:02:17.33009
1323	43	39	22022475.0000	auto	2026-03-07 15:02:17.33009
1324	43	43	2695827.0000	auto	2026-03-07 15:02:17.33009
1325	43	44	8591.0000	auto	2026-03-07 15:02:17.33009
1326	43	46	106255.0000	auto	2026-03-07 15:02:17.33009
1327	43	49	12837.0000	auto	2026-03-07 15:02:17.33009
1328	43	50	310316.0000	auto	2026-03-07 15:02:17.33009
1329	43	48	17500000.0000	auto	2026-03-07 15:02:17.33009
1330	44	52	97776457.0000	auto	2026-03-07 15:02:18.159527
1331	44	53	388785979.0000	auto	2026-03-07 15:02:18.159527
1332	44	54	16572862.0000	auto	2026-03-07 15:02:18.159527
1333	44	60	279338.0000	auto	2026-03-07 15:02:18.159527
1334	44	55	155998273.0000	auto	2026-03-07 15:02:18.159527
1335	44	56	12918913.0000	auto	2026-03-07 15:02:18.159527
1336	44	57	210580350.3550	auto	2026-03-07 15:02:18.159527
1337	44	58	12544326.2550	auto	2026-03-07 15:02:18.159527
1338	44	59	533453.2800	auto	2026-03-07 15:02:18.159527
1339	44	39	17124244.0000	auto	2026-03-07 15:02:18.159527
1340	44	43	2543272.0000	auto	2026-03-07 15:02:18.159527
1341	44	44	8591.0000	auto	2026-03-07 15:02:18.159527
1342	44	46	106229.0000	auto	2026-03-07 15:02:18.159527
1343	44	49	12837.0000	auto	2026-03-07 15:02:18.159527
1344	44	50	310316.0000	auto	2026-03-07 15:02:18.159527
1345	44	48	17500000.0000	auto	2026-03-07 15:02:18.159527
1346	44	47	9000.0000	auto	2026-03-07 15:02:18.159527
1347	45	52	95415052.0000	auto	2026-03-07 15:02:19.042003
1348	45	53	380725214.0000	auto	2026-03-07 15:02:19.042003
1349	45	54	20939258.0000	auto	2026-03-07 15:02:19.042003
1350	45	60	276998.0000	auto	2026-03-07 15:02:19.042003
1351	45	55	156101725.3300	auto	2026-03-07 15:02:19.042003
1352	45	56	13271923.0000	auto	2026-03-07 15:02:19.042003
1353	45	57	212977427.6970	auto	2026-03-07 15:02:19.042003
1354	45	58	12709269.4240	auto	2026-03-07 15:02:19.042003
1355	45	59	539817.1520	auto	2026-03-07 15:02:19.042003
1356	45	39	17124244.0000	auto	2026-03-07 15:02:19.042003
1357	45	43	3043273.0000	auto	2026-03-07 15:02:19.042003
1358	45	44	8591.0000	auto	2026-03-07 15:02:19.042003
1359	45	46	106229.0000	auto	2026-03-07 15:02:19.042003
1360	45	49	12853.0000	auto	2026-03-07 15:02:19.042003
1361	45	50	310316.0000	auto	2026-03-07 15:02:19.042003
1362	45	48	17500000.0000	auto	2026-03-07 15:02:19.042003
1363	46	52	95099256.0000	auto	2026-03-07 15:02:19.881611
1364	46	53	378735067.0000	auto	2026-03-07 15:02:19.881611
1365	46	54	25528426.0000	auto	2026-03-07 15:02:19.881611
1366	46	60	277118.0000	auto	2026-03-07 15:02:19.881611
1367	46	55	148604340.0000	auto	2026-03-07 15:02:19.881611
1368	46	56	13309376.0000	auto	2026-03-07 15:02:19.881611
1369	46	57	190709699.3940	auto	2026-03-07 15:02:19.881611
1370	46	58	12338603.4240	auto	2026-03-07 15:02:19.881611
1371	46	59	581727.1520	auto	2026-03-07 15:02:19.881611
1372	46	16	535630.0000	auto	2026-03-07 15:02:19.881611
1373	46	39	17124244.0000	auto	2026-03-07 15:02:19.881611
1374	46	43	1856133.0000	auto	2026-03-07 15:02:19.881611
1375	46	44	8591.0000	auto	2026-03-07 15:02:19.881611
1376	46	46	106229.0000	auto	2026-03-07 15:02:19.881611
1377	46	49	12853.0000	auto	2026-03-07 15:02:19.881611
1378	46	50	310316.0000	auto	2026-03-07 15:02:19.881611
1379	46	48	17600000.0000	auto	2026-03-07 15:02:19.881611
1380	47	52	93992371.0000	auto	2026-03-07 15:02:20.746271
1381	47	53	375087341.0000	auto	2026-03-07 15:02:20.746271
1382	47	54	25044601.0000	auto	2026-03-07 15:02:20.746271
1383	47	60	277118.0000	auto	2026-03-07 15:02:20.746271
1384	47	55	150294177.0000	auto	2026-03-07 15:02:20.746271
1385	47	56	13408183.0000	auto	2026-03-07 15:02:20.746271
1386	47	57	198658398.0000	auto	2026-03-07 15:02:20.746271
1387	47	58	12797632.5450	auto	2026-03-07 15:02:20.746271
1388	47	59	556978.0000	auto	2026-03-07 15:02:20.746271
1389	47	16	392245.0000	auto	2026-03-07 15:02:20.746271
1390	47	39	17118600.0000	auto	2026-03-07 15:02:20.746271
1391	47	43	1499888.0000	auto	2026-03-07 15:02:20.746271
1392	47	44	8591.0000	auto	2026-03-07 15:02:20.746271
1393	47	46	106229.0000	auto	2026-03-07 15:02:20.746271
1394	47	49	12853.0000	auto	2026-03-07 15:02:20.746271
1395	47	50	310316.0000	auto	2026-03-07 15:02:20.746271
1396	47	48	17600000.0000	auto	2026-03-07 15:02:20.746271
1397	48	52	95805347.0000	auto	2026-03-07 15:02:21.609068
1398	48	53	382148852.0000	auto	2026-03-07 15:02:21.609068
1399	48	54	25817011.0000	auto	2026-03-07 15:02:21.609068
1400	48	60	260658.0000	auto	2026-03-07 15:02:21.609068
1401	48	55	148820750.0000	auto	2026-03-07 15:02:21.609068
1402	48	56	13691806.0000	auto	2026-03-07 15:02:21.609068
1403	48	57	215945791.0000	auto	2026-03-07 15:02:21.609068
1404	48	58	12700653.5450	auto	2026-03-07 15:02:21.609068
1405	48	59	566561.0000	auto	2026-03-07 15:02:21.609068
1406	48	16	367471.0000	auto	2026-03-07 15:02:21.609068
1407	48	39	17118600.0000	auto	2026-03-07 15:02:21.609068
1408	48	43	1417388.0000	auto	2026-03-07 15:02:21.609068
1409	48	44	8591.0000	auto	2026-03-07 15:02:21.609068
1410	48	46	106229.0000	auto	2026-03-07 15:02:21.609068
1411	48	49	12853.0000	auto	2026-03-07 15:02:21.609068
1412	48	50	310316.0000	auto	2026-03-07 15:02:21.609068
1413	48	48	17600000.0000	auto	2026-03-07 15:02:21.609068
1414	49	52	94366774.0000	auto	2026-03-07 15:02:22.487882
1415	49	53	380823647.0000	auto	2026-03-07 15:02:22.487882
1416	49	54	25585883.0000	auto	2026-03-07 15:02:22.487882
1417	49	60	256258.0000	auto	2026-03-07 15:02:22.487882
1418	49	55	148525998.0000	auto	2026-03-07 15:02:22.487882
1419	49	56	13996112.0000	auto	2026-03-07 15:02:22.487882
1420	49	57	178287255.6200	auto	2026-03-07 15:02:22.487882
1421	49	58	12639915.6950	auto	2026-03-07 15:02:22.487882
1422	49	59	537141.0000	auto	2026-03-07 15:02:22.487882
1423	49	16	367633.0000	auto	2026-03-07 15:02:22.487882
1424	49	39	15164545.0000	auto	2026-03-07 15:02:22.487882
1425	49	43	1417388.0000	auto	2026-03-07 15:02:22.487882
1426	49	44	8591.0000	auto	2026-03-07 15:02:22.487882
1427	49	46	106229.0000	auto	2026-03-07 15:02:22.487882
1428	49	49	12853.0000	auto	2026-03-07 15:02:22.487882
1429	49	50	310316.0000	auto	2026-03-07 15:02:22.487882
1430	49	48	17600000.0000	auto	2026-03-07 15:02:22.487882
1431	50	52	93865191.0000	auto	2026-03-07 15:02:23.358413
1432	50	53	379206169.0000	auto	2026-03-07 15:02:23.358413
1433	50	54	30549068.0000	auto	2026-03-07 15:02:23.358413
1434	50	60	252925.0000	auto	2026-03-07 15:02:23.358413
1435	50	55	142106113.0000	auto	2026-03-07 15:02:23.358413
1436	50	56	15293056.0000	auto	2026-03-07 15:02:23.358413
1437	50	57	191091611.0000	auto	2026-03-07 15:02:23.358413
1438	50	58	12855945.9650	auto	2026-03-07 15:02:23.358413
1439	50	59	533637.9850	auto	2026-03-07 15:02:23.358413
1440	50	16	367822.0000	auto	2026-03-07 15:02:23.358413
1441	50	39	14188095.0000	auto	2026-03-07 15:02:23.358413
1442	50	43	1417388.0000	auto	2026-03-07 15:02:23.358413
1443	50	44	8591.0000	auto	2026-03-07 15:02:23.358413
1444	50	46	106229.0000	auto	2026-03-07 15:02:23.358413
1445	50	49	12853.0000	auto	2026-03-07 15:02:23.358413
1446	50	50	310316.0000	auto	2026-03-07 15:02:23.358413
1447	50	48	17600000.0000	auto	2026-03-07 15:02:23.358413
1448	50	47	9000.0000	auto	2026-03-07 15:02:23.358413
1449	51	52	94938939.0000	auto	2026-03-07 15:02:24.205581
1450	51	53	380665579.0000	auto	2026-03-07 15:02:24.205581
1451	51	54	30723181.0000	auto	2026-03-07 15:02:24.205581
1452	51	60	257965.0000	auto	2026-03-07 15:02:24.205581
1453	51	55	143290219.0000	auto	2026-03-07 15:02:24.205581
1454	51	56	17175706.0000	auto	2026-03-07 15:02:24.205581
1455	51	57	211830831.0000	auto	2026-03-07 15:02:24.205581
1456	51	58	12832796.8020	auto	2026-03-07 15:02:24.205581
1457	51	59	541894.4990	auto	2026-03-07 15:02:24.205581
1458	51	16	368011.0000	auto	2026-03-07 15:02:24.205581
1459	51	39	14165882.0000	auto	2026-03-07 15:02:24.205581
1460	51	43	1417388.0000	auto	2026-03-07 15:02:24.205581
1461	51	44	8591.0000	auto	2026-03-07 15:02:24.205581
1462	51	46	106229.0000	auto	2026-03-07 15:02:24.205581
1463	51	49	12869.0000	auto	2026-03-07 15:02:24.205581
1464	51	50	310316.0000	auto	2026-03-07 15:02:24.205581
1465	51	48	17600000.0000	auto	2026-03-07 15:02:24.205581
1466	51	47	9000.0000	auto	2026-03-07 15:02:24.205581
1467	52	52	94642727.0000	auto	2026-03-07 15:02:25.091578
1468	52	53	376580789.0000	auto	2026-03-07 15:02:25.091578
1469	52	54	30131400.0000	auto	2026-03-07 15:02:25.091578
1470	52	60	250185.0000	auto	2026-03-07 15:02:25.091578
1471	52	55	141242690.0000	auto	2026-03-07 15:02:25.091578
1472	52	56	15543256.0000	auto	2026-03-07 15:02:25.091578
1473	52	57	187594766.0000	auto	2026-03-07 15:02:25.091578
1474	52	58	12834799.7170	auto	2026-03-07 15:02:25.091578
1475	52	59	523196.4990	auto	2026-03-07 15:02:25.091578
1476	52	16	524744.0000	auto	2026-03-07 15:02:25.091578
1477	52	39	14165882.0000	auto	2026-03-07 15:02:25.091578
1478	52	43	1417388.0000	auto	2026-03-07 15:02:25.091578
1479	52	44	8591.0000	auto	2026-03-07 15:02:25.091578
1480	52	46	106229.0000	auto	2026-03-07 15:02:25.091578
1481	52	49	12869.0000	auto	2026-03-07 15:02:25.091578
1482	52	50	310316.0000	auto	2026-03-07 15:02:25.091578
1483	52	48	17600000.0000	auto	2026-03-07 15:02:25.091578
1484	52	47	9000.0000	auto	2026-03-07 15:02:25.091578
1485	53	52	89375935.0000	auto	2026-03-07 15:02:25.925843
1486	53	53	356048269.0000	auto	2026-03-07 15:02:25.925843
1487	53	54	30131400.0000	auto	2026-03-07 15:02:25.925843
1488	53	60	239425.0000	auto	2026-03-07 15:02:25.925843
1489	53	55	141267929.0000	auto	2026-03-07 15:02:25.925843
1490	53	56	14744016.0000	auto	2026-03-07 15:02:25.925843
1491	53	57	163367370.0000	auto	2026-03-07 15:02:25.925843
1492	53	58	12868330.0000	auto	2026-03-07 15:02:25.925843
1493	53	59	502393.6000	auto	2026-03-07 15:02:25.925843
1494	53	16	525010.0000	auto	2026-03-07 15:02:25.925843
1495	53	39	14165882.0000	auto	2026-03-07 15:02:25.925843
1496	53	43	1417388.0000	auto	2026-03-07 15:02:25.925843
1497	53	44	8591.0000	auto	2026-03-07 15:02:25.925843
1498	53	46	106229.0000	auto	2026-03-07 15:02:25.925843
1499	53	49	12883.0000	auto	2026-03-07 15:02:25.925843
1500	53	50	310316.0000	auto	2026-03-07 15:02:25.925843
1501	53	48	17600000.0000	auto	2026-03-07 15:02:25.925843
1502	53	47	9000.0000	auto	2026-03-07 15:02:25.925843
1503	54	52	86369623.0000	auto	2026-03-07 15:02:26.836623
1504	54	53	343965795.0000	auto	2026-03-07 15:02:26.836623
1505	54	54	25377578.0000	auto	2026-03-07 15:02:26.836623
1506	54	60	239425.0000	auto	2026-03-07 15:02:26.836623
1507	54	55	139049867.0000	auto	2026-03-07 15:02:26.836623
1508	54	56	14825646.0000	auto	2026-03-07 15:02:26.836623
1509	54	57	133162484.0000	auto	2026-03-07 15:02:26.836623
1510	54	58	12796832.6000	auto	2026-03-07 15:02:26.836623
1511	54	59	485364.6000	auto	2026-03-07 15:02:26.836623
1512	54	16	525273.0000	auto	2026-03-07 15:02:26.836623
1513	54	39	12217091.0000	auto	2026-03-07 15:02:26.836623
1514	54	43	1417388.0000	auto	2026-03-07 15:02:26.836623
1515	54	44	8591.0000	auto	2026-03-07 15:02:26.836623
1516	54	46	106229.0000	auto	2026-03-07 15:02:26.836623
1517	54	49	12883.0000	auto	2026-03-07 15:02:26.836623
1518	54	50	310316.0000	auto	2026-03-07 15:02:26.836623
1519	54	48	17600000.0000	auto	2026-03-07 15:02:26.836623
1520	54	47	9000.0000	auto	2026-03-07 15:02:26.836623
1521	55	52	84837691.0000	auto	2026-03-07 15:02:27.689942
1522	55	53	334014405.0000	auto	2026-03-07 15:02:27.689942
1523	55	54	23910633.0000	auto	2026-03-07 15:02:27.689942
1524	55	60	248240.0000	auto	2026-03-07 15:02:27.689942
1525	55	55	137939197.0000	auto	2026-03-07 15:02:27.689942
1526	55	56	14952846.0000	auto	2026-03-07 15:02:27.689942
1527	55	57	140008717.0000	auto	2026-03-07 15:02:27.689942
1528	55	58	12659133.8000	auto	2026-03-07 15:02:27.689942
1529	55	59	490802.0000	auto	2026-03-07 15:02:27.689942
1530	55	16	525518.0000	auto	2026-03-07 15:02:27.689942
1531	55	39	12217091.0000	auto	2026-03-07 15:02:27.689942
1532	55	43	1417388.0000	auto	2026-03-07 15:02:27.689942
1533	55	44	8591.0000	auto	2026-03-07 15:02:27.689942
1534	55	46	106229.0000	auto	2026-03-07 15:02:27.689942
1535	55	49	12883.0000	auto	2026-03-07 15:02:27.689942
1536	55	50	310316.0000	auto	2026-03-07 15:02:27.689942
1537	55	48	17600000.0000	auto	2026-03-07 15:02:27.689942
1538	55	47	9000.0000	auto	2026-03-07 15:02:27.689942
1539	56	52	85324919.0000	auto	2026-03-07 15:02:28.517966
1540	56	53	336685385.0000	auto	2026-03-07 15:02:28.517966
1541	56	54	24149810.0000	auto	2026-03-07 15:02:28.517966
1542	56	60	233390.0000	auto	2026-03-07 15:02:28.517966
1543	56	55	138958317.0000	auto	2026-03-07 15:02:28.517966
1544	56	56	15231626.0000	auto	2026-03-07 15:02:28.517966
1545	56	57	136011826.0000	auto	2026-03-07 15:02:28.517966
1546	56	58	12704978.8000	auto	2026-03-07 15:02:28.517966
1547	56	59	487941.6000	auto	2026-03-07 15:02:28.517966
1548	56	16	525763.0000	auto	2026-03-07 15:02:28.517966
1549	56	39	11841627.0000	auto	2026-03-07 15:02:28.517966
1550	56	43	1417388.0000	auto	2026-03-07 15:02:28.517966
1551	56	44	1614198.0000	auto	2026-03-07 15:02:28.517966
1552	56	46	106253.0000	auto	2026-03-07 15:02:28.517966
1553	56	49	12883.0000	auto	2026-03-07 15:02:28.517966
1554	56	50	310316.0000	auto	2026-03-07 15:02:28.517966
1555	56	48	17600000.0000	auto	2026-03-07 15:02:28.517966
1556	56	47	9029.0000	auto	2026-03-07 15:02:28.517966
1557	57	52	86066643.0000	auto	2026-03-07 15:02:29.382984
1558	57	53	342411515.0000	auto	2026-03-07 15:02:29.382984
1559	57	54	25014296.0000	auto	2026-03-07 15:02:29.382984
1560	57	60	220310.0000	auto	2026-03-07 15:02:29.382984
1561	57	55	137968497.0000	auto	2026-03-07 15:02:29.382984
1562	57	56	15435146.0000	auto	2026-03-07 15:02:29.382984
1563	57	57	118500172.8000	auto	2026-03-07 15:02:29.382984
1564	57	58	12757722.4000	auto	2026-03-07 15:02:29.382984
1565	57	59	508627.6000	auto	2026-03-07 15:02:29.382984
1566	57	16	275941.0000	auto	2026-03-07 15:02:29.382984
1567	57	39	11859072.0000	auto	2026-03-07 15:02:29.382984
1568	57	43	1417388.0000	auto	2026-03-07 15:02:29.382984
1569	57	44	114198.0000	auto	2026-03-07 15:02:29.382984
1570	57	46	116253.0000	auto	2026-03-07 15:02:29.382984
1571	57	49	12883.0000	auto	2026-03-07 15:02:29.382984
1572	57	50	320316.0000	auto	2026-03-07 15:02:29.382984
1573	57	48	17719029.0000	auto	2026-03-07 15:02:29.382984
1574	57	47	19029.0000	auto	2026-03-07 15:02:29.382984
1575	58	52	79059245.0000	auto	2026-03-07 15:02:30.232721
1576	58	53	311106485.0000	auto	2026-03-07 15:02:30.232721
1577	58	54	20529291.0000	auto	2026-03-07 15:02:30.232721
1578	58	60	222750.0000	auto	2026-03-07 15:02:30.232721
1579	58	55	132328755.5500	auto	2026-03-07 15:02:30.232721
1580	58	56	15269786.0000	auto	2026-03-07 15:02:30.232721
1581	58	57	85246690.6400	auto	2026-03-07 15:02:30.232721
1582	58	58	12513030.0600	auto	2026-03-07 15:02:30.232721
1583	58	59	466602.4200	auto	2026-03-07 15:02:30.232721
1584	58	16	276067.0000	auto	2026-03-07 15:02:30.232721
1585	58	39	11892956.0000	auto	2026-03-07 15:02:30.232721
1586	58	43	1417388.0000	auto	2026-03-07 15:02:30.232721
1587	58	44	114198.0000	auto	2026-03-07 15:02:30.232721
1588	58	46	116253.0000	auto	2026-03-07 15:02:30.232721
1589	58	49	12883.0000	auto	2026-03-07 15:02:30.232721
1590	58	50	320316.0000	auto	2026-03-07 15:02:30.232721
1591	58	48	17719029.0000	auto	2026-03-07 15:02:30.232721
1592	58	47	19029.0000	auto	2026-03-07 15:02:30.232721
1593	59	52	81810267.0000	auto	2026-03-07 15:02:31.086693
1594	59	53	319986780.0000	auto	2026-03-07 15:02:31.086693
1595	59	54	21428336.0000	auto	2026-03-07 15:02:31.086693
1596	59	60	355890.0000	auto	2026-03-07 15:02:31.086693
1597	59	55	134648497.5500	auto	2026-03-07 15:02:31.086693
1598	59	56	15816172.0000	auto	2026-03-07 15:02:31.086693
1599	59	57	110378343.0400	auto	2026-03-07 15:02:31.086693
1600	59	58	12290548.2000	auto	2026-03-07 15:02:31.086693
1601	59	59	544383.6200	auto	2026-03-07 15:02:31.086693
1602	59	16	276175.0000	auto	2026-03-07 15:02:31.086693
1603	59	39	11892956.0000	auto	2026-03-07 15:02:31.086693
1604	59	43	1417388.0000	auto	2026-03-07 15:02:31.086693
1605	59	44	114198.0000	auto	2026-03-07 15:02:31.086693
1606	59	46	116253.0000	auto	2026-03-07 15:02:31.086693
1607	59	49	12896.0000	auto	2026-03-07 15:02:31.086693
1608	59	50	320316.0000	auto	2026-03-07 15:02:31.086693
1609	59	48	17719029.0000	auto	2026-03-07 15:02:31.086693
1610	59	47	19029.0000	auto	2026-03-07 15:02:31.086693
1611	60	52	78036569.0000	auto	2026-03-07 15:02:31.925315
1612	60	53	303763505.0000	auto	2026-03-07 15:02:31.925315
1613	60	54	19230181.0000	auto	2026-03-07 15:02:31.925315
1614	60	60	528730.0000	auto	2026-03-07 15:02:31.925315
1615	60	55	122001453.5500	auto	2026-03-07 15:02:31.925315
1616	60	56	16146406.0000	auto	2026-03-07 15:02:31.925315
1617	60	57	93669558.0400	auto	2026-03-07 15:02:31.925315
1618	60	58	12151819.3700	auto	2026-03-07 15:02:31.925315
1619	60	59	465888.6200	auto	2026-03-07 15:02:31.925315
1620	60	16	276319.0000	auto	2026-03-07 15:02:31.925315
1621	60	39	12019541.0000	auto	2026-03-07 15:02:31.925315
1622	60	43	1417388.0000	auto	2026-03-07 15:02:31.925315
1623	60	44	114198.0000	auto	2026-03-07 15:02:31.925315
1624	60	46	116253.0000	auto	2026-03-07 15:02:31.925315
1625	60	49	12896.0000	auto	2026-03-07 15:02:31.925315
1626	60	50	320316.0000	auto	2026-03-07 15:02:31.925315
1627	60	48	17719029.0000	auto	2026-03-07 15:02:31.925315
1628	60	47	19029.0000	auto	2026-03-07 15:02:31.925315
1629	61	52	82810749.0000	auto	2026-03-07 15:02:32.825659
1630	61	53	325486480.0000	auto	2026-03-07 15:02:32.825659
1631	61	54	21765507.0000	auto	2026-03-07 15:02:32.825659
1632	61	60	473507.0000	auto	2026-03-07 15:02:32.825659
1633	61	55	135687107.5500	auto	2026-03-07 15:02:32.825659
1634	61	56	16225332.0000	auto	2026-03-07 15:02:32.825659
1635	61	57	119768930.0400	auto	2026-03-07 15:02:32.825659
1636	61	58	12442768.3700	auto	2026-03-07 15:02:32.825659
1637	61	59	506421.0000	auto	2026-03-07 15:02:32.825659
1638	61	16	276445.0000	auto	2026-03-07 15:02:32.825659
1639	61	39	12019541.0000	auto	2026-03-07 15:02:32.825659
1640	61	43	1202983.0000	auto	2026-03-07 15:02:32.825659
1641	61	44	114198.0000	auto	2026-03-07 15:02:32.825659
1642	61	46	116253.0000	auto	2026-03-07 15:02:32.825659
1643	61	49	12896.0000	auto	2026-03-07 15:02:32.825659
1644	61	50	320316.0000	auto	2026-03-07 15:02:32.825659
1645	61	48	17700000.0000	auto	2026-03-07 15:02:32.825659
1646	61	47	19029.0000	auto	2026-03-07 15:02:32.825659
1647	62	52	83692334.0000	auto	2026-03-07 15:02:33.678157
1648	62	53	327952816.0000	auto	2026-03-07 15:02:33.678157
1649	62	54	22290576.0000	auto	2026-03-07 15:02:33.678157
1650	62	60	601321.0000	auto	2026-03-07 15:02:33.678157
1651	62	55	136143858.0000	auto	2026-03-07 15:02:33.678157
1652	62	56	15878406.0000	auto	2026-03-07 15:02:33.678157
1653	62	57	130669563.5200	auto	2026-03-07 15:02:33.678157
1654	62	58	12440012.4600	auto	2026-03-07 15:02:33.678157
1655	62	59	567217.0000	auto	2026-03-07 15:02:33.678157
1656	62	16	917059.0000	auto	2026-03-07 15:02:33.678157
1657	62	39	12019541.0000	auto	2026-03-07 15:02:33.678157
1658	62	43	1202983.0000	auto	2026-03-07 15:02:33.678157
1659	62	44	114198.0000	auto	2026-03-07 15:02:33.678157
1660	62	46	116253.0000	auto	2026-03-07 15:02:33.678157
1661	62	49	12908.0000	auto	2026-03-07 15:02:33.678157
1662	62	50	320316.0000	auto	2026-03-07 15:02:33.678157
1663	62	48	17700000.0000	auto	2026-03-07 15:02:33.678157
1664	62	47	19029.0000	auto	2026-03-07 15:02:33.678157
1665	63	52	84111438.0000	auto	2026-03-07 15:02:34.533235
1666	63	53	328672252.0000	auto	2026-03-07 15:02:34.533235
1667	63	54	22340154.0000	auto	2026-03-07 15:02:34.533235
1668	63	60	65420.0000	auto	2026-03-07 15:02:34.533235
1669	63	55	134320559.0000	auto	2026-03-07 15:02:34.533235
1670	63	56	16057096.0000	auto	2026-03-07 15:02:34.533235
1671	63	57	127853252.5200	auto	2026-03-07 15:02:34.533235
1672	63	58	12199561.0800	auto	2026-03-07 15:02:34.533235
1673	63	59	552632.0000	auto	2026-03-07 15:02:34.533235
1674	63	16	917608.0000	auto	2026-03-07 15:02:34.533235
1675	63	39	11042809.0000	auto	2026-03-07 15:02:34.533235
1676	63	43	1018553.0000	auto	2026-03-07 15:02:34.533235
1677	63	44	114198.0000	auto	2026-03-07 15:02:34.533235
1678	63	46	116253.0000	auto	2026-03-07 15:02:34.533235
1679	63	49	517989.0000	auto	2026-03-07 15:02:34.533235
1680	63	50	320316.0000	auto	2026-03-07 15:02:34.533235
1681	63	48	17700000.0000	auto	2026-03-07 15:02:34.533235
1682	63	47	19029.0000	auto	2026-03-07 15:02:34.533235
1683	64	52	89322460.0000	auto	2026-03-07 15:02:35.401376
1684	64	53	350403728.0000	auto	2026-03-07 15:02:35.401376
1685	64	54	25565795.0000	auto	2026-03-07 15:02:35.401376
1686	64	60	43910.0000	auto	2026-03-07 15:02:35.401376
1687	64	55	137903673.0000	auto	2026-03-07 15:02:35.401376
1688	64	56	15482112.0000	auto	2026-03-07 15:02:35.401376
1689	64	57	144082164.7800	auto	2026-03-07 15:02:35.401376
1690	64	58	12350765.1000	auto	2026-03-07 15:02:35.401376
1691	64	59	599675.2800	auto	2026-03-07 15:02:35.401376
1692	64	16	917974.0000	auto	2026-03-07 15:02:35.401376
1693	64	39	10912610.0000	auto	2026-03-07 15:02:35.401376
1694	64	43	760041.0000	auto	2026-03-07 15:02:35.401376
1695	64	44	114198.0000	auto	2026-03-07 15:02:35.401376
1696	64	46	116253.0000	auto	2026-03-07 15:02:35.401376
1697	64	49	517989.0000	auto	2026-03-07 15:02:35.401376
1698	64	50	320316.0000	auto	2026-03-07 15:02:35.401376
1699	64	48	17700000.0000	auto	2026-03-07 15:02:35.401376
1700	64	47	19029.0000	auto	2026-03-07 15:02:35.401376
1701	65	52	87835922.0000	auto	2026-03-07 15:02:36.229616
1702	65	53	344632148.0000	auto	2026-03-07 15:02:36.229616
1703	65	54	24484109.0000	auto	2026-03-07 15:02:36.229616
1704	65	60	42640.0000	auto	2026-03-07 15:02:36.229616
1705	65	55	134850867.0000	auto	2026-03-07 15:02:36.229616
1706	65	56	15781036.0000	auto	2026-03-07 15:02:36.229616
1707	65	57	136839191.7050	auto	2026-03-07 15:02:36.229616
1708	65	58	11994712.1750	auto	2026-03-07 15:02:36.229616
1709	65	59	583342.6900	auto	2026-03-07 15:02:36.229616
1710	65	16	918462.0000	auto	2026-03-07 15:02:36.229616
1711	65	39	10912610.0000	auto	2026-03-07 15:02:36.229616
1712	65	43	697542.0000	auto	2026-03-07 15:02:36.229616
1713	65	44	114198.0000	auto	2026-03-07 15:02:36.229616
1714	65	46	116253.0000	auto	2026-03-07 15:02:36.229616
1715	65	49	517989.0000	auto	2026-03-07 15:02:36.229616
1716	65	50	320316.0000	auto	2026-03-07 15:02:36.229616
1717	65	48	17700000.0000	auto	2026-03-07 15:02:36.229616
1718	65	47	19029.0000	auto	2026-03-07 15:02:36.229616
1719	66	52	89450944.0000	auto	2026-03-07 15:02:37.096836
1720	66	53	351163278.0000	auto	2026-03-07 15:02:37.096836
1721	66	54	25715780.0000	auto	2026-03-07 15:02:37.096836
1722	66	60	42820.0000	auto	2026-03-07 15:02:37.096836
1723	66	55	136372374.0000	auto	2026-03-07 15:02:37.096836
1724	66	56	15672966.0000	auto	2026-03-07 15:02:37.096836
1725	66	57	143029572.8870	auto	2026-03-07 15:02:37.096836
1726	66	58	12173812.3450	auto	2026-03-07 15:02:37.096836
1727	66	59	653158.7660	auto	2026-03-07 15:02:37.096836
1728	66	16	918889.0000	auto	2026-03-07 15:02:37.096836
1729	66	39	10912610.0000	auto	2026-03-07 15:02:37.096836
1730	66	43	464433.0000	auto	2026-03-07 15:02:37.096836
1731	66	44	114198.0000	auto	2026-03-07 15:02:37.096836
1732	66	46	116253.0000	auto	2026-03-07 15:02:37.096836
1733	66	49	517989.0000	auto	2026-03-07 15:02:37.096836
1734	66	50	320316.0000	auto	2026-03-07 15:02:37.096836
1735	66	48	17700000.0000	auto	2026-03-07 15:02:37.096836
1736	66	47	19029.0000	auto	2026-03-07 15:02:37.096836
1737	67	52	89618167.0000	auto	2026-03-07 15:02:37.946651
1738	67	53	348203204.0000	auto	2026-03-07 15:02:37.946651
1739	67	54	25196811.0000	auto	2026-03-07 15:02:37.946651
1740	67	60	43305.0000	auto	2026-03-07 15:02:37.946651
1741	67	55	137032708.0000	auto	2026-03-07 15:02:37.946651
1742	67	56	15789248.0000	auto	2026-03-07 15:02:37.946651
1743	67	57	148898434.5050	auto	2026-03-07 15:02:37.946651
1744	67	58	12102532.1700	auto	2026-03-07 15:02:37.946651
1745	67	59	666931.0900	auto	2026-03-07 15:02:37.946651
1746	67	16	919255.0000	auto	2026-03-07 15:02:37.946651
1747	67	39	10912610.0000	auto	2026-03-07 15:02:37.946651
1748	67	43	384433.0000	auto	2026-03-07 15:02:37.946651
1749	67	44	114198.0000	auto	2026-03-07 15:02:37.946651
1750	67	46	116253.0000	auto	2026-03-07 15:02:37.946651
1751	67	49	517989.0000	auto	2026-03-07 15:02:37.946651
1752	67	50	320316.0000	auto	2026-03-07 15:02:37.946651
1753	67	48	17700000.0000	auto	2026-03-07 15:02:37.946651
1754	67	47	19029.0000	auto	2026-03-07 15:02:37.946651
1755	68	52	89866350.0000	auto	2026-03-07 15:02:38.784538
1756	68	53	349674819.0000	auto	2026-03-07 15:02:38.784538
1757	68	54	25036183.0000	auto	2026-03-07 15:02:38.784538
1758	68	60	42328.0000	auto	2026-03-07 15:02:38.784538
1759	68	55	136625003.0000	auto	2026-03-07 15:02:38.784538
1760	68	56	16120249.0000	auto	2026-03-07 15:02:38.784538
1761	68	57	147056684.3450	auto	2026-03-07 15:02:38.784538
1762	68	58	12177727.4750	auto	2026-03-07 15:02:38.784538
1763	68	59	663822.3400	auto	2026-03-07 15:02:38.784538
1764	68	16	919707.0000	auto	2026-03-07 15:02:38.784538
1765	68	39	10912610.0000	auto	2026-03-07 15:02:38.784538
1766	68	43	289727.0000	auto	2026-03-07 15:02:38.784538
1767	68	44	114198.0000	auto	2026-03-07 15:02:38.784538
1768	68	46	116253.0000	auto	2026-03-07 15:02:38.784538
1769	68	49	1280305.0000	auto	2026-03-07 15:02:38.784538
1770	68	50	320316.0000	auto	2026-03-07 15:02:38.784538
1771	68	48	17700000.0000	auto	2026-03-07 15:02:38.784538
1772	68	47	19029.0000	auto	2026-03-07 15:02:38.784538
1773	69	52	90832992.0000	auto	2026-03-07 15:02:39.614388
1774	69	53	353940039.0000	auto	2026-03-07 15:02:39.614388
1775	69	54	25828744.0000	auto	2026-03-07 15:02:39.614388
1776	69	60	43235.0000	auto	2026-03-07 15:02:39.614388
1777	69	55	137172505.0000	auto	2026-03-07 15:02:39.614388
1778	69	56	15846329.0000	auto	2026-03-07 15:02:39.614388
1779	69	57	149167768.6400	auto	2026-03-07 15:02:39.614388
1780	69	58	12284508.1600	auto	2026-03-07 15:02:39.614388
1781	69	59	666375.3000	auto	2026-03-07 15:02:39.614388
1782	69	16	920147.0000	auto	2026-03-07 15:02:39.614388
1783	69	39	10912610.0000	auto	2026-03-07 15:02:39.614388
1784	69	43	1029464.0000	auto	2026-03-07 15:02:39.614388
1785	69	44	114198.0000	auto	2026-03-07 15:02:39.614388
1786	69	46	116253.0000	auto	2026-03-07 15:02:39.614388
1787	69	49	280305.0000	auto	2026-03-07 15:02:39.614388
1788	69	50	320316.0000	auto	2026-03-07 15:02:39.614388
1789	69	48	17700000.0000	auto	2026-03-07 15:02:39.614388
1790	69	47	19029.0000	auto	2026-03-07 15:02:39.614388
1791	70	52	93627614.0000	auto	2026-03-07 15:02:40.483177
1792	70	53	362635649.0000	auto	2026-03-07 15:02:40.483177
1793	70	54	27279963.0000	auto	2026-03-07 15:02:40.483177
1794	70	60	43235.0000	auto	2026-03-07 15:02:40.483177
1795	70	55	138419588.0000	auto	2026-03-07 15:02:40.483177
1796	70	56	15464339.0000	auto	2026-03-07 15:02:40.483177
1797	70	57	164349197.6400	auto	2026-03-07 15:02:40.483177
1798	70	58	12259358.0600	auto	2026-03-07 15:02:40.483177
1799	70	59	699105.3000	auto	2026-03-07 15:02:40.483177
1800	70	16	920422.0000	auto	2026-03-07 15:02:40.483177
1801	70	39	10912610.0000	auto	2026-03-07 15:02:40.483177
1802	70	43	874855.0000	auto	2026-03-07 15:02:40.483177
1803	70	44	114198.0000	auto	2026-03-07 15:02:40.483177
1804	70	46	116253.0000	auto	2026-03-07 15:02:40.483177
1805	70	49	280305.0000	auto	2026-03-07 15:02:40.483177
1806	70	50	320316.0000	auto	2026-03-07 15:02:40.483177
1807	70	48	17700000.0000	auto	2026-03-07 15:02:40.483177
1808	70	47	19029.0000	auto	2026-03-07 15:02:40.483177
1809	71	52	95018396.0000	auto	2026-03-07 15:02:41.350186
1810	71	53	367656969.0000	auto	2026-03-07 15:02:41.350186
1811	71	54	27954715.0000	auto	2026-03-07 15:02:41.350186
1812	71	60	42279.0000	auto	2026-03-07 15:02:41.350186
1813	71	55	139876971.2600	auto	2026-03-07 15:02:41.350186
1814	71	56	15887679.0000	auto	2026-03-07 15:02:41.350186
1815	71	57	166959535.4400	auto	2026-03-07 15:02:41.350186
1816	71	58	12347693.0600	auto	2026-03-07 15:02:41.350186
1817	71	59	703211.3000	auto	2026-03-07 15:02:41.350186
1818	71	16	770844.0000	auto	2026-03-07 15:02:41.350186
1819	71	39	10912610.0000	auto	2026-03-07 15:02:41.350186
1820	71	43	649855.0000	auto	2026-03-07 15:02:41.350186
1821	71	44	114198.0000	auto	2026-03-07 15:02:41.350186
1822	71	46	116253.0000	auto	2026-03-07 15:02:41.350186
1823	71	49	280686.0000	auto	2026-03-07 15:02:41.350186
1824	71	50	320316.0000	auto	2026-03-07 15:02:41.350186
1825	71	48	17700000.0000	auto	2026-03-07 15:02:41.350186
1826	71	47	19029.0000	auto	2026-03-07 15:02:41.350186
1827	72	52	96324518.0000	auto	2026-03-07 15:02:42.205
1828	72	53	372481688.0000	auto	2026-03-07 15:02:42.205
1829	72	54	28677658.0000	auto	2026-03-07 15:02:42.205
1830	72	60	42663.0000	auto	2026-03-07 15:02:42.205
1831	72	55	139630606.0000	auto	2026-03-07 15:02:42.205
1832	72	56	16162949.0000	auto	2026-03-07 15:02:42.205
1833	72	57	167302092.0600	auto	2026-03-07 15:02:42.205
1834	72	58	12520841.3800	auto	2026-03-07 15:02:42.205
1835	72	59	721206.8200	auto	2026-03-07 15:02:42.205
1836	72	16	1475891.0000	auto	2026-03-07 15:02:42.205
1837	72	39	12996386.0000	auto	2026-03-07 15:02:42.205
1838	72	43	7202715.0000	auto	2026-03-07 15:02:42.205
1839	72	44	114234.0000	auto	2026-03-07 15:02:42.205
1840	72	46	116253.0000	auto	2026-03-07 15:02:42.205
1841	72	49	202186.0000	auto	2026-03-07 15:02:42.205
1842	72	50	320316.0000	auto	2026-03-07 15:02:42.205
1843	72	48	17700000.0000	auto	2026-03-07 15:02:42.205
1844	72	47	19029.0000	auto	2026-03-07 15:02:42.205
1845	73	52	99479440.0000	auto	2026-03-07 15:02:43.058294
1846	73	53	384363853.0000	auto	2026-03-07 15:02:43.058294
1847	73	54	30642787.0000	auto	2026-03-07 15:02:43.058294
1848	73	60	42722.0000	auto	2026-03-07 15:02:43.058294
1849	73	55	141175199.0000	auto	2026-03-07 15:02:43.058294
1850	73	56	16304649.0000	auto	2026-03-07 15:02:43.058294
1851	73	57	175367455.0600	auto	2026-03-07 15:02:43.058294
1852	73	58	12610015.4000	auto	2026-03-07 15:02:43.058294
1853	73	59	748056.0000	auto	2026-03-07 15:02:43.058294
1854	73	16	1476437.0000	auto	2026-03-07 15:02:43.058294
1855	73	39	12114375.0000	auto	2026-03-07 15:02:43.058294
1856	73	43	6797162.0000	auto	2026-03-07 15:02:43.058294
1857	73	44	114234.0000	auto	2026-03-07 15:02:43.058294
1858	73	46	116253.0000	auto	2026-03-07 15:02:43.058294
1859	73	49	202186.0000	auto	2026-03-07 15:02:43.058294
1860	73	50	320316.0000	auto	2026-03-07 15:02:43.058294
1861	73	48	17700000.0000	auto	2026-03-07 15:02:43.058294
1862	73	47	19029.0000	auto	2026-03-07 15:02:43.058294
1863	74	52	99376462.0000	auto	2026-03-07 15:02:43.876996
1864	74	53	384690878.0000	auto	2026-03-07 15:02:43.876996
1865	74	54	30584086.0000	auto	2026-03-07 15:02:43.876996
1866	74	60	41803.0000	auto	2026-03-07 15:02:43.876996
1867	74	55	141024220.0000	auto	2026-03-07 15:02:43.876996
1868	74	56	16216359.0000	auto	2026-03-07 15:02:43.876996
1869	74	57	175598473.0600	auto	2026-03-07 15:02:43.876996
1870	74	58	12600753.4000	auto	2026-03-07 15:02:43.876996
1871	74	59	750107.0000	auto	2026-03-07 15:02:43.876996
1872	74	16	1476988.0000	auto	2026-03-07 15:02:43.876996
1873	74	39	12114375.0000	auto	2026-03-07 15:02:43.876996
1874	74	43	6561553.0000	auto	2026-03-07 15:02:43.876996
1875	74	44	114234.0000	auto	2026-03-07 15:02:43.876996
1876	74	46	116253.0000	auto	2026-03-07 15:02:43.876996
1877	74	49	167186.0000	auto	2026-03-07 15:02:43.876996
1878	74	50	320316.0000	auto	2026-03-07 15:02:43.876996
1879	74	48	17700000.0000	auto	2026-03-07 15:02:43.876996
1880	74	47	19029.0000	auto	2026-03-07 15:02:43.876996
1881	75	52	101518204.0000	auto	2026-03-07 15:02:43.649127
1882	75	53	392405618.0000	auto	2026-03-07 15:02:43.649127
1883	75	54	31778859.0000	auto	2026-03-07 15:02:43.649127
1884	75	60	40287.0000	auto	2026-03-07 15:02:43.649127
1885	75	55	140739961.0000	auto	2026-03-07 15:02:43.649127
1886	75	56	16200009.0000	auto	2026-03-07 15:02:43.649127
1887	75	57	173142004.0600	auto	2026-03-07 15:02:43.649127
1888	75	58	12613584.6200	auto	2026-03-07 15:02:43.649127
1889	75	59	750451.0000	auto	2026-03-07 15:02:43.649127
1890	75	16	1477541.0000	auto	2026-03-07 15:02:43.649127
1891	75	39	12114375.0000	auto	2026-03-07 15:02:43.649127
1892	75	43	6661553.0000	auto	2026-03-07 15:02:43.649127
1893	75	44	114234.0000	auto	2026-03-07 15:02:43.649127
1894	75	46	116253.0000	auto	2026-03-07 15:02:43.649127
1895	75	49	167348.0000	auto	2026-03-07 15:02:43.649127
1896	75	50	320316.0000	auto	2026-03-07 15:02:43.649127
1897	75	48	17700000.0000	auto	2026-03-07 15:02:43.649127
1898	75	47	19029.0000	auto	2026-03-07 15:02:43.649127
1899	76	52	103600926.0000	auto	2026-03-07 15:02:44.548274
1900	76	53	398624410.0000	auto	2026-03-07 15:02:44.548274
1901	76	54	32374179.0000	auto	2026-03-07 15:02:44.548274
1902	76	60	41122.0000	auto	2026-03-07 15:02:44.548274
1903	76	55	141982591.0000	auto	2026-03-07 15:02:44.548274
1904	76	56	17009149.0000	auto	2026-03-07 15:02:44.548274
1905	76	57	184187811.0600	auto	2026-03-07 15:02:44.548274
1906	76	58	13293845.2600	auto	2026-03-07 15:02:44.548274
1907	76	59	825029.0000	auto	2026-03-07 15:02:44.548274
1908	76	16	724198.0000	auto	2026-03-07 15:02:44.548274
1909	76	39	14114375.0000	auto	2026-03-07 15:02:44.548274
1910	76	43	9091557.0000	auto	2026-03-07 15:02:44.548274
1911	76	44	124234.0000	auto	2026-03-07 15:02:44.548274
1912	76	46	136283.0000	auto	2026-03-07 15:02:44.548274
1913	76	49	167348.0000	auto	2026-03-07 15:02:44.548274
1914	76	50	340453.0000	auto	2026-03-07 15:02:44.548274
1915	76	48	17900000.0000	auto	2026-03-07 15:02:44.548274
1916	76	47	39033.0000	auto	2026-03-07 15:02:44.548274
1917	77	52	104691235.0000	auto	2026-03-07 15:02:45.347857
1918	77	53	403590340.0000	auto	2026-03-07 15:02:45.347857
1919	77	54	33159229.0000	auto	2026-03-07 15:02:45.347857
1920	77	60	41453.0000	auto	2026-03-07 15:02:45.347857
1921	77	55	142739351.0000	auto	2026-03-07 15:02:45.347857
1922	77	56	16632859.0000	auto	2026-03-07 15:02:45.347857
1923	77	57	184114707.5000	auto	2026-03-07 15:02:45.347857
1924	77	58	13115049.3600	auto	2026-03-07 15:02:45.347857
1925	77	59	855526.0000	auto	2026-03-07 15:02:45.347857
1926	77	16	724456.0000	auto	2026-03-07 15:02:45.347857
1927	77	39	14102915.0000	auto	2026-03-07 15:02:45.347857
1928	77	43	8952302.0000	auto	2026-03-07 15:02:45.347857
1929	77	44	124234.0000	auto	2026-03-07 15:02:45.347857
1930	77	46	136283.0000	auto	2026-03-07 15:02:45.347857
1931	77	49	167348.0000	auto	2026-03-07 15:02:45.347857
1932	77	50	340453.0000	auto	2026-03-07 15:02:45.347857
1933	77	48	17900000.0000	auto	2026-03-07 15:02:45.347857
1934	77	47	39033.0000	auto	2026-03-07 15:02:45.347857
1935	78	52	102031841.0000	auto	2026-03-07 15:02:46.20859
1936	78	53	392070040.0000	auto	2026-03-07 15:02:46.20859
1937	78	54	31418146.0000	auto	2026-03-07 15:02:46.20859
1938	78	60	42626.0000	auto	2026-03-07 15:02:46.20859
1939	78	55	142723913.0000	auto	2026-03-07 15:02:46.20859
1940	78	56	16587349.0000	auto	2026-03-07 15:02:46.20859
1941	78	57	180419130.0000	auto	2026-03-07 15:02:46.20859
1942	78	58	13352401.0000	auto	2026-03-07 15:02:46.20859
1943	78	59	856080.0000	auto	2026-03-07 15:02:46.20859
1944	78	16	724757.0000	auto	2026-03-07 15:02:46.20859
1945	78	39	14102915.0000	auto	2026-03-07 15:02:46.20859
1946	78	43	7679238.0000	auto	2026-03-07 15:02:46.20859
1947	78	44	124234.0000	auto	2026-03-07 15:02:46.20859
1948	78	46	136283.0000	auto	2026-03-07 15:02:46.20859
1949	78	49	87848.0000	auto	2026-03-07 15:02:46.20859
1950	78	50	340453.0000	auto	2026-03-07 15:02:46.20859
1951	78	48	17900000.0000	auto	2026-03-07 15:02:46.20859
1952	78	47	39033.0000	auto	2026-03-07 15:02:46.20859
1953	79	52	104843257.0000	auto	2026-03-07 15:02:47.080573
1954	79	53	404944540.0000	auto	2026-03-07 15:02:47.080573
1955	79	54	33369984.0000	auto	2026-03-07 15:02:47.080573
1956	79	60	41506.0000	auto	2026-03-07 15:02:47.080573
1957	79	55	143212856.0000	auto	2026-03-07 15:02:47.080573
1958	79	56	16972519.0000	auto	2026-03-07 15:02:47.080573
1959	79	57	177825536.0000	auto	2026-03-07 15:02:47.080573
1960	79	58	13134523.5800	auto	2026-03-07 15:02:47.080573
1961	79	59	851988.0000	auto	2026-03-07 15:02:47.080573
1962	79	16	725058.0000	auto	2026-03-07 15:02:47.080573
1963	79	39	14102915.0000	auto	2026-03-07 15:02:47.080573
1964	79	43	5664209.0000	auto	2026-03-07 15:02:47.080573
1965	79	44	124234.0000	auto	2026-03-07 15:02:47.080573
1966	79	46	136283.0000	auto	2026-03-07 15:02:47.080573
1967	79	49	87848.0000	auto	2026-03-07 15:02:47.080573
1968	79	50	340453.0000	auto	2026-03-07 15:02:47.080573
1969	79	48	17900000.0000	auto	2026-03-07 15:02:47.080573
1970	79	47	39033.0000	auto	2026-03-07 15:02:47.080573
1971	80	52	106515124.0000	auto	2026-03-07 15:02:47.969025
1972	80	53	422620189.0000	auto	2026-03-07 15:02:47.969025
1973	80	54	40571294.0000	auto	2026-03-07 15:02:47.969025
1974	80	60	42247.0000	auto	2026-03-07 15:02:47.969025
1975	80	55	144895135.0000	auto	2026-03-07 15:02:47.969025
1976	80	56	18331183.0000	auto	2026-03-07 15:02:47.969025
1977	80	57	189238243.0000	auto	2026-03-07 15:02:47.969025
1978	80	58	13543334.2800	auto	2026-03-07 15:02:47.969025
1979	80	59	885279.0000	auto	2026-03-07 15:02:47.969025
1980	80	16	28620.0000	auto	2026-03-07 15:02:47.969025
1981	80	39	16102915.0000	auto	2026-03-07 15:02:47.969025
1982	80	43	1194878.0000	auto	2026-03-07 15:02:47.969025
1983	80	44	124234.0000	auto	2026-03-07 15:02:47.969025
1984	80	46	146283.0000	auto	2026-03-07 15:02:47.969025
1985	80	49	87947.0000	auto	2026-03-07 15:02:47.969025
1986	80	50	350453.0000	auto	2026-03-07 15:02:47.969025
1987	80	48	18000000.0000	auto	2026-03-07 15:02:47.969025
1988	80	47	49033.0000	auto	2026-03-07 15:02:47.969025
1989	81	52	109295882.0000	auto	2026-03-07 15:02:48.881096
1990	81	53	436756073.0000	auto	2026-03-07 15:02:48.881096
1991	81	54	45618569.0000	auto	2026-03-07 15:02:48.881096
1992	81	60	41914.0000	auto	2026-03-07 15:02:48.881096
1993	81	55	95434571.0000	auto	2026-03-07 15:02:48.881096
1994	81	56	18849486.0000	auto	2026-03-07 15:02:48.881096
1995	81	57	204830088.5640	auto	2026-03-07 15:02:48.881096
1996	81	58	14107855.0000	auto	2026-03-07 15:02:48.881096
1997	81	59	950791.9980	auto	2026-03-07 15:02:48.881096
1998	81	16	30084644.0000	auto	2026-03-07 15:02:48.881096
1999	81	38	184753.0000	auto	2026-03-07 15:02:48.881096
2000	81	39	13632203.0000	auto	2026-03-07 15:02:48.881096
2001	81	43	1320453.0000	auto	2026-03-07 15:02:48.881096
2002	81	44	124263.0000	auto	2026-03-07 15:02:48.881096
2003	81	46	146315.0000	auto	2026-03-07 15:02:48.881096
2004	81	49	87948.0000	auto	2026-03-07 15:02:48.881096
2005	81	50	350453.0000	auto	2026-03-07 15:02:48.881096
2006	81	48	18000000.0000	auto	2026-03-07 15:02:48.881096
2007	81	47	49041.0000	auto	2026-03-07 15:02:48.881096
2008	82	52	110432162.0000	auto	2026-03-07 15:02:49.717243
2009	82	53	439669148.0000	auto	2026-03-07 15:02:49.717243
2010	82	54	46577844.0000	auto	2026-03-07 15:02:49.717243
2011	82	60	40605.0000	auto	2026-03-07 15:02:49.717243
2012	82	55	96176149.0000	auto	2026-03-07 15:02:49.717243
2013	82	56	21308066.0000	auto	2026-03-07 15:02:49.717243
2014	82	57	201361556.0000	auto	2026-03-07 15:02:49.717243
2015	82	58	14239366.0000	auto	2026-03-07 15:02:49.717243
2016	82	59	924811.9980	auto	2026-03-07 15:02:49.717243
2017	82	16	29095195.0000	auto	2026-03-07 15:02:49.717243
2018	82	38	185046.0000	auto	2026-03-07 15:02:49.717243
2019	82	39	13632203.0000	auto	2026-03-07 15:02:49.717243
2020	82	43	989054.0000	auto	2026-03-07 15:02:49.717243
2021	82	44	124263.0000	auto	2026-03-07 15:02:49.717243
2022	82	46	146315.0000	auto	2026-03-07 15:02:49.717243
2023	82	49	52005.0000	auto	2026-03-07 15:02:49.717243
2024	82	50	350453.0000	auto	2026-03-07 15:02:49.717243
2025	82	48	18000000.0000	auto	2026-03-07 15:02:49.717243
2026	82	47	49041.0000	auto	2026-03-07 15:02:49.717243
2027	83	52	111800102.0000	auto	2026-03-07 15:02:50.558111
2028	83	53	440536619.0000	auto	2026-03-07 15:02:50.558111
2029	83	54	47046094.0000	auto	2026-03-07 15:02:50.558111
2030	83	60	41020.0000	auto	2026-03-07 15:02:50.558111
2031	83	55	97342077.6900	auto	2026-03-07 15:02:50.558111
2032	83	56	23012963.0000	auto	2026-03-07 15:02:50.558111
2033	83	57	208113633.2900	auto	2026-03-07 15:02:50.558111
2034	83	58	14443005.3780	auto	2026-03-07 15:02:50.558111
2035	83	59	960717.9980	auto	2026-03-07 15:02:50.558111
2036	83	16	27105196.0000	auto	2026-03-07 15:02:50.558111
2037	83	38	185122.0000	auto	2026-03-07 15:02:50.558111
2038	83	39	13632203.0000	auto	2026-03-07 15:02:50.558111
2039	83	43	923054.0000	auto	2026-03-07 15:02:50.558111
2040	83	44	124263.0000	auto	2026-03-07 15:02:50.558111
2041	83	46	146315.0000	auto	2026-03-07 15:02:50.558111
2042	83	49	52005.0000	auto	2026-03-07 15:02:50.558111
2043	83	50	350453.0000	auto	2026-03-07 15:02:50.558111
2044	83	48	18000000.0000	auto	2026-03-07 15:02:50.558111
2045	83	47	49041.0000	auto	2026-03-07 15:02:50.558111
2046	84	52	113722084.0000	auto	2026-03-07 15:02:51.432194
2047	84	53	449092804.0000	auto	2026-03-07 15:02:51.432194
2048	84	54	49139064.0000	auto	2026-03-07 15:02:51.432194
2049	84	60	40129.0000	auto	2026-03-07 15:02:51.432194
2050	84	55	95482195.0500	auto	2026-03-07 15:02:51.432194
2051	84	56	25529193.0000	auto	2026-03-07 15:02:51.432194
2052	84	57	201555108.2900	auto	2026-03-07 15:02:51.432194
2053	84	58	14216843.6100	auto	2026-03-07 15:02:51.432194
2054	84	59	935653.0300	auto	2026-03-07 15:02:51.432194
2055	84	16	25114507.0000	auto	2026-03-07 15:02:51.432194
2056	84	39	15632203.0000	auto	2026-03-07 15:02:51.432194
2057	84	43	6500414.0000	auto	2026-03-07 15:02:51.432194
2058	84	44	124263.0000	auto	2026-03-07 15:02:51.432194
2059	84	46	156315.0000	auto	2026-03-07 15:02:51.432194
2060	84	49	52017.0000	auto	2026-03-07 15:02:51.432194
2061	84	50	360453.0000	auto	2026-03-07 15:02:51.432194
2062	84	48	18100000.0000	auto	2026-03-07 15:02:51.432194
2063	84	47	59041.0000	auto	2026-03-07 15:02:51.432194
2064	85	52	110495764.0000	auto	2026-03-07 15:02:52.300755
2065	85	53	439174554.0000	auto	2026-03-07 15:02:52.300755
2066	85	54	48359373.0000	auto	2026-03-07 15:02:52.300755
2067	85	60	42375.0000	auto	2026-03-07 15:02:52.300755
2068	85	55	97753457.0000	auto	2026-03-07 15:02:52.300755
2069	85	56	28316713.0000	auto	2026-03-07 15:02:52.300755
2070	85	57	210865472.0000	auto	2026-03-07 15:02:52.300755
2071	85	58	14623149.0000	auto	2026-03-07 15:02:52.300755
2072	85	59	993187.0000	auto	2026-03-07 15:02:52.300755
2073	85	16	25367610.0000	auto	2026-03-07 15:02:52.300755
2074	85	39	15546312.0000	auto	2026-03-07 15:02:52.300755
2075	85	43	2023204.0000	auto	2026-03-07 15:02:52.300755
2076	85	44	124263.0000	auto	2026-03-07 15:02:52.300755
2077	85	46	156315.0000	auto	2026-03-07 15:02:52.300755
2078	85	49	52017.0000	auto	2026-03-07 15:02:52.300755
2079	85	50	360453.0000	auto	2026-03-07 15:02:52.300755
2080	85	48	18100000.0000	auto	2026-03-07 15:02:52.300755
2081	85	47	59041.0000	auto	2026-03-07 15:02:52.300755
2082	86	52	114096064.0000	auto	2026-03-07 15:02:53.096312
2083	86	53	455705909.0000	auto	2026-03-07 15:02:53.096312
2084	86	54	50034113.0000	auto	2026-03-07 15:02:53.096312
2085	86	60	43842.0000	auto	2026-03-07 15:02:53.096312
2086	86	55	100392909.0000	auto	2026-03-07 15:02:53.096312
2087	86	56	25734873.0000	auto	2026-03-07 15:02:53.096312
2088	86	57	221608841.0000	auto	2026-03-07 15:02:53.096312
2089	86	58	14932509.0000	auto	2026-03-07 15:02:53.096312
2090	86	59	1030609.0000	auto	2026-03-07 15:02:53.096312
2091	86	16	24376451.0000	auto	2026-03-07 15:02:53.096312
2092	86	39	15546312.0000	auto	2026-03-07 15:02:53.096312
2093	86	43	1921704.0000	auto	2026-03-07 15:02:53.096312
2094	86	44	124263.0000	auto	2026-03-07 15:02:53.096312
2095	86	46	156315.0000	auto	2026-03-07 15:02:53.096312
2096	86	49	52017.0000	auto	2026-03-07 15:02:53.096312
2097	86	50	360453.0000	auto	2026-03-07 15:02:53.096312
2098	86	48	18100000.0000	auto	2026-03-07 15:02:53.096312
2099	86	47	59041.0000	auto	2026-03-07 15:02:53.096312
2100	87	52	119638644.0000	auto	2026-03-07 15:02:53.944822
2101	87	53	479016894.0000	auto	2026-03-07 15:02:53.944822
2102	87	54	54533173.0000	auto	2026-03-07 15:02:53.944822
2103	87	60	43995.0000	auto	2026-03-07 15:02:53.944822
2104	87	55	99786252.0000	auto	2026-03-07 15:02:53.944822
2105	87	56	25963893.0000	auto	2026-03-07 15:02:53.944822
2106	87	57	236744192.0000	auto	2026-03-07 15:02:53.944822
2107	87	58	14564563.1300	auto	2026-03-07 15:02:53.944822
2108	87	59	1083052.0000	auto	2026-03-07 15:02:53.944822
2109	87	16	23384994.0000	auto	2026-03-07 15:02:53.944822
2110	87	39	15546312.0000	auto	2026-03-07 15:02:53.944822
2111	87	43	1803595.0000	auto	2026-03-07 15:02:53.944822
2112	87	44	124263.0000	auto	2026-03-07 15:02:53.944822
2113	87	46	156315.0000	auto	2026-03-07 15:02:53.944822
2114	87	49	4653.0000	auto	2026-03-07 15:02:53.944822
2115	87	50	360453.0000	auto	2026-03-07 15:02:53.944822
2116	87	48	18100000.0000	auto	2026-03-07 15:02:53.944822
2117	87	47	59041.0000	auto	2026-03-07 15:02:53.944822
2173	91	52	119129584.0000	auto	2026-03-07 15:02:57.464384
2174	91	53	482629306.0000	auto	2026-03-07 15:02:57.464384
2175	91	54	55499183.0000	auto	2026-03-07 15:02:57.464384
2176	91	60	41687.0000	auto	2026-03-07 15:02:57.464384
2177	91	55	102856277.0000	auto	2026-03-07 15:02:57.464384
2178	91	56	31453583.0000	auto	2026-03-07 15:02:57.464384
2179	91	57	220661316.2920	auto	2026-03-07 15:02:57.464384
2180	91	58	14860109.5800	auto	2026-03-07 15:02:57.464384
2181	91	59	1095858.0000	auto	2026-03-07 15:02:57.464384
2182	91	16	21981945.0000	auto	2026-03-07 15:02:57.464384
2183	91	39	16983303.0000	auto	2026-03-07 15:02:57.464384
2184	91	43	1556824.0000	auto	2026-03-07 15:02:57.464384
2185	91	44	134263.0000	auto	2026-03-07 15:02:57.464384
2186	91	46	166315.0000	auto	2026-03-07 15:02:57.464384
2217	93	59	1101315.0000	auto	2026-03-07 15:02:59.157342
2218	93	16	26362259.0000	auto	2026-03-07 15:02:59.157342
2219	93	39	18983303.0000	auto	2026-03-07 15:02:59.157342
2220	93	43	786111.0000	auto	2026-03-07 15:02:59.157342
2221	93	44	134263.0000	auto	2026-03-07 15:02:59.157342
2222	93	46	176315.0000	auto	2026-03-07 15:02:59.157342
2223	93	49	28657.0000	auto	2026-03-07 15:02:59.157342
2224	93	50	380453.0000	auto	2026-03-07 15:02:59.157342
2225	93	48	18300000.0000	auto	2026-03-07 15:02:59.157342
2226	93	47	79041.0000	auto	2026-03-07 15:02:59.157342
2227	94	52	116745644.0000	auto	2026-03-07 15:03:00.001089
2228	94	53	471338163.0000	auto	2026-03-07 15:03:00.001089
2229	94	54	53514113.0000	auto	2026-03-07 15:03:00.001089
2230	94	60	42280.0000	auto	2026-03-07 15:03:00.001089
2231	94	55	103531266.0000	auto	2026-03-07 15:03:00.001089
2232	94	56	35762345.0000	auto	2026-03-07 15:03:00.001089
2233	94	57	209493571.4800	auto	2026-03-07 15:03:00.001089
2234	94	58	14955132.4800	auto	2026-03-07 15:03:00.001089
2235	94	59	1119040.0000	auto	2026-03-07 15:03:00.001089
2236	94	16	25372293.0000	auto	2026-03-07 15:03:00.001089
2237	94	39	18800585.0000	auto	2026-03-07 15:03:00.001089
2238	94	43	834535.0000	auto	2026-03-07 15:03:00.001089
2239	94	44	134294.0000	auto	2026-03-07 15:03:00.001089
2240	94	46	176354.0000	auto	2026-03-07 15:03:00.001089
2241	94	49	28662.0000	auto	2026-03-07 15:03:00.001089
2242	94	50	380606.0000	auto	2026-03-07 15:03:00.001089
2243	94	48	18300000.0000	auto	2026-03-07 15:03:00.001089
2244	94	47	79056.0000	auto	2026-03-07 15:03:00.001089
2245	95	52	117616684.0000	auto	2026-03-07 15:03:00.84477
2246	95	53	470608233.0000	auto	2026-03-07 15:03:00.84477
2247	95	54	53315073.0000	auto	2026-03-07 15:03:00.84477
2248	95	60	41474.0000	auto	2026-03-07 15:03:00.84477
2249	95	55	103146923.0000	auto	2026-03-07 15:03:00.84477
2250	95	56	38085010.0000	auto	2026-03-07 15:03:00.84477
2251	95	57	219718490.0000	auto	2026-03-07 15:03:00.84477
2252	95	58	14847585.0000	auto	2026-03-07 15:03:00.84477
2253	95	59	1135183.0000	auto	2026-03-07 15:03:00.84477
2254	95	16	20381190.0000	auto	2026-03-07 15:03:00.84477
2255	95	39	18800585.0000	auto	2026-03-07 15:03:00.84477
2256	95	43	508877.0000	auto	2026-03-07 15:03:00.84477
2257	95	44	134294.0000	auto	2026-03-07 15:03:00.84477
2258	95	46	176354.0000	auto	2026-03-07 15:03:00.84477
2259	95	49	23862.0000	auto	2026-03-07 15:03:00.84477
2260	95	50	380606.0000	auto	2026-03-07 15:03:00.84477
2261	95	47	79056.0000	auto	2026-03-07 15:03:00.84477
2262	96	52	116643204.0000	auto	2026-03-07 15:03:01.676938
2263	96	53	469019343.0000	auto	2026-03-07 15:03:01.676938
2264	96	54	73022453.0000	auto	2026-03-07 15:03:01.676938
2265	96	60	41624.0000	auto	2026-03-07 15:03:01.676938
2266	96	55	100817987.5650	auto	2026-03-07 15:03:01.676938
2267	96	56	37497225.0000	auto	2026-03-07 15:03:01.676938
2268	96	57	205603846.8850	auto	2026-03-07 15:03:01.676938
2269	96	58	14610719.7950	auto	2026-03-07 15:03:01.676938
2270	96	59	1102119.3200	auto	2026-03-07 15:03:01.676938
2271	96	16	3375.0000	auto	2026-03-07 15:03:01.676938
2272	96	39	18800585.0000	auto	2026-03-07 15:03:01.676938
2273	96	43	428877.0000	auto	2026-03-07 15:03:01.676938
2274	96	44	134294.0000	auto	2026-03-07 15:03:01.676938
2275	96	46	176354.0000	auto	2026-03-07 15:03:01.676938
2276	96	49	53878.0000	auto	2026-03-07 15:03:01.676938
2277	96	50	380606.0000	auto	2026-03-07 15:03:01.676938
2278	96	47	79056.0000	auto	2026-03-07 15:03:01.676938
2279	96	48	18300000.0000	auto	2026-03-07 15:03:01.676938
2280	97	52	119763210.0000	auto	2026-03-07 15:03:02.552711
2281	97	53	487337704.0000	auto	2026-03-07 15:03:02.552711
2282	97	54	73967264.0000	auto	2026-03-07 15:03:02.552711
2283	97	60	38612.0000	auto	2026-03-07 15:03:02.552711
2284	97	55	81606655.0180	auto	2026-03-07 15:03:02.552711
2285	97	56	37861790.0000	auto	2026-03-07 15:03:02.552711
2286	97	57	210916433.4700	auto	2026-03-07 15:03:02.552711
2287	97	58	14958322.1620	auto	2026-03-07 15:03:02.552711
2288	97	59	1145209.9040	auto	2026-03-07 15:03:02.552711
2289	97	16	2928147.0000	auto	2026-03-07 15:03:02.552711
2290	97	38	25.0000	auto	2026-03-07 15:03:02.552711
2291	97	39	20800585.0000	auto	2026-03-07 15:03:02.552711
2292	97	43	7008877.0000	auto	2026-03-07 15:03:02.552711
2293	97	44	134294.0000	auto	2026-03-07 15:03:02.552711
2294	97	46	186354.0000	auto	2026-03-07 15:03:02.552711
2295	97	49	53891.0000	auto	2026-03-07 15:03:02.552711
2296	97	50	390606.0000	auto	2026-03-07 15:03:02.552711
2297	97	47	89056.0000	auto	2026-03-07 15:03:02.552711
2298	97	48	18400000.0000	auto	2026-03-07 15:03:02.552711
2299	98	52	120948476.0000	auto	2026-03-07 15:03:03.412491
2300	98	53	490020109.0000	auto	2026-03-07 15:03:03.412491
2301	98	54	75256414.0000	auto	2026-03-07 15:03:03.412491
2302	98	60	40367.0000	auto	2026-03-07 15:03:03.412491
2303	98	55	82463056.5330	auto	2026-03-07 15:03:03.412491
2304	98	56	39378895.0000	auto	2026-03-07 15:03:03.412491
2305	98	57	209258838.6950	auto	2026-03-07 15:03:03.412491
2306	98	58	15396721.6960	auto	2026-03-07 15:03:03.412491
2307	98	59	1187822.8240	auto	2026-03-07 15:03:03.412491
2308	98	16	8931026.0000	auto	2026-03-07 15:03:03.412491
2309	98	38	10025.0000	auto	2026-03-07 15:03:03.412491
2310	98	39	20268640.0000	auto	2026-03-07 15:03:03.412491
2311	98	43	454250.0000	auto	2026-03-07 15:03:03.412491
2312	98	44	134294.0000	auto	2026-03-07 15:03:03.412491
2313	98	46	186354.0000	auto	2026-03-07 15:03:03.412491
2314	98	49	75391.0000	auto	2026-03-07 15:03:03.412491
2315	98	50	390606.0000	auto	2026-03-07 15:03:03.412491
2316	98	47	89056.0000	auto	2026-03-07 15:03:03.412491
2317	98	48	18400000.0000	auto	2026-03-07 15:03:03.412491
2318	99	52	119051737.0000	auto	2026-03-07 15:03:04.276421
2319	99	53	480954459.0000	auto	2026-03-07 15:03:04.276421
2320	99	54	73876814.0000	auto	2026-03-07 15:03:04.276421
2321	99	60	40089.0000	auto	2026-03-07 15:03:04.276421
2322	99	55	82098557.2140	auto	2026-03-07 15:03:04.276421
2323	99	56	42147295.0000	auto	2026-03-07 15:03:04.276421
2324	99	57	207901749.8100	auto	2026-03-07 15:03:04.276421
2325	99	58	15291853.9680	auto	2026-03-07 15:03:04.276421
2326	99	59	1189702.1920	auto	2026-03-07 15:03:04.276421
2327	99	16	8934467.0000	auto	2026-03-07 15:03:04.276421
2328	99	38	10027.0000	auto	2026-03-07 15:03:04.276421
2329	99	39	20268640.0000	auto	2026-03-07 15:03:04.276421
2330	99	43	477700.0000	auto	2026-03-07 15:03:04.276421
2331	99	44	134294.0000	auto	2026-03-07 15:03:04.276421
2332	99	46	186354.0000	auto	2026-03-07 15:03:04.276421
2333	99	49	75391.0000	auto	2026-03-07 15:03:04.276421
2334	99	50	390606.0000	auto	2026-03-07 15:03:04.276421
2335	99	47	89056.0000	auto	2026-03-07 15:03:04.276421
2336	99	48	18400000.0000	auto	2026-03-07 15:03:04.276421
2337	100	52	118113168.0000	auto	2026-03-07 15:03:05.150069
2338	100	53	473308414.0000	auto	2026-03-07 15:03:05.150069
2339	100	54	74343464.0000	auto	2026-03-07 15:03:05.150069
2340	100	60	39253.0000	auto	2026-03-07 15:03:05.150069
2341	100	55	80274216.4450	auto	2026-03-07 15:03:05.150069
2342	100	56	45558590.0000	auto	2026-03-07 15:03:05.150069
2343	100	57	201841221.1750	auto	2026-03-07 15:03:05.150069
2344	100	58	14832841.5550	auto	2026-03-07 15:03:05.150069
2345	100	59	1157779.9600	auto	2026-03-07 15:03:05.150069
2346	100	16	8937827.0000	auto	2026-03-07 15:03:05.150069
2347	100	38	10032.0000	auto	2026-03-07 15:03:05.150069
2348	100	39	20268640.0000	auto	2026-03-07 15:03:05.150069
2349	100	43	284591.0000	auto	2026-03-07 15:03:05.150069
2350	100	44	134294.0000	auto	2026-03-07 15:03:05.150069
2351	100	46	186354.0000	auto	2026-03-07 15:03:05.150069
2352	100	49	12391.0000	auto	2026-03-07 15:03:05.150069
2353	100	50	390606.0000	auto	2026-03-07 15:03:05.150069
2354	100	47	89056.0000	auto	2026-03-07 15:03:05.150069
2355	100	48	18400000.0000	auto	2026-03-07 15:03:05.150069
2356	101	52	115015984.0000	auto	2026-03-07 15:03:06.053145
2357	101	53	456947619.0000	auto	2026-03-07 15:03:06.053145
2358	101	54	69301664.0000	auto	2026-03-07 15:03:06.053145
2359	101	60	38967.0000	auto	2026-03-07 15:03:06.053145
2360	101	55	82038632.6100	auto	2026-03-07 15:03:06.053145
2361	101	56	41684695.0000	auto	2026-03-07 15:03:06.053145
2362	101	57	189216442.2600	auto	2026-03-07 15:03:06.053145
2363	101	58	15356557.8200	auto	2026-03-07 15:03:06.053145
2364	101	59	1118015.0800	auto	2026-03-07 15:03:06.053145
2365	101	16	8941192.0000	auto	2026-03-07 15:03:06.053145
2366	101	38	10036.0000	auto	2026-03-07 15:03:06.053145
2367	101	39	19284363.0000	auto	2026-03-07 15:03:06.053145
2368	101	43	964791.0000	auto	2026-03-07 15:03:06.053145
2369	101	44	134294.0000	auto	2026-03-07 15:03:06.053145
2370	101	46	186354.0000	auto	2026-03-07 15:03:06.053145
2371	101	49	12423.0000	auto	2026-03-07 15:03:06.053145
2372	101	50	390606.0000	auto	2026-03-07 15:03:06.053145
2373	101	47	89056.0000	auto	2026-03-07 15:03:06.053145
2374	101	48	18400000.0000	auto	2026-03-07 15:03:06.053145
2375	102	52	113716880.0000	auto	2026-03-07 15:03:06.920604
2376	102	53	448436578.0000	auto	2026-03-07 15:03:06.920604
2377	102	54	66637414.0000	auto	2026-03-07 15:03:06.920604
2378	102	60	39323.0000	auto	2026-03-07 15:03:06.920604
2379	102	55	79818432.1620	auto	2026-03-07 15:03:06.920604
2380	102	56	41842295.0000	auto	2026-03-07 15:03:06.920604
2381	102	57	178452425.0000	auto	2026-03-07 15:03:06.920604
2382	102	58	15631736.0000	auto	2026-03-07 15:03:06.920604
2383	102	59	1106147.0000	auto	2026-03-07 15:03:06.920604
2384	102	16	9694718.0000	auto	2026-03-07 15:03:06.920604
2385	102	38	1420300.0000	auto	2026-03-07 15:03:06.920604
2386	102	39	21284363.0000	auto	2026-03-07 15:03:06.920604
2387	102	43	3215962.0000	auto	2026-03-07 15:03:06.920604
2388	102	44	134294.0000	auto	2026-03-07 15:03:06.920604
2389	102	46	196354.0000	auto	2026-03-07 15:03:06.920604
2390	102	49	12423.0000	auto	2026-03-07 15:03:06.920604
2391	102	50	400606.0000	auto	2026-03-07 15:03:06.920604
2392	102	47	99056.0000	auto	2026-03-07 15:03:06.920604
2393	102	48	18500000.0000	auto	2026-03-07 15:03:06.920604
2394	103	52	114407883.0000	auto	2026-03-07 15:03:07.810205
2395	103	53	453324483.0000	auto	2026-03-07 15:03:07.810205
2396	103	54	67396464.0000	auto	2026-03-07 15:03:07.810205
2397	103	60	39382.0000	auto	2026-03-07 15:03:07.810205
2398	103	55	81131638.1020	auto	2026-03-07 15:03:07.810205
2399	103	56	42383485.0000	auto	2026-03-07 15:03:07.810205
2400	103	57	187175352.0000	auto	2026-03-07 15:03:07.810205
2401	103	58	15755636.5060	auto	2026-03-07 15:03:07.810205
2402	103	59	1143292.0000	auto	2026-03-07 15:03:07.810205
2403	103	16	9698337.0000	auto	2026-03-07 15:03:07.810205
2404	103	38	1421000.0000	auto	2026-03-07 15:03:07.810205
2405	103	39	20909032.0000	auto	2026-03-07 15:03:07.810205
2406	103	43	3229172.0000	auto	2026-03-07 15:03:07.810205
2407	103	44	134294.0000	auto	2026-03-07 15:03:07.810205
2408	103	46	196354.0000	auto	2026-03-07 15:03:07.810205
2409	103	49	12423.0000	auto	2026-03-07 15:03:07.810205
2410	103	50	400606.0000	auto	2026-03-07 15:03:07.810205
2411	103	47	99056.0000	auto	2026-03-07 15:03:07.810205
2412	103	48	18500000.0000	auto	2026-03-07 15:03:07.810205
2413	104	52	114220379.0000	auto	2026-03-07 15:03:08.648725
2414	104	53	451269442.0000	auto	2026-03-07 15:03:08.648725
2415	104	54	67486414.0000	auto	2026-03-07 15:03:08.648725
2416	104	60	43013.0000	auto	2026-03-07 15:03:08.648725
2417	104	55	79295406.8000	auto	2026-03-07 15:03:08.648725
2418	104	56	43564365.0000	auto	2026-03-07 15:03:08.648725
2419	104	57	176159372.0000	auto	2026-03-07 15:03:08.648725
2420	104	58	15584490.8000	auto	2026-03-07 15:03:08.648725
2421	104	59	1096865.0000	auto	2026-03-07 15:03:08.648725
2422	104	16	9471886.0000	auto	2026-03-07 15:03:08.648725
2423	104	38	1421525.0000	auto	2026-03-07 15:03:08.648725
2424	104	39	20909032.0000	auto	2026-03-07 15:03:08.648725
2425	104	43	2933513.0000	auto	2026-03-07 15:03:08.648725
2426	104	44	134294.0000	auto	2026-03-07 15:03:08.648725
2427	104	46	196354.0000	auto	2026-03-07 15:03:08.648725
2428	104	49	12423.0000	auto	2026-03-07 15:03:08.648725
2429	104	50	400606.0000	auto	2026-03-07 15:03:08.648725
2430	104	47	99056.0000	auto	2026-03-07 15:03:08.648725
2431	104	48	18500000.0000	auto	2026-03-07 15:03:08.648725
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
40	1	40	20124.0000	manual	2026-03-07 07:59:56.749208
41	1	41	18340.0000	manual	2026-03-07 07:59:56.749208
42	1	42	133.0000	manual	2026-03-07 07:59:56.749208
50	1	51	0.0000	manual	2026-03-07 07:59:56.749208
2472	1	52	116716336.0000	auto	2026-03-07 15:03:09.209118
2473	1	53	468720024.0000	auto	2026-03-07 15:03:09.209118
2474	1	54	71377564.0000	auto	2026-03-07 15:03:09.209118
2475	1	60	38597.0000	auto	2026-03-07 15:03:09.209118
2476	1	55	79886167.5520	auto	2026-03-07 15:03:09.209118
2477	1	56	44009290.0000	auto	2026-03-07 15:03:09.209118
2478	1	57	185202071.0560	auto	2026-03-07 15:03:09.209118
2479	1	58	15633114.4000	auto	2026-03-07 15:03:09.209118
2480	1	59	1122685.0000	auto	2026-03-07 15:03:09.209118
17	1	16	9475410.0000	manual	2026-03-07 07:59:56.749208
38	1	38	1422138.0000	manual	2026-03-07 07:59:56.749208
39	1	39	20909032.0000	manual	2026-03-07 07:59:56.749208
43	1	43	2933513.0000	manual	2026-03-07 07:59:56.749208
44	1	44	134294.0000	manual	2026-03-07 07:59:56.749208
45	1	46	196354.0000	manual	2026-03-07 07:59:56.749208
47	1	49	12432.0000	manual	2026-03-07 07:59:56.749208
49	1	50	400606.0000	manual	2026-03-07 07:59:56.749208
46	1	47	99056.0000	manual	2026-03-07 07:59:56.749208
48	1	48	18500000.0000	manual	2026-03-07 07:59:56.749208
\.


--
-- Data for Name: weekly_snapshots; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.weekly_snapshots (weekly_snapshot_id, user_id, reference_date, source_snapshot_id, status, editable_until, created_at) FROM stdin;
1	1	2026-03-07	7	in_progress	2026-03-14 00:00:00	2026-03-07 07:59:56.748099
2	1	2024-03-09	13	in_progress	\N	2026-03-07 14:59:04.67023
3	1	2024-03-16	14	in_progress	\N	2026-03-07 14:59:08.027375
4	1	2024-03-23	15	in_progress	\N	2026-03-07 14:59:11.618108
5	1	2024-03-30	16	in_progress	\N	2026-03-07 14:59:15.328636
6	1	2024-04-06	17	in_progress	\N	2026-03-07 14:59:18.787886
7	1	2024-04-13	18	in_progress	\N	2026-03-07 14:59:21.086315
8	1	2024-04-20	19	in_progress	\N	2026-03-07 14:59:24.696547
9	1	2024-04-27	20	in_progress	\N	2026-03-07 14:59:28.156591
10	1	2024-05-04	21	in_progress	\N	2026-03-07 14:59:31.554451
11	1	2024-05-11	22	in_progress	\N	2026-03-07 14:59:35.338548
12	1	2024-05-18	23	in_progress	\N	2026-03-07 14:59:38.771782
13	1	2024-05-25	24	in_progress	\N	2026-03-07 14:59:42.29198
14	1	2024-06-01	25	in_progress	\N	2026-03-07 14:59:45.633543
15	1	2024-06-08	26	in_progress	\N	2026-03-07 14:59:49.011871
16	1	2024-06-15	27	in_progress	\N	2026-03-07 14:59:51.302692
17	1	2024-06-22	28	in_progress	\N	2026-03-07 14:59:54.721093
18	1	2024-06-29	29	in_progress	\N	2026-03-07 14:59:58.064144
19	1	2024-07-06	30	in_progress	\N	2026-03-07 15:00:01.460961
20	1	2024-07-13	31	in_progress	\N	2026-03-07 15:00:04.87829
21	1	2024-07-20	32	in_progress	\N	2026-03-07 15:00:08.24887
22	1	2024-07-27	33	in_progress	\N	2026-03-07 15:00:11.643127
23	1	2024-08-03	34	in_progress	\N	2026-03-07 15:00:14.774711
24	1	2024-08-10	35	in_progress	\N	2026-03-07 15:00:18.160902
25	1	2024-08-17	36	in_progress	\N	2026-03-07 15:00:20.487438
26	1	2024-08-24	37	in_progress	\N	2026-03-07 15:00:23.702666
27	1	2024-08-31	38	in_progress	\N	2026-03-07 15:00:27.066515
28	1	2024-09-07	39	in_progress	\N	2026-03-07 15:00:30.179468
29	1	2024-09-14	40	in_progress	\N	2026-03-07 15:00:33.336187
30	1	2024-09-21	41	in_progress	\N	2026-03-07 15:00:36.565154
31	1	2024-09-28	42	in_progress	\N	2026-03-07 15:00:39.999181
32	1	2024-10-05	43	in_progress	\N	2026-03-07 15:00:43.264663
33	1	2024-10-12	44	in_progress	\N	2026-03-07 15:02:09.509878
34	1	2024-10-19	45	in_progress	\N	2026-03-07 15:02:10.373859
35	1	2024-10-26	46	in_progress	\N	2026-03-07 15:02:11.218685
36	1	2024-11-02	47	in_progress	\N	2026-03-07 15:02:12.059502
37	1	2024-11-09	48	in_progress	\N	2026-03-07 15:02:12.920985
38	1	2024-11-16	49	in_progress	\N	2026-03-07 15:02:13.793358
39	1	2024-11-23	50	in_progress	\N	2026-03-07 15:02:14.680839
40	1	2024-11-30	51	in_progress	\N	2026-03-07 15:02:14.535355
41	1	2024-12-07	52	in_progress	\N	2026-03-07 15:02:15.481584
42	1	2024-12-14	53	in_progress	\N	2026-03-07 15:02:16.313076
43	1	2024-12-21	54	in_progress	\N	2026-03-07 15:02:17.18501
44	1	2024-12-28	55	in_progress	\N	2026-03-07 15:02:18.025089
45	1	2025-01-04	56	in_progress	\N	2026-03-07 15:02:18.892389
46	1	2025-01-11	57	in_progress	\N	2026-03-07 15:02:19.749899
47	1	2025-01-18	58	in_progress	\N	2026-03-07 15:02:20.601454
48	1	2025-01-25	59	in_progress	\N	2026-03-07 15:02:21.477777
49	1	2025-02-01	60	in_progress	\N	2026-03-07 15:02:22.334154
50	1	2025-02-08	61	in_progress	\N	2026-03-07 15:02:23.214074
51	1	2025-02-15	62	in_progress	\N	2026-03-07 15:02:24.057775
52	1	2025-02-22	63	in_progress	\N	2026-03-07 15:02:24.937001
53	1	2025-03-01	64	in_progress	\N	2026-03-07 15:02:25.790774
54	1	2025-03-08	65	in_progress	\N	2026-03-07 15:02:26.665052
55	1	2025-03-15	66	in_progress	\N	2026-03-07 15:02:27.543288
56	1	2025-03-22	67	in_progress	\N	2026-03-07 15:02:28.38153
57	1	2025-03-29	68	in_progress	\N	2026-03-07 15:02:29.233217
58	1	2025-04-05	69	in_progress	\N	2026-03-07 15:02:30.09888
59	1	2025-04-12	70	in_progress	\N	2026-03-07 15:02:30.946173
60	1	2025-04-19	71	in_progress	\N	2026-03-07 15:02:31.789376
61	1	2025-04-26	72	in_progress	\N	2026-03-07 15:02:32.670073
62	1	2025-05-03	73	in_progress	\N	2026-03-07 15:02:33.542965
63	1	2025-05-10	74	in_progress	\N	2026-03-07 15:02:34.398228
64	1	2025-05-17	75	in_progress	\N	2026-03-07 15:02:35.269215
65	1	2025-05-24	76	in_progress	\N	2026-03-07 15:02:36.089893
66	1	2025-05-31	77	in_progress	\N	2026-03-07 15:02:36.942384
67	1	2025-06-07	78	in_progress	\N	2026-03-07 15:02:37.807852
68	1	2025-06-14	79	in_progress	\N	2026-03-07 15:02:38.650386
69	1	2025-06-21	80	in_progress	\N	2026-03-07 15:02:39.46621
70	1	2025-06-28	81	in_progress	\N	2026-03-07 15:02:40.330873
71	1	2025-07-05	82	in_progress	\N	2026-03-07 15:02:41.217354
72	1	2025-07-12	83	in_progress	\N	2026-03-07 15:02:42.059199
73	1	2025-07-19	84	in_progress	\N	2026-03-07 15:02:42.914074
74	1	2025-07-26	85	in_progress	\N	2026-03-07 15:02:43.744953
75	1	2025-08-02	86	in_progress	\N	2026-03-07 15:02:43.51404
76	1	2025-08-09	87	in_progress	\N	2026-03-07 15:02:44.397706
77	1	2025-08-16	88	in_progress	\N	2026-03-07 15:02:45.220943
78	1	2025-08-23	89	in_progress	\N	2026-03-07 15:02:46.056846
79	1	2025-08-30	90	in_progress	\N	2026-03-07 15:02:46.948662
80	1	2025-09-13	91	in_progress	\N	2026-03-07 15:02:47.820388
81	1	2025-09-20	92	in_progress	\N	2026-03-07 15:02:48.734811
82	1	2025-09-27	93	in_progress	\N	2026-03-07 15:02:49.580181
83	1	2025-10-04	94	in_progress	\N	2026-03-07 15:02:50.405453
84	1	2025-10-11	95	in_progress	\N	2026-03-07 15:02:51.293058
85	1	2025-10-18	96	in_progress	\N	2026-03-07 15:02:52.151299
86	1	2025-10-25	97	in_progress	\N	2026-03-07 15:02:52.968126
87	1	2025-11-01	98	in_progress	\N	2026-03-07 15:02:53.812337
88	1	2025-11-08	99	in_progress	\N	2026-03-07 15:02:54.66142
89	1	2025-11-15	100	in_progress	\N	2026-03-07 15:02:55.601379
90	1	2025-11-22	101	in_progress	\N	2026-03-07 15:02:56.464792
91	1	2025-11-29	102	in_progress	\N	2026-03-07 15:02:57.325406
92	1	2025-12-06	103	in_progress	\N	2026-03-07 15:02:58.183938
93	1	2025-12-13	104	in_progress	\N	2026-03-07 15:02:59.016019
94	1	2025-12-20	105	in_progress	\N	2026-03-07 15:02:59.853188
95	1	2025-12-27	106	in_progress	\N	2026-03-07 15:03:00.721135
96	1	2026-01-03	107	in_progress	\N	2026-03-07 15:03:01.54067
97	1	2026-01-10	108	in_progress	\N	2026-03-07 15:03:02.408725
98	1	2026-01-17	109	in_progress	\N	2026-03-07 15:03:03.26118
99	1	2026-01-24	110	in_progress	\N	2026-03-07 15:03:04.136847
100	1	2026-01-31	111	in_progress	\N	2026-03-07 15:03:04.99246
101	1	2026-02-07	112	in_progress	\N	2026-03-07 15:03:05.909381
102	1	2026-02-14	113	in_progress	\N	2026-03-07 15:03:06.77611
103	1	2026-02-21	114	in_progress	\N	2026-03-07 15:03:07.652158
104	1	2026-02-28	115	in_progress	\N	2026-03-07 15:03:08.499434
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

SELECT pg_catalog.setval('public.annual_snapshot_holdings_annual_snapshot_holding_id_seq', 89, true);


--
-- Name: annual_snapshots_annual_snapshot_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.annual_snapshots_annual_snapshot_id_seq', 5, true);


--
-- Name: holdings_holding_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.holdings_holding_id_seq', 62, true);


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

SELECT pg_catalog.setval('public.snapshot_holdings_snapshot_holding_id_seq', 2658, true);


--
-- Name: snapshots_snapshot_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.snapshots_snapshot_id_seq', 120, true);


--
-- Name: target_allocation_accounts_target_allocation_account_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.target_allocation_accounts_target_allocation_account_id_seq', 21, true);


--
-- Name: target_allocation_asset_class_target_allocation_asset_class_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.target_allocation_asset_class_target_allocation_asset_class_seq', 6, true);


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

SELECT pg_catalog.setval('public.weekly_snapshot_holdings_weekly_snapshot_holding_id_seq', 2490, true);


--
-- Name: weekly_snapshots_weekly_snapshot_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.weekly_snapshots_weekly_snapshot_id_seq', 104, true);


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
-- Name: target_allocation_asset_classes target_allocation_asset_classes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.target_allocation_asset_classes
    ADD CONSTRAINT target_allocation_asset_classes_pkey PRIMARY KEY (target_allocation_asset_class_id);


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

\unrestrict 6mZHKf6oKaKfXz3TYhmhfdVlM4gIrsdu17B4zWbuft3PlOitfosd9yTyDZ9BS0N

