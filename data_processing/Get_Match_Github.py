# Reading an excel file using Python 
import xlrd 
 
loc_TopVenue = '/Users/kamel/Desktop/CMU/Final_GitHub_links/TopVenuePapers.xlsx'

wb_2 = xlrd.open_workbook(loc_TopVenue) 
sheet_2 = wb_2.sheet_by_index(0) 
TopVenue = []
TopVenue_dic = {}
for i in range(457):
	TopVenue.append(sheet_2.cell_value(i, 0)+".pdf")
	TopVenue_dic[sheet_2.cell_value(i, 0)] = sheet_2.cell_value(i, 1)

loc = ("/Users/kamel/Desktop/CMU/Final_GitHub_links/PapersName_GithubLinks_2.xlsx") 
  
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
  
for row in range(10529):
	for column in range(2):
		if column == 0:
			Venue = "http://arxiv.org/pdf/" + sheet.cell_value(row, column)

			if Venue in TopVenue:
				print(Venue,';', sheet.cell_value(row, 1), end = '; ')