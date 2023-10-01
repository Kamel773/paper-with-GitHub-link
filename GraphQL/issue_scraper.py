# An example to get the remaining rate limit using the Github GraphQL API.

import requests
import xlrd 
import re

headers = {"Authorization": "token "}

def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    #print(request)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))



# The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.       
base_query = """
{
  repository(owner:%s, name:%s) {
	nameWithOwner
    mergeCommitAllowed
    forkCount : forkCount
    pushedAt
	updatedAt
    createdAt
    isLocked
    Count_watchers : watchers(first:1){
  totalCount
}
Count_stargazers : stargazers(first:1){
   totalCount
}
    openIssues: issues(states: OPEN) {
      totalCount
    }
	closedIssues: issues(states: CLOSED) {
      totalCount
    }
    OpenpullRequests : pullRequests(states: OPEN){
  totalCount
}
ClosedpullRequests : pullRequests(states: CLOSED){
  totalCount
}
LastClosedIssues: issues(last:1, states:CLOSED) {
      edges {
        node {
          createdAt
        }
      }
}
  
LastOpenIssues:   issues(last:1, states:OPEN) {
      edges {
        node {
          createdAt
        }
      }
}  
ProgrammingLanguage : languages(first:1){
  edges{
    node{
      name
    }
  }
}

Count_releases : releases(first: 1){
 totalCount

} 

Count_commitComments : commitComments(first : 1){
  totalCount
  }

    }
  }
"""

Github_Respond = {}
loc = ("/Users/kamel/Desktop/CMU/Dataset/Links.xlsx") 
repository = []
# To open Workbook 
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
for row in range(3093):
	try:
		if sheet.cell_value(row, 3) == 1 or sheet.cell_value(row, 3) == 2:
			if (sheet.cell_value(row, 2)[-1]) == '/':
				repository_link = sheet.cell_value(row, 2)[:-1]
			else:
				repository_link = sheet.cell_value(row, 2)

			x = repository_link.rfind('/')
			repository_name = repository_link[x+1:]

			repository_own = (repository_link[:x]).rfind('/')
			repository_own = repository_link[repository_own+1:]

			x = repository_own.split('/')
			repository.append((x[0],x[1],sheet.cell_value(row, 1),sheet.cell_value(row, 3)))

	except:
		print('Error in Github link', sheet.cell_value(row, 1))


k = 0
repo_list = []
for i in repository:
	repo_list.append((i[0],i[1],i[2],i[3]))


print(len(repo_list))

for repo_org, repo_name, paper_link, category in repo_list:
	repo_query = base_query % ("\"" + repo_org + "\"", "\"" + repo_name + "\"")

	result = run_query(repo_query) # Execute the query
	if result['data']['repository'] == None:

		continue

	#continue
	Github_Respond["PaperLink"] = paper_link
	Github_Respond["category"] = int(category)
	Github_Respond["nameWithOwner"] = result['data']['repository']['nameWithOwner']
	Github_Respond["mergeCommitAllowed"] = result['data']['repository']['mergeCommitAllowed'] 
	Github_Respond["forkCount"] = result['data']['repository']['forkCount'] 
	Github_Respond["Count_watchers"] = result['data']['repository']['Count_watchers']['totalCount']
	Github_Respond["Count_stargazers"] = result['data']['repository']['Count_stargazers']['totalCount']
	Github_Respond["pushedAt"] = result['data']['repository']['pushedAt'] 
	Github_Respond["updatedAt"] = result['data']['repository']['updatedAt'] 
	Github_Respond["createdAt"] = result['data']['repository']['createdAt'] 
	Github_Respond["isLocked"] = result['data']['repository']['isLocked'] 
	Github_Respond["CountopenIssues"] = result['data']['repository']['openIssues']['totalCount'] 
	Github_Respond["CountclosedIssues"] = result['data']['repository']['closedIssues']['totalCount']
	Github_Respond["CountOpenpullRequests"] = result['data']['repository']['OpenpullRequests']['totalCount'] 
	Github_Respond["CountClosedpullRequests"] = result['data']['repository']['ClosedpullRequests']['totalCount']
	if result['data']['repository']['LastClosedIssues']['edges']:
		Github_Respond["LastClosedIssues"] = result['data']['repository']['LastClosedIssues']['edges'][0]['node']['createdAt']
	else:
		Github_Respond["LastClosedIssues"] = 0

	if result['data']['repository']['LastOpenIssues']['edges']:

		Github_Respond["LastOpenIssues"] = result['data']['repository']['LastOpenIssues']['edges'][0]['node']['createdAt']
	else:
		Github_Respond["LastOpenIssues"] = 0
	if result['data']['repository']['ProgrammingLanguage']['edges']:
		Github_Respond["ProgrammingLanguage"] = result['data']['repository']['ProgrammingLanguage']['edges'][0]['node']['name']
	else:
		Github_Respond["ProgrammingLanguage"] = 0

	Github_Respond["Count_releases"] = result['data']['repository']['Count_releases']['totalCount'] 
	Github_Respond["Count_commitComments"] = result['data']['repository']['Count_commitComments']['totalCount']


	
	for (key,value) in Github_Respond.items():
		print(value, end = '; ')
	print()
	Github_Respond.clear()

