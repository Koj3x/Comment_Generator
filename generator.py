import csv
import requests
import json

# to-do list

# 8. As an extension, you could see if you could make your code work for reading an Excel File, or reading a Google Spreadsheet directly so teachers would not have to export a csv file.
# 9. DICTIONARY FOR LO STRATEGIES - currently linked to row, make it link to the growth word needed

link_code = '1GsKlGy25Dwi9dfT7bn1-mNpCVOOjAJ_83vBn5wyn3ME'

response = requests.get(f'https://docs.google.com/spreadsheets/d/{link_code}/export?format=csv')
assert response.status_code == 200, 'Wrong status code'
data = response.content.decode("utf-8")

with open('teacher.csv', 'w') as f:
    f.write(data)
    
with open('teacher.csv', 'r') as f:
    HEADER = next(f)
    data = csv.reader(f, delimiter=',')
    
    stats = [row for row in data]

   
# This code will build up the "comment" as it goes, using the information incorporated in your spreadsheet to build a complete piece of text & file for each student!
    
def an(num):
    return str(num)[0] == '8'
    
for row in stats[:9]:
    comment = ''
    
    
    # Comment Setup — Establishing important variables for later on. Please make sure to order and fill your spreadsheet using the following guidelines:
    
    # Column A - Name
    # Column B - Class
    # Column C - Overall Class Grade
    # Column D - LO Strengths (Please include two)
    
    # Note: use established keywords for each LO, separate them using a space (ie: "Strategic Evaluative")
    
    # Column E - LO Growth (Please include one, use established keyword)
    # Column F - Test Score (Please include first one, chronologically — Just a number value (ie: 90))
    # Column G - Test Score (Please include second one, chronologically — Just a number value (ie: 90))
    # Column H - Extra Comments (If you'd like to add anything else specific about your student)
    # Column I - Essay Topic (If relevant, include topic! Otherwise, leave it blank)
    # Column J - Essay Excerpts (If relevant, include a quote WITHOUT quotation marks! Otherwise, leave it blank)
    # Column K - Course Type ("Semester", "Year")
    # Column L - Course Length (If yearlong, indicate whether "First" or "Second" semester)    
    # Column M - Reflection (If relevant, quote from their reflection WITHOUT quotation marks! Otherwise, leave it blank)
    
    first_name = row[0].split()[0]
    last_name = row[0].split()[1]
    course = row[1]
    grade = row[2]
    
    strengths = row[3].split()
    
    growth = row[4]
    scores = [int(row[5]), int(row[6])]
    
    improved = scores[1] > scores[0]
    improvement_percentage = scores[1]-scores[0]
    
    notes = row[7]
    
    first_name = first_name.title()
    last_name = last_name.title()
    
    # File Sorting - Makes a new folder for each course, if one does not exist.
    
    try:
        with open('folder_paths.json', 'r') as f:
            folder_paths = json.load(f)
    except FileNotFoundError:
        folder_paths = {}
    
    try:
        folder_path = folder_paths[course]
    except KeyError:
        folder_path = f'comments/{course}'
        folder_paths[course] = folder_path
        with open('folder_paths.json', 'w') as f:
            json.dump(folder_paths, f)
    
    # Course Description - This is a basic, short description of what your course is about.
    
    course_dict = {
        'AP Statistics': 'AP Statistics involves descriptive statistics (interpreting, organizing, and visualizing data), research design (designing survey, observational studies, and experiments), probability theory, simulation (modeling real-world situations with calculators and computers), and statistical inference. This course is equivalent to one semester of college-level Statistics and prepares students to take the AP Statistics exam.',
        'Python III': 'This course builds on the skills and concepts learned in our previous computer science courses.  The topics challenge students to explore how computing and technology can impact the world, with a unique focus on creative problem solving and real-world applications.  A successful student will know more advanced data structures and object-oriented programming basics.  A successful student will be able to communicate with popular APIs including Twitter and Google in order to “grab” data and to organize the data and display it.',
        'Economics': 'This course introduces the basic language and core principles of economics in a non-traditional way. You will develop an economic way of thinking - like an economist - using chains of deductive reasoning in conjunction with simplified models. A Microeconomic and Macroeconomic analysis will help explain why individuals, businesses, and even governments behave as they do.',
        'AP Spanish': 'The AP Spanish Language and Culture course is equivalent to an intermediate-level college course in Spanish. This rigorous course is taught exclusively in Spanish and requires students to improve their proficiency across the three modes of communication.'
    }
    
    
    comment += f"{course_dict[course]} \n\n"
    
    semester_course = row[10].lower() == 'semester'
    first_semester = row[11].lower() == 'first'
    
    # Reflection section - This section is a space to add in any quotes from student's self-reflections as a point of comparison.
    
    if row[12] != "":
        comment += f'{first_name.title()}, in your class reflection, you recognized your developement, saying:\n"{row[12]}"\n\n'
    
    # LO Prep - These are "dictionaries" of info based on the learning outcomes. Please do the following:
    # Inside of the following dictionary please put the learning outcomes.
    # Make sure that the learning outcomes are linked to a key word, and that, in your spreadsheet, you use those key words to determine which LO you want to reference per student.
    # For the strength LOs, separate them with just a space on the spreadsheet, but keep them in a single file!
    
    keyword_dict = {
        'Innovative': 'make sense of material and persevere through work',
        'Reasoned': 'reason abstractly',
        'Articulate': 'express ideas or fluently and coherently',
        'Adaptive': 'apply and adapt previous learning to tackle new problems',
        'Strategic': 'use appropriate tools strategically',
        'Precise': 'attend to precision',
        'Structured': 'look for and make use of structure',
        'Investigative': 'ask guiding questions and deeply investigate concepts',
        'Evaluative': 'develop and evaluate unique ideas',
        'Proficient': 'demonstrating an understanding of culture by reflecting on practices, products, and perspectives',
        'Competent': 'construct a strong foundation in intercultural competence by demonstrating timely knowledge of other cultures and their products',
        'Uncreative': 'make sense of material and persevere through work',
        'Unreasoned': 'reason abstractly',
        'Unintelligible': 'express ideas or fluently and coherentls',
        'Inflexible': 'apply and adapt previous learning to tackle new problems',
        'Random': 'use appropriate tools strategically',
        'Inaccurate': 'attend to precision',
        'Disorganized': 'look for and make use of structure',
        'Uninvestigative': 'ask guiding questions and deeply investigate concepts',
        'Unevaluative': 'develop and evaluate unique ideas',
        'Developing': 'demonstrating an understanding of culture by reflecting on practices, products, and perspectives',
        'Incompetent': 'construct a strong foundation in intercultural competence by demonstrating timely knowledge of other cultures and their products'
    }

    strategies_dict = {
        'Uncreative': 'interpreting the material in new spaces, allowing for new ideas',
        'Unreasoned': 'explaining concepts to others in a teaching format',
        'Unintelligible': 'explaining concepts to others in a teaching format',
        'Inflexible': 'working with Maego & myself (or future teachers) to define apporach strategies',
        'Random': 'working with Maego & myself (or future teachers) to define apporach strategies',
        'Inaccurate': 'explaining the reasoning behind each decision made in your work',
        'Disorganized': 'explaining the reasoning behind each decision made in your work',
        'Uninvestigative': 'conversing with classmates to see interesting ideas that come up, and diving into them',
        'Unevaluative': 'interpreting the material in new spaces, allowing for new ideas',
        'Developing': 'diving into the roots of our culture and comparing those roots with other cultures',
        'Incompetent': 'spending time with products of other cultures: music, shows, news, etc, to learn more through environment'
    }
        
    
    # LO Strength 1 - Demonstrating the first LO they showed proficiency in.
    
    comment += f'\t- {first_name}, you are consistently able to {keyword_dict[strengths[0]]}.\n'
    
    # LO Strength 2 - Demonstrating the second LO they showed proficiency in.
    
    comment += f'\t- You have also shown your capacity to {keyword_dict[strengths[1]]}.\n'
    
    # LO Growth - Demonstrating the  LO they showed a larger struggle in / where they have room to grow.    
    
    comment += f'\t- However, I find that you struggle to {keyword_dict[growth]} at times.\n A strategy to help develop your proficiency is {strategies_dict[growth]}.\n\n'
    
    # Grade View / Growth / Decline - Comparison of assessments throughout the semester to highlight growth, requires specific percentage scores.
    
    if improvement_percentage > 10:
        comment += 'You showed great improvement through the semester, with a' + 'n' * int(an(scores[1]-scores[0])) + f' {scores[1]-scores[0]} percent increase between the key assessments.\n'
    elif 0 < improvement_percentage < 10:
        comment += 'You showed slight improvement through the semester, with a' + 'n' * int(an(scores[1]-scores[0])) + f' {scores[1]-scores[0]} percent increase between the key assessments.\n'
    elif scores[1] == scores[0]:
        comment += f'You showed steady performance throughout the semester, scoring {scores[0]} on both key assessments.\n'
    else:
        comment += f"Although {first_name}'s test scores did not increase, {first_name}'s showed improvement in some aspects.\n"
       
    
    # Input Space - Adding on any additional, possibly-important information.

    if row[7] != "":
        comment += f'{row[7]} \n'
        
    # Essay excerpts (if applicable) - If a writing-focused class, space to include student work for deeper investigation.
    
    if row[9] != "":
        comment += f'\nIn your essay titled "{row[8].title()}," I was impressed by your language and thoughtfulness when you wrote the following:\n"{row[9]}"\nIt was quite exciting to see your thoughtfulness in this paper. \n\n'
    
    # Wrap-Up - Establishes their grade in the course, recognizing their development / improvement based on semester or year-long course & time of year.
 
# A to B+
    if grade == 'A' or grade == 'A-' or grade == 'B+':
        comment += f"Keep up the good work {first_name}! Your final grade for this class: {grade}. "
        if semester_course:
            comment += f"{first_name}, it was wonderful to have you in class this semester. Your focus, energy, and collaborative spirit were on full display every day, and you were an excellent partner in the learning process for everyone in the room. I look forward to all of your future successes at OES and beyond, and thank you!"
        else:
            if first_semester:
                comment += f"{first_name}, it was wonderful to have you in class this semester. Your focus, energy, and collaborative spirit were on full display every day, and you were an excellent partner in the learning process for everyone in the room. Continue to embrace these qualities; they are the foundation of lifelong learning and will undoubtedly lead to your continued success in any endeavor! See you next semester!"
            else:
                  comment += f"{first_name}, it was wonderful to have you in class this semester. Your focus, energy, and collaborative spirit were on full display every day, and you were an excellent partner in the learning process for everyone in the room. I look forward to all of your future successes at OES and beyond, and thank you!"
 
# B
    elif grade == 'B':
        comment += f"Hello {first_name}. You have shown understanding on most of the concepts we have learned in class. Your final grade for this class: {grade}."
        if semester_course:
            comment += f"{first_name}, it was great having you in this class this semester. Although there were times when you were distracted, the effort you put into the class was apparent. I look forward to seeing you grow as a student through your future efforts at OES!"
        else:
            if first_semester:
                  comment += f"{first_name}, it was great having you in this class this semester. Although you were distracted at times, the effort you put in the class was apparent. Continue this momentum you have built for this class to further improve your work in this class. I am excited to see you next semester!"
            else:
                  comment += f"{first_name}, it was great having you in class this year. Although you were distracted at times, you have shown your strong dedication towards your work this year. I look forward to seeing you grow as a student in your future classes at OES!"
 
# B-
    elif grade == 'B-':
        comment += f"Hello {first_name}. You have shown understanding on most of the major concepts we have learned in this class. Your final grade for this class: {grade}."
        if semester_course:
            comment += f"{first_name}, it was fun having you in this class this semester. In order to keep developing as a learner, I would encourage you to check in with teachers when you have the time, to make sure you are on track to getting a grade you are striving for. I look forward to seeing you grow as a learner throughout your time at OES!"
        else:
            if first_semester:
                  comment += f"{first_name}, it was fun having you in this class this semester. In order to improve your work in this class, I would encourage you to come in to my office when you have the time, to make sure you are on track to getting the grade you are striving for. I look forward to seeing your improvement throughout the second semester!"
            else:
                  comment += f"{first_name}, it was great having you in class this year. In order to keep developing as a learner, I would encourage you to check in with teachers when you have the time, to make sure you are on track to getting a grade you are striving for. I look forward to seein gyou grow as a learner throughout your time at OES!"
   
# C+ or lower   
    else:
        comment += f"Hello {first_name}. You have shown understanding on some of the concepts we have learned in this class. Your final grade for this class: {grade}."
        if semester_course:
            comment += f"{first_name}, it was great having you in this class this semester. You may not have gotten the grade that you strived to receive. As we've spoken about multiple times throughout the semester, I would encourage you to check in with your teachers during free block throughout your courses to make sure you are staying on track. I look forward to seeing you progress as a learner!"
        else:
            if first_semester:
                  comment += f"{first_name}, it was great having you in this class this semester. You may not have gotten the grade that you would've like to recieve, but with more dedication towards to course, you will able to increase this grade. As we've spoken multiple times throughout the semester, I encourage you to come by to my office during free block or office hours to make sure you are on track. I look forward to seeing your improvement throughut the second semester! "
            else:
                  comment += f"{first_name}, it was great having you in this class this year. You may not have gotten the grade that you strived to receive. As we've spoken about multiple times throughout the year, I would encourage you to check in with your teachers during free block throughout your courses to make sure you are staying on track. I look forward to seeing you progress as a learner!"
        
        
        
# Write to a file - Creates a new file with each individual student's comments, sorting them into a folder based on their course.
        
    with open(f'comments/{first_name}_{last_name}.txt', 'w') as f:
        f.write(comment)