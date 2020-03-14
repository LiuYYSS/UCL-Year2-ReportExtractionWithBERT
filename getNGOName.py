import pymysql

connection = pymysql.connect(host='ancssc-db.mysql.database.azure.com',
							 user='ancssc@ancssc-db',
							 password='819UiC@Uj&$Z^GY',
							 db='team_36_db_do_not_touch',
							 charset='utf8mb4',
							 cursorclass=pymysql.cursors.DictCursor)


def getNGOName(reportName):
	"""

	:param reportName: name of report, not including "report/", example : IHAP2018.pdf
	:return: empty string if not found, name if found
	"""

	with connection.cursor() as cursor:
		# Create a new record

		sql = "SELECT `NGO_NAME` FROM `pdfs` WHERE `PDF_NAME` = %s"
		cursor.execute(sql, (reportName,))
		result = cursor.fetchone()
	if result is None:
		return ""
	return result



def getAvailableReports():
	"""

	:return: list of all reports e.g. ['Prakriye – Annual Report.pdf', 'PLANACT-AR-17_18-002...pdf', 'tanzania-2018.pdf']
	"""

	with connection.cursor() as cursor:
		# Create a new record

		sql = "SELECT `PDF_NAME` FROM `pdfs`"
		cursor.execute(sql)
		result = cursor.fetchall()
	data = []
	for r in result:
		data.append(r['PDF_NAME'])

	return data

