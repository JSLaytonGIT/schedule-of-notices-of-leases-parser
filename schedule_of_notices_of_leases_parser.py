import PyPDF2
import re
import json
import logging

def schedule_of_notices_of_leases_parser(pdf_path):
    try:
        # I define the array that will contain the data 
        registration_date_and_plan_ref = []
        property_description = []
        date_of_lease_and_term = []
        lessees_title = []
        index_array = []
        note_array = []
        
        # these are headers/lines that I don't want in the final data, so I will filter them out
        filter_lines = ['Registration','date','and plan ref.Property description Date of lease',"and termLessee's",'title','Schedule of notices of leases continued']
        
        start_flag = False # I only want the processes to begin once it has reached the data
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            note_flag = False # are the current set of lines part of a note
            current_note = ''
            registration_date_and_plan_ref_string = ''
            property_description_string = ''
            date_of_lease_and_term_string = ''
            
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                
                if 'Schedule of notices of leases' in page_text: # start the processes at this page
                    start_flag = True

                if start_flag:
                    lines = page_text.split('\n')
                    position_adjuster = 0 # the index number shifts the position of the text
                    for line in lines:
                        if 'Title number EGL363613' in line:
                            line = line.replace('Title number EGL363613', '') # Title number EGL363613 is added onto the last string of each page for some reason. This removes it
                              
                        if re.search('^\d+\s+(\d{2}\.\d{2}\.\d{4})', line): # checks to see if there is a lessee's title code
                            if len(index_array) == 0: # if the first encounter in the pdf
                                index_array.append(1)
                            else:
                                index_array.append(index_array[len(index_array)-1]+1) # adds a new index to the index array
                                note_array.append(current_note)
                                note_flag = False # stops note section
                                current_note = ''
                                registration_date_and_plan_ref.append(registration_date_and_plan_ref_string.strip()) # append the current concatenated string (see lower down) to the array
                                registration_date_and_plan_ref_string= ''
                                property_description.append(property_description_string.strip())
                                property_description_string= ''
                                date_of_lease_and_term.append(date_of_lease_and_term_string.strip())
                                date_of_lease_and_term_string = ''
                            position_adjuster = len(line.split(maxsplit=1)[0]) + 1 # counts the length of the index plus the blankspace
                            lessees_title.append(line[62+position_adjuster:71+position_adjuster].strip()) # appends the lessee title to the array
                        else:
                            position_adjuster = 0 # is not a line with an index
                        
                        if len(lessees_title) < 1:
                            continue # ignore the bits before the actual schedule of notices of leases data begins
                        
                        
                        if 'End of register' in line: # append the final lines
                            registration_date_and_plan_ref.append(registration_date_and_plan_ref_string.strip())
                            property_description.append(property_description_string.strip())
                            date_of_lease_and_term.append(date_of_lease_and_term_string.strip())                        
                        
                        skip_line_flag = False # creates a flag to call check if the inner for loop needs to pass 'continue' to the outer for loop
                        for filter_line in filter_lines: # filtering out the unwanted lines
                            if filter_line in line:
                                skip_line_flag = True
                                break
                        if skip_line_flag:
                            continue # this is a line I want to filter, so I skip it

                        if re.match(r'\b\d+\sof\b', line.strip()) or (line.strip().isdigit() and len(line.strip()) <= 2):
                            continue # filtering out the page numbers
                        
                        if line[0:4] == "NOTE" or note_flag == True: # sometimes there are multiple note lines
                            note_flag = True
                            current_note = current_note + ' ' + line
                        else:
                            registration_date_and_plan_ref_string = registration_date_and_plan_ref_string + ' ' + line[0+position_adjuster:16+position_adjuster].strip()
                            property_description_string = property_description_string + ' ' + line[16+position_adjuster:46+position_adjuster].strip()
                            date_of_lease_and_term_string = date_of_lease_and_term_string + ' ' + line[46+position_adjuster:62+position_adjuster].strip()
            
            schedule_of_notices_of_leases_json = []
            
            for i in range(len(lessees_title)): # add them all to a json object array
                try:
                    json_object = {
                        "Registration date and plan ref": registration_date_and_plan_ref[i],
                        "Property description": property_description[i],
                        "Date of lease and term": date_of_lease_and_term[i],
                        "Lessee's title": lessees_title[i],
                        "Notes": note_array[i]
                    }
                except Exception as e:
                    print("An error occurred:", e)
                schedule_of_notices_of_leases_json.append(json_object)
            with open('schedule_of_notices_of_leases.json', "w") as json_file: # writes the json object to the file
                json.dump(schedule_of_notices_of_leases_json, json_file, indent=4)
    
    except Exception as e:
        logging.error(f"Error in parsing PDF: {e}")
        return str(e), 500
    
    return 'Finished'