import pymysql
connection = pymysql.connect(host='ancssc-db.mysql.database.azure.com',
							 user='ancssc@ancssc-db',
							 password='819UiC@Uj&$Z^GY',
							 db='team_36_db_do_not_touch',
							 charset='utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)


def submit(data):
	ngo_name = data["ngo"]["NGO_NAME"]
	ngo_id = -1
	if ngo_name in get_existing_ngos():
		ngo_id = get_ngo_id(ngo_name)
	else:
		ngo_id = create_new_ngo


def get_existing_ngos():
	with connection.cursor() as cursor:
		# Create a new record

		sql = "SELECT `NGO_NAME` FROM `ngo`"
		cursor.execute(sql)
		result = cursor.fetchall()
	data = []
	for r in result:
		data.append(r['NGO_NAME'])

	return data


def get_ngo_id(ngo_name):
	with connection.cursor() as cursor:
		sql = "SELECT `NGO_ID` FROM `ngo` WHERE `NGO_NAME` = %s"
		cursor.execute(sql, ngo_name)
		result = cursor.fetchone()

	return result
get_existing_ngos()