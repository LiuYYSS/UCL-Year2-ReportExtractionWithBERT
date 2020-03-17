import pymysql
connection = pymysql.connect(host='ancssc-db.mysql.database.azure.com',
							 user='ancssc@ancssc-db',
							 password='819UiC@Uj&$Z^GY',
							 db='team_36_db_do_not_touch',
							 charset='utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)


def submit(data):
	ngo_name = data["ngo"]["NGO_NAME"]
	ngo_id = get_ngo_id(ngo_name)

	ngo_data_id = submit_data(data["ngo_data"])



def get_ngo_id(ngo_name):

	result = fetch_ngo_id_from_db(ngo_name)

	if result is None:
		with connection.cursor() as cursor:
			# Create a new record
			sql = "INSERT INTO `ngo` (`NAME`) VALUES (%s)"
			cursor.execute(sql, (ngo_name))
		connection.commit()

	result = fetch_ngo_id_from_db(ngo_name)
	return result




def fetch_ngo_id_from_db(ngo_name):
	with connection.cursor() as cursor:
			# Create a new record

		sql = "SELECT `ID` FROM `ngo` WHERE `NAME` = %s"
		cursor.execute(sql, ngo_name)
		result = cursor.fetchone()
	return result
def create_new_ngo():
	pass



print(get_ngo_id("actionaid"))
# def get_existing_ngos():
# 	with connection.cursor() as cursor:
# 		# Create a new record
#
# 		sql = "SELECT `NGO_NAME` FROM `ngo`"
# 		cursor.execute(sql)
# 		result = cursor.fetchall()
# 	data = []
# 	for r in result:
# 		data.append(r['NGO_NAME'])
#
# 	return data
#
#
# def get_ngo_id(ngo_name):
# 	with connection.cursor() as cursor:
# 		sql = "SELECT `NGO_ID` FROM `ngo` WHERE `NGO_NAME` = %s"
# 		cursor.execute(sql, ngo_name)
# 		result = cursor.fetchone()
#
# 	return result
# get_existing_ngos()