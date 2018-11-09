import datetime
import postgresql
import config
import threading
import SQLScripts

class Postgres(object):
    """Postgres singleton class"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            print('connecting to DataBase...')
            print(config.getDBCredentials() )
            connection = Postgres._instance.connection = postgresql.open(
                config.getDBCredentials())
        return cls._instance
    
    def __init__(self):
        self.connection = self._instance.connection

    def log(self, user_id, message):
        ins = self.connection.prepare(
            """
            INSERT INTO USERS_LOG (user_id, message) 
            SELECT $1, $2;
            """)
        ins(str(user_id), str(message))

    def getUsage(self):
        select = self.connection.query(
            """
            SELECT COUNT(*) usage_stat FROM USERS_LOG;
            """
        )
        return str(int(select[0]['usage_stat']))

    def getUsersCount(self):
        select = self.connection.query(
            """
            SELECT COUNT(*) users_count FROM T_USERS;
            """
        )
        return select[0]

    def initDB(self):
        for script in SQLScripts.init_scripts:
            print(script)
            self.connection.execute(script)
        
    def addUser(self, telegramId, groupId=''):
        ins = self.connection.prepare(
            """
            INSERT INTO T_USERS (TELEGRAM_ID, GROUP_ID)
            select $1, $2;
            """)
        ins(str(telegramId), str(groupId))

    def updateUser(self, telegramId, groupId):
        ins = self.connection.prepare(
            """
            UPDATE T_USERS
            SET GROUP_ID = $1
            WHERE TELEGRAM_ID = $2;
            """)
        ins(str(groupId), str(telegramId))

    def getUserFaculty(self, telegramId):
        select = self.connection.query(
            """
            SELECT G.FACULTY_ID 
            FROM USERS U, GROUPS G 
            WHERE U.TELEGRAM_ID = {0} 
            AND G.ID=U.GROUP_ID;
            """.format(str(telegramId))
        )
        return select
        
    def getGroupsByFaculty(self, faculty):
        select = self.connection.query(
            """
            SELECT NAME
            FROM GROUPS 
            WHERE FACULTY_ID = {0}
            ORDER BY NAME;
            """.format(str(faculty)) 
        )
        return select
    
    def getGroupList(self):
        select = self.connection.query(
            """
            SELECT DISTINCT NAME
            FROM GROUPS;
            """)
        return select
    
    def getFaculties(self):
        select = self.connection.query(
            """
            SELECT DISTINCT NAME
            FROM T_FACULTIES;
            """)
        return select

    def getSchedule(self, telegramId):
        return self.connection.query(
            """
            SELECT S.DATA
            FROM T_SCHEDULES S
            JOIN USERS U ON U.GROUP_ID = S.GROUP_ID
            WHERE U.ID = '{0}';
            """.format(str(telegramId))
        )
    
    def getScheduleByGroup(self, groupId):
        return self.connection.query(
            """
            SELECT S.SCHEDULE
            FROM T_SCHEDULES S
            WHERE S.GROUP_ID = '{0}';
            """.format(str(groupId))
        )

    def setSchedule(self, groupId, schedule):
        ins = self.connection.prepare(
            """
            INSERT INTO T_SCHEDULES
            (GROUP_ID, DATA)
            VALUES ($1, $2);
            """)
        ins(str(groupId), str(schedule))

    def getGroups(self):
        return self.connection.query(
            """
            SELECT GROUP_ID FROM T_GROUPS;
            """)

    def getAllUsers(self):
        select = self.connection.query('SELECT * FROM T_USERS;')
        return select
