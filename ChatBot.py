import requests
import tkinter as tk
from tkinter import ttk
import spacy
from requests.exceptions import RequestException

api_endpoint = "https://devapi.beyondchats.com/api/get_message_with_sources"


# Here we are loading en_core_web_lg 
nlp = spacy.load("en_core_web_lg")


# function to fetch all pages data 

def fetch_all_pages(api_endpoint:str)->list:
    """
    :param api-endpoint: Base api url from where we will fetch data
    :return all_pages_data : return a list of object data
    """

    all_pages_data = []

    next_page = api_endpoint 

    while next_page :
        try:
 
            api_response = requests.get(next_page)
            api_response.raise_for_status()
            api_data = api_response.json()
            
            # storing all list of objects in single list 
            all_pages_data.extend(api_data["data"]["data"])
    
            # check and assing the next page api url
            next_page = api_data["data"].get('next_page_url',None)
        except RequestException as e:
            print(f"Not able to fetch data, error: {e}")
            break

    return all_pages_data

    
all_data = fetch_all_pages(api_endpoint)


# function to process the data
def process_data(all_pages_data:list)->list:

    """
    :note : We are using the spacy module's built-in similarity method to compare two paragraphs. The method returns a value between 0 and 1: 0 means the paragraphs are different, and 1 means they are identical. 
    :param all_pages_data: list of objects
    :return citations: a list of object tains to properties 1: response_id , 2 : response_citations (array of objects with context_id, and link)
    """

    citations = [] # [{response_id: int , response_citations: [{ id : str , link : str }]}]
  
    for data_responce in all_pages_data:
       
       text1 = nlp(data_responce["response"])

       #list to store the objects with props {id , link}
       arr =[]

       #object to store responce id  and list of objects with props {response_id , response_citations}
       temp_obj = {}

       for source in data_responce["source"]:
            
            #check if context is list or not is it is list then convert it in to str
            if  not isinstance(source["context"], str) :

                text2 = nlp(" ".join(source["context"]))
            else:
                text2 = nlp(source["context"])
            
            #object to store the id and link for on context
            temp_citations_obj = {}

            similarity=text1.similarity(text2)
            
            #here i have choose the 0.6 as base for similarity but we can change it as per the requirement 
            if similarity >= 0.6:
                temp_citations_obj["id"] = source["id"]
                temp_citations_obj["link"] = source["link"]
            
            #will store the object temp_citations_obj only it contails value
            if temp_citations_obj:
                arr.append(temp_citations_obj)

       temp_obj["response_id"] = data_responce["id"]
       temp_obj["response_citations"] = arr

       citations.append(temp_obj)

    return citations 
        

# processed_data = process_data(all_data)

def show_citations_table(processed_data:list) -> None:

    #Create the main window
    root = tk.Tk()
    root.title("Table UI")
    
    #object for styling
    style = ttk.Style(root)
    style.theme_use('clam')
    
    #setting bg for table heading 
    style.configure("Treeview.Heading", background="blue", foreground="black", font=('Helvetica', 10, 'bold'))

    
    #columns for the main table
    columns = ('response_id', "ID", "Link")
    tree = ttk.Treeview(root, columns=columns, show='headings')
    
    #headings for the main columns
    tree.heading('response_id', text='Response ID')
    tree.heading('ID', text='ID')
    tree.heading('Link', text='Link')
    
    #columns width and alignment
    tree.column('response_id', anchor='center', width=100)
    tree.column('ID', anchor='w', width=100)
    tree.column('Link', anchor='w', width=150)

    for response in processed_data:

        #insert the main row with the response ID
        values=(response['response_id'])

        #insert sub-items for each citation under the main row
        for citation in response['response_citations']:

            #check if link is preset if not insert Url Not Found
            Link = citation['link'] if citation['link'] !="" else "Url Not Found"

            tree.insert("", 'end', values=(values, citation['id'], Link))
    
    
    #create the vertical scroll bar in table
    v_scroll = ttk.Scrollbar(root, orient='vertical', command=tree.yview)
    v_scroll.pack(side='right', fill='y')
    tree.configure(yscrollcommand=v_scroll.set)
    
    #expand the table to full window size
    tree.pack(expand=True, fill='both')
        
    #run the ui 
    root.mainloop()

def main():

    print("Please wait, code is executing...")

    all_data = fetch_all_pages(api_endpoint)
    processed_data = process_data(all_data)
    show_citations_table(processed_data)

    print("Execution finished.")

if __name__ == "__main__":
    main()
    