import pymysql
import os
class getDataFromDB:
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


	def getNGOName(self, reportName):
		"""

		:param reportName: name of report, not including "report/", example : IHAP2018.pdf
		:return: empty string if not found, name if found
		"""

		with self.connection.cursor() as cursor:
			# Create a new record

			sql = "SELECT `NGO_NAME` FROM `pdfs` WHERE `PDF_NAME` = %s"
			cursor.execute(sql, (reportName,))
			result = cursor.fetchone()
		if result is None:
			return ""
		return result



	def getAvailableReports(self):
		"""

		:return: list of all reports e.g. ['Prakriye – Annual Report.pdf', 'PLANACT-AR-17_18-002...pdf', 'tanzania-2018.pdf']
		"""

		with self.connection.cursor() as cursor:
			# Create a new record

			sql = "SELECT `PDF_NAME` FROM `pdfs`"
			cursor.execute(sql)
			result = cursor.fetchall()
		data = []
		for r in result:
			data.append(r['PDF_NAME'])

		return data


	def getCompletedReports(self):

		with self.connection.cursor() as cursor:
			# Create a new record

			sql = "SELECT `PDF_NAME` FROM `ngo_data`"
			cursor.execute(sql)
			result = cursor.fetchall()
		data = []
		for r in result:
			data.append(r['PDF_NAME'])


		final_data = []
		for item in data:
			address = item.split(os.sep)
			final_data.append(address[-1])


		return final_data

