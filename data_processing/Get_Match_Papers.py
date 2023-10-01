# Reading an excel file using Python 
import xlrd 
 
loc_TopVenue = '/Users/kamel/Desktop/CMU/Final_GitHub_links/TopVenuePapers.xlsx'

wb_2 = xlrd.open_workbook(loc_TopVenue) 
sheet_2 = wb_2.sheet_by_index(0) 
TopVenue = []
TopVenue_dic = {}
for i in range(457):
	TopVenue.append(sheet_2.cell_value(i, 0))
	TopVenue_dic[sheet_2.cell_value(i, 0)] = sheet_2.cell_value(i, 1)
	
print(len(TopVenue))
print(len(TopVenue_dic))
print(TopVenue_dic["http://arxiv.org/pdf/1912.01703v1"])

# Give the location of the file 
loc = ("/Users/kamel/Desktop/CMU/Software_22000Papers.xlsx") 
  
# To open Workbook 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
  
# For row 0 and column 0 

for row in range(20608):
	for column in range(6):
		if column == 1:
			Venue = sheet.cell_value(row, column)
			if Venue in TopVenue:
				for column_2 in range(6):
					if column_2 == 4:
						print(int(sheet.cell_value(row, column_2)), end = '; ')
					else:
						print(sheet.cell_value(row, column_2), end = '; ')
				print(TopVenue_dic[sheet.cell_value(row, 1)]) 
