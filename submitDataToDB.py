import pymysql
connection = pymysql.connect(host='ancssc-db.mysql.database.azure.com',
							 user='ancssc@ancssc-db',
							 password='819UiC@Uj&$Z^GY',
							 db='team_36_db_do_not_touch',
							 charset='utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)




def submit(data, pdf_name):
	ngo_name = data["ngo"]["NGO_NAME"]
	ngo_id = get_ngo_id(ngo_name)
	# data["ngo"]["NGO_ID"] = ngo_id
	data["ngo"]["PDF_NAME"] = pdf_name
	data["ngo"].pop("NGO_NAME", None)
	ngo_data_id = submit_data("ngo_data", data["ngo"], ngo_id)

	submit_data("sponsors", data["sponsors"], ngo_data_id)
	submit_data("ngo_staff", data["ngo_staff"], ngo_data_id)

	submit_project_data(data, ngo_data_id)





def submit_data(table_name, table_data, ngo_data_id):
	table_data["NGO_ID"] = ngo_data_id
	with connection.cursor() as cursor:
		# Create a new record
		fields = "( "
		for item in table_data:
			if fields != "( ":
				fields += ", " + "`"+item+"`"
			else:
				fields += " `"+item+"`"
		fields += ")"

		data = "( "
		for item in table_data:
			if data != "( ":
				data += ", " + "'"+str(table_data[item])+"'"
			else:
				data += " '"+str(table_data[item])+"'"
		data += ")"

		sql = "INSERT INTO " + table_name +  fields + " VALUES " + data + " "
		cursor.execute(sql)
	connection.commit()



	with connection.cursor() as cursor:
			# Create a new record

		sql = "SELECT LAST_INSERT_ID()"
		cursor.execute(sql)
		result = cursor.fetchone()

	return result["LAST_INSERT_ID()"]



def submit_project_data(data, ngo_data_id):
	s = {}
	ids = []
	for i in range(0, len(data["projects"]["PROJECT_DESCRIPTION"])):
		s = {}
		for field in data["projects"]:
			s[field] = data["projects"][field][i]
		s["NGO_ID"] = ngo_data_id
		ids.append(submit_data("projects", s))


	for i, proj_id in enumerate(ids):
		submit_project_related_table("project_geo_info", data, i , proj_id)
		submit_project_related_table("classifications", data, i, proj_id)
		submit_project_related_table("project_impact", data, i, proj_id)
		submit_project_related_table("project_finance", data, i, proj_id)


def submit_project_related_table(table_name, data, i, proj_id):
	s = {}
	for field in data[table_name]:
		s[field] = data[table_name][field][i]
	s["PROJECT_ID"] = proj_id
	submit_data(table_name, s)

# n = submit_data("ngo_data", {
# 	"NGO_SINCE": "4 april"
# })





def get_ngo_id(ngo_name):

	result = fetch_ngo_id_from_db(ngo_name)


	if result is None:
		with connection.cursor() as cursor:
			# Create a new record
			sql = "INSERT INTO `ngo` (`NAME`) VALUES (%s)"
			cursor.execute(sql, (ngo_name))
		connection.commit()
	else:
		return result["ID"]


	result = fetch_ngo_id_from_db(ngo_name)
	return result["ID"]




def fetch_ngo_id_from_db(ngo_name):
	with connection.cursor() as cursor:
			# Create a new record

		sql = "SELECT `ID` FROM `ngo` WHERE `NAME` = %s"
		cursor.execute(sql, ngo_name)
		result = cursor.fetchone()
	return result
def create_new_ngo():
	pass


#
# print(get_ngo_id("actionaid"))

# submit_data("ngo_data", {
# 	"NGO_SINCE": "4 april"
# })



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

