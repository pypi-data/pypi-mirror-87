#!/bin/bash


PROP_PATH="/opt/iParapheur/tomcat/shared/classes/alfresco-global.properties"

if [ -f "$PROP_PATH" ]
then
  while IFS='=' read -r key value
  do
    key=$(echo $key | tr '.' '_')
    eval "${key}"=\${"value"} 2> /dev/null
  done < "$PROP_PATH"
else
  echo "- LE FICHIER DE PROPRIETE $1 EST INTROUVABLE : FIN DU SCRIPT"
  exit 1
fi


## -- Des variables
FILE=/var/run/parapheur.pid
alfresco="/etc/init.d/alfresco"
PATH_IP="/opt/iParapheur/tomcat/shared/classes/"
db_url=`echo "$db_url" | awk -F/ '{ print $3 }' | awk -F: '{ print $1 }'`
db_port=`echo "$db_url" | awk -F/ '{ print $3 }' | awk -F: '{ print $2 }'`
DATA_PATH="$dir_root/contentstore/"
if [ -z "$db_port" ]
then
  db_port="3306"
fi
mysql="-h $db_url -P $db_port -u $db_username -p$db_password"


## -- Quelques test
IF_FILE_EXIST ()
{
if [ ! -f $1 ]; then
  echo "- LE DOSSIER $1 N'EXISTE PAS"
  echo " -FIN DU SCRIPT"
  exit 1
else
  echo -e "$1 => ok\n"
fi
}



IF_DIR_EXIST ()
{
if [ ! -d $1 ]; then
  echo "LE DOSSIER $1 N'EXISE PAS"
  echo "- FIN DU SCRIPT"
  exit 1
else
  echo -e "$1 => ok\n"
fi
}


TEST_SERVICE ()
{
if ! which $1 >/dev/null; then
  echo "- LE SERVICE $1 N EXISTE PAS"
  echo "FIN DU SCRIPT"
  exit 1
else
  echo -e "$1 => ok\n"
fi
}


## -- ON LANCE LES TESTS
echo -e "\n ** PREREQUIS **\n"
IF_FILE_EXIST $alfresco
IF_DIR_EXIST $PATH_IP
IF_FILE_EXIST $PROP_PATH
TEST_SERVICE "mysql"
IF_DIR_EXIST $DATA_PATH


## -- On s'assure de stopper l'application
echo -e "\nARRET DE L APPLICATION EN COURS ... \n"
/etc/init.d/alfresco stop > /dev/null 2>&1
kill $(ps aux | grep '/opt/iParapheur/java/bin/java' | awk '{print $2}') > /dev/null 2>&1
kill $(ps aux | grep '/opt/jre/bin/java' | awk '{print $2}') > /dev/null 2>&1
if [ -f $FILE ]; then
   rm $FILE
fi


## -- Test connexion à la base
mysql $mysql -e 'exit' $db_name
if [ $? -ne 0 ]; then
    echo "- CONNEXION A LA BASE DE DONNEES IMPOSSIBLE"
    echo "- FIN DU SCRIPT"
    exit 1
fi
echo -e "\n- CONNEXION A LA BASE DE DONNEES => OK\n"

## -- Supression des noeuds
mysql $mysql -e 'UPDATE alf_node SET NODE_DELETED =1 WHERE NODE_DELETED =0 AND id NOT IN ( SELECT root_node_id FROM alf_store ) AND id NOT IN ( SELECT child_node_id FROM alf_child_assoc );' $db_name > /dev/null 2>&1
echo -e "\n- SUPPRESSION DES NOEUDS => OK\n"

## --   Procedure de nettoyage des transcations alfresco
echo "DELIMITER //" > myproc.sql
echo "CREATE PROCEDURE doCleanIPTransaction()" >> myproc.sql
echo "bEGIN" >> myproc.sql
echo "SET @timestampOneMonthAgo = (SELECT UNIX_TIMESTAMP(DATE_SUB(NOW(), INTERVAL 30 day))) * 1000;" >> myproc.sql
echo "CREATE TEMPORARY TABLE temp1 (id bigint(20), index (id));" >> myproc.sql
echo "INSERT INTO temp1 SELECT alf_node.id FROM alf_node" >> myproc.sql
echo "INNER JOIN alf_transaction ON alf_node.transaction_id = alf_transaction.id" >> myproc.sql
echo "WHERE alf_transaction.commit_time_ms < @timestampOneMonthAgo AND alf_node.node_deleted=TRUE;" >> myproc.sql
echo "DELETE FROM alf_node_aspects WHERE node_id IN (SELECT id FROM temp1);" >> myproc.sql
echo "DELETE FROM alf_node WHERE id IN (SELECT id FROM temp1);" >> myproc.sql
echo "DELETE from alf_transaction where id not in (select transaction_id from alf_node);" >> myproc.sql
echo "DROP TABLE temp1;" >> myproc.sql
echo "OPTIMIZE TABLE alf_node_aspects;" >> myproc.sql
echo "OPTIMIZE TABLE alf_node;" >> myproc.sql
echo "OPTIMIZE TABLE alf_transaction;" >> myproc.sql
echo "END;" >> myproc.sql
echo "//" >> myproc.sql
echo "DELIMITER ;" >> myproc.sql


## -- ON injecte la procédure
mysql $mysql $db_name < myproc.sql >/dev/null 2>&1


## -- Nettoyage des transactions
mysql $mysql -e 'CALL doCleanIPTransaction();' $db_name >/dev/null 2>&1
echo -e "\n- PROCEDURE SQL VISANT À SUPPRIMER DES TRANSACTIONS INUTILES => OK\n"

## -- Reconstruction des indexes
rm -rf $dir_root/lucene-indexes $dir_root/backup-lucene-indexes
echo -e "\n- SUPPRESSION DES DOSSIERS LUCENE-INDEXES ET BACKUP-LUCENE-NDEXES => OK\n"

##  -- Demarrage de l'application
echo -e "\n- DEMARRAGE DE L'APPLICATION ...\n"
sleep 10
/etc/init.d/alfresco start && tail -f /opt/iParapheur/tomcat/logs/catalina.out | sed '/^INFOS: Server startup in/ q'
echo -e "\n** FIN DU SCRIPT LE PARAPHEUR EST DEMARRE **\n"
exit 0