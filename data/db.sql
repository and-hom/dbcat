truncate table frontend_db cascade;

CREATE OR REPLACE FUNCTION db(name character varying(64),
				short_description text,
				description text,
				homepage character varying(200)) RETURNS INTEGER
AS $$
DECLARE
   db_id integer;
BEGIN
    INSERT INTO frontend_db(name,short_description,description,homepage) VALUES (name,short_description,description,homepage) RETURNING id INTO db_id;
    return db_id;
END;
$$
 LANGUAGE plpgsql; 

CREATE OR REPLACE FUNCTION db_param_simple(db_id integer,code character varying(16), val integer) RETURNS VOID
AS $$
DECLARE
   p_id integer;
BEGIN	
	INSERT INTO frontend_dbparam(db_id,filter_id) VALUES(db_id,code) RETURNING id INTO p_id;
	INSERT INTO frontend_simpledbparam(dbparam_ptr_id,value) VALUES (p_id,val);
END;
$$
 LANGUAGE plpgsql; 

CREATE OR REPLACE FUNCTION db_param_select(db_id_ integer,code character varying(16)) RETURNS INTEGER
AS $$
DECLARE
   p_id integer;
BEGIN	
	SELECT id INTO p_id FROM frontend_dbparam WHERE db_id=db_id_ AND filter_id=code;
	IF p_id is null then
		INSERT INTO frontend_dbparam(db_id,filter_id) VALUES(db_id_,code) RETURNING id INTO p_id;
		INSERT INTO frontend_selectdbparam(dbparam_ptr_id) VALUES (p_id);
	END IF;	
	return p_id;
END;
$$
 LANGUAGE plpgsql; 
  
CREATE OR REPLACE FUNCTION db_param_select_opt(db_id_ integer,filter_code character varying(16), opt_code character varying(16), value integer) RETURNS VOID
AS $$
DECLARE
	opt_id integer;
	p_id integer;
BEGIN	
	SELECT id INTO opt_id FROM frontend_selectoption WHERE filter_id=filter_code AND code=opt_code;
	SELECT id INTO p_id FROM frontend_dbparam WHERE filter_id=filter_code AND db_id=db_id_; 
	IF p_id IS NULL
	THEN
		select db_param_select(db_id_,filter_code) into p_id;
	END IF;	
	INSERT INTO frontend_selectdbparamoption(param_id,option_id,value) VALUES (p_id,opt_id,value);
END;
$$
 LANGUAGE plpgsql; 




 DO
$$
DECLARE
	db_id integer;
	p_id integer;
BEGIN
--    postgres
	select db('PostgreSQL','Свободная объектно-реляционная система управления базами данных','PostgreSQL ведет свою «родословную» от некоммерческой СУБД Postgres, разработанной, как и многие open-source проекты, в Калифорнийском университете в Беркли. К разработке Postgres, начавшейся в 1986 году, имел непосредственное отношение Майкл Стоунбрейкер, руководитель более раннего проекта Ingres, на тот момент уже приобретённого компанией Computer Associates. Само название «Postgres» расшифровывалось как «Post Ingres», соответственно, при создании Postgres были применены многие уже ранее сделанные наработки.

Стоунбрейкер и его студенты разрабатывали новую СУБД в течение восьми лет с 1986 по 1994 год. За этот период в синтаксис были введены процедуры, правила, пользовательские типы и многие другие компоненты. Работа не прошла даром — в 1995 году разработка снова разделилась: Стоунбрейкер использовал полученный опыт в создании коммерческой СУБД Illustra, продвигаемой его собственной одноимённой компанией (приобретённой впоследствии компанией Informix), а его студенты разработали новую версию Postgres — Postgres95, в которой язык запросов POSTQUEL — наследие Ingres — был заменен на SQL.',
'http://www.postgresql.org/') into db_id;


	execute db_param_select_opt(db_id,'paradigm','rel',100);
	execute db_param_select_opt(db_id,'atomic','tx',100);
	execute db_param_select_opt(db_id,'isolation','ver',100);
	execute db_param_simple(db_id,'shard',0); --Из коробки нет, см PostgreSQL-XC
	execute db_param_select_opt(db_id,'repl','ms',100);
	execute db_param_select_opt(db_id,'repl','p2p',0); --bucardo
	execute db_param_simple(db_id,'ttl',0);
	execute db_param_select_opt(db_id,'lic','otherfree',100);
	execute db_param_select_opt(db_id,'idgen','seq',100);
	execute db_param_select_opt(db_id,'sort','any',100);
	execute db_param_select_opt(db_id,'codelang','native',100);

--   mysql
	select db('MySQL','Объектно-реляционная система управления базами данных','Разработку и поддержку MySQL осуществляет корпорация Oracle, получившая права на торговую марку вместе с поглощённой Sun Microsystems, которая ранее приобрела шведскую компанию MySQL AB. Продукт распространяется как под GNU General Public License, так и под собственной коммерческой лицензией. Помимо этого, разработчики создают функциональность по заказу лицензионных пользователей. Именно благодаря такому заказу почти в самых ранних версиях появился механизм репликации.

MySQL является решением для малых и средних приложений. Входит в состав серверов WAMP, AppServ, LAMP и в портативные сборки серверов Денвер, XAMPP, VertrigoServ. Обычно MySQL используется в качестве сервера, к которому обращаются локальные или удалённые клиенты, однако в дистрибутив входит библиотека внутреннего сервера, позволяющая включать MySQL в автономные программы.

Гибкость СУБД MySQL обеспечивается поддержкой большого количества типов таблиц: пользователи могут выбрать как таблицы типа MyISAM, поддерживающие полнотекстовый поиск, так и таблицы InnoDB, поддерживающие транзакции на уровне отдельных записей. Более того, СУБД MySQL поставляется со специальным типом таблиц EXAMPLE, демонстрирующим принципы создания новых типов таблиц. Благодаря открытой архитектуре и GPL-лицензированию, в СУБД MySQL постоянно появляются новые типы таблиц.

26 февраля 2008 года Sun Microsystems приобрела MySQL AB за $1 млрд[4], 27 января 2010 года Oracle приобрела Sun Microsystems за $7,4 млрд[5] и включила MySQL в свою линейку СУБД.[6]

Сообществом разработчиков MySQL созданы различные ответвления кода, такие, как Drizzle (англ.), OurDelta, Percona Server и MariaDB. Все эти ответвления уже существовали на момент поглощения компании Sun корпорацией Oracle.

',
'http://www.mysql.com/') into db_id;

	execute db_param_select_opt(db_id,'paradigm','rel',100);
	execute db_param_select_opt(db_id,'atomic','tx',100);
	execute db_param_select_opt(db_id,'isolation','block',100);
	
	--execute db_param_simple(db_id,'shard',60); 
	execute db_param_select_opt(db_id,'repl','ms',100);
	
	execute db_param_simple(db_id,'ttl',0);
	execute db_param_select_opt(db_id,'lic','comm',100);
	execute db_param_select_opt(db_id,'lic','gpl2',100);
	
	execute db_param_select_opt(db_id,'idgen','autoinc',100);
	execute db_param_select_opt(db_id,'sort','any',100);
	execute db_param_select_opt(db_id,'codelang','native',100);
	

--   MongoDB
	select db('MongoDB','Документо-ориентированная система управления базами данных (СУБД) с открытым исходным кодом','',
'http://www.mongodb.org/') into db_id;

	execute db_param_select_opt(db_id,'paradigm','doc',100);
	execute db_param_select_opt(db_id,'atomic','cas',100);
	execute db_param_select_opt(db_id,'isolation','ver',100);
	
	execute db_param_simple(db_id,'shard',100); 
	execute db_param_select_opt(db_id,'repl','ms',100);
	
	execute db_param_simple(db_id,'ttl',100);
	execute db_param_select_opt(db_id,'lic','agpl',100);
	execute db_param_select_opt(db_id,'lic','comm',100);
	
	execute db_param_select_opt(db_id,'idgen','autoinc',100);
	execute db_param_select_opt(db_id,'sort','any',100);
	execute db_param_select_opt(db_id,'codelang','native',100);
	

END;
$$;
