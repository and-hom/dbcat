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
                multichoice boolean,
                options character varying(64)[][]) RETURNS VOID
AS $$
DECLARE
   option   varchar[];
BEGIN
    INSERT INTO frontend_filter(code,name,description,priority) VALUES (code,name,description,priority);
    INSERT INTO frontend_selectfilter(filter_ptr_id,required,multichoice) VALUES (code,required,multichoice);
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
   execute select_filter('paradigm','Парадигма','',0, false, true,
			array[['rel','Реляционная'],['keyval','Ключ-Значение'],['doc','Документно-ориентированная'],['col','Семейство столбцов'],['graph','Граф']]);
   execute select_filter('atomic','Атомарность','',10, false, false,
			array[['tx','Транзакции'],['cas','Одна запись атомарна'],['no','Нет']]);			
   execute select_filter('isolation','Изоляция','',20,false, false,
			array[['block','Блокировки'],['ver','Версии']]);
			
   execute boolean_filter('shard','Шардирование','',30);
   execute select_filter('repl','Репликация','',40, false, false,
			array[['ms','Master-Slave'],['p2p','Peer-to-Peer'],['other','Другая'],['no','Нет']]);
   execute boolean_filter('ttl','Удаление устаревших записей','',5);

   execute select_filter('lic','Лицензия','',60, false, false,
			array[['comm','Коммерческая'],['apache2','Apache 2'],['agpl','AGPL'],['gpl2','GPLv2'],['otherfree','Другая cвободная'],['edu','Образовательная'],['other','Другая']]);
   	
   execute select_filter('idgen','Генерация id','',70, false, false,
			array[['seq','Последоватльности'],['autoinc','Автоинкрементное поле'],['uuid','UUID'],['other','Другая'],['no','Отсутствует']]);
   execute select_filter('sort','Сортировка','',80, false, false,
			array[['any','По любому полю'],['idx','Только по индексу'],['id','Только по id'],['no','Невозможна']]);
   execute select_filter('access','Доступ','',90, false, false,
			array[['net','По сети'],['builtin','Встраиваемая в приложение']]);
   execute select_filter('codelang','Исполняемый код СУБД','',100, false, false,
			array[['native','Нативный код'],['java','Java'],['erlang','Erlang']]);
   	
END;
$$;