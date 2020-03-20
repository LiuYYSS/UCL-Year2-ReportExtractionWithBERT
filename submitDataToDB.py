import pymysql
import pickle

class submitDataToDB:
	connection = None
	def __init__(self):
		self.create_connection()


	def close_connection(self):
		self.connection.close()


	def create_connection(self):
		self.connection = pymysql.connect(host='ancssc-db.mysql.database.azure.com',
									 user='ancssc@ancssc-db',
									 password='819UiC@Uj&$Z^GY',
									 db='team_36_db_do_not_touch',
									 charset='utf8mb4',
									 cursorclass=pymysql.cursors.DictCursor)



	def submit(self, d, pdf_name):
		data = d.information
		ngo_name = data["ngo"]["NGO_NAME"]
		ngo_id = self.get_ngo_id(ngo_name)
		# data["ngo"]["NGO_ID"] = ngo_id
		data["ngo"]["PDF_NAME"] = pdf_name
		data["ngo"].pop("NGO_NAME", None)
		data["ngo"].pop("PROJECT_TITLE", None)
		ngo_data_id = self.submit_data("ngo_data", data["ngo"], ngo_id)

		self.submit_data("sponsors", data["sponsors"], ngo_data_id)

		staff = ""

		for r in data["ngo_staff"]["PERSON_NAME"]:
			if staff == "":
				staff = r
			else:
				staff = staff + ", " + r
		data["ngo_staff"]["PERSON_NAME"] = staff

		self.submit_data("ngo_staff", data["ngo_staff"], ngo_data_id)

		self.submit_project_data(data, ngo_data_id)





	def submit_data(self, table_name, table_data, ngo_data_id):
		if ngo_data_id is not None:
			table_data["NGO_ID"] = ngo_data_id
		with self.connection.cursor() as cursor:
			# Create a new record
			fields = " ( "
			for item in table_data:
				if fields != " ( ":
					fields += ", " + "`"+item+"`"
				else:
					fields += " `"+item+"`"
			fields += ")"

			data = "( "
			for item in table_data:
				table_data[item] = table_data[item].replace("'", "")
				table_data[item] = table_data[item].replace(",", "")
				table_data[item] = table_data[item].replace("\"", "")
				if data != "( ":
					data += ", " + "'"+str(table_data[item])+"'"
				else:
					data += " '"+str(table_data[item])+"'"

			data += ")"

			sql = "INSERT INTO " + table_name +  fields + " VALUES " + data + " "
			print(sql)
			cursor.execute(sql)
		self.connection.commit()



		with self.connection.cursor() as cursor:
				# Create a new record

			sql = "SELECT LAST_INSERT_ID()"
			cursor.execute(sql)
			result = cursor.fetchone()

		return result["LAST_INSERT_ID()"]



	def submit_project_data(self, data, ngo_data_id):
		s = {}
		ids = []
		for i in range(0, len(data["projects"]["PROJECT_DESCRIPTION"])):
			s = {}
			for field in data["projects"]:
				s[field] = data["projects"][field][i]
			s["NGO_ID"] = ngo_data_id
			ids.append(self.submit_data("projects", s, ngo_data_id))


		for i, proj_id in enumerate(ids):
			self.submit_project_related_table("project_geo_info", data, i, proj_id)
			self.submit_project_related_table("classifications", data, i, proj_id)
			self.submit_project_related_table("project_impact", data, i, proj_id)
			self.submit_project_related_table("project_finance", data, i, proj_id)


	def submit_project_related_table(self, table_name, data, i, proj_id):
		s = {}
		for field in data[table_name]:
			s[field] = data[table_name][field][i]
		s["PROJECT_ID"] = proj_id
		self.submit_data(table_name, s, None)

	# n = submit_data("ngo_data", {
	# 	"NGO_SINCE": "4 april"
	# })





	def get_ngo_id(self, ngo_name):

		result = self.fetch_ngo_id_from_db(ngo_name)


		if result is None:
			with self.connection.cursor() as cursor:
				# Create a new record
				sql = "INSERT INTO `ngo` (`NAME`) VALUES (%s)"
				cursor.execute(sql, (ngo_name))
			self.connection.commit()
		else:
			return result["ID"]


		result = self.fetch_ngo_id_from_db(ngo_name)
		return result["ID"]




	def fetch_ngo_id_from_db(self, ngo_name):
		with self.connection.cursor() as cursor:
				# Create a new record

			sql = "SELECT `ID` FROM `ngo` WHERE `NAME` = %s"
			cursor.execute(sql, ngo_name)
			result = cursor.fetchone()
		return result






