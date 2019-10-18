# -*- coding: utf-8 -*-
#####################################
# DAT-129
# Purpose: Exercise in using the Pubmed API (Entrez) to write
# selected publications to a csv file
# Author: Lisa Nydick
# Last Modified: 10/17/2019
#####################################

import xml.etree.ElementTree as ET
import requests
import csv

#URL parameter constants
BASE = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
DB = 'db=pubmed'
QUERY = '&term=(ketamine[Title]+AND+("depressive disorder"[MeSH Terms]+OR+"depression"[MeSH Terms]))+AND+("2017/01/01"[PDAT]:"2019/10/01"[PDAT])'
RETMODE= '&retmode=xml'
RETTYPE= '&rettype=uilist'
IDPARM = '&id='

#Utilities
ESEARCH = 'esearch.fcgi?'
ESUMMARY = 'esummary.fcgi?'
EFETCH = 'efetch.fcgi?'


#CSV header record
HEADER = 'PMID', 'PubYear', 'Source', 'Title', 'PubType', 'Volume', 'Issue', 'Pages', 'DOI', 'Authors', 'Keywords'

#Errors and Other Messages
ERROR_PERMISSIONS = 'CSV output file is open by another user or process.  Close it and optionally try again.'
ERROR_CSV = 'CSV file could not be written. Ending program.'
MSG_TRY_AGAIN = 'Try again? (Y or N): '
MSG_CSV_WRITTEN = 'Output file written.'
MSG_CSV_NOT_WRITTEN = 'Output file was NOT written due to permissions error.'
MSG_ABNORMAL_END = 'Program ended abnormally due to fatal error.'
MSG_ENTER_RETSTART = 'Enter starting ID number (retstart): '
MSG_ENTER_RETMAX = 'Enter the max number of IDs (retmax): '
MSG_ENTER_CSV_FILE = 'Enter the name of the CSV output file: '
MSG_INVALID_FILENAME = 'Invalid output filename.  Please try again.'
MSG_INVALID_INTEGER = 'Invalid integer value for numeric field.  Please try again.'


fatal_error = False
###################################################################################################
# Main Function
###################################################################################################
def main():
    
    xml_file_ids = 'id_list.xml'
    xml_file_summary = 'summary.xml'
    xml_file_full = 'full.xml'
        
    publication_list = []
    summary_list = []
    author_list = []
    keyword_list = []
    
     #Get retstart, retmax, and pubs_out_file from console input
    retstart_input, retmax_input, csv_out_file = get_input()

    #Initialize the CSV output file with a header record
    initializeCSVFile(csv_out_file)
    
    #If CSV file was successfully initialized, proceed with the rest of the program
    if fatal_error == False:
        #Set parameter values that all utilities have in common
        retstart, retmax = setCommonParms(retstart_input, retmax_input)

        #Get a list of PMIDs from the esearch utility
        id_list_str = getPMIDs(retstart, retmax, xml_file_ids)
    
        #Get summary data (meta data) out of the eSummary utility based on a list of PMIDs 
        summary_list = getSummaryInfo(retstart, retmax, xml_file_summary, id_list_str)
    
        #Get a list of authors and keywords from the eFetch utility based on a list of PMIDs
        author_list, keyword_list = getFullInfo(retstart, retmax, xml_file_full, id_list_str)
    
        #Concatinate values from the summary and full XML files into a new list
        publication_list = concat_summary_and_full_lists(summary_list, author_list, keyword_list)

        #Write the new list out to a csv file
        write_csv(csv_out_file, publication_list)
    else:
        print(MSG_ABNORMAL_END)

###################################################################################################
# Reads in a couple of url parms and and the name of the csv output file from the console input
###################################################################################################
def get_input():
    invalid_entries = True
    while invalid_entries == True:
        try:
            retstart = int(input(MSG_ENTER_RETSTART))      
            retmax = int(input(MSG_ENTER_RETMAX))
            csv_outfile = input(MSG_ENTER_CSV_FILE)
            if csv_outfile == '':
                print(MSG_INVALID_FILENAME)
                invalid_entries = True
            else:
                invalid_entries = False    
        except ValueError:
            print(MSG_INVALID_INTEGER)
            invalid_entries = True
            
    return retstart, retmax, csv_outfile

###################################################################################################
# Initializes a CSV output file with a header record
###################################################################################################
def initializeCSVFile(csv_outfile):
    global fatal_error
    repeat = True
    while repeat == True:
        try:
            with open(csv_outfile, 'w', newline = '') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(HEADER)
                repeat = False
        except PermissionError:
            print(ERROR_PERMISSIONS)
            try_again = input(MSG_TRY_AGAIN)
            if try_again == 'Y' or try_again == 'y':
                repeat = True
            else:
                repeat = False
                print()
                print(ERROR_CSV)
                fatal_error = True
        except Exception as err:
            print()
            print(err)
            repeat = False
            fatal_error = True


###################################################################################################
# Sets the values of retstart and retmax URL parms that all utilities have in common
###################################################################################################
def setCommonParms(retstart_input, retmax_input):
    retstart = '&retstart=' + str(retstart_input)   #Starting record    
    retmax = '&retmax=' + str(retmax_input)         #Maximum records returned
                             
    return retstart, retmax      

###################################################################################################
# Uses the esearch utility to obtain a list of PMIDs.  Returns the list of PMIDs as a string.
###################################################################################################
def getPMIDs(retstart, retmax, xml_file_ids):
    
    #Enter the query parameters that are specific to the esearch utility
    util = ESEARCH
    
    
    #Build the url to pull the PMIDs via the eSearch utility
    url = BASE + util + DB + retstart + retmax + RETTYPE + RETMODE + QUERY
       
    #Issue url request, write response to an xml file, and parse the pmids in it
    response = issue_request(url)
    write_response(xml_file_ids, response)
    id_list_str = parse_pmids(xml_file_ids)

    return id_list_str    

###################################################################################################
# Uses the eSummary utility to extract summary information.  Returns a list of summary data.
###################################################################################################
def getSummaryInfo(retstart, retmax, xml_file_summary, id_list_str):
    #Build the url for the eSummary util, passing in the id_list from the parsing routine
    util = ESUMMARY
    pmids = id_list_str

    url = BASE + util + DB + retstart + retmax + RETMODE + IDPARM + pmids
    
    #Issue url request, write response to an XML summary file, parse the summary
    response = issue_request(url)
    write_response(xml_file_summary, response)
    summary_list = parse_summary(xml_file_summary)
    
    return summary_list

###################################################################################################
# Uses the eFetch utility to extract author and keyword information from full xml records.  
# Returns lists of authors and keywords.
###################################################################################################
def getFullInfo(retstart, retmax, xml_file_full, id_list_str):
    #Build the url for the eFetch util, passing in the id_list
    util = EFETCH
    pmids = id_list_str

    url = BASE + util + DB + retstart + retmax + RETMODE + IDPARM + pmids

    #Issue url request, write response to an XML full details file, parse the full details file
    response = issue_request(url)
    write_response(xml_file_full, response)
    author_list = parse_authors(xml_file_full)
    keyword_list = parse_keywords(xml_file_full)
    
    return author_list, keyword_list    

###################################################################################################
# Issues url request and returns a response
###################################################################################################
def issue_request(url):
    #issue the http request and store xml response
    response = requests.get(url)    
    return response

###################################################################################################
# Writes a response to an XML file
###################################################################################################
def write_response(xml_file, response):
    #write the xml response to a file
    with open(xml_file, 'wb') as id_file:
        id_file.write(response.content)

###################################################################################################
# Uses ElementTree library to parse PMIDs in an XML file and returns a list of PMIDs as a string
###################################################################################################
def parse_pmids(xml_file):
    #Use elementTree to parse the xml files for pmids
    tree = ET.parse(xml_file)
    root = tree.getroot()

    #Store the pmid ids in a list
    id_list = []
    for idlist in root.findall('IdList'):
        for pmid in idlist:
            id_list.append(pmid.text)
    #join the ids in the list together in a comma-separated string    
    id_list_str = ','.join(id_list)
    #print(id_list_str)
    return id_list_str

###################################################################################################
# Uses ElementTree library to parse the document summary XML file and returns a list of publication meta data
###################################################################################################
def parse_summary(xml_file):
        
    #Use elementTree to parse the xml files for document summary info
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    summary_list = []
    for docsum in root.findall('DocSum'):
        docsum_list = []
        pubtype_list = []
            
        for docid in docsum.findall('Id'):
            pmid = docid.text
            docsum_list.append(pmid)
            for item in docsum.findall('Item'):
                item_name = item.get('Name')
                if item_name == 'PubDate':
                    pubdate = item.text
                    #only save the year portion of the pubdate
                    pubyear = pubdate[0:4]
                    
                elif item_name == 'FullJournalName':
                    journalname = item.text

                elif item_name == 'Title':
                    #title = quote + item.text + quote
                    title = item.text

                elif item_name == 'PubTypeList':
                    pubtypes = item.findall('Item')
                    #pubtypes is a list
                    for pubtype in pubtypes:
                        pubt = pubtype.text
                        pubtype_list.append(pubt) 
                   
                elif item_name == 'Volume':
                    volume = item.text
                    if volume == None:
                        volume = ''
                    
                elif item_name == 'Issue':
                    issue = item.text
                    if issue == None:
                        issue = ''
                    
                elif item_name == 'Pages':
                    pages = item.text
                    if pages == None:
                        pages = ''
                                                              
                elif item_name == 'DOI':
                    doi = item.text
                    
        #Append elements to the document summary list
        docsum_list.append(pubyear)
        docsum_list.append(journalname)
        docsum_list.append(title)

        pubtype_str = ','.join(pubtype_list)
        
        docsum_list.append(pubtype_str)        
        docsum_list.append(volume)
        docsum_list.append(issue)        
        docsum_list.append(pages)
        docsum_list.append(doi)
        
        #Append the document summary list to a publication list
        summary_list.append(docsum_list)

    return summary_list

###################################################################################################
# Uses ElementTree library to parse the full document XML file and returns a list of full author names
###################################################################################################
def parse_authors(xml_file):
    author_list = []
    
    #Use elementTree to parse the xml files for full document info
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    for pubmedarticle in root.findall('PubmedArticle'):  
        for medlinecit in pubmedarticle.findall('MedlineCitation'): 
            for article in medlinecit.findall('Article'):
                for authorlist in article.findall('AuthorList'):
                    authlist = []
                    auth_list = []
 
                    for author in authorlist.findall('Author'):                         
                        for forname in author.findall('ForeName'):
                            fname = forname.text
                        for initials in author.findall('Initials'):
                            inits = initials.text
                            if inits == None:
                                inits = ''                            
                        for lastname in author.findall('LastName'):
                            lname = lastname.text                        
                        if inits != '' and len(inits) == 1:
                            authstr = fname + ' ' + inits + ' ' + lname
                        else:
                            authstr = fname + ' ' + lname
                            
                        auth_list.append(authstr)
                        
                    authlist_str = ','.join(auth_list)

                    author_list.append(authlist_str)
 
                    
                        
    return author_list

###################################################################################################
# Uses ElementTree library to parse the full document XML file and returns a list of keywords
###################################################################################################
def parse_keywords(xml_file):
    keyword_list = []
    no_keywords = 'No Keywords'
    
    #Use elementTree to parse the xml files for full document info
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    for pubmedarticle in root.findall('PubmedArticle'):  
        for medlinecit in pubmedarticle.findall('MedlineCitation'): 
            keywordlist = medlinecit.findtext('KeywordList')
            if keywordlist != None:
                
                for KeywordList in medlinecit.findall('KeywordList'):
                    keystr = ''
                    for Keyword in KeywordList.findall('Keyword'):
                        key = Keyword.text
                        if keystr != '':
                            keystr = keystr + ', ' + key
                        else:
                            keystr = key

                    keyword_list.append(keystr)
                    
                               
            else:
                keyword_list.append(no_keywords)
             

    return keyword_list
###################################################################################################
# Concatinates info from the Summary file with the Author info from the Full file
###################################################################################################
def concat_summary_and_full_lists(summary_list, author_list, keyword_list):
    #Populate the publication list with the values in summary_list
    publication_list = summary_list
    
    #Summary_list and Full_list will be the same length because they contain the same # of records
    for i in range(len(author_list)):
        #Extract the author list from the full list
        authorlist = author_list[i]
        keywordlist = keyword_list[i]
        #Append the author to the publication list, which already includes the summary info
        publication_list[i].append(authorlist)
        publication_list[i].append(keywordlist)
        
    return publication_list
    
###################################################################################################
# Writes the publication list to a CSV file
###################################################################################################
def write_csv(out_file, publication_list):
    global fatal_error
    repeat = True
    
    while repeat == True:
        try:
            with open(out_file, 'a', newline='', encoding='UTF-8') as publications:
                repeat = False
                writer = csv.writer(publications)
                for i in range(len(publication_list)):
                    writer.writerow(publication_list[i])
                print(MSG_CSV_WRITTEN)
        except PermissionError:
            print()
            print(ERROR_PERMISSIONS)
            try_again = input(MSG_TRY_AGAIN)
            if try_again == 'Y' or try_again == 'y':
                repeat = True
            else:
                repeat = False
                print()
                print(MSG_CSV_NOT_WRITTEN)
                fatal_error = True
        except Exception as err:
            print()
            print(err)
            print(MSG_CSV_NOT_WRITTEN)
            repeat = False
            fatal_error = True
            
###################################################################################################
if __name__=='__main__':
    main()