truncate table frontend_filter CASCADE;

CREATE OR REPLACE FUNCTION boolean_filter(code character varying(32), 
                name character varying(128),
                description text,
                priority integer) RETURNS VOID
AS $$
DECLARE
BEGIN
    INSERT INTO frontend_filter(code,name,description,priority) VALUES (code,name,description,priority);
    INSERT INTO frontend_booleanfilter(filter_ptr_id) VALUES (code);
END;
$$
 LANGUAGE plpgsql; 

 CREATE OR REPLACE FUNCTION intrange_filter(code character varying(32), 
                name character varying(128),
                description text,
                priority integer,
                min integer,
                max integer) RETURNS VOID
AS $$
DECLARE
BEGIN
    INSERT INTO frontend_filter(code,name,description,priority) VALUES (code,name,description,priority);
    INSERT INTO frontend_intrangefilter(filter_ptr_id,min,max) VALUES (code,min,max);
END;
$$
 LANGUAGE plpgsql; 
 
 CREATE OR REPLACE FUNCTION select_filter(code character varying(32), 
                name character varying(128),
                description text,
                priority integer,
                required boolean,
                options character varying(64)[][]) RETURNS VOID
AS $$
DECLARE
   option   varchar[];
BEGIN
    INSERT INTO frontend_filter(code,name,description,priority) VALUES (code,name,description,priority);
    INSERT INTO frontend_selectfilter(filter_ptr_id,required) VALUES (code,required);
    FOREACH option SLICE 1 IN ARRAY options
    LOOP
	INSERT INTO frontend_selectoption(filter_id,code,name) VALUES (code,option[1],option[2]);
    END LOOP;	
END;
$$
 LANGUAGE plpgsql; 

DO
$$
DECLARE
BEGIN
   execute select_filter('paradigm','Парадигма','',0, false,
			array[['rel','Реляционная'],['keyval','Ключ-Значение'],['doc','Документно-ориентированная'],['col','Семейство столбцов'],['graph','Граф']]);
   execute select_filter('atomic','Атомарность','',1, false,
			array[['tx','Транзакции'],['cas','Одна запись атомарна'],['no','Нет']]);			
   execute select_filter('isolation','Изоляция','',2,false, 
			array[['block','Блокировки'],['ver','Версии']]);
			
   execute boolean_filter('shard','Шардирование','',3);	
   execute select_filter('repl','Репликация','',4, false,
			array[['ms','Блокировки'],['p2p','Версии'],['other','Другая'],['no','Нет']]); 
   execute boolean_filter('ttl','Удаление устаревших записей','',5);

   execute select_filter('lic','Лицензия','',6, false,
			array[['comm','Коммерческая'],['free','Свободная'],['edu','Образовательная'],['other','Другая']]); 
   	
   execute select_filter('idgen','Генерация id','',7, false,
			array[['seq','Последоватльности'],['autoinc','Автоинкрементное поле'],['uuid','UUID'],['other','Другая']]); 
   execute select_filter('sort','Сортировка','',8, false,
			array[['any','По любому полю'],['idx','Только по индексу'],['id','Только по id'],['no','Невозможна']]); 
   execute select_filter('access','Доступ','',9, false,
			array[['net','По сети'],['bundled','Встраиваемая']]); 
   	
END;
$$;