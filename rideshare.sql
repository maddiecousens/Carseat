--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.4
-- Dumped by pg_dump version 9.5.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'LATIN1';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: requests; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE requests (
    id integer NOT NULL,
    ride_id integer NOT NULL,
    requester integer NOT NULL,
    seats integer NOT NULL
);


ALTER TABLE requests OWNER TO vagrant;

--
-- Name: requests_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE requests_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE requests_id_seq OWNER TO vagrant;

--
-- Name: requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE requests_id_seq OWNED BY requests.id;


--
-- Name: riders; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE riders (
    id integer NOT NULL,
    ride_id integer NOT NULL,
    user_id integer NOT NULL,
    seats integer NOT NULL
);


ALTER TABLE riders OWNER TO vagrant;

--
-- Name: riders_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE riders_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE riders_id_seq OWNER TO vagrant;

--
-- Name: riders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE riders_id_seq OWNED BY riders.id;


--
-- Name: rides; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE rides (
    ride_id integer NOT NULL,
    driver integer NOT NULL,
    seats integer NOT NULL,
    cost integer NOT NULL,
    start_lat real NOT NULL,
    start_lng real NOT NULL,
    start_name character varying(200),
    start_number character varying(50),
    start_street character varying(100),
    start_city character varying(50) NOT NULL,
    start_state character varying(15) NOT NULL,
    start_zip character varying(10),
    end_lat real NOT NULL,
    end_lng real NOT NULL,
    end_name character varying(200),
    end_number character varying(50),
    end_street character varying(100),
    end_city character varying(50) NOT NULL,
    end_state character varying(15) NOT NULL,
    end_zip character varying(10),
    start_timestamp timestamp without time zone NOT NULL,
    end_timestamp timestamp without time zone NOT NULL,
    mileage character varying(10),
    duration character varying(100),
    luggage character varying(50),
    comments text,
    pickup_window character varying(50),
    detour character varying(50),
    car_type character varying(100)
);


ALTER TABLE rides OWNER TO vagrant;

--
-- Name: rides_ride_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE rides_ride_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE rides_ride_id_seq OWNER TO vagrant;

--
-- Name: rides_ride_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE rides_ride_id_seq OWNED BY rides.ride_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE users (
    user_id integer NOT NULL,
    fb_userid character varying(20) NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    age integer,
    photo character varying(300),
    email character varying(64),
    password character varying(64),
    member_since timestamp without time zone,
    image character varying(200)
);


ALTER TABLE users OWNER TO vagrant;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_user_id_seq OWNER TO vagrant;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE users_user_id_seq OWNED BY users.user_id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY requests ALTER COLUMN id SET DEFAULT nextval('requests_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY riders ALTER COLUMN id SET DEFAULT nextval('riders_id_seq'::regclass);


--
-- Name: ride_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY rides ALTER COLUMN ride_id SET DEFAULT nextval('rides_ride_id_seq'::regclass);


--
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY users ALTER COLUMN user_id SET DEFAULT nextval('users_user_id_seq'::regclass);


--
-- Data for Name: requests; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY requests (id, ride_id, requester, seats) FROM stdin;
3	5	1	3
4	16	1	3
\.


--
-- Name: requests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('requests_id_seq', 4, true);


--
-- Data for Name: riders; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY riders (id, ride_id, user_id, seats) FROM stdin;
1	1	2	3
\.


--
-- Name: riders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('riders_id_seq', 1, true);


--
-- Data for Name: rides; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY rides (ride_id, driver, seats, cost, start_lat, start_lng, start_name, start_number, start_street, start_city, start_state, start_zip, end_lat, end_lng, end_name, end_number, end_street, end_city, end_state, end_zip, start_timestamp, end_timestamp, mileage, duration, luggage, comments, pickup_window, detour, car_type) FROM stdin;
2	2	5	15	38.9544716	-119.942627	\N	4005	Lake Tahoe Blvd	South Lake Tahoe	CA	96150	37.8973694	-122.30088	\N	427	San Pablo Ave	Albany	CA	94706	2016-11-21 18:15:00	2016-12-07 20:30:00	\N	\N	medium	Will be a short driver. Willing to stop for bathroom breaks	flexible	No	Honda
3	3	5	20	37.8973694	-122.30088	\N	427	San Pablo Ave	Albany	CA	94706	38.9544716	-119.942627	\N	4005	Lake Tahoe Blvd	South Lake Tahoe	CA	96150	2016-11-21 17:15:00	2016-11-21 20:30:00	\N	\N	large	Will be a short driver. Willing to stop for bathroom breaks	15 min	15 min	Honda
4	4	5	15	38.9544716	-119.942627	\N	4005	Lake Tahoe Blvd	South Lake Tahoe	CA	96150	37.8973694	-122.30088	\N	427	San Pablo Ave	Albany	CA	94706	2016-12-16 17:15:00	2016-12-16 20:30:00	178 mi	3 hours 6 mins	small	Will be a short driver. Willing to stop for bathroom breaks	30 min	30 min	Honda
5	5	5	15	37.8973694	-122.30088	\N	427	San Pablo Ave	Albany	CA	94706	38.9544716	-119.942627	\N	4005	Lake Tahoe Blvd	South Lake Tahoe	CA	96150	2016-11-22 19:15:00	2016-12-22 20:30:00	176 mi	3 hours 4 mins	small	Will be a short driver. Willing to stop for bathroom breaks	No	flexible	Honda
6	6	5	15	38.9544716	-119.942627	\N	4005	Lake Tahoe Blvd	South Lake Tahoe	CA	96150	37.8973694	-122.30088	\N	427	San Pablo Ave	Albany	CA	94706	2016-12-17 17:15:00	2016-12-17 20:30:00	178 mi	3 hours 6 mins	medium	Will be a short driver. Willing to stop for bathroom breaks	flexible	No	Honda
7	7	5	10	37.8973694	-122.30088	\N	427	San Pablo Ave	Albany	CA	94706	38.9544716	-119.942627	\N	4005	Lake Tahoe Blvd	South Lake Tahoe	CA	96150	2016-11-22 19:15:00	2016-11-22 22:15:00	176 mi	3 hours 4 mins	large	Will be a short driver. Willing to stop for bathroom breaks	15 min	15 min	Honda
8	1	5	15	38.9544716	-119.942627	\N	4005	Lake Tahoe Blvd	South Lake Tahoe	CA	96150	37.8973694	-122.30088	\N	427	San Pablo Ave	Albany	CA	94706	2016-12-19 17:15:00	2016-12-19 20:30:00	178 mi	3 hours 6 mins	small	Will be a short driver. Willing to stop for bathroom breaks	30 min	30 min	Honda
9	2	4	21	37.7896957	-122.411606	\N	883	Bush St	SF	CA	94108	33.9465637	-118.384064	\N	5855	W Century Blvd	Los Angeles	CA	90045	2016-12-25 10:15:00	2016-12-25 10:15:00	385 mi	5 hours 45 mins	small	I drive FAST	1 hour	No	Tesla
10	3	4	21	33.9465637	-118.384064	\N	5855	W Century Blvd	Los Angeles	CA	90045	37.7896957	-122.411606	\N	883	Bush St	SF	CA	94108	2016-12-26 10:15:00	2016-12-26 10:15:00	385 mi	5 hours 53 mins	medium	I drive FAST	2 hour	flexible	Tesla
11	4	4	21	37.7896957	-122.411606	\N	883	Bush St	SF	CA	94108	33.9465637	-118.384064	\N	5855	W Century Blvd	Los Angeles	CA	90045	2016-12-27 10:15:00	2016-12-27 10:15:00	385 mi	5 hours 45 mins	small	I drive FAST	1 hour	No	Tesla
12	5	4	21	33.9465637	-118.384064	\N	5855	W Century Blvd	Los Angeles	CA	90045	37.7896957	-122.411606	\N	883	Bush St	SF	CA	94108	2016-12-28 10:15:00	2016-12-28 10:15:00	385 mi	5 hours 53 mins	medium	I drive FAST	2 hour	flexible	Tesla
13	6	4	21	37.7896957	-122.411606	\N	883	Bush St	SF	CA	94108	33.9465637	-118.384064	\N	5855	W Century Blvd	Los Angeles	CA	90045	2016-12-29 10:15:00	2016-12-29 10:15:00	385 mi	5 hours 45 mins	small	I drive FAST	1 hour	No	Tesla
14	7	4	21	33.9465637	-118.384064	\N	5855	W Century Blvd	Los Angeles	CA	90045	37.7896957	-122.411606	\N	883	Bush St	SF	CA	94108	2016-12-30 10:15:00	2016-12-30 10:15:00	385 mi	5 hours 53 mins	medium	I drive FAST	2 hour	flexible	Tesla
15	1	4	13	38.9265137	-77.0145721	\N	167-241	Michigan Ave NW	Washington	DC	20010	40.7127991	-74.0058975	\N	\N	\N	New York	NY	10007	2016-12-15 15:15:00	2016-12-15 18:15:00	224 mi	3 hours 45 mins	small	Lololol I'm a dog!	flexible	15 min	Audi
16	2	4	14	40.7127991	-74.0058975	\N	\N	\N	New York	NY	10007	38.9265137	-77.0145721	\N	167-241	Michigan Ave NW	Washington	DC	20010	2016-12-16 16:15:00	2016-12-16 19:15:00	225 mi	3 hours 46 mins	medium	Lololol I'm a dog!	15 min	30 min	Audi
17	3	4	15	38.9265137	-77.0145721	\N	167-241	Michigan Ave NW	Washington	DC	20010	40.7127991	-74.0058975	\N	\N	\N	New York	NY	10007	2016-12-17 17:30:00	2016-12-17 17:30:00	224 mi	3 hours 45 mins	large	Lololol I'm a dog!	30 min	No	Audi
18	4	4	16	40.7127991	-74.0058975	\N	\N	\N	New York	NY	10007	38.9265137	-77.0145721	\N	167-241	Michigan Ave NW	Washington	DC	20010	2016-12-18 18:30:00	2016-12-18 18:30:00	225 mi	3 hours 46 mins	small	Lololol I'm a dog!	1 hour	flexible	Audi
19	5	4	17	38.9265137	-77.0145721	\N	167-241	Michigan Ave NW	Washington	DC	20010	42.3600998	-71.0588989	\N	\N	City Hall Plaza	Boston	MA	02203	2016-12-19 19:15:00	2016-12-20 00:15:00	437 mi	7 hours 4 mins	medium	Lololol I'm a dog!	2 hour	15 min	Audi
20	6	4	13	42.3600998	-71.0588989	\N	\N	City Hall Plaza	Boston	MA	02203	38.9265137	-77.0145721	\N	167-241	Michigan Ave NW	Washington	DC	20010	2016-12-20 21:15:00	2016-12-21 01:15:00	438 mi	7 hours 3 mins	large	Corgis CAN TO drive	flexible	30 min	Lexus
21	7	4	14	38.9265137	-77.0145721	\N	167-241	Michigan Ave NW	Washington	DC	20010	42.3600998	-71.0588989	\N	\N	City Hall Plaza	Boston	MA	02203	2016-12-21 22:15:00	2016-12-22 04:15:00	437 mi	7 hours 4 mins	small	Corgis CAN TO drive	15 min	No	Lexus
22	1	4	15	42.3600998	-71.0588989	\N	\N	City Hall Plaza	Boston	MA	02203	38.9265137	-77.0145721	\N	167-241	Michigan Ave NW	Washington	DC	20010	2016-12-22 23:30:00	2016-12-23 02:30:00	438 mi	7 hours 3 mins	medium	Corgis CAN TO drive	30 min	flexible	Lexus
23	2	4	16	38.9265137	-77.0145721	\N	167-241	Michigan Ave NW	Washington	DC	20010	40.7127991	-74.0058975	\N	\N	\N	New York	NY	10007	2016-12-24 00:30:00	2016-12-25 01:30:00	224 mi	3 hours 45 mins	large	Corgis CAN TO drive	1 hour	15 min	Lexus
24	3	4	17	38.9265137	-77.0145721	\N	167-241	Michigan Ave NW	Washington	DC	20010	40.7127991	-74.0058975	\N	\N	\N	New York	NY	10007	2016-12-25 01:30:00	2016-12-25 17:15:00	224 mi	3 hours 45 mins	small	Corgis CAN TO drive	2 hour	30 min	Lexus
25	4	4	13	43.5637016	-70.1999969	\N	211	Two Lights Rd	Cape Elizabeth	ME	04107	40.7127991	-74.0058975	\N	\N	\N	New York	NY	10007	2016-12-25 17:15:00	2016-12-26 18:45:00	320 mi	5 hours 20 mins	medium	My short legs make me an excellent driver	flexible	No	Jeep
26	5	4	14	40.7127991	-74.0058975	\N	\N	\N	New York	NY	10007	43.5637016	-70.1999969	\N	211	Two Lights Rd	Cape Elizabeth	ME	04107	2016-12-26 18:45:00	2016-12-27 19:45:00	319 mi	5 hours 15 mins	large	My short legs make me an excellent driver	15 min	flexible	Jeep
27	6	4	15	43.5637016	-70.1999969	\N	211	Two Lights Rd	Cape Elizabeth	ME	04107	40.7127991	-74.0058975	\N	\N	\N	New York	NY	10007	2016-12-27 19:45:00	2016-12-28 20:45:00	320 mi	5 hours 20 mins	small	My short legs make me an excellent driver	30 min	15 min	Jeep
28	7	4	16	40.7127991	-74.0058975	\N	\N	\N	New York	NY	10007	43.5637016	-70.1999969	\N	211	Two Lights Rd	Cape Elizabeth	ME	04107	2016-12-28 20:45:00	2016-12-29 15:15:00	319 mi	5 hours 15 mins	medium	My short legs make me an excellent driver	1 hour	30 min	Jeep
29	6	4	17	43.5637016	-70.1999969	\N	211	Two Lights Rd	Cape Elizabeth	ME	04107	40.7127991	-74.0058975	\N	\N	\N	New York	NY	10007	2016-12-29 15:15:00	2016-12-30 10:15:00	330 mi	5 hours 32 mins	large	My short legs make me an excellent driver	2 hour	No	Jeep
30	1	5	25	37.7748985	-122.419403	\N	10	S Van Ness Ave	SF	CA	94103	39.7428856	-104.944427	\N	1651	Garfield St	Denver	CO	80206	2016-12-25 10:15:00	2016-12-25 10:15:00	1,253 mi	18 hours 8 mins	small	Let's ride!	flexible	flexible	VW Van
31	2	5	25	39.7428856	-104.944427	\N	1651	Garfield St	Denver	CO	80206	37.7748985	-122.419403	\N	10	S Van Ness Ave	SF	CA	94103	2016-12-26 10:15:00	2016-12-26 10:15:00	1,255 mi	18 hours 17 mins	medium	Let's ride!	45 min	45 min	VW Van
32	3	5	25	37.7748985	-122.419403	\N	10	S Van Ness Ave	SF	CA	94103	39.7428856	-104.944427	\N	1651	Garfield St	Denver	CO	80206	2016-12-27 10:15:00	2016-12-27 10:15:00	1,253 mi	18 hours 8 mins	large	Let's ride!	60 min	60 min	VW Van
33	4	5	25	39.7428856	-104.944427	\N	1651	Garfield St	Denver	CO	80206	37.7748985	-122.419403	\N	10	S Van Ness Ave	SF	CA	94103	2016-12-28 10:15:00	2016-12-28 10:15:00	1,255 mi	18 hours 17 mins	small	Let's ride!	3 hour	No	VW Van
34	5	5	10	37.7748985	-122.419403	\N	10	S Van Ness Ave	SF	CA	94103	39.7428856	-104.944427	\N	1651	Garfield St	Denver	CO	80206	2016-12-29 10:15:00	2016-12-29 10:15:00	1,253 mi	18 hours 8 mins	medium	Let's ride!	4 hour	flexible	VW Van
35	6	5	10	39.7428856	-104.944427	\N	1651	Garfield St	Denver	CO	80206	37.7748985	-122.419403	\N	10	S Van Ness Ave	SF	CA	94103	2016-12-30 10:15:00	2016-12-30 10:15:00	1,255 mi	18 hours 17 mins	large	Let's ride!	flexible	75 min	VW Van
36	7	5	50	37.7748985	-122.419403	\N	10	S Van Ness Ave	SF	CA	94103	39.7428856	-104.944427	\N	1651	Garfield St	Denver	CO	80206	2016-12-15 15:15:00	2016-12-15 18:15:00	1,253 mi	18 hours 8 mins	small	Let's ride!	75 min	90 min	VW Van
37	1	5	50	39.7428856	-104.944427	\N	1651	Garfield St	Denver	CO	80206	37.7748985	-122.419403	\N	10	S Van Ness Ave	SF	CA	94103	2016-12-16 16:15:00	2016-12-16 19:15:00	1,255 mi	18 hours 17 mins	medium	Let's ride!	90 min	No	VW Van
38	2	5	10	37.7748985	-122.419403	\N	10	S Van Ness Ave	SF	CA	94103	39.7428856	-104.944427	\N	1651	Garfield St	Denver	CO	80206	2016-12-17 17:30:00	2016-12-17 17:30:00	1,253 mi	18 hours 8 mins	large	Let's ride!	5 hour	flexible	VW Van
39	3	5	20	39.7428856	-104.944427	\N	1651	Garfield St	Denver	CO	80206	37.7748985	-122.419403	\N	10	S Van Ness Ave	SF	CA	94103	2016-12-18 18:30:00	2016-12-18 18:30:00	1,255 mi	18 hours 17 mins	small	This will be fun	6 hour	105 min	VW Van
40	4	3	11	45.5231018	-122.676498	\N	17	NW 6th Ave	Portland	OR	97209	47.6062012	-122.3321	\N	\N	\N	Seattle	WA	98164	2016-12-19 19:15:00	2016-12-20 00:15:00	173 mi	2 hours 44 mins	medium	This will be fun	flexible	120 min	Junker
41	5	3	12	47.6062012	-122.3321	\N	\N	\N	Seattle	WA	98164	45.5231018	-122.676498	\N	17	NW 6th Ave	Portland	OR	97209	2016-12-20 21:15:00	2016-12-21 01:15:00	174 mi	2 hours 45 mins	large	This will be fun	105 min	No	Junker
42	6	3	13	45.5231018	-122.676498	\N	17	NW 6th Ave	Portland	OR	97209	47.6062012	-122.3321	\N	\N	\N	Seattle	WA	98164	2016-12-21 22:15:00	2016-12-22 04:15:00	173 mi	2 hours 44 mins	small	This will be fun	120 min	flexible	Junker
43	7	3	14	47.6062012	-122.3321	\N	\N	\N	Seattle	WA	98164	45.5231018	-122.676498	\N	17	NW 6th Ave	Portland	OR	97209	2016-12-22 23:30:00	2016-12-23 02:30:00	174 mi	2 hours 45 mins	medium	This will be fun	7 hour	135 min	Junker
44	1	3	15	45.5231018	-122.676498	\N	17	NW 6th Ave	Portland	OR	97209	47.6062012	-122.3321	\N	\N	\N	Seattle	WA	98164	2016-12-24 00:30:00	2016-12-25 01:30:00	173 mi	2 hours 44 mins	large	This will be fun	8 hour	150 min	Junker
45	2	3	16	47.6062012	-122.3321	\N	\N	\N	Seattle	WA	98164	45.5231018	-122.676498	\N	17	NW 6th Ave	Portland	OR	97209	2016-12-25 01:30:00	2016-12-25 17:15:00	174 mi	2 hours 45 mins	small	This will be fun	flexible	No	Junker
46	3	3	17	45.5231018	-122.676498	\N	17	NW 6th Ave	Portland	OR	97209	47.6062012	-122.3321	\N	\N	\N	Seattle	WA	98164	2016-12-25 17:15:00	2016-12-26 18:45:00	173 mi	2 hours 44 mins	medium	This will be fun	135 min	flexible	Junker
47	4	3	18	47.6062012	-122.3321	\N	\N	\N	Seattle	WA	98164	45.5231018	-122.676498	\N	17	NW 6th Ave	Portland	OR	97209	2016-12-26 18:45:00	2016-12-27 19:45:00	174 mi	2 hours 45 mins	large	This will be fun	150 min	165 min	Junker
48	5	3	19	45.5231018	-122.676498	\N	17	NW 6th Ave	Portland	OR	97209	47.6062012	-122.3321	\N	\N	\N	Seattle	WA	98164	2016-12-27 19:45:00	2016-12-28 20:45:00	173 mi	2 hours 44 mins	small	This will be fun	9 hour	180 min	Junker
49	6	3	20	47.6062012	-122.3321	\N	\N	\N	Seattle	WA	98164	45.5231018	-122.676498	\N	17	NW 6th Ave	Portland	OR	97209	2016-12-28 20:45:00	2016-12-29 15:15:00	174 mi	2 hours 45 mins	medium	This will be fun	10 hour	No	Junker
50	1	5	35	37.8973694	-122.30088	\N	427	San Pablo Ave	Albany	CA	94706	38.9544716	-119.942627	\N	4005	Lake Tahoe Blvd	South Lake Tahoe	CA	96150	2016-11-28 01:15:00	2016-11-27 18:30:00	176 mi	3 hours 4 mins	small	Will be a short driver. Willing to stop for bathroom breaks	No	flexible	Honda
51	2	4	13	37.7887459	-122.411583	\N	\N	\N	San Francisco	CA	94109	38.9399261	-119.977188	\N	\N	\N	South Lake Tahoe	CA	96150	2016-11-25 14:45:00	2016-11-25 14:45:00	187 mi	3 hours 18 mins	small	Hi	No	No	Junker
52	2	6	17	37.8715935	-122.272743	\N	\N	\N	Berkeley	CA	\N	39.2748413	-120.120605	\N	\N	\N	Truckee	CA	96161	2016-11-27 03:00:00	2016-11-27 03:00:00	185 mi	2 hours 57 mins	large	\N	No	No	Honda
53	2	4	17	37.8715935	-122.272743	\N	\N	\N	Berkeley	CA	\N	37.7622643	-122.404472	\N	\N	\N	San Francisco	CA	94107	2016-11-29 03:00:00	2016-11-29 03:00:00	13.2 mi	25 mins	small	Hi	No	No	Honda
1	1	2	15	37.8973694	-122.30088	\N	427	San Pablo Ave	Albany	CA	94706	38.9544716	-119.942627	\N	4005	Lake Tahoe Blvd	South Lake Tahoe	CA	96150	2016-11-21 17:15:00	2016-11-21 20:30:00	\N	\N	small	Will be a short driver. Willing to stop for bathroom breaks	No	flexible	Honda
\.


--
-- Name: rides_ride_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('rides_ride_id_seq', 53, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY users (user_id, fb_userid, first_name, last_name, age, photo, email, password, member_since, image) FROM stdin;
1	10154085900708339	Maddie	Cousens	24	\N	maddie@	doge1	2016-11-21 22:25:32.801161	https://s-media-cache-ak0.pinimg.com/236x/3a/8e/6e/3a8e6eec898c6f3d1c9352503a9c8e37.jpg
2	108875526264733	Ahmad	Alawad	30	\N	ahmad@	maddie2	2016-11-21 22:25:32.801161	http://theverybesttop10.com/wp-content/uploads/2014/10/Top-10-Images-of-Cats-Driving-2.jpg
3	100014238157245	Aretha	Franklin	51	\N	carl@	maddie3	2016-11-21 22:25:32.801161	https://i.ytimg.com/vi/BWAK0J8Uhzk/hqdefault.jpg
4	100014205218090	Graham	Egan	27	\N	graham@	maddie4	2016-11-21 22:25:32.801161	http://67.media.tumblr.com/tumblr_md019wlf781rz4vr8o1_1280.jpg
5	105608939924154	Grom	Gromoth	27	\N	grom@	maddie5	2016-11-21 22:25:32.801161	https://s-media-cache-ak0.pinimg.com/originals/84/42/a7/8442a778bf0b163a3c30aefe7a64be61.jpg
6	100014168388615	Beyonce	Knowles	27	\N	thomoth@	maddie6	2016-11-21 22:25:32.801161	https://s-media-cache-ak0.pinimg.com/originals/13/44/06/134406e512f3ab5b252df70df541bf56.jpg
7	100014175948968	Lexie	Cousens	27	\N	lexie@	maddie7	2016-11-21 22:25:32.801161	http://www.zercustoms.com/news/images/Subaru-dog-driving-lessons-b.jpg
\.


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('users_user_id_seq', 7, true);


--
-- Name: requests_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY requests
    ADD CONSTRAINT requests_pkey PRIMARY KEY (id);


--
-- Name: riders_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY riders
    ADD CONSTRAINT riders_pkey PRIMARY KEY (id);


--
-- Name: rides_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY rides
    ADD CONSTRAINT rides_pkey PRIMARY KEY (ride_id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: requests_requester_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY requests
    ADD CONSTRAINT requests_requester_fkey FOREIGN KEY (requester) REFERENCES users(user_id);


--
-- Name: requests_ride_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY requests
    ADD CONSTRAINT requests_ride_id_fkey FOREIGN KEY (ride_id) REFERENCES rides(ride_id);


--
-- Name: riders_ride_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY riders
    ADD CONSTRAINT riders_ride_id_fkey FOREIGN KEY (ride_id) REFERENCES rides(ride_id);


--
-- Name: riders_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY riders
    ADD CONSTRAINT riders_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: rides_driver_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY rides
    ADD CONSTRAINT rides_driver_fkey FOREIGN KEY (driver) REFERENCES users(user_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

