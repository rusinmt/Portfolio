```sql
create warehouse OTODOM_WH
use warehouse OTODOM_WH

create file format json_format
    type = JSON
  
create or replace TABLE OTODOM_DATA (
	LISTING VARCHAR(16777216),
	PRICE NUMBER(38,0),
	SQMUP NUMBER(38,0),
	ROOM_INFO NUMBER(38,0),
	AREA NUMBER(38,0),
	LOCATION VARCHAR(16777216),
	ADS VARCHAR(16777216)
)

use database PROJECT

select * from PROJECT.DATA.OTODOM_DATA

delete from PROJECT.DATA.OTODOM_DATA
where LOCATION not in (
    'Bemowo', 'Białołęka', 'Bielany', 'Mokotów', 'Ochota', 'Praga-Południe',
    'Praga-Północ', 'Rembertów', 'Śródmieście', 'Targówek', 'Ursus', 'Ursynów',
    'Wawer', 'Wesoła', 'Wilanów', 'Włochy', 'Wola', 'Żoliborz'
)

select * from PROJECT.DATA.OTODOM_DATA
where LOCATION = 'Targówek'
order by PRICE desc

delete from PROJECT.DATA.OTODOM_DATA
where LOCATION = 'Targówek'
    and PRICE > 55000000

select * from PROJECT.DATA.OTODOM_DATA
where LOCATION = 'Białołęka'
order by PRICE desc

delete from PROJECT.DATA.OTODOM_DATA
where LOCATION = 'Białołęka'
    and PRICE > 46000000

select * from PROJECT.DATA.OTODOM_DATA
where LOCATION = 'Praga-Północ'
order by PRICE desc

delete from PROJECT.DATA.OTODOM_DATA
where LOCATION = 'Praga-Północ'
    and PRICE > 100000000

select * from PROJECT.DATA.OTODOM_DATA
where LOCATION = 'Praga-Południe'
order by PRICE desc

delete from PROJECT.DATA.OTODOM_DATA
where LOCATION = 'Praga-Południe'
    and PRICE > 90000000

select * from PROJECT.DATA.OTODOM_DATA
where LOCATION = 'Wola'
order by PRICE desc

delete from PROJECT.DATA.OTODOM_DATA
where LOCATION = 'Wola'
    and PRICE > 90000000

select * from PROJECT.DATA.OTODOM_DATA
where LOCATION = 'Włochy'
order by PRICE desc

delete from PROJECT.DATA.OTODOM_DATA
where LOCATION = 'Włochy'
    and PRICE > 40000000

select * from PROJECT.DATA.OTODOM_DATA
where LOCATION = 'Ursynów'
order by PRICE desc

delete from PROJECT.DATA.OTODOM_DATA
where LOCATION = 'Ursynów'
    and PRICE > 50000000
```
