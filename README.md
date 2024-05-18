
#ChatBot-NLP

It is an NLP project. First, we fetch data from an API and collect it in a single unit. Then, we process it using a Python NLP library such as spaCy. Finally, we display the processed data in a user-friendly UI.




## API Reference

#### Get all items

```http
  https://devapi.beyondchats.com/api/get_message_with_sources
```
- Above is the base page API URL. We can use this URL to fetch the remaining 13 pages of data using the next_page_url property provided in the data.


## Documentation

#### The flow of code execution:



 -> The main method serves as the entry point for the code. When we execute the ChatBot.py file, the execution begins from the main method and then follows the flow below: 
  

        
         
           1. fetch_all_pages(api_endpoint:str)->list 
               
               -> The fetch_all_pages method takes a string as a parameter. We pass the API URL here, and it fetches the data from all the pages until the next_page_url becomes null


            2. process_data(all_pages_data:list)->list 
               
               ->  This method takes a list of objects as a parameter, iterates over the data, and compares the response with each source context using the Python spaCy NLP library.
               ->  Here have used spacy module's built-in similarity method to compare two paragraphs.  
                   The method returns a value between 0 and 1: 0 means the paragraphs are different,  
                   and 1 means they are identical.
               ->  And based on the comparison result, return a list containing all the data in the format: [{response_id: int, response_citations: [{id: str, link: str}]}]
               -> Here, I have chosen 0.6 as the base for the similarity check, but we can change it as per the requirement.


            3. show_citations_table(processed_data:list) -> None
                Above method takes the processed data and displays it in a user-friendly UI.To create the UI table, we used the tkinter Python UI library

[](https://linktodocumentation)


## Library Used

- [spaCy](https://spacy.io/)    :   For natural language processing, I used the en_core_web_lg model to achieve better accuracy.

- [requests](https://pypi.org/project/requests/)    :   For fetching data fron the API. 


- [tkinter](https://docs.python.org/3/library/tkinter.html)    :   To create ui. 





## Setup Intructuions
#### List of Python Libraries need to install Befor Execution of script: 

 - Request: 
           
              -> pip install requests
    
    
- large English model en_core_web_lg: 
           
              -> python -m spacy download en_core_web_lg
- spaCy: 
           
              -> pip install -U pip setuptools wheel

              -> pip install -U spacy
        

- tkinter:    
               
               -> pip install tk
